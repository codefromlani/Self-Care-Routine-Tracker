from fastapi import FastAPI, HTTPException
from schemas import SelfCareActivity, CategoryEnum, ActivityStats, ActivityUpdate
from typing import List, Optional
from datetime import date, timedelta

app = FastAPI(title="Self-Care Routine Tracker")


# In-memory storage
activities_db = []

activity_counter = 1

#Routes
@app.post("/activities/", response_model=SelfCareActivity)
async def create_activity(activity: SelfCareActivity):
    global activity_counter
    activity.id = activity_counter
    activity_counter += 1
    activities_db.append(activity)
    return activity

@app.get("/activities/", response_model=List[SelfCareActivity])
async def get_activities(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[CategoryEnum] = None,
    search: Optional[str] = None
):
    filtered_activities = []

    for a in activities_db:
        # date range filter
        if start_date and a.date < start_date:
            continue
        if end_date and a.date > end_date:
            continue

        # category filter
        if category and a.category != category:
            continue

        # search filter
        if search and not (search.lower() in a.activity_name.lower() or (a.notes and search.lower() in a.notes.lower())):
            continue

        # If all filters pass, add the activity to the result
        filtered_activities.append(a)

    return filtered_activities

@app.get("/activities/{activity_id}", response_model=SelfCareActivity)
async def get_activity(activity_id: int):
    for a in activities_db:
        if a.id == activity_id:
            return a
    raise HTTPException(status_code=404, detail="Activity with ID {activity_id} not found")

@app.patch("/activities/{activity_id}", response_model=SelfCareActivity)
async def update_activity(activity_id: int, update_data: ActivityUpdate):
    for idx, activity in enumerate(activities_db):
        if activity["id"] == activity_id:
            if update_data.activity_name is not None:
                activity["activity_name"] = update_data.activity_name
            if update_data.category is not None:
                activity["category"] = update_data.category
            if update_data.date is not None:
                activity["date"] = update_data.date
            if update_data.duration_minutes is not None:
                activity["duration_minutes"] = update_data.duration_minutes
            if update_data.notes is not None:
                activity["notes"] = update_data.notes

            return {"activity": activity, "index": idx}
        
    raise HTTPException(status_code=404, detail="Activity with ID {activity_id} not found")

@app.delete("activities/{activity_id}", status_code=204)
async def delete_activity(activity_id: int):
    for idx, activity in enumerate(activities_db):
        if activity.id == activity_id:
            activities_db.pop(idx)
            return None
    raise HTTPException(status_code=404, detail="Activity with ID {activity_id} not found")
    
@app.get("/stats/", response_model=ActivityStats)
async def get_statistics(start_date: Optional[date] = None, end_date: Optional[date] = None):
    filtered_activities = activities_db

    if start_date:
        filtered_activities = [a for a in filtered_activities if a.date >= start_date]

    if end_date:
        filtered_activities = [a for a in filtered_activities if a.date <= end_date]

    # If no activities match the filter, return empty stats
    if not filtered_activities:
        return ActivityStats(
            total_activities=0,
            total_duration_munites=0,
            activities_by_category={},
            average_duration=0.0,
            streak_days=0
        )
    
    # Calculate the total number of activities
    total_activities = len(filtered_activities)

     # Calculate the total duration of all activities
    total_duration = sum(a.duration_minutes for a in filtered_activities)

   # Count activities by category
    category_counts = {}
    for activity in filtered_activities:
        category = activity.category
        if category not in category_counts:
            category_counts[category] = 0  
        category_counts[category] += 1  

    # Calculate streak of consecutive days with activities
    activity_dates = {a.date for a in filtered_activities}  
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
        total_duration_munites=total_duration,
        activities_by_category=category_counts,
        average_duration=average_duration,
        streak_days=current_streak
    )