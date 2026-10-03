USE employee_analytics;

DROP TABLE IF EXISTS fact_performance_reviews;
DROP TABLE IF EXISTS dim_employee;
DROP TABLE IF EXISTS dim_project;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_department;

CREATE TABLE dim_department (
    department_key INT PRIMARY KEY AUTO_INCREMENT,
    department_id INT NOT NULL,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    UNIQUE KEY uk_dim_department (department_id)
);

CREATE TABLE dim_employee (
    employee_key INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(120),
    department_id INT,
    job_title VARCHAR(100),
    hire_date DATE,
    salary DECIMAL(12,2),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    UNIQUE KEY uk_dim_employee (employee_id, start_date)
);

CREATE TABLE dim_project (
    project_key INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    project_name VARCHAR(150),
    department_id INT,
    budget DECIMAL(14,2),
    start_date DATE,
    end_date DATE,
    UNIQUE KEY uk_dim_project (project_id)
);

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year_num INT,
    quarter_num INT,
    month_num INT,
    day_num INT,
    UNIQUE KEY uk_dim_date (full_date)
);

CREATE TABLE fact_performance_reviews (
    review_fact_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    department_id INT,
    project_id INT,
    review_date DATE,
    overall_score DECIMAL(5,2),
    rating VARCHAR(25),
    review_year INT,
    FOREIGN KEY (employee_id) REFERENCES dim_employee(employee_key),
    FOREIGN KEY (department_id) REFERENCES dim_department(department_key),
    FOREIGN KEY (project_id) REFERENCES dim_project(project_key)
);
