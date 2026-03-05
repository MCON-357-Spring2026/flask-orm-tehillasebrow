"""Exercises: ORM fundamentals.

Implement the TODO functions. Autograder will test them.
"""

from __future__ import annotations

from typing import Optional, Any

from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from src.exercises.extensions import db
from src.exercises.models import Student, Grade, Assignment


# ===== BASIC CRUD =====

def create_student(name: str, email: str) -> Student:
    """TODO: Create and commit a Student; handle duplicate email.

    If email is duplicate:
      - rollback
      - raise ValueError("duplicate email")
    """
    s=Student(name=name, email=email)
    db.session.add(s)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("email must be unique")
    return s


def find_student_by_email(email: str) -> ValueError | Any:
    """TODO: Return Student by email or None."""
    s=Student.query.filter_by(email=email).first()
    if not s:
        return None
    return s


def add_grade(student_id: int, assignment_id: int, score: int) -> Grade:
    """TODO: Add a Grade for the student+assignment and commit.

    If student doesn't exist: raise LookupError
    If assignment doesn't exist: raise LookupError
    If duplicate grade: raise ValueError("duplicate grade")
    """
    s=Student.query.get(student_id)
    if not s:
        raise LookupError
    a=Assignment.query.get(assignment_id)
    if not a:
        raise LookupError
    g=Grade(student_id=student_id, score=score, assignment_id=assignment_id)
    db.session.add(g)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("duplicate grade")
    return g


def average_percent(student_id: int) -> float:
    """TODO: Return student's average percent across assignments.

    percent per grade = score / assignment.max_points * 100

    If student doesn't exist: raise LookupError
    If student has no grades: return 0.0
    """
    s=Student.query.get(student_id)
    if not s:
        raise LookupError
    g=Grade.query.filter_by(student_id=student_id).all()
    if not g:
        return 0.0
    total_percent = 0.0

    for grade in g:
        percent = (grade.score / grade.assignment.max_points) * 100
        total_percent += percent

    return total_percent / len(g)



# ===== QUERYING & FILTERING =====

def get_all_students() -> list[Student]:
    """TODO: Return all students in database, ordered by name."""
    s=Student.query.order_by(Student.name).all()
    return [st for st in s]



def get_assignment_by_title(title: str) -> Optional[Assignment]:
    """TODO: Return assignment by title or None."""
    a=Assignment.query.filter_by(title=title).first()
    if not a:
        return None
    return a

def get_student_grades(student_id: int) -> list[Grade]:
    """TODO: Return all grades for a student, ordered by assignment title.

    If student doesn't exist: raise LookupError
    """
    s=db.session.get(Student, student_id)
    if not s:
        raise LookupError
    rows=(
        Grade.query.filter_by(student_id=student_id)
        .order_by(Grade.assignment).all()
    )
    payload=[]
    for g in rows:
        g["assignment"] = {"id": g.assignment.id, "title": g.assignment.title, "max_points": g.assignment.max_points}
        payload.append(g)
    return payload



def get_grades_for_assignment(assignment_id: int) -> list[Grade]:
    """TODO: Return all grades for an assignment, ordered by student name.

    If assignment doesn't exist: raise LookupError
    """
    raise NotImplementedError


# ===== AGGREGATION =====

def total_student_grade_count() -> int:
    """TODO: Return total number of grades in database."""
    raise NotImplementedError


def highest_score_on_assignment(assignment_id: int) -> Optional[int]:
    """TODO: Return the highest score on an assignment, or None if no grades.

    If assignment doesn't exist: raise LookupError
    """
    raise NotImplementedError


def class_average_percent() -> float:
    """TODO: Return average percent across all students and all assignments.

    percent per grade = score / assignment.max_points * 100
    Return average of all these percents.
    If no grades: return 0.0
    """
    raise NotImplementedError


def student_grade_count(student_id: int) -> int:
    """TODO: Return number of grades for a student.

    If student doesn't exist: raise LookupError
    """
    raise NotImplementedError


# ===== UPDATING & DELETION =====

def update_student_email(student_id: int, new_email: str) -> Student:
    """TODO: Update a student's email and commit.

    If student doesn't exist: raise LookupError
    If new email is duplicate: rollback and raise ValueError("duplicate email")
    Return the updated student.
    """
    raise NotImplementedError


def delete_student(student_id: int) -> None:
    """TODO: Delete a student and all their grades; commit.

    If student doesn't exist: raise LookupError
    """
    raise NotImplementedError


def delete_grade(grade_id: int) -> None:
    """TODO: Delete a grade by id; commit.

    If grade doesn't exist: raise LookupError
    """
    raise NotImplementedError


# ===== FILTERING & FILTERING WITH AGGREGATION =====

def students_with_average_above(threshold: float) -> list[Student]:
    """TODO: Return students whose average percent is above threshold.

    List should be ordered by average percent descending.
    percent per grade = score / assignment.max_points * 100
    """
    raise NotImplementedError


def assignments_without_grades() -> list[Assignment]:
    """TODO: Return assignments that have no grades yet, ordered by title."""
    raise NotImplementedError


def top_scorer_on_assignment(assignment_id: int) -> Optional[Student]:
    """TODO: Return the Student with the highest score on an assignment.

    If assignment doesn't exist: raise LookupError
    If no grades on assignment: return None
    If tie (multiple students with same high score): return any one
    """
    raise NotImplementedError

