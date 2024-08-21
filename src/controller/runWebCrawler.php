<?php

// Get parameters from POST request
$filterType = isset($_POST['filterType']) ? escapeshellarg($_POST['filterType']) : '';
$filterLength = isset($_POST['filterLength']) ? (int)$_POST['filterLength'] : '';
$orderBy = isset($_POST['orderBy']) ? escapeshellarg($_POST['orderBy']) : '';
$orderByDirection = isset($_POST['orderByDirection']) ? escapeshellarg($_POST['orderByDirection']) : '';

// Path to the Python script
$pythonScriptPath = '../scripts/webCrawler.py';

// Construct the command to run the Python script
$command = escapeshellcmd("python3 $pythonScriptPath $filterType $filterLength $orderBy $orderByDirection");

// Execute the Python script and capture the output
$output = shell_exec("$command 2>&1");

if ($output === null) {
    echo "There was an error running the Python script.";
} else {
    echo $output;
}

?>
