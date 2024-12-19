from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the input model for the POST request
class CelestialRequest(BaseModel):
    name: str

def format_ra(decimal_degrees):
    """Convert RA from degrees to HH:MM:SS."""
    try:
        decimal_hours = decimal_degrees / 15
        hours = int(decimal_hours)
        minutes = int((decimal_hours - hours) * 60)
        seconds = ((decimal_hours - hours) * 60 - minutes) * 60
        return f"{hours:02d}h {minutes:02d}m {seconds:.2f}s"
    except Exception as e:
        return "Invalid RA"

def format_degrees(decimal_degrees):
    """Convert decimal degrees to degrees, arcminutes, arcseconds."""
    try:
        sign = "-" if decimal_degrees < 0 else ""
        decimal_degrees = abs(decimal_degrees)
        degrees = int(decimal_degrees)
        arcminutes = int((decimal_degrees - degrees) * 60)
        arcseconds = ((decimal_degrees - degrees) * 60 - arcminutes) * 60
        return f"{sign}{degrees}° {arcminutes}' {arcseconds:.2f}\""
    except Exception as e:
        return "Invalid Degrees"

@app.get("/")
async def root():
    return {"message": "Welcome to the Celestial Tracker API"}

@app.post("/get-coordinates/")
async def get_coordinates(request: CelestialRequest):
    celestial_name = request.name
    stellarium_api_url = "http://localhost:8090/api/objects/info"  # Stellarium API endpoint
    params = {
        "name": celestial_name,
        "format": "json",
    }

    try:
        # Fetch data from Stellarium
        response = requests.get(stellarium_api_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract raw values
        ra_decimal = data.get("ra")
        dec_decimal = data.get("dec")
        azimuth_decimal = data.get("azimuth")
        altitude_decimal = data.get("altitude")

        # Format the coordinates
        formatted_ra = format_ra(ra_decimal)
        formatted_dec = format_degrees(dec_decimal)
        formatted_azimuth = format_degrees(azimuth_decimal)
        formatted_altitude = format_degrees(altitude_decimal)

        # Return formatted data as JSON
        return {
            "name": celestial_name,
            "coordinates": {
                "RA": formatted_ra,
                "Dec": formatted_dec,
                "Azimuth": formatted_azimuth,
                "Altitude": formatted_altitude,
            },
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Stellarium API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
