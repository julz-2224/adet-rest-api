<?php
use TheSeer\Tokenizer\Exception;

// Set headers for security and JSON handling
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");

// AI server address, Change accordingly...
$ai_host = "127.0.0.1";
$ai_port = 1234;

// DB sqlite
$db_conn = new SQLite3("api_keys.db");
$db_conn->exec("
    CREATE TABLE IF NOT EXISTS `api_keys`(
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `api_key` TEXT UNIQUE,
        `created_at` TEXT
    );
");

// Establish connection
$socket = fsockopen($ai_host, $ai_port, $ai_errno, $ai_errstr, 10);
$data = [
    "cmd" => "ping"
];
$json_data = json_encode($data);

// ai server API, authorized users only!!!
if (!$socket) {
    echo "Error: $ai_errstr ($ai_errno)";
    return;
} 

// check ai connection
stream_set_timeout($socket, 5);
fwrite($socket, $json_data);
$response = json_decode(fread($socket, 1024));

try {
    if (!isset($response->response_code) || $response->response_code != 0) {
        throw new Exception("Error within the AI server has occurred", 0);
    }
    //echo "AI Server has connected successfully\n";
} catch (Exception $e) {
    echo "UError: " . $e->getMessage();
}

//echo "Server: $response->response_message\n";
//fclose($socket);





