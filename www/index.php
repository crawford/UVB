<?php
require_once 'uvb.class.php';


$username = $_SERVER['WEBAUTH_USER']; // get from webauth
$uvb = new UVB();
$registered =$uvb->isRegistered($username);
$userInfo = NULL;

if(isset($_POST['register']) && !$registered){
	$secret_key = $uvb->registerUser($username);
	$userInfo = $uvb->getUserInfo($username); // not the best w/e
	$registered = true;
} else if ($registered){
	$userInfo = $uvb->getUserInfo($username); 
}
?>

<html>
<head>
<title>Ultimate Victory Battle</title>
</head>
<body>
<?php
include_once('nav.php');
?>

<?php if(!$registered){?>
	<p>
		<h3>What's up <?php echo $username; ?>, want to register?</h3>
		<form action="" method="POST">
		<input type="submit" name="register" value="Register!">
		</form>
		<?php } ?>
		<?php if($userInfo != NULL){ ?>
		<h1> Welcome <?php echo $username; ?></h1>
		<h2>User Info</h2>
		<p>
		<strong>SecretKey: </strong><?php echo $userInfo[1]; ?>
		</p>
		<?php } ?>
		<h2>Instructions on how to play</h2>
		<ul>
			<li>Do this</li>
			<li>than that</li>
		</ul>
		</body>
		</html>
