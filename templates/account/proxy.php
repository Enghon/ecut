<?php
$url = 'http://hbkgds.com/api/tj.php?name=yhAPI&a=2';
$response = file_get_contents($url);
echo $response;
?>