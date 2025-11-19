-- Create ENUM types
CREATE TYPE cuisine_type_enum AS ENUM ('Italian', 'Mexican', 'American', 'Chinese', 'Indian', 'Other');
CREATE TYPE payment_method_enum AS ENUM ('Credit Card', 'Cash', 'Online Payment', 'Gift Card');
CREATE TYPE order_status_enum AS ENUM ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Refunded');
CREATE TYPE menu_category_enum AS ENUM ('Appetizer', 'Main Course', 'Dessert', 'Beverage', 'Special');
CREATE TYPE vehicle_type_enum AS ENUM ('Car', 'Motorcycle', 'Bicycle');
CREATE TYPE availability_status_enum AS ENUM ('Available', 'Busy', 'Unavailable');

-- Restaurants table
CREATE TABLE Restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(10),
    phone_number VARCHAR(20),
    cuisine_type cuisine_type_enum NOT NULL,
    opening_hours VARCHAR(255),
    rating NUMERIC(3,2)
);

-- Customers table
CREATE TABLE Customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES Customers(customer_id),
    restaurant_id INT NOT NULL REFERENCES Restaurants(restaurant_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(10,2) NOT NULL,
    payment_method payment_method_enum NOT NULL,
    order_status order_status_enum DEFAULT 'Pending',
    delivery_address VARCHAR(255)
);

-- Menu table
CREATE TABLE Menu (
    menu_id SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL REFERENCES Restaurants(restaurant_id),
    item_name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    category menu_category_enum NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

-- Order_Items table
CREATE TABLE Order_Items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES Orders(order_id),
    menu_id INT NOT NULL REFERENCES Menu(menu_id),
    quantity INT NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL,
    special_instructions TEXT
);

-- Reviews table
CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL REFERENCES Restaurants(restaurant_id),
    customer_id INT NOT NULL REFERENCES Customers(customer_id),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Delivery_Drivers table
CREATE TABLE Delivery_Drivers (
    driver_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    vehicle_type vehicle_type_enum NOT NULL,
    license_number VARCHAR(20) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    availability_status availability_status_enum DEFAULT 'Available',
    join_date DATE,
    termination_date DATE
);
