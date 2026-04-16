<?php
require_once "connection.php";

$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? '';
$data = json_decode(file_get_contents("php://input"), true);

function response($statusCode, $status, $message, $data = null) {
    http_response_code($statusCode);
    echo json_encode([
        "status" => $status,
        "message" => $message,
        "data" => $data
    ]);
    global $socket;
    if (isset($socket) && is_resource($socket)) {
        fclose($socket);
    } 
    exit;
}

// CREATE APIS
if ($method === "POST" && $action === "generate_api") {
    $row = false;
    $key = '';  
    do {
        $key = bin2hex(random_bytes(16));
        $check = $db_conn->prepare("SELECT api_key FROM api_keys WHERE api_key = :api_key");
        $check->bindValue(":api_key", $key);
        $result = $check->execute();
        $row = $result->fetchArray(SQLITE3_ASSOC);
    } while($row);

    $stmt = $db_conn->prepare("INSERT INTO api_keys (api_key) VALUES (:api_key)");
    $stmt->bindValue(":api_key", $key, SQLITE3_TEXT);
    $result = $stmt->execute();
    if ($result) {
        response(201, "success", "API key generated successfully", [
            "api_key" => $key,
        ]);
    }
    response(500, "error", "API generation failed");
}

// EXECUTE AI 
if ($method === "POST" && $action === "execute_ai") {
    $key = $data["api_key"] ?? null;
    $month = $data["month"] ?? null;
    $raw = $data["raw"] ?? null; // boolean

    if (!$key || !$month || $raw === null) {
        response(400, "error", "api_key, month, raw parameters are required");
    }

    $check = $db_conn->prepare("SELECT api_key FROM api_keys WHERE api_key = :api_key");
    $check->bindValue(":api_key", $key, SQLITE3_TEXT);
    $result = $check->execute();
    $row = $result->fetchArray(SQLITE3_ASSOC);
    if (!$row) {
        response(404, "error", "api_key not found");
    }

    $data = [
        "cmd" => "run",
        "month" => $month,
        "raw" => $raw
    ];

    $json_data = json_encode($data);
    fwrite($socket, $json_data);
    $response = json_decode(fread($socket, 1024));  
    response(200, "success", "AI Execution is successful!", $response->data);
}

// GET ALL API KEYS
if ($method === "GET" && $action === "api_keys") {
    $result = $db_conn->query("SELECT id, api_key, created_at FROM api_keys");
    $keys = [];

    if (!$result) {
        response(500, "error", "Query failed", $db_conn->lastErrorMsg());
        exit;
    }

    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $keys[] = $row;
    }

    response(200, "success", "API keys retrieved successfully", $keys);
}

// DELETE API KEY
if ($method === "DELETE" && $action === "delete_api_key") {
    $key = $_GET['api_key'] ?? '';

    if (!$key) {
        response(400, "error", "API key is required");
        exit;
    }

    $stmt = $db_conn->prepare("DELETE FROM api_keys WHERE api_key = :api_key");
    $stmt->bindValue(":api_key", $key, SQLITE3_TEXT);
    $result = $stmt->execute();

    if ($result) {
        if ($db_conn->changes() > 0) {
            response(200, "success", "API key deleted successfully");
        }
        response(404, "error", "API key not found");
    }

    response(500, "error", "Delete failed");
}

response(404, "error", "Endpoint not found");
fclose($socket);