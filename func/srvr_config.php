<?php
// Server configuration, must be defined before executing any queries.

define("USERNAME", "root");
define("PASSWORD", "");
define("HOST", "localhost");
define("DATABASE", "vehicle");

function IsConfigValid() {
	return (strlen(USERNAME) > 0) && 
		   (strlen(HOST) > 0) && 
		   (strlen(DATABASE) > 0);
}
?>