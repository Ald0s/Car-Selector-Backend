import json

from flask import request, render_template, abort

from base import app
from base.models import Car, Bike, Make, Model, Badge

@app.route("/", methods = [ "GET" ])
@app.route("/vehicle", methods = [ "GET" ])
def ChooseVehicle():
    # Serve the basic form to the user.
    return render_template("index.html")

def Response(name, value):
    return json.dumps({
        name:       value
    })

def GetAllMakes(type):
    vehicles = Make.GetByType(type)
    if not vehicles:
        abort(500)

    schemas = []
    for x in vehicles:
        schemas.append( 
            x.Serialize( exclude = ("models",)) )

    return Response("response", schemas)

def GetModels(makeid):
    make = Make.GetById(makeid)
    if not make:
        abort(400)

    # Can improve by make.Serialize( only = ("models",) ) ["models"]
    # TODO: But must exclude model->badges & model->make as well.
    schemas = []
    for x in make.models:
        schemas.append( 
            x.Serialize( exclude = ( "make", "badges", )) )

    return Response("response", schemas)

def GetBadges(modelid):
    model = Model.GetById(modelid)
    if not model:
        abort(400)

    # Same as above sort've.
    schemas = []
    for x in model.badges:
        schemas.append( 
            x.Serialize( exclude = ( "model", )) )

    return Response("response", schemas)

# Note: it's never a great idea to use auto increment IDs to exchange references with a user.
# But its a simple way to do it for now.
@app.route("/api/vehicles", methods = [ "POST" ])
def GetVehicles():
    # Return vehicle data for display.
    what    = request.values.get("what") or None

    if what == "all-makes":
        vehicle_type    = request.values.get("vehicle-type") or None
        if vehicle_type == "":
            abort(400)

        return GetAllMakes(vehicle_type)

    elif what == "models":
        makeid          = request.values.get("makeid") or None

        try:
            makeid      = int(makeid)
        except ValueError as e:
            abort(400)

        return GetModels(makeid)

    elif what == "badges":
        modelid         = request.values.get("modelid") or None

        try:
            modelid     = int(modelid)
        except ValueError as e:
            abort(400)

        return GetBadges(modelid)

    else:
        print("User sent rubbish: what={0}".format(what))
        abort(400)
