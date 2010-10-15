<?php
require_once 'uvb.class.php';
require_once 'statsorter.class.php';

$username = $_SERVER['WEBAUTH_USER']; // get from webauth
$uvb = new UVB();
$stats = $uvb->getAllUsers();
$sort = new StatSorter("kills");
$stats = $sort->sort($stats);
?>
<?php $i=1;foreach($stats as $stat){
	if($stat['username'] == $username){
		$class="user";
	} else if ($i % 2 == 0){
		$class="odd";
	} else {
		$class="";
	}
	?>
<tr class="<?php echo $class;?>">
<td> <?php echo $stat['username'];?> </td><td> <?php echo $stat['kills'];?>
</td><td> <?php echo $stat['deaths'];?></td><td><?php echo $stat['steps']?>
</tr>
<?php $i++;}?>
