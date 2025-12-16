# PromptCraft - Gamification Endpoints

from datetime import datetime, date, timedelta
from typing import Optional
import json
from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy import select, func, desc

from app.core.deps import DbSession, CurrentUser, RedisClient
from app.db.redis import RedisKeys
from app.models.user import User
from app.models.gamification import (
    UserGamification,
    XPTransaction,
    Badge,
    UserBadge,
    DailyChallenge,
    UserDailyChallenge
)
from app.schemas.gamification import (
    GamificationStatsResponse,
    XPTransactionResponse,
    XPTransactionList,
    BadgeResponse,
    BadgeListResponse,
    UserBadgeResponse,
    LeaderboardEntry,
    LeaderboardResponse,
    DailyChallengeResponse,
    StreakResponse,
    DailyGoalUpdate
)
from app.config import settings

router = APIRouter()


def calculate_level_xp(level: int) -> int:
    """Calculate XP required to reach a level."""
    return int(settings.BASE_XP_PER_LEVEL * (settings.XP_MULTIPLIER ** (level - 1)))


def calculate_level_from_xp(total_xp: int) -> tuple[int, int, int]:
    """
    Calculate level from total XP.
    Returns: (level, xp_in_current_level, xp_to_next_level)
    """
    level = 1
    xp_remaining = total_xp

    while True:
        xp_for_next = calculate_level_xp(level + 1)
        if xp_remaining < xp_for_next:
            return level, xp_remaining, xp_for_next
        xp_remaining -= xp_for_next
        level += 1


@router.get("/stats", response_model=GamificationStatsResponse)
async def get_my_stats(
    db: DbSession,
    current_user: CurrentUser
) -> GamificationStatsResponse:
    """
    Get current user's gamification stats.
    """
    # Get gamification record
    result = await db.execute(
        select(UserGamification)
        .where(UserGamification.user_id == current_user.id)
    )
    gamification = result.scalar_one_or_none()

    if not gamification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gamification data not found"
        )

    # Calculate level info
    level, xp_in_level, xp_to_next = calculate_level_from_xp(gamification.total_xp)
    level_progress = int((xp_in_level / xp_to_next) * 100) if xp_to_next > 0 else 0

    # Check streak status
    today = date.today()
    streak_at_risk = (
        gamification.last_activity_date is not None and
        gamification.last_activity_date < today and
        gamification.current_streak > 0
    )

    # Count badges
    badges_result = await db.execute(
        select(func.count())
        .select_from(UserBadge)
        .where(UserBadge.user_id == current_user.id)
    )
    badges_earned = badges_result.scalar() or 0

    total_badges_result = await db.execute(
        select(func.count())
        .select_from(Badge)
        .where(Badge.is_hidden == False)
    )
    badges_total = total_badges_result.scalar() or 0

    return GamificationStatsResponse(
        user_id=current_user.id,
        total_xp=gamification.total_xp,
        level=level,
        xp_in_current_level=xp_in_level,
        xp_to_next_level=xp_to_next,
        level_progress_percent=level_progress,
        current_streak=gamification.current_streak,
        longest_streak=gamification.longest_streak,
        streak_freezes=gamification.streak_freezes,
        last_activity_date=gamification.last_activity_date,
        streak_at_risk=streak_at_risk,
        lessons_completed=gamification.lessons_completed,
        puzzles_completed=gamification.puzzles_completed,
        puzzles_3_stars=gamification.puzzles_3_stars,
        total_time_minutes=gamification.total_time_minutes,
        daily_xp_goal=gamification.daily_xp_goal,
        daily_xp_earned=gamification.daily_xp_earned,
        daily_goal_completed=gamification.daily_xp_earned >= gamification.daily_xp_goal,
        daily_goal_streak=gamification.daily_goal_streak,
        badges_earned=badges_earned,
        badges_total=badges_total
    )


@router.get("/xp/history", response_model=XPTransactionList)
async def get_xp_history(
    db: DbSession,
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
) -> XPTransactionList:
    """
    Get user's XP transaction history.
    """
    # Get total count
    count_result = await db.execute(
        select(func.count())
        .select_from(XPTransaction)
        .where(XPTransaction.user_id == current_user.id)
    )
    total = count_result.scalar() or 0

    # Get transactions
    result = await db.execute(
        select(XPTransaction)
        .where(XPTransaction.user_id == current_user.id)
        .order_by(XPTransaction.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    transactions = result.scalars().all()

    return XPTransactionList(
        items=[XPTransactionResponse.model_validate(t) for t in transactions],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/badges", response_model=BadgeListResponse)
async def get_badges(
    db: DbSession,
    current_user: CurrentUser
) -> BadgeListResponse:
    """
    Get all badges with user's progress.
    """
    # Get all badges
    badges_result = await db.execute(
        select(Badge)
        .order_by(Badge.category, Badge.order)
    )
    all_badges = badges_result.scalars().all()

    # Get user's earned badges
    earned_result = await db.execute(
        select(UserBadge)
        .where(UserBadge.user_id == current_user.id)
    )
    earned_badges = {ub.badge_id: ub for ub in earned_result.scalars().all()}

    # Get gamification for progress calculation
    gam_result = await db.execute(
        select(UserGamification)
        .where(UserGamification.user_id == current_user.id)
    )
    gamification = gam_result.scalar_one_or_none()

    earned = []
    available = []
    hidden_count = 0

    for badge in all_badges:
        # Parse condition
        try:
            condition = json.loads(badge.condition)
        except:
            condition = {"type": "unknown", "value": 0}

        # Calculate progress
        progress_current = 0
        progress_target = condition.get("value", 0)

        if gamification:
            condition_type = condition.get("type", "")
            if condition_type == "lessons_completed":
                progress_current = gamification.lessons_completed
            elif condition_type == "puzzles_completed":
                progress_current = gamification.puzzles_completed
            elif condition_type == "streak":
                progress_current = gamification.current_streak
            elif condition_type == "xp":
                progress_current = gamification.total_xp
            elif condition_type == "puzzles_3_stars":
                progress_current = gamification.puzzles_3_stars

        progress_percent = min(100, int((progress_current / progress_target) * 100)) if progress_target > 0 else 0

        badge_response = BadgeResponse(
            id=badge.id,
            slug=badge.slug,
            name=badge.name,
            description=badge.description,
            icon=badge.icon,
            category=badge.category,
            rarity=badge.rarity,
            xp_reward=badge.xp_reward,
            is_hidden=badge.is_hidden,
            is_earned=badge.id in earned_badges,
            earned_at=earned_badges[badge.id].earned_at if badge.id in earned_badges else None,
            progress=progress_percent,
            progress_current=progress_current,
            progress_target=progress_target
        )

        if badge.id in earned_badges:
            earned.append(UserBadgeResponse(
                badge=badge_response,
                earned_at=earned_badges[badge.id].earned_at,
                notified=earned_badges[badge.id].notified
            ))
        elif badge.is_hidden:
            hidden_count += 1
        else:
            available.append(badge_response)

    return BadgeListResponse(
        earned=earned,
        available=available,
        hidden_count=hidden_count
    )


@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(
    db: DbSession,
    redis: RedisClient,
    current_user: CurrentUser,
    type: str = Query("weekly", regex="^(daily|weekly|monthly|all_time)$")
) -> LeaderboardResponse:
    """
    Get leaderboard by type.
    """
    # Try to get from Redis cache
    cache_key = RedisKeys.leaderboard(type)

    # Get from database (fallback if not in cache)
    query = (
        select(User, UserGamification)
        .join(UserGamification)
        .where(User.is_active == True)
        .order_by(UserGamification.total_xp.desc())
        .limit(100)
    )

    result = await db.execute(query)
    rows = result.all()

    entries = []
    current_user_entry = None
    current_user_rank = None

    for rank, (user, gam) in enumerate(rows, 1):
        entry = LeaderboardEntry(
            rank=rank,
            user_id=user.id,
            username=user.username,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            score=gam.total_xp,
            level=gam.level,
            is_current_user=user.id == current_user.id
        )
        entries.append(entry)

        if user.id == current_user.id:
            current_user_entry = entry
            current_user_rank = rank

    return LeaderboardResponse(
        type=type,
        entries=entries[:50],  # Return top 50
        current_user_rank=current_user_rank,
        current_user_entry=current_user_entry,
        total_users=len(rows),
        last_updated=datetime.utcnow()
    )


@router.get("/streak", response_model=StreakResponse)
async def get_streak_status(
    db: DbSession,
    current_user: CurrentUser
) -> StreakResponse:
    """
    Get detailed streak status.
    """
    result = await db.execute(
        select(UserGamification)
        .where(UserGamification.user_id == current_user.id)
    )
    gamification = result.scalar_one_or_none()

    if not gamification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gamification data not found"
        )

    today = date.today()
    streak_at_risk = (
        gamification.last_activity_date is not None and
        gamification.last_activity_date < today and
        gamification.current_streak > 0
    )

    # Calculate milestones
    milestones = [7, 30, 100, 365]
    next_milestone = None
    days_to_milestone = None

    for milestone in milestones:
        if gamification.current_streak < milestone:
            next_milestone = milestone
            days_to_milestone = milestone - gamification.current_streak
            break

    return StreakResponse(
        current_streak=gamification.current_streak,
        longest_streak=gamification.longest_streak,
        streak_freezes=gamification.streak_freezes,
        last_activity_date=gamification.last_activity_date,
        streak_at_risk=streak_at_risk,
        streak_milestones=milestones,
        next_milestone=next_milestone,
        days_to_next_milestone=days_to_milestone
    )


@router.post("/streak/freeze")
async def use_streak_freeze(
    db: DbSession,
    current_user: CurrentUser
) -> dict:
    """
    Use a streak freeze to protect streak.
    """
    result = await db.execute(
        select(UserGamification)
        .where(UserGamification.user_id == current_user.id)
    )
    gamification = result.scalar_one_or_none()

    if not gamification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gamification data not found"
        )

    if gamification.streak_freezes <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No streak freezes available"
        )

    today = date.today()
    if gamification.last_activity_date == today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already active today, no freeze needed"
        )

    # Use freeze
    gamification.streak_freezes -= 1
    gamification.last_activity_date = today

    await db.commit()

    return {
        "message": "Streak freeze used successfully",
        "freezes_remaining": gamification.streak_freezes,
        "current_streak": gamification.current_streak
    }


@router.get("/daily-challenge", response_model=DailyChallengeResponse)
async def get_daily_challenge(
    db: DbSession,
    current_user: CurrentUser
) -> DailyChallengeResponse:
    """
    Get today's daily challenge.
    """
    today = date.today()

    result = await db.execute(
        select(DailyChallenge)
        .where(DailyChallenge.challenge_date == today)
    )
    challenge = result.scalar_one_or_none()

    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No daily challenge available"
        )

    # Get user's progress
    progress_result = await db.execute(
        select(UserDailyChallenge)
        .where(UserDailyChallenge.user_id == current_user.id)
        .where(UserDailyChallenge.challenge_id == challenge.id)
    )
    user_challenge = progress_result.scalar_one_or_none()

    return DailyChallengeResponse(
        id=challenge.id,
        challenge_date=challenge.challenge_date,
        challenge_type=challenge.challenge_type,
        target_id=challenge.target_id,
        target_count=challenge.target_count,
        xp_reward=challenge.xp_reward,
        title=challenge.title,
        description=challenge.description,
        progress=user_challenge.progress if user_challenge else 0,
        is_completed=user_challenge.is_completed if user_challenge else False,
        completed_at=user_challenge.completed_at if user_challenge else None
    )


@router.patch("/settings/daily-goal", response_model=dict)
async def update_daily_goal(
    data: DailyGoalUpdate,
    db: DbSession,
    current_user: CurrentUser
) -> dict:
    """
    Update user's daily XP goal.
    """
    result = await db.execute(
        select(UserGamification)
        .where(UserGamification.user_id == current_user.id)
    )
    gamification = result.scalar_one_or_none()

    if not gamification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gamification data not found"
        )

    gamification.daily_xp_goal = data.daily_xp_goal
    await db.commit()

    return {
        "message": "Daily goal updated",
        "daily_xp_goal": data.daily_xp_goal
    }
