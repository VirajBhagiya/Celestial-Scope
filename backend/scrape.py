from turtle import distance
from skyfield.api import N, S, E, W, wgs84, load

ts = load.timescale()
planets = load('de421.bsp')

def get_planet_coordinates(planet_name, latitude, longitude):
    try:
        # Get the planet object dynamically
        planet = planets[planet_name]
        
        # Get current time
        t = ts.now()
        
        # RA and Dec from Earth's perspective
        earth = planets['earth']
        astrometric = earth.at(t).observe(planet)
        apparent = astrometric.apparent()
        ra, dec, distance = apparent.radec('date')
        
        # Altitude and Azimuth from a specific location
        observer = earth + wgs84.latlon(latitude * N, longitude * E)
        astro = observer.at(t).observe(planet)
        app = astro.apparent()
        alt, az, distance = app.altaz()
        
        return {
            "RA": ra,
            "Dec": dec,
            "Altitude": alt,
            "Azimuth": az,
        }
    
    except KeyError:
        return {"error": f"Planet '{planet_name}' not found in the ephemeris."}

latitude = 23.2156
longitude = 72.6369  
planet_name = 'moon'

coordinates = get_planet_coordinates(planet_name, latitude, longitude)

if "error" in coordinates:
    print(coordinates["error"])
else:
    print(f"Coordinates for {planet_name.capitalize()}:")
    print(f"RA: {coordinates['RA']}")
    print(f"Dec: {coordinates['Dec']}")
    print(f"Altitude: {coordinates['Altitude']}")
    print(f"Azimuth: {coordinates['Azimuth']}")
