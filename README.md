# Innovision - PM Internship Portal

A straightforward web app to match students with relevant internship opportunities based on their skill sets and preferences.

## Tech Stack

*   **Frontend**: React.js (Create React App), HTML5, CSS3
*   **Backend**: Python, Flask, scikit-learn (used in the advanced recommender)
*   **Database**: MongoDB
*   **Chatbot**: Dialogflow (embedded via Dialogflow Messenger)

## How to Run

### Backend

You have two backend options depending on your needs. The standard root one is lightweight, while the one in `backend/` uses a machine learning recommendation engine.

**Option 1: ML Backend (Recommended)**
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python app.py` 
*(Runs on `http://127.0.0.1:5000`)*

**Option 2: Simple Backend**
1. Make sure you are in the project root.
2. `pip install -r requirements.txt`
3. `python app.py`

### Frontend

1. `cd frontend`
2. `npm install`
3. `npm start`

This will start the local development server at `http://localhost:3000`.

### Chatbot

The chatbot is integrated directly via an HTML script tag. To see the test page:
1. `cd chatbot`
2. Just open `index.html` in your browser.