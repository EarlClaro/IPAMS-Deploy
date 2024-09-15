<?php
// Establish a connection to your MySQL database
$servername = "localhost"; // Change this to your MySQL server address
$username = "root"; // Change this to your MySQL username
$password = "new_password"; // Change this to your MySQL password
$database = "ipamsdjango"; // Change this to your MySQL database name

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve the user's message from the frontend
$userMessage = $_POST['message'];

// Process the user's message (e.g., execute SQL query against your database)
// For demonstration purposes, let's assume a simple SQL query to retrieve data
$sql = "SELECT response FROM chat_responses WHERE user_message = '$userMessage'";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // If the query returns results, fetch and return the response
    $row = $result->fetch_assoc();
    $response = $row["response"];
    echo $response;
} else {
    // If no results found, return a default response or handle accordingly
    echo "I'm sorry, I couldn't understand that.";
}

// Close the database connection
$conn->close();
?>
