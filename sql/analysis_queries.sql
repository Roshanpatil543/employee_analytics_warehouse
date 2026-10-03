USE employee_analytics;

-- Year-over-year performance trend
SELECT
    YEAR(review_date) AS review_year,
    AVG(overall_score) AS avg_score
FROM performance_reviews
GROUP BY YEAR(review_date)
ORDER BY review_year;

-- Top performers by department using window functions
WITH ranked_reviews AS (
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        d.department_name,
        pr.overall_score,
        DENSE_RANK() OVER (
            PARTITION BY d.department_name
            ORDER BY pr.overall_score DESC
        ) AS dept_rank
    FROM performance_reviews pr
    JOIN employees e ON pr.employee_id = e.employee_id
    JOIN departments d ON e.department_id = d.department_id
)
SELECT *
FROM ranked_reviews
WHERE dept_rank <= 5
ORDER BY department_name, dept_rank;

-- Attrition risk summary for current employees
SELECT
    d.department_name,
    COUNT(e.employee_id) AS total_employees,
    AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.status = 'active'
GROUP BY d.department_name
ORDER BY avg_salary DESC;
