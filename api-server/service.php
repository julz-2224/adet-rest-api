<?php
require_once "connection.php";

$method = $_SERVER['REQUEST_METHOD'];
$request = $_SERVER['REQUEST_URI'];


$path = str_replace($base_path, "", parse_url($request, PHP_URL_PATH));
$pathParts = explode("/", trim($path, "/"));

// Read JSON input
$data = json_decode(file_get_contents("php://input"), true);


// Helper function
function response($statusCode, $status, $message, $data = null) {
    http_response_code($statusCode);
    echo json_encode([
        "status" => $status,
        "message" => $message,
        "data" => $data
    ]);
    exit;
}


// ROUTES

// POST /register
if ($method === "POST" && $path === "/register") {
    $username = $data['username'] ?? '';
    $email = $data['email'] ?? '';
    $password = $data['password'] ?? '';

    if (empty($username) || empty($email) || empty($password)) {
        response(400, "error", "Username, email, and password are required");
    }

    $check = $conn->prepare("SELECT id FROM users WHERE email = ?");
    $check->bind_param("s", $email);
    $check->execute();
    $result = $check->get_result();

    if ($result->num_rows > 0) {
        response(409, "error", "Email already exists");
    }

    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

    $stmt = $conn->prepare("INSERT INTO users (username, email, password) VALUES (?, ?, ?)");
    $stmt->bind_param("sss", $username, $email, $hashedPassword);

    if ($stmt->execute()) {
        response(201, "success", "User registered successfully", [
            "id" => $stmt->insert_id,
            "username" => $username,
            "email" => $email
        ]);
    } else {
        response(500, "error", "Registration failed");
    }
}


// POST /login
if ($method === "POST" && $path === "/login") {
    $email = $data['email'] ?? '';
    $password = $data['password'] ?? '';

    if (empty($email) || empty($password)) {
        response(400, "error", "Email and password are required");
    }

    $stmt = $conn->prepare("SELECT id, username, email, password FROM users WHERE email = ?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows === 0) {
        response(404, "error", "User not found");
    }

    $user = $result->fetch_assoc();

    if (!password_verify($password, $user['password'])) {
        response(401, "error", "Invalid password");
    }

    unset($user['password']);

    response(200, "success", "Login successful", $user);
}



// GET /users
if ($method === "GET" && $path === "/users") {
    $result = $conn->query("SELECT id, username, email, created_at FROM users");
    $users = [];

    while ($row = $result->fetch_assoc()) {
        $users[] = $row;
    }

    response(200, "success", "Users retrieved successfully", $users);
}



// GET /users/{id}
if ($method === "GET" && $pathParts[0] === "users" && isset($pathParts[1])) {
    $id = intval($pathParts[1]);

    $stmt = $conn->prepare("SELECT id, username, email, created_at FROM users WHERE id = ?");
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows === 0) {
        response(404, "error", "User not found");
    }

    response(200, "success", "User retrieved successfully", $result->fetch_assoc());
}



// PUT /users/{id}
if ($method === "PUT" && $pathParts[0] === "users" && isset($pathParts[1])) {
    $id = intval($pathParts[1]);
    $username = $data['username'] ?? '';
    $email = $data['email'] ?? '';

    if (empty($username) || empty($email)) {
        response(400, "error", "Username and email are required");
    }

    $stmt = $conn->prepare("UPDATE users SET username = ?, email = ? WHERE id = ?");
    $stmt->bind_param("ssi", $username, $email, $id);

    if ($stmt->execute()) {
        if ($stmt->affected_rows > 0) {
            response(200, "success", "User updated successfully");
        } else {
            response(404, "error", "User not found or no changes made");
        }
    } else {
        response(500, "error", "Update failed");
    }
}



// DELETE /users/{id}
if ($method === "DELETE" && $pathParts[0] === "users" && isset($pathParts[1])) {
    $id = intval($pathParts[1]);

    $stmt = $conn->prepare("DELETE FROM users WHERE id = ?");
    $stmt->bind_param("i", $id);

    if ($stmt->execute()) {
        if ($stmt->affected_rows > 0) {
            response(200, "success", "User deleted successfully");
        } else {
            response(404, "error", "User not found");
        }
    } else {
        response(500, "error", "Delete failed");
    }
}


// Default
response(404, "error", "Endpoint not found");
