<?php

// Database connection 
$host = "localhost";
$dbname = "user_api";
$username = "root";
$password = "pass";

$conn = new mysqli($host, $username, $password, $dbname);

if ($conn->connect_error) {
    die(json_encode([
        "status" => "error",
        "message" => "Database connection failed"
    ]));
}



// Set headers for security and JSON handling
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
