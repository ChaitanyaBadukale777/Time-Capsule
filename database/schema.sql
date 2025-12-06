-- database/schema.sql

CREATE DATABASE IF NOT EXISTS digital_time_capsule;

USE digital_time_capsule;

CREATE TABLE IF NOT EXISTS capsules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    unlock_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'LOCKED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
