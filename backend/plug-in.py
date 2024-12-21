import requests

def format_ra(decimal_degrees):
    try:
        # Convert degrees to hours
        decimal_hours = decimal_degrees / 15
        hours = int(decimal_hours)
        minutes = int((decimal_hours - hours) * 60)
        seconds = ((decimal_hours - hours) * 60 - minutes) * 60
        return f"{hours:02d}h {minutes:02d}m {seconds:.2f}s"
    except Exception as e:
        print(f"Error formatting RA: {e}")
        return "Invalid RA"

def format_degrees(decimal_degrees):
    try:
        # Handle negative degrees
        sign = "-" if decimal_degrees < 0 else ""
        decimal_degrees = abs(decimal_degrees)
        degrees = int(decimal_degrees)
        arcminutes = int((decimal_degrees - degrees) * 60)
        arcseconds = ((decimal_degrees - degrees) * 60 - arcminutes) * 60
        return f"{sign}{degrees}° {arcminutes}' {arcseconds:.2f}\""
    except Exception as e:
        print(f"Error formatting degrees: {e}")
        return "Invalid Degrees"

def get_celestial_coordinates(celestial_name):
    base_url = 'http://localhost:8090/api/objects/info'
    params = {
        'name': celestial_name,
        'format': 'json'
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract raw values
        ra_decimal = data.get('ra')
        dec_decimal = data.get('dec')
        az_decimal = data.get('azimuth')
        alt_decimal = data.get('altitude')

        # Debugging raw values
        print(f"Raw RA: {ra_decimal}")
        print(f"Raw Dec: {dec_decimal}")
        print(f"Raw Azimuth: {az_decimal}")
        print(f"Raw Altitude: {alt_decimal}")

        # Convert to desired formats
        ra_formatted = format_ra(ra_decimal)
        dec_formatted = format_degrees(dec_decimal)
        az_formatted = format_degrees(az_decimal)
        alt_formatted = format_degrees(alt_decimal)

        # Display the results
        print(f"Formatted RA: {ra_formatted}")
        print(f"Formatted Dec: {dec_formatted}")
        print(f"Formatted Azimuth: {az_formatted}")
        print(f"Formatted Altitude: {alt_formatted}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

get_celestial_coordinates("Mars")