<?php
$page = $_SERVER['PHP_SELF'];
$sec = "60";
?>
<html>
    <head>
    	<meta http-equiv="refresh" content="<?php echo $sec?>;URL='<?php echo $page?>'">
		<link rel="shortcut icon" type="image/png" href="favicon.png"/>
		<link href="default.css" rel="stylesheet" type="text/css">
		<script src="Chart.js"></script>
		<meta 
		     name='viewport' 
		     content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0' 
		/>
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
			$uptime_result->close();
			
			$irrigation_result = mysqli_query($con,"SELECT NIGHT_SECONDS,DAY_EXTRA FROM weather_settings");
			$irrigation_array = mysqli_fetch_array($irrigation_result);
			$irrigation_result->close();
			
			$data_result = mysqli_query($con,"SELECT * FROM weather_data ORDER BY DATETIME DESC");
			$data_array = mysqli_fetch_array($data_result);
			$data_result->close();
			
			$irrigate_now_result = mysqli_query($con,"SELECT IRRIGATE_NOW FROM weather_settings");
			$irrigate_now_array = mysqli_fetch_array($irrigate_now_result);
			$irrigationstart = $irrigate_now_array[0];
			$irrigate_now_result->close();
			// echo $irrigationstart;
			
			$weather_now_result = mysqli_query($con,"SELECT WEATHERNOW FROM weather_settings");
			$weather_now_array = mysqli_fetch_array($weather_now_result);
			$weather_now_result->close();
			
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
				
			// Fetching the data needed to show the weather data in the dashboard
			$data_result1 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 6 HOUR ORDER BY DATETIME LIMIT 1");
			$result1_array = mysqli_fetch_array($data_result1);
			$data_result2 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 12 HOUR ORDER BY DATETIME LIMIT 1");
			$result2_array = mysqli_fetch_array($data_result2);
			$data_result3 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 18 HOUR ORDER BY DATETIME LIMIT 1");
			$result3_array = mysqli_fetch_array($data_result3);
			$data_result4 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 24 HOUR ORDER BY DATETIME LIMIT 1");
			$result4_array = mysqli_fetch_array($data_result4);
			$data_result5 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 30 HOUR ORDER BY DATETIME LIMIT 1");
			$result5_array = mysqli_fetch_array($data_result5);
			$data_result6 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 36 HOUR ORDER BY DATETIME LIMIT 1");
			$result6_array = mysqli_fetch_array($data_result6);
			$data_result7 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 42 HOUR ORDER BY DATETIME LIMIT 1");
			$result7_array = mysqli_fetch_array($data_result7);
			$data_result8 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 48 HOUR ORDER BY DATETIME LIMIT 1");
			$result8_array = mysqli_fetch_array($data_result8);
			$data_result9 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 54 HOUR ORDER BY DATETIME LIMIT 1");
			$result9_array = mysqli_fetch_array($data_result9);
			$data_result10 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 60 HOUR ORDER BY DATETIME LIMIT 1");
			$result10_array = mysqli_fetch_array($data_result10);
			$data_result11 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 66 HOUR ORDER BY DATETIME LIMIT 1");
			$result11_array = mysqli_fetch_array($data_result11);
			$data_result12 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 72 HOUR ORDER BY DATETIME LIMIT 1");
			$result12_array = mysqli_fetch_array($data_result12);
			$data_result13 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 78 HOUR ORDER BY DATETIME LIMIT 1");
			$result13_array = mysqli_fetch_array($data_result13);
			$data_result14 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 84 HOUR ORDER BY DATETIME LIMIT 1");
			$result14_array = mysqli_fetch_array($data_result14);
			$data_result15 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 90 HOUR ORDER BY DATETIME LIMIT 1");
			$result15_array = mysqli_fetch_array($data_result15);
			$data_result16 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 96 HOUR ORDER BY DATETIME LIMIT 1");
			$result16_array = mysqli_fetch_array($data_result16);
			$data_result17 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 102 HOUR ORDER BY DATETIME LIMIT 1");
			$result17_array = mysqli_fetch_array($data_result17);
			$data_result18 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 108 HOUR ORDER BY DATETIME LIMIT 1");
			$result18_array = mysqli_fetch_array($data_result18);
			$data_result19 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 114 HOUR ORDER BY DATETIME LIMIT 1");
			$result19_array = mysqli_fetch_array($data_result19);
			$data_result20 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 120 HOUR ORDER BY DATETIME LIMIT 1");
			$result20_array = mysqli_fetch_array($data_result20);
			$data_result21 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 126 HOUR ORDER BY DATETIME LIMIT 1");
			$result21_array = mysqli_fetch_array($data_result21);
			$data_result22 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 132 HOUR ORDER BY DATETIME LIMIT 1");
			$result22_array = mysqli_fetch_array($data_result22);
			$data_result23 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 138 HOUR ORDER BY DATETIME LIMIT 1");
			$result23_array = mysqli_fetch_array($data_result23);
			$data_result24 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 144 HOUR ORDER BY DATETIME LIMIT 1");
			$result24_array = mysqli_fetch_array($data_result24);
			$data_result25 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 150 HOUR ORDER BY DATETIME LIMIT 1");
			$result25_array = mysqli_fetch_array($data_result25);
			$data_result26 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 156 HOUR ORDER BY DATETIME LIMIT 1");
			$result26_array = mysqli_fetch_array($data_result26);
			$data_result27 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 162 HOUR ORDER BY DATETIME LIMIT 1");
			$result27_array = mysqli_fetch_array($data_result27);
			$data_result28 = mysqli_query($con,"SELECT TEMPERATURE, HUMIDITY, PRESSURE FROM weather_data WHERE DATETIME > NOW() - INTERVAL 168 HOUR ORDER BY DATETIME LIMIT 1");
			$result28_array = mysqli_fetch_array($data_result28);

			// getting the current day and setting weekdays accordingly
			$thisday = date('l');
			if ($thisday == "Monday")
			{
				$weekdaysBig = "       tue       |        wed       |        thu       |        fri       |        sat       |        sun       |       mon       ";
				$weekdaysSmall = "   tu   |    we   |    th   |    fr   |    sa   |    su   |    mo   ";
			} elseif ($thisday == "Tuesday")
			{
				$weekdaysBig = "       wed       |        thu       |        fri       |        sat       |        sun       |        mon       |       tue       ";
				$weekdaysSmall = "   we   |    th   |    fr   |    sa   |    su   |    mo   |   tu   ";
			} elseif ($thisday == "Wednesday")
			{
				$weekdaysBig = "       thu       |        fri       |        sat       |        sun       |        mon       |        tue       |       wed       ";
				$weekdaysSmall = "   th   |    fr   |    sa   |    su   |    mo   |    tu   |   we   ";
			} elseif ($thisday == "Thursday")
			{
				$weekdaysBig = "       fri       |        sat       |        sun       |        mon       |        tue       |        wed       |       thu       ";
				$weekdaysSmall = "   fr   |    sa   |    su   |    mo   |    tu   |    we   |   th   ";
			} elseif ($thisday == "Friday")
			{
				$weekdaysBig = "       sat       |        sun       |        mon       |        tue       |        wed       |        thu       |       fri       ";
				$weekdaysSmall = "   sa   |    su   |    mo   |    tu   |    we   |    th   |   fr   ";
			} elseif ($thisday == "Saturday")
			{
				$weekdaysBig = "       sun       |        mon       |        tue       |        wed       |        thu       |        fri       |       sat       ";
				$weekdaysSmall = "   su   |    mo   |    tu   |    we   |    th   |    fr   |   sa   ";
			} elseif ($thisday == "Sunday")
			{
				$weekdaysBig = "       mon       |        tue       |        wed       |        thu       |        fri       |        sat       |       sun       ";
				$weekdaysSmall = "   mo   |    tu   |    we   |    th   |    fr   |    sa   |   su   ";
			}
			
			// Maintaining whitespaces..
			$weekdaysBig = str_replace(' ', '&nbsp;', $weekdaysBig);
			$weekdaysSmall = str_replace(' ', '&nbsp;', $weekdaysSmall);

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
			
			// This part checks to see if a button has been clicked and runs irrigation functions as a result as well as setting tap icon color
			if (isset($_GET['tap'])) 
				{
					irrigate_now($irrigationstart);
					if ($irrigationstart == 0)
						{
							$tapicon = "<img src='tapoff.png'></img>";
						}	else 
						{
							$tapicon = "<img src='tapon.png'></img>";
						}
				} else {
					if ($irrigationstart == 0)
						{
							$tapicon = "<img src='tapon.png'></img>";
						}	else 
						{
							$tapicon = "<img src='tapoff.png'></img>";
						}
				}
			
			// This part checks to see if a button has been clicked and runs reboot functions as a result			
			if (isset($_GET['rboot']))
				{
					runreboot();
				}
			
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
				if ($seconds < 3600)
					{
						return $dtF->diff($dtT)->format('%im');
					}	elseif ($seconds < 86400)
					{
						return $dtF->diff($dtT)->format('%hh %im');
					} 	else
					{
						return $dtF->diff($dtT)->format('%ad %hh %im');
					}
			}
	    ?>
		<!-- Aligning the dahboards data and buttons in the CSS, these are the div containers for them -->
		<div id="TemperatureGraph" class="tempgraph"><canvas id="Temperature"></canvas></div>
		<div id="HumidityGraph" class="humgraph"><canvas id="Humidity"></canvas></div>
		<div id="PressureGraph" class="pressgraph"><canvas id="Pressure"></canvas></div>
		<div id="UptimeCounter" class="uptime">Uptime: <?php echo secondsToTime($difference); ?></div>
		<div id="TimeClock" class="clock"><?php echo date("Y/m/d - H:i"); ?></div>
		<div id="CurrentTemperature" class="bigtemp"><?php echo "$largetemp<sup>$smalltemp &#8451;</sup>"; ?></div>
		<div id="CurrentWeather" class="tempicon"><img src="<?php echo $weatherimage ?>" align="right"></div>
		<div id="CurrentPressure" class="pressdata"><?php echo "$pressdata hpa"; ?></div>
		<div id="CurrentHumidity" class="humdata"><?php echo "$humdata %"; ?></div>
		<div id="NightIrrigation" class="nightirrigation"><?php echo "~".$nirritime."m"; ?></div>
		<div id="DayIrrigation" class="dayirrigation"><?php echo "~".$dirritime."m"; ?></div>
		<div id="TapButton" class="tapbutton"><button id="btntap" name="btntap"  onClick='location.href="?tap=1"'><?php echo $tapicon ?></button></div>
		<div id="RebootButton" class="rebootbutton"><button id="btnrboot" name="btnrboot" onClick='location.href="?rboot=1"'><img src="power.png"></img></button></div>
		<div id="TemperatureDays" class="weekdaystemp"><?php echo $weekdaysBig; ?></div>
		<div id="PressureDays" class="weekdayspress"><?php echo $weekdaysSmall; ?></div>
		<div id="HumidityDays" class="weekdayshum"><?php echo $weekdaysSmall; ?></div>
		<div id="Logo" class="logoicon"><img src="logo.png"></img></div>
		<div id="PressureIcon" class="pressureicon"><img src="pressureicon.png"></img></div>
		<div id="HumidityIcon" class="humidityicon"><img src="humidityicon.png"></img></div>
		<div id="NightImage" class="nightimage"><img src="night.png"></img></div>
		<div id="DayImage" class="dayimage"><img src="day.png"></img></div>
		<table>
			<tr>
				<!-- This seems to be needed in order to properly show the full site in Chrome/Chromium. Otherwise it cuts the page about halfway down -->
				<td height="1000">&nbsp;</td><td></td>
			</tr>
		</table>
<script>
	// This script sets the Temperature graph for showing the past 7 days area chart
	var ct1 = document.getElementById("Temperature");
	ct1.width = 608;
	ct1.height = 120;
	var myTempChart = new Chart(ct1, {
	    type: 'line',
	    data: {
			labels: ["", "", "", "", "", "", "", "",  "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
	        datasets: [{
	            data: [<?php echo $result28_array[0]; ?>, <?php echo $result27_array[0]; ?>, <?php echo $result26_array[0]; ?>, <?php echo $result25_array[0]; ?>, <?php echo $result24_array[0]; ?>, <?php echo $result23_array[0]; ?>, <?php echo $result22_array[0]; ?>, <?php echo $result21_array[0]; ?>, <?php echo $result20_array[0]; ?>, <?php echo $result19_array[0]; ?>, <?php echo $result18_array[0]; ?>, <?php echo $result17_array[0]; ?>, <?php echo $result16_array[0]; ?>, <?php echo $result15_array[0]; ?>, <?php echo $result14_array[0]; ?>, <?php echo $result13_array[0]; ?>, <?php echo $result12_array[0]; ?>, <?php echo $result11_array[0]; ?>, <?php echo $result10_array[0]; ?>, <?php echo $result9_array[0]; ?>, <?php echo $result8_array[0]; ?>, <?php echo $result7_array[0]; ?>, <?php echo $result6_array[0]; ?>, <?php echo $result5_array[0]; ?>, <?php echo $result4_array[0]; ?>, <?php echo $result3_array[0]; ?>, <?php echo $result2_array[0]; ?>, <?php echo $result1_array[0]; ?>],
	            backgroundColor: [
	                'rgba(88, 82, 57, 1)'
	            ],
	            borderColor: [
	                'rgba(241,224,148,1)'
	            ],
	            borderWidth: 2
	        }]
	    },
	    options: {
	        scales: {
				xAxes: [{
	                ticks: {
						fontColor: '#bebcbc',
                    	fontSize: 12,
                    	maxRotation: 0,
                    	minRotation: 0
	                },
				    gridLines: {
				        display:false,
						tickMarkLength: 2
				    }
				}],
				yAxes: [{
	                ticks: {
						// autoSkip: false,
                    	// maxRotation: 90,
                    	// minRotation: 90,
	                    beginAtZero:false,
						suggestedMin: 15,
						suggestedMax: 35,
						fontColor: '#bebcbc',
                    	fontSize: 12
	                },
				    gridLines: {
				        display:false
				    }
	            }]
	        },
			legend: {
				display: false
			        },
         tooltips: {
            enabled: false
         },
		 elements: { point: { radius: 0 } },
		 animation: {
		         duration: 0
		     }
	    }
	});
</script>
<script>
	// This script sets the Humidity graph for showing the past 7 days area chart
	var ct2 = document.getElementById("Humidity");
	ct2.width = 330;
	ct2.height = 100;
	var myHumChart = new Chart(ct2, {
	    type: 'line',
	    data: {
			labels: ["", "", "", "", "", "", "", "",  "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
	        datasets: [{
	            data: [<?php echo $result28_array[1]; ?>, <?php echo $result27_array[1]; ?>, <?php echo $result26_array[1]; ?>, <?php echo $result25_array[1]; ?>, <?php echo $result24_array[1]; ?>, <?php echo $result23_array[1]; ?>, <?php echo $result22_array[1]; ?>, <?php echo $result21_array[1]; ?>, <?php echo $result20_array[1]; ?>, <?php echo $result19_array[1]; ?>, <?php echo $result18_array[1]; ?>, <?php echo $result17_array[1]; ?>, <?php echo $result16_array[1]; ?>, <?php echo $result15_array[1]; ?>, <?php echo $result14_array[1]; ?>, <?php echo $result13_array[1]; ?>, <?php echo $result12_array[1]; ?>, <?php echo $result11_array[1]; ?>, <?php echo $result10_array[1]; ?>, <?php echo $result9_array[1]; ?>, <?php echo $result8_array[1]; ?>, <?php echo $result7_array[1]; ?>, <?php echo $result6_array[1]; ?>, <?php echo $result5_array[1]; ?>, <?php echo $result4_array[1]; ?>, <?php echo $result3_array[1]; ?>, <?php echo $result2_array[1]; ?>, <?php echo $result1_array[1]; ?>],
	            backgroundColor: [
	                'rgba(88, 82, 57, 1)'
	            ],
	            borderColor: [
	                'rgba(241,224,148,1)'
	            ],
	            borderWidth: 2
	        }]
	    },
	    options: {
	        scales: {
				xAxes: [{
	                ticks: {
						fontColor: '#bebcbc',
                    	fontSize: 12,
                    	maxRotation: 0,
                    	minRotation: 0
	                },
				    gridLines: {
				        display:false,
						tickMarkLength: 2
				    }
				}],
				yAxes: [{
	                ticks: {
	                    beginAtZero:false,
						suggestedMin: 25,
						suggestedMax: 45,
						fontColor: '#bebcbc',
                    	fontSize: 12
	                },
				    gridLines: {
				        display:false
				    }
	            }]
	        },
			legend: {
				display: false
			        },
         tooltips: {
            enabled: false
         },
		 elements: { point: { radius: 0 } },
		 animation: {
		         duration: 0
		     }
	    }
	});
</script>
<script>
	// This script sets the Pressure graph for showing the past 7 days area chart
	var ct3 = document.getElementById("Pressure");
	ct3.width = 342;
	ct3.height = 100;
	var myPressChart = new Chart(ct3, {
	    type: 'line',
	    data: {
			labels: ["", "", "", "", "", "", "", "",  "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
	        datasets: [{
	            data: [<?php echo $result28_array[2]; ?>, <?php echo $result27_array[2]; ?>, <?php echo $result26_array[2]; ?>, <?php echo $result25_array[2]; ?>, <?php echo $result24_array[2]; ?>, <?php echo $result23_array[2]; ?>, <?php echo $result22_array[2]; ?>, <?php echo $result21_array[2]; ?>, <?php echo $result20_array[2]; ?>, <?php echo $result19_array[2]; ?>, <?php echo $result18_array[2]; ?>, <?php echo $result17_array[2]; ?>, <?php echo $result16_array[2]; ?>, <?php echo $result15_array[2]; ?>, <?php echo $result14_array[2]; ?>, <?php echo $result13_array[2]; ?>, <?php echo $result12_array[2]; ?>, <?php echo $result11_array[2]; ?>, <?php echo $result10_array[2]; ?>, <?php echo $result9_array[2]; ?>, <?php echo $result8_array[2]; ?>, <?php echo $result7_array[2]; ?>, <?php echo $result6_array[2]; ?>, <?php echo $result5_array[2]; ?>, <?php echo $result4_array[2]; ?>, <?php echo $result3_array[2]; ?>, <?php echo $result2_array[2]; ?>, <?php echo $result1_array[2]; ?>],
	            backgroundColor: [
	                'rgba(88, 82, 57, 1)'
	            ],
	            borderColor: [
	                'rgba(241,224,148,1)'
	            ],
	            borderWidth: 2
	        }]
	    },
	    options: {
	        scales: {
				xAxes: [{
	                ticks: {
						fontColor: '#bebcbc',
                    	fontSize: 12,
                    	maxRotation: 0,
                    	minRotation: 0
	                },
				    gridLines: {
				        display:false,
						tickMarkLength: 2
				    }
				}],
				yAxes: [{
	                ticks: {
	                    beginAtZero:false,
						suggestedMin: 950,
						suggestedMax: 1050,
						fontColor: '#bebcbc',
                    	fontSize: 12
	                },
				    gridLines: {
				        display:false
				    }
	            }]
	        },
			legend: {
				display: false
			        },
         tooltips: {
            enabled: false
         },
		 elements: { point: { radius: 0 } },
		 animation: {
		         duration: 0
		     }
	    }
	});
</script>
    </body>
</html>
