<?php
// Database connection variables
$host = 'localhost';
$dbUsername = 'root';
$dbPassword = 'Admin1234!';
$dbName = 'real_estate_app';

// Create connection
$conn = new mysqli($host, $dbUsername, $dbPassword, $dbName);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get user input
$username = $_POST['username'];
$password = $_POST['password']; // Note: In a real application, this should be hashed!

// SQL query to find the user
$sql = "SELECT * FROM users WHERE username='$username' AND password='$password'"; // Danger: SQL Injection vulnerability

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Success, login valid
    echo "Login successful!";
    // Handle session/redirect here
} else {
    // Invalid login
    echo "Invalid username or password.";
}

$conn->close();
