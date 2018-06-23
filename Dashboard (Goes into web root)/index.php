<?php
$page = $_SERVER['PHP_SELF'];
$sec = "10";
?>
<html>
    <head>
    	<meta http-equiv="refresh" content="<?php echo $sec?>;URL='<?php echo $page?>'">
		<link rel="shortcut icon" type="image/png" href="favicon.png"/>
		<style>
			@font-face {
			    font-family: "GardenBrain";
			    src: url(http://localhost/font.ttf) format("truetype");
			}
			@media screen and (min-width: 1000px) and (max-width: 1100px) and (orientation: landscape) {
			  html {
			    transform: rotate(-90deg);
			    transform-origin: left top;
			    width: 100vh;
			    overflow-x: hidden;
			    position: absolute;
			    top: 100%;
			    left: 0;
  			  	background-color: #2e2f31;
  			  	color: #ffffff;
			  	}
				.tdheight1 {
			      height: 150;
				}
				.tdheight2 {
			      height: 120;
				}
				.tdheight3 {
			      height: 50;
				}
				.tdheight4 {
			      height: 67;
				  width: 50%;
				}
				.tdheight5 {
			      height: 15;
				}
			}
			@media screen and (min-width: 1100px) and (max-width: 5000px) and (orientation: landscape) {
			  html {
			    width: 100vh;
			    position: fixed;
			    top: -70px;
			    left: 50%;
  			  	background-color: #2e2f31;
  			  	color: #ffffff;
				margin-left: -300px;
			    -moz-transform: scale(0.85);
			    -webkit-transform: scale(0.85);
			    transform: scale(0.85);
			  	}
				.tdheight1 {
			      height: 170;
				}
				.tdheight2 {
			      height: 125;
				}
				.tdheight3 {
			      height: 55;
				}
				.tdheight4 {
			      height: 67;
				  width: 50%;
				}
				.tdheight5 {
			      height: 15;
				}
			}
			@media screen and (min-width: 300px) and (max-width: 1000px) and (orientation: portrait) {
			  html {
			    width: 100vh;
			    position: fixed;
			    top: 450;
			    left: 50%;
  			  	background-color: #2e2f31;
  			  	color: #ffffff;
				margin-left: 0;
			    -moz-transform: scale(1.5);
			    -webkit-transform: scale(1.5);
			    transform: scale(1.5);
			  	}
				.tdheight1 {
			      height: 170;
				}
				.tdheight2 {
			      height: 125;
				}
				.tdheight3 {
			      height: 55;
				}
				.tdheight4 {
			      height: 67;
				  width: 50%;
				}
				.tdheight5 {
			      height: 15;
				}
			}
			.main {
			  font-family: GardenBrain, Helvetica Neue, Helvetica, Arial, sans-serif;
			  font-size:1.2em;
			  color:#ffffff;
			}
			body {
			  background-image: url("background.jpg");
    		  background-repeat: no-repeat;
  			  background-color: #2e2f31;
			  color: #ffffff;
			}
			table {
			  font-family: GardenBrain, Helvetica Neue, Helvetica, Arial, sans-serif;
			  font-size:0.7em;
			  color: #ffffff;
			}
			sup {
			  font-size:0.5em;
			}
			.bigtemp {
			  font-family: GardenBrain, Helvetica Neue, Helvetica, Arial, sans-serif;
			  font-size:7.5em;
			  color: #76c83f;
			}
			.wdata {
			  font-family: GardenBrain, Helvetica Neue, Helvetica, Arial, sans-serif;
			  font-size:3.4em;
			  color: #bebcbc;
			}
			.idata {
			  font-family: GardenBrain, Helvetica Neue, Helvetica, Arial, sans-serif;
			  font-size:2.6em;
			  color: #bebcbc;
			}
			div.absolute {
			  font-family: GardenBrain, Helvetica Neue, Helvetica, Arial, sans-serif;
			  font-size:7.5em;
			  color: #76c83f;
			  position: absolute;
			  top: 80px;
			  right: 350;
			  width: 200px;
			  height: 80px;
			}
			button {
			    background-color: Transparent;
			    background-repeat:no-repeat;
			    border: none;
			    cursor:pointer;
			    overflow: hidden;
			    outline:none;
			}
			}
		</style>
    </head>
    <body>
	    <?php
			// Enabling displaying of errors
			// ini_set('error_reporting', E_ALL);
			// ini_set('display_errors', 1);
			// ini_set('display_startup_errors', 1);
			
			// Connecting to MySQL
			$con=mysqli_connect("localhost","user","pass","weather");
			// Checking the connection
			if (mysqli_connect_errno())
			{
			echo "Failed to connect to MySQL: " . mysqli_connect_error();
			}

			// Fetching the data needed to show the dashboard
			$uptime_result = mysqli_query($con,"SELECT UPTIME FROM weather_settings");
			$uptime_array = mysqli_fetch_array($uptime_result);
			
			$irrigation_result = mysqli_query($con,"SELECT NIGHT_SECONDS,DAY_EXTRA FROM weather_settings");
			$irrigation_array = mysqli_fetch_array($irrigation_result);
			
			$data_result = mysqli_query($con,"SELECT * FROM weather_data ORDER BY DATETIME DESC");
			$data_array = mysqli_fetch_array($data_result);
			
			$irrigate_now_result = mysqli_query($con,"SELECT IRRIGATE_NOW FROM weather_settings");
			$irrigate_now_array = mysqli_fetch_array($irrigate_now_result);
			$irrigationstart = $irrigate_now_array[0];
			// echo $irrigationstart;
	      
	      		if ($irrigationstart == 0)
				{
					$tapicon = "<img src='tapon.png'></img>";
				}	else 
				{
					$tapicon = "<img src='tapoff.png'></img>";
				}
			
			$weather_now_result = mysqli_query($con,"SELECT WEATHERNOW FROM weather_settings");
			$weather_now_array = mysqli_fetch_array($weather_now_result);
			
			//Setting the correct uptime format
			$time1 = strtotime($uptime_array[0]);
			$time2 = strtotime(date("Y-m-d H:i:m"));
			$difference = round(abs($time2 - $time1),2);
			
			//Getting passed time in seconds since the last night irrigation, approximately..
			$npassedtime = time() - strtotime(date("Y-m-d 01:00:00"));
			
			// Setting the right weather icon depending on current weather
			if ($weather_now_array[0] == 0)
				{
					$weatherimage = "0.png";
				}	elseif ($weather_now_array[0] == 1) {
					$weatherimage = "1.png";
				}	elseif ($weather_now_array[0] == 2) {
					$weatherimage = "2.png";
				}	elseif ($weather_now_array[0] == 3) {
					$weatherimage = "3.png";
				}

			// Closing the MySQL connection
			mysqli_close($con);
			
			// These get the temperature, humidity and pressure data in correct formats to show on the site
			$largetemp = substr($data_array[1],0,-2);
			$smalltemp = substr($data_array[1],-2,2);
			$pressdata = round($data_array[3]);
			$humdata = round($data_array[2]);
			
			// These make sure we show irrigation time in minutes and not in seconds as we have in the database
			if ($irrigation_array[0] > 0)
				{
					if ($npassedtime > 0)
						{
							// If we have upcoming night time irrigation and we are still on the same date as when irrigation last ran
							$nirritime = $irrigation_array[0];
							$nirritime = ($nirritime/$npassedtime) * 60 * 23;
							$nirritime = round($nirritime,2);
						} else {
							// If we have upcoming night time irrigation and we  are on the next date from when irrigation last ran
							$nirritime = $irrigation_array[0];
							$npassedtime = time() - strtotime(date("Y-m-d 00:00:00"));
							$nirritime = ($nirritime/($npassedtime + (3600 * 23))) * 60 * 23;
							$nirritime = round($nirritime,2);
							
						}
				}	else {
					$nirritime = "0";
				}
			if ($irrigation_array[1] > 0)
				{
					$dirritime = substr($irrigation_array[1]/60,0,3);
				}	else {
					$dirritime = "0";
				}
			
			// This part checks to see if a button has been clicked and runs PHP functions as a result
			if(isset($_GET['tap'])){irrigate_now($irrigationstart);}
			if(isset($_GET['rboot'])){runreboot();}
			
			// This function toggles the IRRIGATE_NOW value in database
			function irrigate_now($irrigationstart)
			{
				// Connecting to MySQL
				$con=mysqli_connect("localhost","user","pass","weather");
				// Checking the connection
				mysqli_connect_errno();
					
				// Setting the appropriate SQL query depending on what the current DB setting is
				if ($irrigationstart == 0)
					{
						$sql = "UPDATE weather_settings SET IRRIGATE_NOW='1'";
						mysqli_query($con, $sql);
					}	else 
					{
						$sql = "UPDATE weather_settings SET IRRIGATE_NOW='2'";
						mysqli_query($con, $sql);
					}
					
				// Closing the MySQL connection
				mysqli_close($con);
			}
			
			// This function reboots the Raspberry Pi - It runs the python script, but the Pi isn't rebooting?
			function runreboot()
			{
				// Connecting to MySQL
				$con=mysqli_connect("localhost","user","pass","weather");
				// Checking the connection
				mysqli_connect_errno();
					
				// Setting REBOOTNOW value in database to 1
				$sql = "UPDATE weather_settings SET REBOOTNOW='1'";
				mysqli_query($con, $sql);
					
				// Closing the MySQL connection
				mysqli_close($con);
			}
			
			// This function converts uptime date and current date to current uptime
			function secondsToTime($seconds) {
			    $dtF = new \DateTime('@0');
			    $dtT = new \DateTime("@$seconds");
			    return $dtF->diff($dtT)->format('%ad %hh %im');
			}
	    ?>
		<table width="600">
			<tr>
				<td align="left" width="180">Uptime: <?php echo secondsToTime($difference); ?></td>
				<td align="center"><?php echo date("Y/m/d - H:i"); ?> </td>
				<td align="right" width="180">&nbsp;</td>
			</tr>
		</table>
		<table>
			<tr height="170">
				<td width="80">&nbsp;</td>
				<td width="250" class="bigtemp"><?php echo "$largetemp<sup>$smalltemp &#8451;</sup>"; ?></td>
				<td><img src="<?php echo $weatherimage ?>" align="right"></td>
			</tr>
		</table>
		<table>
			<tr>
				<td class="tdheight2">&nbsp;</td><td></td>
			</tr>
		</table>
		<table>
			<tr>
				<td width="70">&nbsp;</td><td class="wdata"><?php echo "$pressdata hpa"; ?></td>
			</tr>
		</table>
		<table>
			<tr>
				<td class="tdheight3">&nbsp;</td><td></td>
			</tr>
			<tr>
				<td width="70">&nbsp;</td><td class="wdata"><?php echo "$humdata %"; ?></td>
			</tr>
		</table>
		<table>
			<tr>
				<td class="tdheight1">&nbsp;</td><td></td>
			</tr>
			<tr>
				<td width="105">&nbsp;</td><td class="idata" width="265"><?php echo "~".$nirritime."m"; ?></td><td class="idata"><?php echo "~".$dirritime."m"; ?></td><td width="20">&nbsp;</td>
			</tr>
		</table>
		<table>
			<tr>
				<td height="25">&nbsp;</td><td></td>
			</tr>
			<tr>
				<td width="200">&nbsp;</td><td class="idata" width="195" height="200"><button id="btntap" name="btntap"  onClick='location.href="?tap=1"'><?php echo $tapicon ?></button></td><td width="190">&nbsp;</td>
			</tr>
		</table>
		<table>
			<tr>
				<td height="65" width="507">&nbsp;</td><td width="75"><button id="btnrboot" name="btnrboot" onClick='location.href="?rboot=1"'><img src="power.png"></img></button></td>
			</tr>
		</table>
    </body>
</html>
