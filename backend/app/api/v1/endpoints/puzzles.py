# PromptCraft - Puzzles Endpoints

from datetime import datetime
from typing import Optional
import json
from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy import select, func

from app.core.deps import DbSession, CurrentUser, OptionalUser
from app.models.puzzle import Puzzle, PuzzleAttempt
from app.models.gamification import UserGamification, XPTransaction, XPSource
from app.schemas.puzzle import (
    PuzzleResponse,
    PuzzleListItem,
    PuzzleListResponse,
    PuzzleAttemptCreate,
    PuzzleAttemptResponse,
    PuzzleSubmit,
    PuzzleResult,
    HintRequest,
    HintResponse,
    PuzzleGridSize,
    PuzzleCategory_,
    PuzzleClue
)
from app.config import settings

router = APIRouter()


def parse_puzzle_data(puzzle: Puzzle) -> tuple:
    """Parse puzzle JSON fields."""
    grid_size = PuzzleGridSize(**json.loads(puzzle.grid_size))
    categories = [PuzzleCategory_(**c) for c in json.loads(puzzle.categories)]
    clues = [PuzzleClue(**c) for c in json.loads(puzzle.clues)]
    return grid_size, categories, clues


@router.get("/", response_model=PuzzleListResponse)
async def list_puzzles(
    db: DbSession,
    current_user: OptionalUser = None,
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
) -> PuzzleListResponse:
    """
    List all published puzzles with optional filters.
    """
    # Base query
    query = select(Puzzle).where(Puzzle.is_published == True)

    # Apply filters
    if category:
        query = query.where(Puzzle.category == category)
    if difficulty:
        query = query.where(Puzzle.difficulty == difficulty)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Order and paginate
    query = (
        query
        .order_by(Puzzle.order, Puzzle.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
    )

    result = await db.execute(query)
    puzzles = result.scalars().all()

    # Get user attempts if authenticated
    user_attempts = {}
    if current_user:
        attempts_result = await db.execute(
            select(PuzzleAttempt)
            .where(PuzzleAttempt.user_id == current_user.id)
            .where(PuzzleAttempt.puzzle_id.in_([p.id for p in puzzles]))
        )
        for attempt in attempts_result.scalars().all():
            puzzle_id = attempt.puzzle_id
            if puzzle_id not in user_attempts:
                user_attempts[puzzle_id] = {"count": 0, "best_stars": 0, "completed": False}
            user_attempts[puzzle_id]["count"] += 1
            if attempt.is_correct:
                user_attempts[puzzle_id]["completed"] = True
                user_attempts[puzzle_id]["best_stars"] = max(
                    user_attempts[puzzle_id]["best_stars"],
                    attempt.stars
                )

    # Build response
    items = []
    for puzzle in puzzles:
        attempt_info = user_attempts.get(puzzle.id, {"count": 0, "best_stars": 0, "completed": False})
        items.append(PuzzleListItem(
            id=puzzle.id,
            slug=puzzle.slug,
            title=puzzle.title,
            description=puzzle.description,
            icon=puzzle.icon,
            category=puzzle.category,
            difficulty=puzzle.difficulty,
            xp_reward=puzzle.xp_reward,
            time_limit_seconds=puzzle.time_limit_seconds,
            order=puzzle.order,
            is_completed=attempt_info["completed"],
            best_stars=attempt_info["best_stars"],
            attempts_count=attempt_info["count"]
        ))

    return PuzzleListResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=(total + per_page - 1) // per_page
    )


@router.get("/daily", response_model=PuzzleResponse)
async def get_daily_puzzle(
    db: DbSession,
    current_user: OptionalUser = None
) -> PuzzleResponse:
    """
    Get today's daily puzzle.
    """
    result = await db.execute(
        select(Puzzle)
        .where(Puzzle.is_daily == True)
        .where(Puzzle.is_published == True)
        .order_by(Puzzle.id.desc())
        .limit(1)
    )
    puzzle = result.scalar_one_or_none()

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No daily puzzle available"
        )

    grid_size, categories, clues = parse_puzzle_data(puzzle)

    # Get user's best attempt
    best_attempt = None
    attempts_count = 0
    if current_user:
        attempts_result = await db.execute(
            select(PuzzleAttempt)
            .where(PuzzleAttempt.user_id == current_user.id)
            .where(PuzzleAttempt.puzzle_id == puzzle.id)
            .order_by(PuzzleAttempt.stars.desc())
        )
        attempts = attempts_result.scalars().all()
        attempts_count = len(attempts)
        if attempts:
            best_attempt = PuzzleAttemptResponse.model_validate(attempts[0])

    return PuzzleResponse(
        id=puzzle.id,
        slug=puzzle.slug,
        title=puzzle.title,
        description=puzzle.description,
        icon=puzzle.icon,
        category=puzzle.category,
        difficulty=puzzle.difficulty,
        xp_reward=puzzle.xp_reward,
        time_limit_seconds=puzzle.time_limit_seconds,
        grid_size=grid_size,
        categories=categories,
        clues=clues,
        is_daily=puzzle.is_daily,
        is_published=puzzle.is_published,
        order=puzzle.order,
        created_at=puzzle.created_at,
        updated_at=puzzle.updated_at,
        best_attempt=best_attempt,
        attempts_count=attempts_count
    )


@router.get("/{slug}", response_model=PuzzleResponse)
async def get_puzzle(
    slug: str,
    db: DbSession,
    current_user: OptionalUser = None
) -> PuzzleResponse:
    """
    Get a single puzzle by slug.
    """
    result = await db.execute(
        select(Puzzle).where(Puzzle.slug == slug)
    )
    puzzle = result.scalar_one_or_none()

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puzzle not found"
        )

    grid_size, categories, clues = parse_puzzle_data(puzzle)

    # Get user's best attempt
    best_attempt = None
    attempts_count = 0
    if current_user:
        attempts_result = await db.execute(
            select(PuzzleAttempt)
            .where(PuzzleAttempt.user_id == current_user.id)
            .where(PuzzleAttempt.puzzle_id == puzzle.id)
            .order_by(PuzzleAttempt.stars.desc())
        )
        attempts = attempts_result.scalars().all()
        attempts_count = len(attempts)
        if attempts:
            best_attempt = PuzzleAttemptResponse.model_validate(attempts[0])

    return PuzzleResponse(
        id=puzzle.id,
        slug=puzzle.slug,
        title=puzzle.title,
        description=puzzle.description,
        icon=puzzle.icon,
        category=puzzle.category,
        difficulty=puzzle.difficulty,
        xp_reward=puzzle.xp_reward,
        time_limit_seconds=puzzle.time_limit_seconds,
        grid_size=grid_size,
        categories=categories,
        clues=clues,
        is_daily=puzzle.is_daily,
        is_published=puzzle.is_published,
        order=puzzle.order,
        created_at=puzzle.created_at,
        updated_at=puzzle.updated_at,
        best_attempt=best_attempt,
        attempts_count=attempts_count
    )


@router.post("/{slug}/start", response_model=PuzzleAttemptResponse)
async def start_puzzle(
    slug: str,
    db: DbSession,
    current_user: CurrentUser
) -> PuzzleAttemptResponse:
    """
    Start a new puzzle attempt.
    """
    # Get puzzle
    result = await db.execute(
        select(Puzzle).where(Puzzle.slug == slug)
    )
    puzzle = result.scalar_one_or_none()

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puzzle not found"
        )

    # Create new attempt
    attempt = PuzzleAttempt(
        user_id=current_user.id,
        puzzle_id=puzzle.id,
        started_at=datetime.utcnow(),
        is_completed=False,
        is_correct=False,
        stars=0,
        hints_used=0,
        xp_earned=0
    )
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)

    return PuzzleAttemptResponse.model_validate(attempt)


@router.post("/{slug}/submit", response_model=PuzzleResult)
async def submit_puzzle(
    slug: str,
    data: PuzzleSubmit,
    db: DbSession,
    current_user: CurrentUser
) -> PuzzleResult:
    """
    Submit puzzle solution.
    """
    # Get puzzle
    result = await db.execute(
        select(Puzzle).where(Puzzle.slug == slug)
    )
    puzzle = result.scalar_one_or_none()

    if not puzzle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puzzle not found"
        )

    # Get attempt
    attempt_result = await db.execute(
        select(PuzzleAttempt)
        .where(PuzzleAttempt.id == data.attempt_id)
        .where(PuzzleAttempt.user_id == current_user.id)
    )
    attempt = attempt_result.scalar_one_or_none()

    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found"
        )

    if attempt.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempt already completed"
        )

    # Parse correct solution
    correct_solution = json.loads(puzzle.solution)

    # Check solution
    correct_pairs = 0
    total_pairs = len(correct_solution)

    for key, value in data.solution.items():
        if correct_solution.get(key) == value:
            correct_pairs += 1

    is_correct = correct_pairs == total_pairs

    # Calculate stars based on time and hints
    stars = 0
    time_bonus = 0
    hints_penalty = attempt.hints_used * 10  # 10 XP per hint

    if is_correct:
        time_limit = puzzle.time_limit_seconds or 300

        if data.time_taken_seconds <= time_limit * 0.5:
            stars = 3
            time_bonus = int(puzzle.xp_reward * 0.3)
        elif data.time_taken_seconds <= time_limit * 0.75:
            stars = 2
            time_bonus = int(puzzle.xp_reward * 0.15)
        else:
            stars = 1

        # Reduce stars for hints used
        if attempt.hints_used >= 2:
            stars = max(1, stars - 1)

    # Calculate XP
    xp_earned = 0
    if is_correct:
        xp_earned = puzzle.xp_reward + time_bonus - hints_penalty
        xp_earned = max(0, xp_earned)  # Don't go negative

    # Update attempt
    attempt.completed_at = datetime.utcnow()
    attempt.time_taken_seconds = data.time_taken_seconds
    attempt.is_completed = True
    attempt.is_correct = is_correct
    attempt.stars = stars
    attempt.xp_earned = xp_earned
    attempt.grid_state = json.dumps(data.solution)

    # Update gamification
    if xp_earned > 0:
        gam_result = await db.execute(
            select(UserGamification)
            .where(UserGamification.user_id == current_user.id)
        )
        gamification = gam_result.scalar_one_or_none()

        if gamification:
            gamification.total_xp += xp_earned
            gamification.daily_xp_earned += xp_earned
            gamification.puzzles_completed += 1
            if stars == 3:
                gamification.puzzles_3_stars += 1

            transaction = XPTransaction(
                user_id=current_user.id,
                amount=xp_earned,
                source=XPSource.PUZZLE_COMPLETE,
                source_id=str(puzzle.id),
                description=f"Completed puzzle: {puzzle.title} ({stars} stars)"
            )
            db.add(transaction)

    await db.commit()

    # Build feedback
    if is_correct:
        if stars == 3:
            feedback = "Perfect! You solved it with 3 stars!"
        elif stars == 2:
            feedback = "Great job! 2 stars earned!"
        else:
            feedback = "Puzzle solved! Try again for more stars!"
    else:
        feedback = f"Not quite right. You got {correct_pairs}/{total_pairs} pairs correct. Try again!"

    return PuzzleResult(
        is_correct=is_correct,
        stars=stars,
        xp_earned=xp_earned,
        time_taken_seconds=data.time_taken_seconds,
        time_bonus=time_bonus,
        hints_penalty=hints_penalty,
        correct_pairs=correct_pairs,
        total_pairs=total_pairs,
        feedback=feedback
    )


@router.post("/{slug}/hint", response_model=HintResponse)
async def get_hint(
    slug: str,
    data: HintRequest,
    db: DbSession,
    current_user: CurrentUser
) -> HintResponse:
    """
    Get a hint for the puzzle (costs XP).
    """
    # Get attempt
    attempt_result = await db.execute(
        select(PuzzleAttempt)
        .where(PuzzleAttempt.id == data.attempt_id)
        .where(PuzzleAttempt.user_id == current_user.id)
    )
    attempt = attempt_result.scalar_one_or_none()

    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found"
        )

    if attempt.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempt already completed"
        )

    max_hints = 3
    if attempt.hints_used >= max_hints:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No more hints available"
        )

    # Get puzzle
    result = await db.execute(
        select(Puzzle).where(Puzzle.id == attempt.puzzle_id)
    )
    puzzle = result.scalar_one_or_none()

    # Generate hint based on hint number
    hint_number = attempt.hints_used + 1
    clues = json.loads(puzzle.clues)

    # Simple hint: reveal a clue interpretation
    hint_text = f"Focus on clue #{hint_number}: Try to identify which items must go together based on this clue."

    if hint_number <= len(clues):
        hint_text = f"Hint for clue '{clues[hint_number - 1].get('text', '')}': Look for direct relationships mentioned."

    # Update hints used
    attempt.hints_used += 1
    xp_penalty = 10 * hint_number  # Increasing penalty

    await db.commit()

    return HintResponse(
        hint_number=hint_number,
        hint_text=hint_text,
        hints_remaining=max_hints - hint_number,
        xp_penalty=xp_penalty
    )
