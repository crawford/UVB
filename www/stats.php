<?php
require_once 'uvb.class.php';
require_once 'statsorter.class.php';

$username = $_SERVER['WEBAUTH_USER']; // get from webauth
$uvb = new UVB();
$registered =$uvb->isRegistered($username);
$stats = $uvb->getAllUsers();
$sort = new StatSorter("kills");
$stats = $sort->sort($stats);
//var_dump($stats);
?>

<html>
<head>
<title>Ultimate Victory Battle - Stats</title>
<script type="text/javascript" src="jquery.min.js"></script>
<script type="text/javascript" src="jquery.tablesorter.min.js"></script>
<link rel="stylesheet" type="text/css" href="style.css" />
<script>
$(document).ready(function() 
    { 
	            $("#stats").tablesorter({
			    
			sortList: [[1,1]]	    
		    }); 
		        } 
			);

function updateStats(){
	$.get('stats_ajax.php', function(data) {
		$('#stats-body').html(data);

		$("#stats").trigger("update");
		var current_sort = $("#stats").get(0).config.sortList;
		$("#stats").trigger("sorton", [current_sort]);
	});

	return false;
}

setInterval("updateStats()", 5000);
</script>
</head>
<body>
<?php
include_once('nav.php');
?>

<h1>Stats</h1>
<table id="stats" class="tablesorter">
<thead>
<tr>
<th>Users</th>
<th>Kills</th>
<th>Deaths</th>
<th>Steps</th>
</tr>
</thead>
<tbody id="stats-body">
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
</tbody>
</table>
</body>
</html>
