<?php

// Database connection 
$host = "localhost";
$dbname = "user_api";
$username = "root";
$password = "pass";

$conn = new mysqli($host, $username, $password);

if ($conn->connect_error) {
    die(json_encode([
        "status" => "error",
        "message" => "Database connection failed"
    ]));
}

$conn->set_charset("utf8mb4");

// Ensure schema exists, then select it.
if (!$conn->query("CREATE DATABASE IF NOT EXISTS `$dbname` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")) {
    die(json_encode([
        "status" => "error",
        "message" => "Failed to create or verify database schema"
    ]));
}

if (!$conn->select_db($dbname)) {
    die(json_encode([
        "status" => "error",
        "message" => "Failed to select database schema"
    ]));
}

// Ensure users table exists.
$createUsersTableSql = "
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        email VARCHAR(150) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
";

if (!$conn->query($createUsersTableSql)) {
    die(json_encode([
        "status" => "error",
        "message" => "Failed to create or verify users table"
    ]));
}


// Set headers for security and JSON handling
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
