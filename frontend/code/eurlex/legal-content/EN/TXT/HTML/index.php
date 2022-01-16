<?php

// curl "http://pri_solr:8983/solr/docs/select?fl=text&q=celex:31987R3193"

$celex = $_GET['celex'];

$ret = file_get_contents("http://pri_solr:8983/solr/docs/select?fl=text&q=celex:$celex");
if($ret === false){
    http_response_code(500);
    exit();
}

$data = json_decode($ret, true);
$text = $data["response"]["docs"][0]["text"];

echo $text;
