# VoteSecure

A secure desktop voting application built with Python. Supports admin controls, voter registration, and live vote counting using socket programming with synchronous multithreading.

## Features

- Admin dashboard to manage voters, start the server, and view live results
- Voter portal to securely cast a ballot
- Socket-based client-server architecture
- CSV-based voter and candidate database

## Requirements

- Python 3.x
- pandas
- pillow

Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

1. Start the app:
```bash
python homePage.py
```

2. Login as Admin (ID: `Admin`, Password: `admin`)
3. Click **Run Server** from the Admin Dashboard
4. Go back to Home and login as a Voter to cast a ballot

## Default Credentials

| Role  | ID    | Password |
|-------|-------|----------|
| Admin | Admin | admin    |
