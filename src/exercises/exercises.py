"""Exercises: ORM fundamentals.

Implemented full file with logic for CRUD, filtering, and aggregation.
"""

from __future__ import annotations

from typing import Optional, Any
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from src.exercises.extensions import db
from src.exercises.models import Student, Grade, Assignment


# ===== BASIC CRUD =====

def create_student(name: str, email: str) -> Student:
    """Create and commit a Student; handle duplicate email."""
    s = Student(name=name, email=email)
    db.session.add(s)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("duplicate email")
    return s


def find_student_by_email(email: str) -> Optional[Student]:
    """Return Student by email or None."""
    return Student.query.filter_by(email=email).first()


def add_grade(student_id: int, assignment_id: int, score: int) -> Grade:
    """Add a Grade for the student+assignment and commit."""
    if not db.session.get(Student, student_id):
        raise LookupError("Student not found")
    if not db.session.get(Assignment, assignment_id):
        raise LookupError("Assignment not found")

    g = Grade(student_id=student_id, assignment_id=assignment_id, score=score)
    db.session.add(g)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("duplicate grade")
    return g


def average_percent(student_id: int) -> float:
    """Return student's average percent across assignments."""
    if not db.session.get(Student, student_id):
        raise LookupError

    grades = Grade.query.filter_by(student_id=student_id).all()
    if not grades:
        return 0.0

    total_percent = sum((g.score / g.assignment.max_points) * 100 for g in grades)
    return total_percent / len(grades)


# ===== QUERYING & FILTERING =====

def get_all_students() -> list[Student]:
    """Return all students in database, ordered by name."""
    return Student.query.order_by(Student.name).all()


def get_assignment_by_title(title: str) -> Optional[Assignment]:
    """Return assignment by title or None."""
    return Assignment.query.filter_by(title=title).first()


def get_student_grades(student_id: int) -> list[Grade]:
    """Return all grades for a student, ordered by assignment title."""
    if not db.session.get(Student, student_id):
        raise LookupError

    return Grade.query.join(Assignment).filter(Grade.student_id == student_id) \
        .order_by(Assignment.title).all()


def get_grades_for_assignment(assignment_id: int) -> list[Grade]:
    """Return all grades for an assignment, ordered by student name."""
    if not db.session.get(Assignment, assignment_id):
        raise LookupError

    return Grade.query.join(Student).filter(Grade.assignment_id == assignment_id) \
        .order_by(Student.name).all()


# ===== AGGREGATION =====

def total_student_grade_count() -> int:
    """Return total number of grades in database."""
    return db.session.query(func.count(Grade.id)).scalar() or 0


def highest_score_on_assignment(assignment_id: int) -> Optional[int]:
    """Return the highest score on an assignment, or None if no grades."""
    if not db.session.get(Assignment, assignment_id):
        raise LookupError

    return db.session.query(func.max(Grade.score)) \
        .filter(Grade.assignment_id == assignment_id).scalar()


def class_average_percent() -> float:
    """Return average percent across all students and all assignments."""
    # We use select_from(Grade) to establish the starting point for the join
    avg_val = db.session.query(
        func.avg((Grade.score * 100.0) / Assignment.max_points)
    ).select_from(Grade).join(Assignment).scalar()

    return float(avg_val) if avg_val is not None else 0.0


def student_grade_count(student_id: int) -> int:
    """Return number of grades for a student."""
    if not db.session.get(Student, student_id):
        raise LookupError
    return Grade.query.filter_by(student_id=student_id).count()


# ===== UPDATING & DELETION =====

def update_student_email(student_id: int, new_email: str) -> Student:
    """Update a student's email and commit."""
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError

    student.email = new_email
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("duplicate email")
    return student


def delete_student(student_id: int) -> None:
    """Delete a student and all their grades; commit."""
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError

    Grade.query.filter_by(student_id=student_id).delete()
    db.session.delete(student)
    db.session.commit()


def delete_grade(grade_id: int) -> None:
    """Delete a grade by id; commit."""
    grade = db.session.get(Grade, grade_id)
    if not grade:
        raise LookupError
    db.session.delete(grade)
    db.session.commit()


# ===== FILTERING & FILTERING WITH AGGREGATION =====

def students_with_average_above(threshold: float) -> list[Student]:
    """Return students whose average percent is above threshold."""
    avg_score_expr = func.avg((Grade.score * 100.0) / Assignment.max_points)

    results = db.session.query(Student) \
        .join(Grade) \
        .join(Assignment) \
        .group_by(Student.id) \
        .having(avg_score_expr > threshold) \
        .order_by(avg_score_expr.desc()) \
        .all()

    return results


def assignments_without_grades() -> list[Assignment]:
    """Return assignments that have no grades yet, ordered by title."""
    return Assignment.query.outerjoin(Grade) \
        .filter(Grade.id == None) \
        .order_by(Assignment.title).all()


def top_scorer_on_assignment(assignment_id: int) -> Optional[Student]:
    """Return the Student with the highest score on an assignment."""
    if not db.session.get(Assignment, assignment_id):
        raise LookupError

    top_grade = Grade.query.filter_by(assignment_id=assignment_id) \
        .order_by(Grade.score.desc()).first()

    return top_grade.student if top_grade else None