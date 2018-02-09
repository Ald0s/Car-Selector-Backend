<?php
	/*
	Summary:
	The form the user will interact with to select a car.
	*/
	
	require_once("func/database.php");
	
	if(!class_exists("CCars")) {
		class CCars extends CDBConnection {
			function __construct() {
				parent::__construct("Cars");
			}
			
			private $_getAllMakes = "SELECT VehicleID AS ID, VehicleMake AS Name FROM vehicle_make";
			public function GetAllMakes() {
				$result = $this->RunGetQuery($this->_getAllMakes);
				
				if($result === NULL || $result->rowCount() <= 0)
					return NULL;
				return $result;
			}
			
			private $_getModels = "SELECT VehicleModelID AS ID, VehicleModel AS Name FROM vehicle_model WHERE VehicleID=:makeid";
			public function GetModels($makeid) {
				$result = $this->RunQuery($this->_getModels,
					[
						"makeid"			=> $makeid
					]);
				
				if($result === NULL || $result->rowCount() <= 0)
					return NULL;
				return $result;
			}
			
			private $_getBadges = "SELECT VehicleBadgeID AS ID, VehicleBadge AS Name FROM vehicle_badge WHERE VehicleModelID=:modelid";
			public function GetBadges($modelid) {
				$result = $this->RunQuery($this->_getBadges,
					[
						"modelid"			=> $modelid
					]);
				
				if($result === NULL || $result->rowCount() <= 0)
					return NULL;
				return $result;
			}
		}
	}
	$cars = new CCars;
?>


<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset="utf-8">
    <meta name="description" content="An example of simple vehicle query form.">
    <meta name="author" content="Alden Viljoen">
	
	<link rel="stylesheet" type="text/css" href="css/cars.css">
	
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
	<script type="text/javascript" src="js/cars.js"></script>

    <title>Vehicle Query</title>
  </head>

  <body>
	<div>
		<?php
			$makeID = "";
			$modelID = "";
			$badgeID = "";
			
			if(isset($_POST["txtMakeID"]))
				$makeID = $_POST["txtMakeID"];
			
			if(isset($_POST["txtModelID"]))
				$modelID = $_POST["txtModelID"];
			
			if(isset($_POST["txtBadgeID	"]))
				$badgeID = $_POST["txtBadgeID"];
		?>
		
		<form action="query_cars.php" method="POST" id="frmVehicles">
			<h2>Query a Car!</h2>
			<input type="hidden" name="txtMakeID" id="txtMakeID" value="">
			<input type="hidden" name="txtModelID" id="txtModelID" value="">
			<input type="hidden" name="txtBadgeID" id="txtBadgeID" value="">
			
			<table>
				<tr>
					<td>
						<select id="selChooseMake">
							<option value="-1" selected>Choose a make...</option>
							<?php
								$makes = $cars->GetAllMakes();
								if($makes === NULL) {
									print("Couldn't retreive Vehicle Makes. The script will now exit.");
									exit();
								}
								
								while($make = $cars->GetRow($makes)) {
									$opt = "<option value=\"" . $make["ID"] . "\" ";
									if($make["ID"] === intval($makeID))
										$opt = $opt . "selected";
									$opt = $opt . ">" . $make["Name"] . "</option>";
									
									echo $opt;
								}
							?>
						</select>
					</td>
				</tr>
						
				<tr>
					<td>
						<select id="selChooseModel" hidden>
							<option value="-1" selected>Choose a model...</option>
							<?php
								$models = $cars->GetModels($makeID);
								if($models === NULL) {
									print("Couldn't retreive Vehicle Models. The script will now exit.");
									exit();
								}
								
								while($model = $cars->GetRow($models)) {
									$opt = "<option value=\"" . $model["ID"] . "\" ";
									if($model["ID"] === intval($modelID))
										$opt = $opt . "selected";
									$opt = $opt . ">" . $model["Name"] . "</option>";
									
									echo $opt;
								}
							?>
						</select>
					</td>
				</tr>
				
				<tr>
					<td>
						<select id="selChooseBadge" hidden>
							<option value="-1" selected>Choose a badge...</option>
							<?php
								$badges = $cars->GetBadges($modelID);
								if($badges === NULL) {
									print("Couldn't retreive Vehicle Badges. The script will now exit.");
									exit();
								}
								
								while($badge = $cars->GetRow($badges)) {
									echo "<option value=\"" . $badge["ID"] . "\">" . $badge["Name"] . "</option>";
								}
							?>
						</select>
					</td>
				</tr>
			</table>
		</form>
	</div>
  </body>
</html>