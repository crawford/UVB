<?php

require_once 'SharedConfigurations.php';
class UVB {
	private $redis;
	private $username;
	function __construct(){
		global $configurations;
		$this->redis = Predis\Client::create($configurations);
		$this->redis->setProfile('dev');
	}
	function registerUser($username){
		$secret = $this->randomString();
		$this->redis->set("secret:".$secret, $username);
		$this->redis->hset("user:".$username,"secret",$secret);
		$this->redis->hset("user:".$username,"kills",0);
		$this->redis->hset("user:".$username,"deaths",0);
		$this->redis->hset("user:".$username,"steps", 0);

		return $secret;
	}

	function isRegistered($username){
		$ret = $this->redis->hexists("user:".$username,"secret");
		if($ret == 0){
			return false;
		}
		return true;
	}

	function getUserInfo($username){
		$ret = $this->redis->hgetall("user:".$username);
		if($ret == "nil"){
			// not registered wtf?
		}
		return $ret;
	}
	function incrUserKills($user, $num=1){
		$user = "user:" . $user;
		$this->redis->hincrby($user, 'kills', $num);
	}
	function incrUserSteps($user, $num=1){
		$user = "user:" . $user;
		$this->redis->hincrby($user, 'steps', $num);
	}
	function incrUserDeaths($user, $num=1){
		$user = "user:" . $user;
		$this->redis->hincrby($user, 'deaths', $num);
	}	
	function getAllUsers(){
		$users = $this->redis->keys("user:*");	
		$stats = array();
		foreach($users as $user){
			$userInfo = $this->redis->hgetall($user);
			if(count($userInfo) != 8){
				continue;
			}
			$username = explode(":", $user);
			$username = $username[1];
			$stats[] = array('username'=> $username, 
					'kills'=>$userInfo[3],
					'deaths'=>$userInfo[5],
					'steps'=>$userInfo[7]
					);
		}
		return $stats;
	}

	private function randomString($length = 32){
		$string = "";
		$possible = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
		for($i=0;$i<$length;$i++){
			$char = $possible[mt_rand(0, strlen($possible)-1)];
			$string .= $char;
		}
		return $string;
	}
}
?>
