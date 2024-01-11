from app import create_app, vehicles
from app.models import init_database, SessionLocal


with SessionLocal() as sesh:
    # Initialise models on database.
    init_database(sesh)
    try:
        # Import vehicle data.
        vehicles.load_vehicles_from_file(sesh, "vehicles.json")
        # Commit this data.
        sesh.commit()
    except Exception as e:
        pass

application = create_app()
