<?php

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

// fix: $socket reinitialize 
function ai_socket_connect() {
    global $ai_host, $ai_port;

    $socket = fsockopen($ai_host, $ai_port, $errno, $errstr, 10);

    if (!$socket) {
        response(503, "error", "No response from AI server");
        throw new Exception("AI connection failed: $errstr ($errno)");
    }

    stream_set_timeout($socket, 5);
    return $socket;
}

function get_msg($socket, $chunk_size = 1024) {
    $buffer = ""; //leftover data
    $messages = []; // processed

    while (!feof($socket)) {
        // check if valid
        $chunk = fread($socket, $chunk_size);

        if ($chunk === false) {
            break;
        }

        if ($chunk === "") {
            break;
        }

        // add to buffer
        $buffer .= $chunk;

        // read until there is no '\n' anymore
        while (($pos = strpos($buffer, "\n")) !== false) {
            // take data from beginning to '\n'
            $message = substr($buffer, 0, $pos);

            // remove processed data, keep remaining data for next loop
            $buffer = substr($buffer, $pos + 1);

            // decode after
            $data = json_decode($message, true);

            // skip when error occurs when decoding
            if (json_last_error() !== JSON_ERROR_NONE) {
                continue;
            }
            // add processed data to messages
            $messages[] = $data;
        }

        if (!empty($messages)) {
            break; // stop after first full response
        }
    }

    return [
        'messages' => $messages,
        'buffer' => $buffer
    ];
}

// // Establish connection
// $socket = fsockopen($ai_host, $ai_port, $ai_errno, $ai_errstr, 10);
// $data = [
//     "cmd" => "ping"
// ];
// $json_data = json_encode($data);

// // ai server API, authorized users only!!!
// if (!$socket) {
//     echo "Error: $ai_errstr ($ai_errno)";
//     return;
// } 

// check ai connection
//stream_set_timeout($socket, 5);
//fwrite($socket, $json_data);
// $response = json_decode(fread($socket, 1024));

// try {
//     if (!isset($response->response_code) || $response->response_code != 0) {
//         throw new Exception("Error within the AI server has occurred", 0);
//     }
//     //echo "AI Server has connected successfully\n";
// } catch (Exception $e) {
//     echo "UError: " . $e->getMessage();
// }

//echo "Server: $response->response_message\n";
//fclose($socket);