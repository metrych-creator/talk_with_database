-- Create ENUM types
CREATE TYPE book_format_enum AS ENUM ('Hardcover', 'Paperback', 'E-book', 'Audiobook');
CREATE TYPE gender_enum AS ENUM ('Male', 'Female', 'Other');
CREATE TYPE membership_type_enum AS ENUM ('Regular', 'Premium', 'Student', 'Senior');
CREATE TYPE account_status_enum AS ENUM ('Active', 'Inactive', 'Suspended', 'Closed');
CREATE TYPE condition_enum AS ENUM ('New', 'Good', 'Fair', 'Poor');
CREATE TYPE loan_status_enum AS ENUM ('Checked Out', 'Returned', 'Overdue', 'Lost', 'Renewed');

-- Authors table
CREATE TABLE Authors (
    author_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE,
    death_date DATE,
    nationality VARCHAR(100),
    biography TEXT
);

-- Publishers table
CREATE TABLE Publishers (
    publisher_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(100),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20)
);

-- Books table
CREATE TABLE Books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INT NOT NULL REFERENCES Authors(author_id),
    publisher_id INT NOT NULL REFERENCES Publishers(publisher_id),
    isbn VARCHAR(20) UNIQUE NOT NULL,
    publication_date DATE,
    genre VARCHAR(100),
    edition VARCHAR(50),
    number_of_pages INT,
    language VARCHAR(50),
    format book_format_enum
);

-- Library_Branches table
CREATE TABLE Library_Branches (
    branch_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(10),
    phone_number VARCHAR(20),
    manager_id INT,
    opening_hours VARCHAR(255)
);

-- Library_Members table
CREATE TABLE Library_Members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender gender_enum,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    join_date DATE NOT NULL,
    membership_type membership_type_enum,
    account_status account_status_enum DEFAULT 'Active'
);

-- Book_Inventory table
CREATE TABLE Book_Inventory (
    inventory_id SERIAL PRIMARY KEY,
    book_id INT NOT NULL REFERENCES Books(book_id),
    branch_id INT NOT NULL REFERENCES Library_Branches(branch_id),
    quantity INT NOT NULL,
    available_quantity INT NOT NULL,
    condition condition_enum
);

-- Book_Loans table
CREATE TABLE Book_Loans (
    loan_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL REFERENCES Library_Members(member_id),
    inventory_id INT NOT NULL REFERENCES Book_Inventory(inventory_id),
    loan_date TIMESTAMP NOT NULL,
    due_date DATE NOT NULL,
    return_date TIMESTAMP,
    loan_status loan_status_enum DEFAULT 'Checked Out',
    fine_amount NUMERIC(10,2) DEFAULT 0
);


-- Departments table
CREATE TABLE Departments (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(255),
    manager_id INT
    -- FOREIGN KEY (manager_id) REFERENCES Employees(employee_id)
);

-- Employees table
CREATE TABLE Employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    job_title VARCHAR(100),
    department_id INT,
    branch_id INT,
    email VARCHAR(255),
    phone_number VARCHAR(20),
    hire_date DATE
    -- FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    -- FOREIGN KEY (branch_id) REFERENCES Library_Branches(branch_id)
);



-- Add foreign key to Library_Branches manager_id
ALTER TABLE Library_Branches
ADD CONSTRAINT FK_Library_Branches_ManagerID FOREIGN KEY (manager_id) REFERENCES Employees(employee_id);

-- Add foreign key from Employees to Departments (cyclic)
ALTER TABLE Employees 
ADD CONSTRAINT FK_Employees_DepartmentID 
FOREIGN KEY (department_id) REFERENCES Departments(department_id);

-- Add foreign key from Departments to Employees (cyclic)
ALTER TABLE Departments 
ADD CONSTRAINT FK_Departments_ManagerID 
FOREIGN KEY (manager_id) REFERENCES Employees(employee_id);

ALTER TABLE Employees 
ADD CONSTRAINT FK_Employees_BranchID 
FOREIGN KEY (branch_id) REFERENCES Library_Branches(branch_id);