-- schema.sql
-- eita MySQL database structure create korar jonno use kora hocche
-- sob data (user, reminder, disease etc) ekhane store hobe

CREATE DATABASE IF NOT EXISTS swastha;
USE swastha;

-- users table: login/signup data store kore
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL
);

-- medicine reminder system er jonno
CREATE TABLE reminders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    medicine_name VARCHAR(100),
    time VARCHAR(50)
);

-- disease information store korar jonno
CREATE TABLE diseases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    symptoms TEXT,
    description TEXT
);

-- diet plan store korar jonno
CREATE TABLE diet_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disease VARCHAR(100),
    recommendation TEXT
);

-- health alert system er jonno
CREATE TABLE alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100),
    disease_name VARCHAR(100),
    severity VARCHAR(50)
);