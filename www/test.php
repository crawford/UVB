<?php
require_once 'SharedConfigurations.php';

// simple set and get scenario

$redis = Predis\Client::create($configurations);
$redis->setProfile('dev');

$redis->set('library', 'predis');
$retval = $redis->get('library');

print_r($retval);

$a = $redis->hgetall("user:madmike");
var_dump($a);


/* OUTPUT
predis
*/
?>
