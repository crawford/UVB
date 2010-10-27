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
			<li>Download and install <a href="http://github.com/jsonpickle/jsonpickle">jsonpicle</a></li>
			<li>Download and unpack the <a href="client.tar">client files</a></li>
			<li>Insert your secret key into your client script</li>
			<li>Program all of your player logic</li>
			<li>Connect to the game server</li>
		</ul>
		<h2>Objective</h2>
		The objective is to avoid colliding with other players, their snowballs, trees, snowmen, and the edge of the map. At the same time, you want to try to hit as many people as you can with your snowballs.
		<h2>Rules</h2>
		<ul>
			<li>Game Step - Every player and object on the game board can move once per game step. The game makes one step once every player has submitted their move. Everyone moves at the same time during the game step.</li>
			<li>You only get one move per game step</li>
			<ul>
				<li>NOP - Do nothing</li>
				<li>MOVE - Move one step in the direction specified</li>
				<li>MAKESNOWBALL - Make a snowball for future throwing</li>
				<li>THROWSNOWBALL - Throw a snowball in the direction specified (you can only throw as many snowballs as you've made)</li>
				<li>SNOWMAN - Build a snowman in the adjacent cell to your own (cell specified by direction)</li>
			</ul>
			<li>(At the moment) you can only play one client at a time</li>
			<li>If you collide with a(n):</li>
			<ul>
				<li>Edge of gameboard - you will be placed in the last legal cell and get one death</li>
				<li>Tree - you will be placed in the last legal cell and get one death</li>
				<li>Snowball - the snowball will be destroyed, you will get one death, and the player who threw the snowball will get one kill</li>
				<li>Snowman - the snowman will be destroyed and you will get one death</li>
				<li>Another player - you both will get one death and one kill</li>
			</ul>
			<li>Objects</li>
			<ul>
				<li>Player - Must respond with a move within the time alloted (currently 3 seconds).  When a player dies, he keeps all of snowballs and stays where he is at (only the death counter is incremented)</li>
				<li>Tree - Static object. Cannot be removed</li>
				<li>Snowball - Thrown by players. Will fly in a straight line until it hits an object or the edge of the map. You can carry as many of these as you want. These take one game step to make.</li>
				<li>Snowman - Built by players. Can be destroyed by a player or a snowball. Cannot be built on top of another object (including other players). These take one game step to make.</li>
			</ul>
			
		</ul>
		</body>
		</html>
