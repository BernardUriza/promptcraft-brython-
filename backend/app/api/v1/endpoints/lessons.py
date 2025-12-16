# PromptCraft - Lessons Endpoints

from datetime import datetime
from typing import Optional
import json
from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.deps import DbSession, CurrentUser, OptionalUser
from app.models.lesson import Lesson, LessonProgress, ProgressStatus
from app.models.gamification import UserGamification, XPTransaction, XPSource
from app.schemas.lesson import (
    LessonResponse,
    LessonListItem,
    LessonListResponse,
    LessonProgressResponse,
    LessonProgressUpdate,
    ExerciseSubmit,
    ExerciseResult,
    LessonSection,
    LessonExercise
)
from app.config import settings

router = APIRouter()


def parse_lesson_content(content_json: str) -> list[LessonSection]:
    """Parse lesson content JSON to list of sections."""
    try:
        sections = json.loads(content_json)
        return [LessonSection(**s) for s in sections]
    except (json.JSONDecodeError, TypeError):
        return []


def parse_lesson_exercise(exercise_json: Optional[str]) -> Optional[LessonExercise]:
    """Parse lesson exercise JSON."""
    if not exercise_json:
        return None
    try:
        return LessonExercise(**json.loads(exercise_json))
    except (json.JSONDecodeError, TypeError):
        return None


@router.get("/", response_model=LessonListResponse)
async def list_lessons(
    db: DbSession,
    current_user: OptionalUser = None,
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
) -> LessonListResponse:
    """
    List all published lessons with optional filters.
    """
    # Base query
    query = select(Lesson).where(Lesson.is_published == True)

    # Apply filters
    if category:
        query = query.where(Lesson.category == category)
    if difficulty:
        query = query.where(Lesson.difficulty == difficulty)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Order and paginate
    query = (
        query
        .order_by(Lesson.order, Lesson.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
    )

    result = await db.execute(query)
    lessons = result.scalars().all()

    # Get user progress if authenticated
    user_progress = {}
    if current_user:
        progress_result = await db.execute(
            select(LessonProgress)
            .where(LessonProgress.user_id == current_user.id)
            .where(LessonProgress.lesson_id.in_([l.id for l in lessons]))
        )
        for progress in progress_result.scalars().all():
            user_progress[progress.lesson_id] = progress

    # Build response
    items = []
    for lesson in lessons:
        progress = user_progress.get(lesson.id)
        items.append(LessonListItem(
            id=lesson.id,
            slug=lesson.slug,
            title=lesson.title,
            description=lesson.description,
            icon=lesson.icon,
            category=lesson.category,
            difficulty=lesson.difficulty,
            duration_minutes=lesson.duration_minutes,
            xp_reward=lesson.xp_reward,
            order=lesson.order,
            status=progress.status if progress else ProgressStatus.NOT_STARTED,
            progress_percent=progress.progress_percent if progress else 0
        ))

    return LessonListResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=(total + per_page - 1) // per_page
    )


@router.get("/{slug}", response_model=LessonResponse)
async def get_lesson(
    slug: str,
    db: DbSession,
    current_user: OptionalUser = None
) -> LessonResponse:
    """
    Get a single lesson by slug.
    """
    result = await db.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    # Get user progress if authenticated
    user_progress = None
    if current_user:
        progress_result = await db.execute(
            select(LessonProgress)
            .where(LessonProgress.user_id == current_user.id)
            .where(LessonProgress.lesson_id == lesson.id)
        )
        progress = progress_result.scalar_one_or_none()
        if progress:
            user_progress = LessonProgressResponse.model_validate(progress)

    # Parse content
    content = parse_lesson_content(lesson.content)
    exercise = parse_lesson_exercise(lesson.exercise)
    objectives = json.loads(lesson.objectives) if lesson.objectives else []

    return LessonResponse(
        id=lesson.id,
        slug=lesson.slug,
        title=lesson.title,
        description=lesson.description,
        icon=lesson.icon,
        category=lesson.category,
        difficulty=lesson.difficulty,
        duration_minutes=lesson.duration_minutes,
        xp_reward=lesson.xp_reward,
        content=content,
        objectives=objectives,
        exercise=exercise,
        next_lesson_id=lesson.next_lesson_id,
        is_published=lesson.is_published,
        order=lesson.order,
        created_at=lesson.created_at,
        updated_at=lesson.updated_at,
        user_progress=user_progress
    )


@router.post("/{slug}/start", response_model=LessonProgressResponse)
async def start_lesson(
    slug: str,
    db: DbSession,
    current_user: CurrentUser
) -> LessonProgressResponse:
    """
    Start a lesson (create progress record).
    """
    # Get lesson
    result = await db.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    # Check for existing progress
    progress_result = await db.execute(
        select(LessonProgress)
        .where(LessonProgress.user_id == current_user.id)
        .where(LessonProgress.lesson_id == lesson.id)
    )
    progress = progress_result.scalar_one_or_none()

    if progress:
        # Update last accessed
        progress.last_accessed = datetime.utcnow()
        if progress.status == ProgressStatus.NOT_STARTED:
            progress.status = ProgressStatus.IN_PROGRESS
            progress.started_at = datetime.utcnow()
    else:
        # Create new progress
        progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson.id,
            status=ProgressStatus.IN_PROGRESS,
            current_section=0,
            progress_percent=0,
            started_at=datetime.utcnow(),
            last_accessed=datetime.utcnow()
        )
        db.add(progress)

    await db.commit()
    await db.refresh(progress)

    return LessonProgressResponse.model_validate(progress)


@router.patch("/{slug}/progress", response_model=LessonProgressResponse)
async def update_lesson_progress(
    slug: str,
    data: LessonProgressUpdate,
    db: DbSession,
    current_user: CurrentUser
) -> LessonProgressResponse:
    """
    Update lesson progress.
    """
    # Get lesson
    result = await db.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    # Get progress
    progress_result = await db.execute(
        select(LessonProgress)
        .where(LessonProgress.user_id == current_user.id)
        .where(LessonProgress.lesson_id == lesson.id)
    )
    progress = progress_result.scalar_one_or_none()

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lesson not started"
        )

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(progress, field, value)

    progress.last_accessed = datetime.utcnow()
    await db.commit()
    await db.refresh(progress)

    return LessonProgressResponse.model_validate(progress)


@router.post("/{slug}/complete", response_model=ExerciseResult)
async def complete_lesson(
    slug: str,
    db: DbSession,
    current_user: CurrentUser
) -> ExerciseResult:
    """
    Mark lesson as completed and award XP.
    """
    # Get lesson
    result = await db.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    # Get progress
    progress_result = await db.execute(
        select(LessonProgress)
        .where(LessonProgress.user_id == current_user.id)
        .where(LessonProgress.lesson_id == lesson.id)
    )
    progress = progress_result.scalar_one_or_none()

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lesson not started"
        )

    # Check if already completed
    already_completed = progress.status == ProgressStatus.COMPLETED
    xp_earned = 0

    if not already_completed:
        # Update progress
        progress.status = ProgressStatus.COMPLETED
        progress.progress_percent = 100
        progress.completed_at = datetime.utcnow()
        progress.last_accessed = datetime.utcnow()

        # Award XP
        xp_earned = lesson.xp_reward

        # Get gamification record
        gam_result = await db.execute(
            select(UserGamification)
            .where(UserGamification.user_id == current_user.id)
        )
        gamification = gam_result.scalar_one_or_none()

        if gamification:
            gamification.total_xp += xp_earned
            gamification.daily_xp_earned += xp_earned
            gamification.lessons_completed += 1

            # Create XP transaction
            transaction = XPTransaction(
                user_id=current_user.id,
                amount=xp_earned,
                source=XPSource.LESSON_COMPLETE,
                source_id=str(lesson.id),
                description=f"Completed lesson: {lesson.title}"
            )
            db.add(transaction)

    await db.commit()

    return ExerciseResult(
        is_correct=True,
        score=100,
        feedback="Lesson completed successfully!" if not already_completed else "Lesson already completed",
        xp_earned=xp_earned
    )


@router.post("/{slug}/exercise", response_model=ExerciseResult)
async def submit_exercise(
    slug: str,
    data: ExerciseSubmit,
    db: DbSession,
    current_user: CurrentUser
) -> ExerciseResult:
    """
    Submit lesson exercise answer.
    """
    # Get lesson
    result = await db.execute(
        select(Lesson).where(Lesson.slug == slug)
    )
    lesson = result.scalar_one_or_none()

    if not lesson or not lesson.exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson or exercise not found"
        )

    # Get progress
    progress_result = await db.execute(
        select(LessonProgress)
        .where(LessonProgress.user_id == current_user.id)
        .where(LessonProgress.lesson_id == lesson.id)
    )
    progress = progress_result.scalar_one_or_none()

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lesson not started"
        )

    # Parse exercise
    exercise = parse_lesson_exercise(lesson.exercise)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid exercise data"
        )

    # Check answer (simplified logic)
    is_correct = False
    score = 0

    if exercise.type == "multiple_choice":
        is_correct = str(data.answer) == str(exercise.correct_answer)
        score = 100 if is_correct else 0
    else:
        # For open-ended exercises, score based on length/quality
        answer_str = str(data.answer)
        if len(answer_str) > 50:
            score = 80
            is_correct = True
        elif len(answer_str) > 20:
            score = 60
            is_correct = True
        else:
            score = 30

    # Update progress
    progress.exercise_completed = is_correct
    progress.exercise_score = score
    progress.exercise_answer = json.dumps(data.answer) if isinstance(data.answer, (list, dict)) else str(data.answer)

    # Award bonus XP for exercise
    xp_earned = 0
    if is_correct and not progress.exercise_completed:
        xp_earned = int(lesson.xp_reward * 0.5)  # 50% bonus for exercise

        gam_result = await db.execute(
            select(UserGamification)
            .where(UserGamification.user_id == current_user.id)
        )
        gamification = gam_result.scalar_one_or_none()

        if gamification:
            gamification.total_xp += xp_earned
            gamification.daily_xp_earned += xp_earned

            transaction = XPTransaction(
                user_id=current_user.id,
                amount=xp_earned,
                source=XPSource.EXERCISE_COMPLETE,
                source_id=str(lesson.id),
                description=f"Exercise completed: {lesson.title}"
            )
            db.add(transaction)

    await db.commit()

    feedback = "Correct! Well done!" if is_correct else "Keep trying! Review the lesson content for hints."

    return ExerciseResult(
        is_correct=is_correct,
        score=score,
        feedback=feedback,
        xp_earned=xp_earned,
        correct_answer=exercise.correct_answer if not is_correct else None
    )
