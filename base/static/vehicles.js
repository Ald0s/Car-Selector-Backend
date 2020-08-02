var statusHandlers = {
	400: function ( ) {
		console.log("400 Bad Request");
	}
};

var GetVehicles 		= null;

var DeserializeBadges 	= null;
var DeserializeModels 	= null;
var DeserializeMakes 	= null;

var GetHost 			= null;
var ResetForm 			= null;
var Hide 				= null;

function GetMakes( type ) {

	ResetForm();
	
	var makes = $("#make");
	makes.append($("<option />").val(-1).text("Choose a make ..."));

	GetVehicles({
		"vehicle-type": 		type,
		"what": 				"all-makes" 				
	}, 

	function ( data ) {

		var response = JSON.parse(data) ["response"];
		for(var i = 0; i < response.length; i++)
			
			makes.append($("<option />")
				.val(response[i].id)
				.text(response[i].name));
		
		if(response.length > 0)
			Hide("#makecontainer", false);

	}, statusHandlers);
}

function GetModels( makeid ) {

	$("#model").empty();
	$("#badge").empty();
	
	Hide("#modelcontainer", true);
	Hide("#badgecontainer", true);
	
	var models = $("#model");
	models.append($("<option />").val(-1).text("Choose a model ..."));

	GetVehicles({
		"what": 				"models",
		"makeid": 				makeid 				
	}, 

	function ( data ) {

		var response = JSON.parse(data) ["response"];
		for(var i = 0; i < response.length; i++)
			models.append($("<option />")
				.val(response[i].id)
				.text(response[i].name));
		
		if(response.length > 0)
			Hide("#modelcontainer", false);
		
	}, statusHandlers);
}

function GetBadges( modelid ) {

	$("#badge").empty();
	
	Hide("#modelcontainer", false);
	Hide("#badgecontainer", false);
	
	var badges = $("#badge");
	badges.append($("<option />").val(-1).text("Choose a badge ..."));

	GetVehicles({
		"what": 				"badges",
		"modelid": 				modelid 				
	}, 

	function ( data ) {

		var response = JSON.parse(data) ["response"];
		for(var i = 0; i < response.length; i++)

			badges.append($("<option />")
				.val(response[i].id)
				.text(response[i].name));
		
		if(response.length > 0)
			Hide("#badgecontainer", false);
		
	}, statusHandlers);
}

$(window).ready( function ( ) {

	ResetForm();
	$("#type").val("none");
	
	$("#type").change( function ( ) {

		// Get the target make ID.
		var chosenType = $(this).val();

		GetMakes(chosenType);
	});
	
	$("#make").change( function ( ) {
		// Get the target make ID.
		var makeid = parseInt( $(this).val() );

		GetModels(makeid);
	});
	
	$("#model").change( function ( ) {
		// Get the target model ID.
		var modelid = parseInt( $(this).val() );
		
		// Only request badges if the user isn't selecting a bike.
		// (Which don't have badges.)
		if( $("#type").val() != "bike" ) {
			GetBadges(modelid);

		} else {

			var chosenType 		= $("#type").val();

			var makeid 			= parseInt( $("#make").val() );
			var modelid 		= parseInt( $("#model").val() );

			// User's chosen a bike.
		}
	});
	
	$("#badge").change( function( ) {
		var badgeid = parseInt( $(this).val() );
		
		// Set a submit button visible here or some other thing.
		var chosenType 		= $("#type").val();

		var makeid 			= parseInt( $("#make").val() );
		var modelid 		= parseInt( $("#model").val() );
		var badgeid 		= parseInt( $(this).val() );

		// User's chosen a car. (Or other type that has badges.)
	});

	GetVehicles = function ( data, success, status_handlers ) {

		var request = function ( host, data, method, success, error, status ) {
			$.ajax({

				url:		GetHost() + host,
				data:		data,
				success:	success,
				error:		error,
				method:		method,
				type:		method,
				xhrFields: {

					// You'll need to organise CORS for this.
					// withCredentials: true
				},
				statusCode: status
			});

		};

		request (
			"api/vehicles",
			data,
			"POST",
			success,
			function ( ) {
				// Improve this..
				console.log("Couldn't perform vehicles request!");
			},
			status_handlers);
	};
});

/* All expect json arrays */
/* Just demo functions, not actually using.

	But you can just plug response from the server in. 
	
	var response = JSON.parse(data) ["response"];
	var makes = DeserializeMakes( response );
*/
DeserializeBadges = function ( j_bdg_array ) {

	badge_cls = {
		id: 			0,
		name: 			null,

		model: 			null
	};

	if( j_bdg_array == null )
		return null;

	var badges = [];
	for( var i = 0; i < j_bdg_array.length; i++ ) {

		badge_cls["id"]			= parseInt( j_bdg_array [i] ["id"] );

		badge_cls["name"]		= j_bdg_array [i] ["name"];

		if( "model" in j_bdg_array [i] )
			badge_cls["model"]	= DeserializeModels( [ j_bdg_array [i] ["model"] ] ) [0]; // These are dirty, but great!

		badges.push( badge_cls );
	}

	return badges;
};

DeserializeModels = function ( j_mdl_array ) {

	model_cls = {
		id: 			0,
		name: 			null,

		make: 			null,
		badges: 		null
	};

	if( j_mdl_array == null )
		return null;

	var models = [];
	for( var i = 0; i < j_mdl_array.length; i++ ) {

		model_cls["id"]			= parseInt( j_mdl_array [i] ["id"] );

		model_cls["name"]		= j_mdl_array [i] ["name"];

		if( "make" in j_mdl_array [i] )
			model_cls["make"]	= DeserializeMakes( [ j_mdl_array [i] ["make"] ] ) [0]; // These are dirty, but great!

		if( "badges" in j_mdl_array [i] )
			model_cls["badges"]	= DeserializeBadges( j_mdl_array [i] ["badges"] );

		models.push( model_cls );
	}

	return models;
};

DeserializeMakes = function ( j_mk_array ) {

	make_cls = {
		id: 			0,
		name: 			null,
		type: 			null,

		models: 		null
	};

	if( j_mk_array == null )
		return null;

	var makes = [];
	for( var i = 0; i < j_mk_array.length; i++ ) {

		make_cls["id"]			= parseInt( j_mk_array [i] ["id"] );

		make_cls["name"]		= j_mk_array [i] ["name"];
		make_cls["type"]		= j_mk_array [i] ["type_"];

		if( "models" in j_mk_array [i] )
			make_cls["models"]	= DeserializeModels( j_mk_array [i] ["models"] );

		makes.push( make_cls );
	}

	return makes;
};

GetHost = function ( ) {
	return "http://127.0.0.1:5000/";
};

ResetForm = function ( ) {

	$("#make").empty();
	$("#model").empty();
	$("#badge").empty();
};

Hide = function ( name, hide ) {
	var element = $(name);
	
	if(element)
		element.css("display", (hide) ? "none" : "block");
};