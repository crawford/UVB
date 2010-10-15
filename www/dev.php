<?php
require_once 'uvb.class.php';
require_once 'statsorter.class.php';

$username = $_SERVER['WEBAUTH_USER']; // get from webauth
$uvb = new UVB();


if(isset($_POST['Go']) && isset($_POST['type']) && isset($_POST['user'])){
	$user = $_POST['user'];
	if(!$uvb->isRegistered($user)){
		$secret = $uvb->registerUser($user);
	}
	$num = $_POST['many'];
	switch($_POST['type']){
		case "kills":
			$uvb->incrUserKills($user, $num);
			break;
		case "deaths":
			$uvb->incrUserDeaths($user, $num);
			break;
		case "steps";
			$uvb->incrUserSteps($user, $num);
			break;
		default:
			break;
		}
}
?>

<head>
<title>Ultimate Victory Battle</title>
</head>
<body>
	<p>
		<h3>You can decrement by entering negative values</h3>
		<form action="" method="POST">
		<label>Username: </label><input type="text" name="user"><br>
		<input type="radio" name="type" value="kills">Kills<br>
		<input type="radio" name="type" value="deaths">Deaths<br>
		<input type="radio" name="type" value="steps">Steps<br>
		<label>By how many? </label><input type="text" name="many">
		<br>
		<input type="submit" name="Go" value="Go">
		</form>
		</body>
		</html>
