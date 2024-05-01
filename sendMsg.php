<?php
// Check if the request method is POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $name = $_POST['name'];
    $email = $_POST['email'];
    $message = $_POST['message'];

    // Set up the email
    $to = 'contactushn@gmail.com';
    $subject = 'New Contact Form Submission';
    $body = "Name: $name\nEmail: $email\nMessage: $message";
    $headers = 'From: ' . $email;

    // Send the email
    if (mail($to, $subject, $body, $headers)) {
        echo 'Form submitted successfully!';
    } else {
        echo 'Failed to submit the form. Please try again later.';
    }
}
?>