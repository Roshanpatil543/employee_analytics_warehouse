USE employee_analytics;

WITH department_stage AS (
    SELECT
        department_id,
        department_name,
        location
    FROM departments
),
employee_stage AS (
    SELECT
        employee_id,
        first_name,
        last_name,
        email,
        department_id,
        job_title,
        hire_date,
        salary
    FROM employees
),
review_stage AS (
    SELECT
        review_id,
        employee_id,
        review_date,
        overall_score,
        rating,
        ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY review_date DESC) AS review_rank
    FROM performance_reviews
)
SELECT *
FROM review_stage
WHERE review_rank = 1;

CREATE PROCEDURE sp_load_dim_employee()
BEGIN
    INSERT INTO dim_employee (
        employee_id, first_name, last_name, email,
        department_id, job_title, hire_date, salary,
        start_date, end_date, is_current
    )
    SELECT
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
        salary = VALUES(salary);
END;

CREATE PROCEDURE sp_load_fact_reviews()
BEGIN
    INSERT INTO fact_performance_reviews (
        employee_id, department_id, project_id, review_date,
        overall_score, rating, review_year
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
    ON DUPLICATE KEY UPDATE overall_score = VALUES(overall_score);
END;
