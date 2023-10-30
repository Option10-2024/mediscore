<?php
// Initialize cURL session
$ch = curl_init();

// Set cURL options
curl_setopt($ch, CURLOPT_URL, 'https://janusinfo.se/beslutsstod/lakemedelochmiljo.4.72866553160e98a7ddf1d01.html');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

// Execute cURL session and store the result in $html
$html = curl_exec($ch);

// Check for cURL errors
if (curl_errno($ch)) {
    echo 'cURL error: ' . curl_error($ch);
    exit;
}

// Close cURL session
curl_close($ch);

// Check if we received a valid response
if ($html === false) {
    echo 'Failed to retrieve the webpage content.';
    exit;
}

// Now, you can parse and process the HTML content as needed using PHP's DOMDocument or a library like SimpleHTMLDomParser.
// For example, if you want to extract the title of the page:
$dom = new DOMDocument;
$dom->loadHTML($html);
$title = $dom->getElementsByTagName('title')->item(0)->textContent;
echo 'Title: ' . $title;

// You can continue to extract more data from the HTML based on your requirements.

?>
