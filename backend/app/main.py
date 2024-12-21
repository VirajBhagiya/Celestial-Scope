from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db, create_tables
from .models import User
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from skyfield.api import load, wgs84
from .auth import hash_password, verify_password, create_access_token, get_current_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    
class TokenRequest(BaseModel):
    username: str
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
class CelestialRequest(BaseModel):
    name: str
    latitude: float = Field(..., ge=-90, le=90, description="Latitude must be between -90 and 90")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude must be between -180 and 180")

ts = load.timescale()
ephemeris = load("de421.bsp")
earth = ephemeris['earth']

@app.on_event("startup")
async def startup_event():
    # Initialize tables on startup
    create_tables()

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Celestial Tracker API is running"}

@app.post("/get-coordinates/")
async def get_coordinates(request: CelestialRequest):
    celestial_name = request.name.lower()
    latitude = request.latitude
    longitude = request.longitude
    observer = earth + wgs84.latlon(latitude, longitude)
    try:
        try:
            celestial_body = ephemeris[celestial_name]
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Celestial object '{celestial_name}' not found in ephemeris")

        t = ts.now()
        astrometric = observer.at(t).observe(celestial_body)
        apparent = astrometric.apparent()
        ra, dec, _ = apparent.radec()
        alt, az, _ = apparent.altaz()

        return {
            "name": celestial_name,
            "coordinates": {
                "RA": format_ra(ra.hours),
                "Dec": format_degrees(dec.degrees),
                "Azimuth": format_degrees(az.degrees),
                "Altitude": format_degrees(alt.degrees),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.post("/register/")
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Hash the password and store the user
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}

@app.post("/token/", response_model=TokenResponse)
async def login_for_access_token(request: TokenRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected/")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"msg": "This is a protected route", "user": current_user}


# Helper functions to format coordinates
def format_ra(decimal_hours):
    try:
        hours = int(decimal_hours)
        minutes = int((decimal_hours - hours) * 60)
        seconds = ((decimal_hours - hours) * 60 - minutes) * 60
        return f"{hours:02d}h {minutes:02d}m {seconds:.2f}s"
    except Exception as e:
        return "Invalid RA"

def format_degrees(decimal_degrees):
    try:
        sign = "-" if decimal_degrees < 0 else ""
        decimal_degrees = abs(decimal_degrees)
        degrees = int(decimal_degrees)
        arcminutes = int((decimal_degrees - degrees) * 60)
        arcseconds = ((decimal_degrees - degrees) * 60 - arcminutes) * 60
        return f"{sign}{degrees}° {arcminutes}' {arcseconds:.2f}\""
    except Exception as e:
        return "Invalid Degrees"