<?php
session_start();
include 'config.php';

$conn = mysql_connect($host, $user, $pass);
mysql_select_db($database);

$result = mysql_query("SELECT * FROM users");
while($row = mysql_fetch_array($result)) {
    echo $row['name'];
}

function processForm() {
    $name = $_POST['name'];
    $email = $_POST['email'];
    // Process form
}
?>