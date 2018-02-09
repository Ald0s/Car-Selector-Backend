<?php
	/*
	Summary:
	Represents a link to the database.
	
	Note:
	This solution uses PDO for security and future proof standards.
	*/
	
	require_once("srvr_config.php");
	
	if(!class_exists("CDBConnection")) {
		class CDBConnection {
			private $name = null;
			
			// The connection handle to the database.
			private $lnk = null;
			
			function __construct($_name) {
				$this->name = $_name;
				if(IsConfigValid() === FALSE) {
					echo "Database config NOT valid. The script will now exit.<br>Please update 'srvr_config.php' to retry!";
					exit();
				}
				
				$host = HOST;
				$database = DATABASE;
				$user = USERNAME;
				$pass = PASSWORD;
				
				$dsn = "mysql:host=$host;dbname=$database;charset=utf8";
				$opt = [
					PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
					PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
					PDO::ATTR_EMULATE_PREPARES   => false,
				];
				
				$this->lnk = new PDO($dsn, $user, $pass, $opt);
				$this->lnk->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );
			}
			
			// Runs a parameterless query.
			protected function RunGetQuery($sql) {
				$obj = $this->lnk->query($sql);
				if($obj === NULL || $obj === FALSE)
					$this->Error("RunQuery() (parameterless) returned NULL or FALSE!");
				
				return $obj;
			}
			
			// Runs a query with parameters.
			protected function RunQuery($sql, $values) {
				$stt = $this->lnk->prepare($sql);
				$obj = $stt->execute($values);
				
				if($stt === NULL || $obj === FALSE)
					$this->Error("RunQuery() (parameters) returned NULL or FALSE!");

				return $stt;
			}
			
			protected function RunQuery_GetLastInsertID($sql, $values) {
				$result = $this->RunQuery($sql, $values);
				$last_id = $this->lnk->lastInsertId();
				
				return array(
					"Result"		=> $result,
					"InsertID"		=> $last_id
					);
			}
			
			protected function DoesTableExist($table) {
				$result = $this->RunGetQuery(
					"SHOW TABLES LIKE '$table'");
					
				if($result === NULL || $result->rowCount() <= 0) {
					return FALSE;
				}
				return TRUE;
			}
			
			protected function GetTableSize($table) {
				return $this->RunGetQuery("SELECT * FROM $table")->rowCount();
			}
			
			// Returns a single row from a statement.
			// By default, associative.
			public function GetRow($statement) {
				if($statement === FALSE || $statement->rowCount() <= 0)
					return NULL;
				
				return @$statement->fetch( PDO::FETCH_ASSOC );
			}
			
			public function GetAllResults($statement) {
				if($statement === FALSE || $statement->rowCount() <= 0)
					return NULL;
				
				return @$statement->fetchAll( PDO::FETCH_ASSOC );
			}
			
			protected function Error($text) {
				error_log("[" . $this->name . "] " . $text);
			}
			
			/*
			Summary
			Gets the last AI ID created by the database.
			*/
			protected function GetLastID() {
				return $this->lnk->lastInsertId();
			}
		}
	}
?>