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
				
				if($_GET["SELECT"] == "MAKES") {
					print(json_encode($this->GetAllMakes()));
				}elseif($_GET["SELECT"] == "MODELS") {
					if(intval($_GET["MAKEID"]) < 0)
						$_GET["MAKEID"] = "1";
					
					print(json_encode($this->GetModels($_GET["MAKEID"])));
				}elseif($_GET["SELECT"] == "BADGES") {
					if(intval($_GET["MODELID"]) < 0)
						$_GET["MODELID"] = "1";
					
					print(json_encode($this->GetBadges($_GET["MODELID"])));
				}
			}
			
			private $_getAllMakes = "SELECT VehicleID AS ID, VehicleMake AS Name FROM vehicle_make";
			public function GetAllMakes() {
				$result = $this->RunGetQuery($this->_getAllMakes);
				
				if($result === NULL || $result->rowCount() <= 0)
					return NULL;
				return $this->GetAllResults($result);
			}
			
			private $_getModels = "SELECT VehicleModelID AS ID, VehicleModel AS Name FROM vehicle_model WHERE VehicleID=:makeid";
			public function GetModels($makeid) {
				$result = $this->RunQuery($this->_getModels,
					[
						"makeid"			=> $makeid
					]);
				
				if($result === NULL || $result->rowCount() <= 0)
					return NULL;
				return $this->GetAllResults($result);
			}
			
			private $_getBadges = "SELECT VehicleBadgeID AS ID, VehicleBadge AS Name FROM vehicle_badge WHERE VehicleModelID=:modelid";
			public function GetBadges($modelid) {
				$result = $this->RunQuery($this->_getBadges,
					[
						"modelid"			=> $modelid
					]);
				
				if($result === NULL || $result->rowCount() <= 0)
					return NULL;
				return $this->GetAllResults($result);
			}
		}
	}
	$cars = new CCars;
?>