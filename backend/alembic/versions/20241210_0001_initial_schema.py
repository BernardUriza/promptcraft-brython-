"""Initial schema with all tables

Revision ID: 0001
Revises:
Create Date: 2024-12-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(100), nullable=True),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_verified', sa.Boolean(), default=False),
        sa.Column('is_admin', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('last_activity', sa.DateTime(), nullable=True),
        sa.Column('settings', sa.Text(), nullable=True),
    )

    # Lessons table
    op.create_table(
        'lessons',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('slug', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(10), default='📚'),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('difficulty', sa.String(50), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), default=10),
        sa.Column('xp_reward', sa.Integer(), default=50),
        sa.Column('order', sa.Integer(), default=0),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('objectives', sa.Text(), nullable=True),
        sa.Column('exercise', sa.Text(), nullable=True),
        sa.Column('next_lesson_id', sa.Integer(), sa.ForeignKey('lessons.id'), nullable=True),
        sa.Column('is_published', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Lesson progress table
    op.create_table(
        'lesson_progress',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('lesson_id', sa.Integer(), sa.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('status', sa.String(50), default='not_started'),
        sa.Column('current_section', sa.Integer(), default=0),
        sa.Column('progress_percent', sa.Integer(), default=0),
        sa.Column('exercise_completed', sa.Boolean(), default=False),
        sa.Column('exercise_answer', sa.Text(), nullable=True),
        sa.Column('exercise_score', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('last_accessed', sa.DateTime(), nullable=False),
    )

    # Puzzles table
    op.create_table(
        'puzzles',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('slug', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(10), default='🧩'),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('difficulty', sa.String(50), nullable=False),
        sa.Column('grid_size', sa.Text(), nullable=True),
        sa.Column('categories', sa.Text(), nullable=True),
        sa.Column('clues', sa.Text(), nullable=True),
        sa.Column('solution', sa.Text(), nullable=True),
        sa.Column('xp_reward', sa.Integer(), default=50),
        sa.Column('time_limit_seconds', sa.Integer(), default=300),
        sa.Column('order', sa.Integer(), default=0),
        sa.Column('is_daily', sa.Boolean(), default=False),
        sa.Column('is_published', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Puzzle attempts table
    op.create_table(
        'puzzle_attempts',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('puzzle_id', sa.Integer(), sa.ForeignKey('puzzles.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('time_taken_seconds', sa.Integer(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), default=False),
        sa.Column('is_correct', sa.Boolean(), default=False),
        sa.Column('stars', sa.Integer(), default=0),
        sa.Column('hints_used', sa.Integer(), default=0),
        sa.Column('xp_earned', sa.Integer(), default=0),
        sa.Column('grid_state', sa.Text(), nullable=True),
    )

    # User gamification table
    op.create_table(
        'user_gamification',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('total_xp', sa.Integer(), default=0),
        sa.Column('level', sa.Integer(), default=1),
        sa.Column('current_streak', sa.Integer(), default=0),
        sa.Column('longest_streak', sa.Integer(), default=0),
        sa.Column('streak_freezes', sa.Integer(), default=0),
        sa.Column('last_activity_date', sa.Date(), nullable=True),
        sa.Column('lessons_completed', sa.Integer(), default=0),
        sa.Column('puzzles_completed', sa.Integer(), default=0),
        sa.Column('puzzles_3_stars', sa.Integer(), default=0),
        sa.Column('total_time_minutes', sa.Integer(), default=0),
        sa.Column('daily_xp_goal', sa.Integer(), default=50),
        sa.Column('daily_xp_earned', sa.Integer(), default=0),
        sa.Column('daily_goal_streak', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # XP transactions table
    op.create_table(
        'xp_transactions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('source_id', sa.String(100), nullable=True),
        sa.Column('multiplier', sa.Float(), default=1.0),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
    )

    # Badges table
    op.create_table(
        'badges',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('slug', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(10), default='🏆'),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('rarity', sa.String(50), default='common'),
        sa.Column('condition', sa.Text(), nullable=True),
        sa.Column('xp_reward', sa.Integer(), default=0),
        sa.Column('is_hidden', sa.Boolean(), default=False),
        sa.Column('order', sa.Integer(), default=0),
    )

    # User badges table
    op.create_table(
        'user_badges',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('badge_id', sa.Integer(), sa.ForeignKey('badges.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('earned_at', sa.DateTime(), nullable=False),
        sa.Column('notified', sa.Boolean(), default=False),
    )

    # Daily challenges table
    op.create_table(
        'daily_challenges',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('challenge_date', sa.Date(), unique=True, nullable=False, index=True),
        sa.Column('challenge_type', sa.String(50), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=True),
        sa.Column('target_count', sa.Integer(), default=1),
        sa.Column('xp_reward', sa.Integer(), default=50),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
    )

    # User daily challenges table
    op.create_table(
        'user_daily_challenges',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('challenge_id', sa.Integer(), sa.ForeignKey('daily_challenges.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('progress', sa.Integer(), default=0),
        sa.Column('is_completed', sa.Boolean(), default=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('user_daily_challenges')
    op.drop_table('daily_challenges')
    op.drop_table('user_badges')
    op.drop_table('badges')
    op.drop_table('xp_transactions')
    op.drop_table('user_gamification')
    op.drop_table('puzzle_attempts')
    op.drop_table('puzzles')
    op.drop_table('lesson_progress')
    op.drop_table('lessons')
    op.drop_table('users')
