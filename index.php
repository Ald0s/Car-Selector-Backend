<?php
	if(isset($_POST["frmVehicles"])) {
		// Do something with the values of selChooseMake, selChooseModel and selChooseBadge.
	}
?>

<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset="utf-8">
    <meta name="description" content="An example of simple vehicle query form.">
    <meta name="author" content="Alden Viljoen">
	
	<link rel="stylesheet" type="text/css" href="css/cars.css?t=<?php print(time()); ?>">
	
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
	<script type="text/javascript" src="js/cars.js?t=<?php print(time()); ?>"></script>

    <title>Vehicle Query</title>
  </head>

  <body>
	<div>
		<h2>Query a Car!</h2>
		<form action="index.php" method="POST" id="frmVehicles">
			<table>
				<tr>
					<td>
						<select id="selChooseMake"></select>
					</td>
				</tr>
				
				<tr>
					<td>
						<select id="selChooseModel"></select>
					</td>
				</tr>
				
				<tr>
					<td>
						<select id="selChooseBadge"></select>
					</td>
				</tr>
			</table>
		</form>
	</div>
  </body>
</html>