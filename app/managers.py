from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Optional

from app.db_manager import DatabaseConnection
from app.models import Employee, Project, Review


class EmployeeManager(DatabaseConnection):
    """CRUD manager for employee transactional records."""

    def create_employee(self, employee: Employee) -> int:
        employee.validate()
        query = """
            INSERT INTO employees (
                first_name, last_name, email, department_id, job_title,
                hire_date, manager_id, salary, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.department_id,
            employee.job_title,
            employee.hire_date,
            employee.manager_id,
            employee.salary,
            employee.status,
        )
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            employee.employee_id = cursor.lastrowid
            cursor.close()
            return employee.employee_id
        except Exception as exc:  # pragma: no cover - DB runtime path
            if conn is not None:
                conn.rollback()
            raise RuntimeError(f"Failed to create employee: {exc}") from exc

    def get_employee(self, employee_id: int) -> Optional[dict]:
        query = "SELECT * FROM employees WHERE employee_id = %s"
        return self.fetch_one(query, (employee_id,))

    def list_employees(self, limit: int = 25) -> List[dict]:
        query = "SELECT * FROM employees ORDER BY employee_id DESC LIMIT %s"
        return self.fetch_all(query, (limit,))

    def update_department(self, employee_id: int, new_department_id: int) -> None:
        query = "UPDATE employees SET department_id = %s WHERE employee_id = %s"
        self.execute(query, (new_department_id, employee_id))
        self.get_connection().commit()

    def update_salary(self, employee_id: int, new_salary: float) -> None:
        query = "UPDATE employees SET salary = %s WHERE employee_id = %s"
        self.execute(query, (new_salary, employee_id))
        self.get_connection().commit()


class ProjectManager(DatabaseConnection):
    """Manager for project lifecycle and assignment tasks."""

    def create_project(self, project: Project) -> int:
        project.validate()
        query = """
            INSERT INTO projects (project_name, department_id, budget, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            project.project_name,
            project.department_id,
            project.budget,
            project.start_date,
            project.end_date,
            project.status,
        )
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            project.project_id = cursor.lastrowid
            cursor.close()
            return project.project_id
        except Exception as exc:  # pragma: no cover - DB runtime path
            if conn is not None:
                conn.rollback()
            raise RuntimeError(f"Failed to create project: {exc}") from exc

    def assign_employee(self, employee_id: int, project_id: int, allocation_pct: float = 100.0) -> None:
        query = """
            INSERT INTO project_assignments (employee_id, project_id, allocation_pct, assigned_date)
            VALUES (%s, %s, %s, %s)
        """
        params = (employee_id, project_id, allocation_pct, datetime.utcnow().date())
        self.execute(query, params)
        self.get_connection().commit()


class AnalyticsManager(DatabaseConnection):
    """Warehouse analytics queries for dashboarding."""

    def get_performance_trends(self):
        query = """
            SELECT review_year, AVG(overall_score) AS avg_score
            FROM fact_performance_reviews
            GROUP BY review_year
            ORDER BY review_year ASC
        """
        return self.fetch_all(query)

    def get_top_performers(self):
        query = """
            WITH ranked AS (
                SELECT
                    e.employee_id,
                    e.first_name,
                    e.last_name,
                    d.department_name,
                    f.overall_score,
                    DENSE_RANK() OVER (
                        PARTITION BY d.department_name ORDER BY f.overall_score DESC
                    ) AS dept_rank
                FROM fact_performance_reviews f
                JOIN dim_employee e ON f.employee_id = e.employee_id
                JOIN dim_department d ON e.department_id = d.department_id
            )
            SELECT * FROM ranked WHERE dept_rank <= 5
            ORDER BY department_name, dept_rank
        """
        return self.fetch_all(query)

    def get_attrition_risk(self):
        query = """
            SELECT department_name, COUNT(*) AS employees, AVG(performance_score) AS avg_performance
            FROM dim_employee e
            JOIN dim_department d ON e.department_id = d.department_id
            WHERE e.is_current = 1
            GROUP BY department_name
            ORDER BY avg_performance ASC
        """
        return self.fetch_all(query)
