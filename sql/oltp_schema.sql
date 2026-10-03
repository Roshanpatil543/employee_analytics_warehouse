CREATE DATABASE IF NOT EXISTS employee_analytics;
USE employee_analytics;

DROP TABLE IF EXISTS performance_reviews;
DROP TABLE IF EXISTS project_assignments;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(100) DEFAULT 'Remote',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    department_id INT,
    job_title VARCHAR(100) NOT NULL,
    hire_date DATE,
    manager_id INT,
    salary DECIMAL(12,2) NOT NULL,
    status ENUM('active', 'inactive', 'terminated') DEFAULT 'active',
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

CREATE TABLE projects (
    project_id INT PRIMARY KEY AUTO_INCREMENT,
    project_name VARCHAR(150) NOT NULL,
    department_id INT,
    budget DECIMAL(14,2) DEFAULT 0,
    start_date DATE,
    end_date DATE,
    status ENUM('active', 'completed', 'on_hold') DEFAULT 'active',
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE project_assignments (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    project_id INT NOT NULL,
    allocation_pct DECIMAL(5,2) DEFAULT 100.00,
    assigned_date DATE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

CREATE TABLE performance_reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    review_date DATE NOT NULL,
    manager_id INT,
    overall_score DECIMAL(5,2) NOT NULL,
    rating VARCHAR(25),
    comments TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

DELIMITER $$
CREATE PROCEDURE sp_insert_employee(
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_email VARCHAR(120),
    IN p_department_id INT,
    IN p_job_title VARCHAR(100),
    IN p_hire_date DATE,
    IN p_manager_id INT,
    IN p_salary DECIMAL(12,2),
    IN p_status ENUM('active', 'inactive', 'terminated')
)
BEGIN
    INSERT INTO employees (
        first_name, last_name, email, department_id, job_title,
        hire_date, manager_id, salary, status
    ) VALUES (
        p_first_name, p_last_name, p_email, p_department_id,
        p_job_title, p_hire_date, p_manager_id, p_salary, p_status
    );
END$$
DELIMITER ;
