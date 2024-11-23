# Self-Care Routine Tracker

## Overview
The Self-Care Routine Tracker is an API designed to help users log, manage, and track their self-care activities like meditation, exercise, journaling, and more. This project uses **FastAPI**, **SQLAlchemy**, and **Pydantic** to provide a simple and scalable backend.

## Features
- **Create, Read, Update, Delete** self-care activities.
- **Track statistics** like total activities, average duration, and streak days.
- **Search and filter activities** by date, category, and activity name.

## Technologies Used
- **FastAPI**: Modern web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: ORM for database management.
- **Pydantic**: Data validation and parsing library.
- **PostgreSQL** (or other database): Used to store activity data.

## Installation

### 1. Clone the repository:
https://github.com/codefromlani/Self-Care-Routine-Tracker
cd Self-Care-Routine-Tracker
pip install -r requirements.txt

## API Endpoints

- **POST /activities/**: Create a new activity
- **GET /activities/**: Get a list of activities (with optional filters)
- **GET /activities/{activity_id}**: Get a specific activity by ID
- **PATCH /activities/{activity_id}**: Update an activity
- **DELETE /activities/{activity_id}**: Delete an activity
- **GET /stats/**: Get statistics on activities


## Contributing
If you'd like to contribute, please fork the repository and submit a pull request with your improvements.