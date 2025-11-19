-- ENUM types
CREATE TYPE employment_status_enum AS ENUM ('Full-time', 'Part-time', 'Contract', 'Temporary');
CREATE TYPE project_status_enum AS ENUM ('Planning', 'In Progress', 'Completed', 'On Hold', 'Cancelled');
CREATE TYPE review_status_enum AS ENUM ('Draft', 'Final', 'Approved');

-- Companies table
CREATE TABLE Companies (
    company_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(10),
    phone_number VARCHAR(20),
    industry VARCHAR(100),
    website VARCHAR(255)
);

-- Departments table
CREATE TABLE Departments (
    department_id SERIAL PRIMARY KEY,
    company_id INT NOT NULL REFERENCES Companies(company_id),
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    manager_id INT
);

-- Employees table
CREATE TABLE Employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    hire_date DATE NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    department_id INT NOT NULL REFERENCES Departments(department_id),
    salary NUMERIC(10,2) NOT NULL,
    employment_status employment_status_enum NOT NULL
);

-- Projects table
CREATE TABLE Projects (
    project_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    company_id INT NOT NULL REFERENCES Companies(company_id),
    project_status project_status_enum NOT NULL,
    budget NUMERIC(12,2)
);

-- Employee_Projects table
CREATE TABLE Employee_Projects (
    employee_project_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES Employees(employee_id),
    project_id INT NOT NULL REFERENCES Projects(project_id),
    role VARCHAR(100),
    hours_worked NUMERIC(8,2),
    start_date DATE,
    end_date DATE
);

-- Employee_Benefits table
CREATE TABLE Employee_Benefits (
    benefit_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES Employees(employee_id),
    benefit_type VARCHAR(100) NOT NULL,
    enrollment_date DATE NOT NULL,
    coverage_amount NUMERIC(10,2)
);

-- Performance_Reviews table
CREATE TABLE Performance_Reviews (
    review_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES Employees(employee_id),
    reviewer_id INT NOT NULL REFERENCES Employees(employee_id),
    review_date DATE NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    goals_set TEXT,
    review_status review_status_enum DEFAULT 'Draft'
);

-- Add foreign key to Departments.manager_id
ALTER TABLE Departments
ADD CONSTRAINT FK_Departments_ManagerID FOREIGN KEY (manager_id) REFERENCES Employees(employee_id);
