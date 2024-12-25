from skyfield.api import N, E, wgs84, load

ts = load.timescale()
planets = load('de421.bsp')

def get_planet_coordinates(planet_name, latitude, longitude):
    try:
        planet = planets[planet_name]
        t = ts.now()
        
        # RA and Dec from Earth's perspective
        earth = planets['earth']
        astrometric = earth.at(t).observe(planet)
        apparent = astrometric.apparent()
        ra, dec, distance = apparent.radec('date') # Right Ascension, Declination
        
        observer = earth + wgs84.latlon(latitude * N, longitude * E)
        astro = observer.at(t).observe(planet)
        app = astro.apparent()
        altitude, azimuth, distance = app.altaz()
        
        return {
            "RA": ra,
            "Dec": dec,
            "Altitude": altitude,
            "Azimuth": azimuth,
        }
    
    except KeyError:
        return {"error": f"Planet '{planet_name}' not found in the ephemeris."}


latitude = 23.150027
longitude = 72.638222
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
