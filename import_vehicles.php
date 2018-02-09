<?php
	/*
	Summary:
	Provides the functionality for reading and entering data pertaining to the list of cars into the database.
	*/
	
	require_once("func/database.php");
	
	if(!class_exists("CImportCars")) {
		class CImportCars extends CDBConnection {
			function __construct() {
				parent::__construct("ImportCars");
				
				$this->CreateRequiredTables();
				$this->ProcessCars();
			}
			
			public function ProcessCars() {
				$h = fopen("cars.txt", "r");
				if(!$h) {
					error_log("Failed to open cars.txt!");
					return;
				}
				
				$json = fread($h, filesize("cars.txt"));
				$cars = json_decode($json, true)["Cars"];
				
				$this->HandleMakes($cars);
			}
			
			private $_createMake = "INSERT INTO vehicle_make(VehicleID, VehicleType, VehicleMake) VALUES (NULL, :type, :make)";
			private function HandleMakes($make_array) {
				if($this->GetTableSize("vehicle_make") > 0) {
					// We have already got data in these tables, forget about doing all this again.
					return;
				}
				
				foreach($make_array as $k => $v) {
					$vehicleid = $this->RunQuery_GetLastInsertID($this->_createMake,
						[
							"type"			=> 0,
							"make"			=> $v["Make"]
						])["InsertID"];
						
					// Then, handle models for this make.
					$this->HandleModels($vehicleid, $v["Models"]);
				}
			}
			
			private $_addModel = "INSERT INTO vehicle_model(VehicleModelID, VehicleModel, VehicleID) VALUES (NULL, :model, :vehicleid)";
			private function HandleModels($vehicleid, $models) {
				foreach($models as $k => $v) {
					// For each model, we want to attach it to the previously created vehicleid.
					$modelid = $this->RunQuery_GetLastInsertID($this->_addModel,
						[
							"model"			=> $v["Model"],
							"vehicleid"		=> $vehicleid
						])["InsertID"];
						
					// Then, handle badges for this model.
					$this->HandleBadges($modelid, $v["Badges"]);
				}
			}
			
			private $_addBadge = "INSERT INTO vehicle_badge(VehicleBadgeID, VehicleBadge, VehicleModelID) VALUES (NULL, :badge, :modelid)";
			private function HandleBadges($modelid, $badges) {
				foreach($badges as $k => $v) {
					// For each badge, we want to attach it to the previously created model.
					$this->RunQuery($this->_addBadge,
						[
							"badge"			=> $v["Badge"],
							"modelid"		=> $modelid
						]);
				}
			}
			
			private function CreateRequiredTables() {
				if($this->DoesTableExist("vehicle_make") === FALSE) {
					$this->RunGetQuery($this->_vehicleMake);
				}
				
				if($this->DoesTableExist("vehicle_model") === FALSE) {
					$this->RunGetQuery($this->_vehicleModel);
				}
				
				if($this->DoesTableExist("vehicle_badge") === FALSE) {
					$this->RunGetQuery($this->_vehicleBadge);
				}
			}
			
			private $_vehicleMake = "
				CREATE TABLE vehicle_make(
				VehicleID				 INT	     		 AUTO_INCREMENT,
				VehicleType				 INT				 NOT NULL,
				VehicleMake				 VARCHAR(255)		 NOT NULL,
				
				PRIMARY KEY(VehicleID)
			)";
			
			private $_vehicleModel = "
				CREATE TABLE vehicle_model(
				VehicleModelID			 INT				 AUTO_INCREMENT,
				VehicleModel			 VARCHAR(255)		 NOT NULL,
				VehicleID				 INT				 NOT NULL,
				
				PRIMARY KEY(VehicleModelID)
			)";
			
			private $_vehicleBadge = "
				CREATE TABLE vehicle_badge(
				VehicleBadgeID			 INT				 AUTO_INCREMENT,
				VehicleBadge			 VARCHAR(255)		 NOT NULL,
				VehicleModelID			 INT				 NOT NULL,
				
				PRIMARY KEY(VehicleBadgeID)
			)";
		}
	}
	$cars = new CImportCars;
?>