var frmChooseVehicle = null;

function ChooseMake(makeid) {
	$("#txtMakeID").val(makeid);
	
	frmChooseVehicle.submit();
}

function ChooseModel(makeid, modelid) {
	$("#txtMakeID").val(makeid);
	$("#txtModelID").val(modelid);
	
	frmChooseVehicle.submit();
}

$(document).ready(function() {
	frmChooseVehicle = $("#frmVehicles");
	
	$("#selChooseMake").change(function() {
		// Get the target make ID.
		var makeid = $(this).val();
		ChooseMake(makeid);
	});
	
	$("#selChooseModel").change(function() {
		// Get the target model ID.
		var modelid = $(this).val();
		ChooseModel($("#selChooseMake").val(), modelid);
	});
	
	var chosenMakeID = $("#selChooseMake").val();
	var chosenModelID = $("#selChooseModel").val();
	
	if(chosenMakeID != "-1") {
		$("#selChooseModel").show();
	}else{
		$("#selChooseModel").hide();
	}
	
	if(chosenModelID != "-1") {
		$("#selChooseBadge").show();
	}else{
		$("#selChooseBadge").hide();
	}
});