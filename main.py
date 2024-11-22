from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from schemas import SelfCareActivity, CategoryEnum, ActivityStats, ActivityUpdate, ActivityResponse
from typing import List, Optional
from datetime import date, timedelta


#models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Self-Care Routine Tracker")


@app.post("/activities/", response_model=SelfCareActivity)
def create_activity(activity: SelfCareActivity, db: Session = Depends(get_db)):
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity

@app.get("/activities/", response_model=List[SelfCareActivity])
async def get_activities(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[CategoryEnum] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Activity)

    if start_date:
       query = query.filter(models.Activity.date >= start_date)

    if end_date:
       query = query.filter(models.Activity.date <= end_date)

    if category:
       query = query.filter(models.Activity.category == category)

    if search:
        query = query.filter(
            (models.Activity.activity_name.ilike(f"%{search}%")) |
            (models.Activity.notes.ilike(f"%{search}%"))
    )
        
    return query.all()

@app.get("/activities/{activity_id}", response_model=SelfCareActivity)
async def get_activity(activity_id: int, db: Session = Depends(get_db)) -> SelfCareActivity:
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail=f"Activity with ID {activity_id} not found")
    
    return activity

@app.patch("/activities/{activity_id}", response_model=SelfCareActivity)
async def update_activity(activity_id: int, update_data: ActivityUpdate, db: Session = Depends(get_db)) -> SelfCareActivity:
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail=f"Activity with ID {activity_id} not found")
    
    # Convert the provided update data into a dictionary
    update_dict = update_data.dict(exclude_unset=True) # Exclude unset values (optional fields)

    for key, value in update_dict.items():
        setattr(activity, key, value) # Set the new value on the activity model

    db.commit()
    db.refresh(activity)
    return activity

@app.delete("/activities/{activity_id}", status_code=204)
async def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail=f"Activity with ID {activity_id} not found")
    
    db.delete(activity)
    db.commit()
    return None
    
@app.get("/stats/", response_model=ActivityStats)
async def get_statistics(start_date: Optional[date] = None, end_date: Optional[date] = None, db: Session = Depends(get_db)):
    query = db.query(models.Activity)

    if start_date:
        query = query.filter(models.Activity.date >= start_date)

    if end_date:
        query = query.filter(models.Activity.date <= end_date)

    activities = query.all()
   
    if not activities:
        return ActivityStats(
            total_activities=0,
            total_duration_minutes=0,
            activities_by_category={},
            average_duration=0.0,
            streak_days=0
        )
    
    # Calculate statistics
    total_activities = len(activities)
    total_duration = sum(a.duration_minutes for a in activities)

   # Count activities by category
    category_counts = {}
    for activity in activities:
        category = activity.category
        if category not in category_counts:
            category_counts[category] = 0  
        category_counts[category] += 1  

    # Calculate streak 
    activity_dates = {a.date for a in activities}  
    current_streak = 0
    current_date = date.today()

    # Loop to count consecutive days
    while current_date in activity_dates:
        current_streak += 1
        current_date -= timedelta(days=1)  # Move to previous day

    # Calculate the average duration of activities
    average_duration = total_duration / total_activities if total_activities > 0 else 0.0

    # Return the final stats
    return ActivityStats(
        total_activities=total_activities,
        total_duration_minutes=total_duration,
        activities_by_category=category_counts,
        average_duration=average_duration,
        streak_days=current_streak
    )