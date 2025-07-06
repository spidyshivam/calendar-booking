# LangChain Calendar Booking Agent

A conversational AI agent that books appointments on your Google Calendar using LangChain, Google Gemini, and FastAPI.

## Features

* **Conversational Interface:** Add events using natural language.
* **Stateful Memory:** Remembers conversation context per user session.
* **Reliable Tool-Calling:** Uses Google Gemini's native tool-calling feature to interact with the Google Calendar API.
* **FastAPI Backend:** Served by a high-performance FastAPI server.
* **Streamlit Frontend:** Simple and intuitive user interface built with Streamlit.

## Setup Instructions

### 1. Clone & Install

First, clone the repository and set up virtual environments for both frontend and backend.

```bash
# Clone the repo
git clone https://github.com/spidyshivam/calendar-booking
cd calendar-booking

# Set up backend
cd backend
python -m venv env
source env/bin/activate  # On macOS/Linux
# .\env\Scripts\activate  # On Windows
pip install -r requirements.txt
cd ..

# Set up frontend
cd frontend
python -m venv env
source env/bin/activate  # On macOS/Linux
# .\env\Scripts\activate  # On Windows
pip install -r requirements.txt
cd ..
```

### 2. Configure Google Cloud Credentials

You need two separate credentials from Google.

#### A. Google Calendar Service Account (`key.json`)

This lets the app control your calendar.

1. Go to the Google Cloud Console, create a project, and enable the Google Calendar API.
2. Navigate to **Credentials** -> **Create Credentials** -> **Service Account**.
3. After creating it, go to the service account's **Keys** tab, click **Add Key** -> **JSON**.
4. A file will be downloaded. Rename it to `key.json` and place it in the root directory.
5. Find your Calendar ID in your Google Calendar settings (often your email).
6. **Important:** Share your calendar with the service account's email address (found in its details page) and give it **"Make changes to events"** permissions.

#### B. Google AI API Key (Gemini)

This gives the agent access to the Gemini model.

1. Go to [Google AI Studio](https://makersuite.google.com/).
2. Click **Create API key** and copy the key.

### 3. Set Environment Variables

Create a file named `.env` in the **backend** folder and add your credentials:

```env
# Your Calendar ID from step 2A
CALENDAR_ID="your_calendar_id@group.calendar.google.com"

# Your API Key from step 2B
GEMINI_API_KEY="your_google_ai_api_key_here"
```

> Note: The `.gitignore` file is configured to prevent `key.json` and `.env` from being committed to your repository.

### 4. Running the Application

#### Run the FastAPI Backend

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`.

#### Run the Streamlit Frontend

```bash
cd frontend
streamlit run app.py
```

The frontend will be available at `http://localhost:8501`.

### Example API Usage (Optional)

You can interact with the backend directly using a tool like `curl`:

```bash
curl -X 'POST' \
  'http://localhost:8000/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "can you add a meeting for tomorrow at 4pm called Launch Planning?",
    "session_id": "user123"
  }'
```
