from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Employee:
    employee_id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    department_id: Optional[int] = None
    job_title: str = ""
    hire_date: Optional[date] = None
    manager_id: Optional[int] = None
    salary: float = 0.0
    status: str = "active"

    def validate(self) -> None:
        if not self.first_name or not self.last_name:
            raise ValueError("Employee name is required.")
        if "@" not in self.email:
            raise ValueError("Valid employee email is required.")
        if self.salary <= 0:
            raise ValueError("Salary must be greater than zero.")


@dataclass
class Project:
    project_id: Optional[int] = None
    project_name: str = ""
    department_id: Optional[int] = None
    budget: float = 0.0
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "active"

    def validate(self) -> None:
        if not self.project_name:
            raise ValueError("Project name is required.")
        if self.budget < 0:
            raise ValueError("Budget cannot be negative.")


@dataclass
class Review:
    review_id: Optional[int] = None
    employee_id: Optional[int] = None
    review_date: Optional[date] = None
    manager_id: Optional[int] = None
    overall_score: float = 0.0
    rating: str = "Needs Improvement"
    comments: str = ""

    def validate(self) -> None:
        if self.employee_id is None:
            raise ValueError("Employee id is required.")
        if not 0 <= self.overall_score <= 100:
            raise ValueError("Review score must be between 0 and 100.")
