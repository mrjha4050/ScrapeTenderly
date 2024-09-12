<?php
$servername = "localhost";
$username = "root";
$password = "password";
$dbname = "tenders";

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Handle search request
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $search = $_POST["search"];
    
    // Query the database
    $sql = "SELECT * FROM tenders WHERE description LIKE '%$search%'";
    $result = $conn->query($sql);

    // Prepare data for JSON response
    $data = [];
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
    } else {
        $data["message"] = "No results found";
    }

    // Output JSON
    header('Content-Type: application/json');
    echo json_encode($data);

    // Close connection
    $conn->close();
}
?>
