"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


def print_activities_table():
    """Print all activities in a formatted table"""
    print("\n" + "="*100)
    print("MERGINGTON HIGH SCHOOL - EXTRACURRICULAR ACTIVITIES")
    print("="*100)
    
    # Print header
    print(f"{'Activity Name':<25} {'Schedule':<40} {'Participants':<15} {'Max':<5}")
    print("-"*100)
    
    # Print each activity
    for activity_name, details in activities.items():
        schedule = details['schedule']
        participant_count = len(details['participants'])
        max_participants = details['max_participants']
        
        print(f"{activity_name:<25} {schedule:<40} {participant_count:<15} {max_participants:<5}")
    
    print("="*100 + "\n")


def print_participants_table():
    """Print participants for each activity in formatted tables"""
    print("\n" + "="*100)
    print("ACTIVITY PARTICIPANTS")
    print("="*100 + "\n")
    
    for activity_name, details in activities.items():
        print(f"Activity: {activity_name}")
        print(f"Description: {details['description']}")
        print(f"Schedule: {details['schedule']}")
        print(f"Capacity: {len(details['participants'])}/{details['max_participants']}")
        print("-"*100)
        
        if details['participants']:
            print(f"{'No.':<5} {'Student Email':<40}")
            print("-"*100)
            for idx, email in enumerate(details['participants'], 1):
                print(f"{idx:<5} {email:<40}")
        else:
            print("No participants yet.")
        
        print("="*100 + "\n")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


# Print tables when the script is run directly
if __name__ == "__main__":
    print_activities_table()
    print_participants_table()
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
