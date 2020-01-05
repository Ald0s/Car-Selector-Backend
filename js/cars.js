function GetAllMakes() {
	$("#selChooseMake").empty();
	$("#selChooseModel").empty();
	$("#selChooseBadge").empty();
	
	$("#selChooseModel").hide();
	$("#selChooseBadge").hide();
	
	var makes = $("#selChooseMake");
	makes.append($("<option />").val(-1).text("Choose a make ..."));
	
	$.get("query_cars.php", { SELECT: "MAKES" }, function ( data ) {
		$.each(JSON.parse(data), function () {
			makes.append($("<option />").val(this.ID).text(this.Name));
		});
	});
}

function GetModelsForMake(make) {
	$("#selChooseModel").empty();
	$("#selChooseBadge").empty();
	
	$("#selChooseModel").show();
	$("#selChooseBadge").hide();
	
	var models = $("#selChooseModel");
	models.append($("<option />").val(-1).text("Choose a model ..."));
	
	$.get("query_cars.php", { SELECT: "MODELS", MAKEID: make }, function ( data ) {
		$.each(JSON.parse(data), function () {
			models.append($("<option />").val(this.ID).text(this.Name));
		});
	});
}

function GetBadgesForModel(model) {
	$("#selChooseBadge").empty();
	
	$("#selChooseModel").show();
	$("#selChooseBadge").show();
	
	var badges = $("#selChooseBadge");
	badges.append($("<option />").val(-1).text("Choose a badge ..."));
	
	$.get("query_cars.php", { SELECT: "BADGES", MODELID: model }, function ( data ) {
		$.each(JSON.parse(data), function () {
			badges.append($("<option />").val(this.ID).text(this.Name));
		});
	});
}

$(document).ready(function() {
	// When document ready, get all makes and populate the combobox.
	GetAllMakes();
	
	$("#selChooseMake").change(function() {
		// Get the target make ID.
		var makeid = $(this).val();
		
		GetModelsForMake(makeid);
	});
	
	$("#selChooseModel").change(function() {
		// Get the target model ID.
		var modelid = $(this).val();
		
		GetBadgesForModel(modelid);
	});
});