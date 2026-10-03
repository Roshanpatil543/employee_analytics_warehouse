from __future__ import annotations

from typing import Iterable

from app.db_manager import DatabaseConnection


class WarehouseETL(DatabaseConnection):
    """ETL helper for loading OLTP data into the warehouse."""

    def build_date_dimension(self) -> None:
        query = """
            INSERT INTO dim_date (date_key, full_date, year_num, quarter_num, month_num, day_num)
            SELECT
                YEAR(d.review_date) * 10000 + MONTH(d.review_date) * 100 + DAY(d.review_date),
                d.review_date,
                YEAR(d.review_date),
                QUARTER(d.review_date),
                MONTH(d.review_date),
                DAY(d.review_date)
            FROM performance_reviews d
            GROUP BY d.review_date
            ON DUPLICATE KEY UPDATE full_date = VALUES(full_date)
        """
        self.execute(query)
        self.get_connection().commit()

    def load_employee_dimension(self) -> None:
        query = """
            INSERT INTO dim_employee (
                employee_key, employee_id, first_name, last_name, email,
                department_id, job_title, hire_date, salary, start_date, end_date, is_current
            )
            SELECT
                e.employee_id,
                e.employee_id,
                e.first_name,
                e.last_name,
                e.email,
                e.department_id,
                e.job_title,
                e.hire_date,
                e.salary,
                COALESCE(e.hire_date, CURRENT_DATE),
                NULL,
                TRUE
            FROM employees e
            ON DUPLICATE KEY UPDATE
                first_name = VALUES(first_name),
                last_name = VALUES(last_name),
                salary = VALUES(salary)
        """
        self.execute(query)
        self.get_connection().commit()

    def load_fact_reviews(self) -> None:
        query = """
            INSERT INTO fact_performance_reviews (
                employee_id, department_id, project_id, review_date, overall_score, rating, review_year
            )
            SELECT
                pr.employee_id,
                e.department_id,
                pa.project_id,
                pr.review_date,
                pr.overall_score,
                pr.rating,
                YEAR(pr.review_date)
            FROM performance_reviews pr
            JOIN employees e ON pr.employee_id = e.employee_id
            LEFT JOIN project_assignments pa ON pa.employee_id = pr.employee_id
            ON DUPLICATE KEY UPDATE overall_score = VALUES(overall_score)
        """
        self.execute(query)
        self.get_connection().commit()

    def run_full_etl(self) -> None:
        self.build_date_dimension()
        self.load_employee_dimension()
        self.load_fact_reviews()
