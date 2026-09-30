# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI web application based on the supplied project specification.

## Features

- Personalized 7-day workout plan generation
- Google Gemini integration
- Gemini Pro-style model for workout generation and feedback updates
- Gemini Flash-style model for concise nutrition/recovery tips
- SQLite + SQLAlchemy persistence
- Jinja2 HTML frontend
- Feedback-based plan revision
- Admin/coach dashboard
- API endpoints and FastAPI Swagger documentation
- Optional DEMO_MODE for testing the UI without a Gemini API key

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   ├── routes.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── result.html
│   │   ├── all_users.html
│   │   └── error.html
│   └── static/
│       └── css/
│           └── style.css
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Important

This application provides general wellness guidance. It is not a medical diagnosis or treatment system.

## Windows quick start

```bat
cd path\to\FitBuddy
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add your Gemini API key.

Then:

```bat
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/view-all-users
- http://127.0.0.1:8000/health

## Demo mode

For a no-key UI/database test:

```text
DEMO_MODE=true
```

in `.env`, then run the server. This uses local sample generation instead of Gemini.

Set it back to `false` for real Gemini calls.

## API

### POST /api/generate

JSON:

```json
{
  "username": "Arthi",
  "user_id": "FB001",
  "age": 21,
  "weight": 60,
  "goal": "weight loss",
  "intensity": "medium"
}
```

### POST /api/feedback

JSON:

```json
{
  "user_id": "FB001",
  "feedback": "Add more cardio and include one extra rest period."
}
```

### GET /api/users

Returns all stored users and plans.

### GET /api/users/{user_id}

Returns one stored user.

## Testing checklist

1. Open the home page.
2. Enter a unique User ID.
3. Generate a plan.
4. Confirm the result page shows the profile, 7-day plan and nutrition tip.
5. Submit feedback.
6. Confirm the updated plan appears.
7. Open `/view-all-users`.
8. Confirm the original and updated plans are stored.
9. Open `/docs` and test the JSON API.
10. Open `/health` and confirm `{"status":"ok","service":"FitBuddy"}`.

## Notes about Gemini model names

The supplied specification explicitly names Gemini 1.5 Pro and Gemini Flash. Model availability can change on Google's side. The names are therefore kept in `.env` so they can be changed without editing application code.
