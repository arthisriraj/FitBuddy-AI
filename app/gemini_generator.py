from app.config import DEMO_MODE, GOOGLE_API_KEY, GEMINI_PRO_MODEL

from google import genai


def _get_client():
    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured. "
            "Add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=GOOGLE_API_KEY)


def _demo_plan(username, age, weight, goal, intensity):
    return f"""FITBUDDY – PERSONALIZED 7-DAY WORKOUT PLAN

User: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

DAY 1 – Full Body Foundation

Warm-up:
5–10 minutes brisk walking and mobility.

Main Workout:
- Bodyweight squats: 3 sets × 12 reps
- Incline push-ups: 3 sets × 10 reps
- Glute bridges: 3 sets × 12 reps
- Plank: 3 sets × 20–30 seconds

Rest:
60–90 seconds between sets.

Cooldown:
5 minutes gentle stretching.


DAY 2 – Cardio + Core

Warm-up:
5–10 minutes.

Main Workout:
- Brisk walk/jog: 20–30 minutes
- Dead bug: 3 × 10 each side
- Bird dog: 3 × 10 each side
- Plank: 3 × 20–30 seconds

Cooldown:
5 minutes.


DAY 3 – Recovery / Mobility

- Easy walk: 15–20 minutes
- Full-body mobility: 15 minutes
- Gentle stretching
- Hydration and recovery focus


DAY 4 – Lower Body

Warm-up:
5–10 minutes.

Main Workout:
- Squats: 3 × 12
- Reverse lunges: 3 × 10 each leg
- Glute bridges: 3 × 15
- Calf raises: 3 × 15

Cooldown:
5–10 minutes.


DAY 5 – Upper Body + Core

Warm-up:
5–10 minutes.

Main Workout:
- Incline push-ups: 3 × 10
- Backpack/band rows: 3 × 12
- Shoulder raises: 3 × 12
- Dead bug: 3 × 10 each side

Cooldown:
5 minutes.


DAY 6 – Cardio + Flexibility

- Moderate cardio: 25–35 minutes
- Hip mobility: 5 minutes
- Hamstring/calf stretches: 5 minutes


DAY 7 – Rest / Active Recovery

- Easy walk: 15–20 minutes if comfortable
- Gentle stretching
- Review how your body feels before the next week


SAFETY NOTE:
This is general wellness guidance and not medical advice.
Stop if you experience pain, dizziness, or unusual symptoms.
"""


def generate_workout_gemini(username, age, weight, goal, intensity):

    if DEMO_MODE:
        return _demo_plan(
            username,
            age,
            weight,
            goal,
            intensity
        )

    client = _get_client()

    prompt = f"""
You are FitBuddy, an AI fitness-plan assistant.

Create a personalized 7-day workout plan for:

Name: {username}
Age: {age}
Weight: {weight} kg
Fitness goal: {goal}
Preferred intensity: {intensity}

Requirements:

1. Create exactly Day 1 through Day 7.
2. Give every day a clear workout focus.
3. Include a 5–10 minute warm-up where appropriate.
4. Include exercises with sets/repetitions or duration.
5. Include suggested rest periods.
6. Include cooldown or recovery guidance.
7. Include at least one rest/recovery day.
8. Make the plan practical for the selected goal.
9. Match the requested intensity.
10. Do not provide medical diagnosis or treatment.
11. Finish with a short safety note.

Return the plan as clear plain text.
Do not use a table.
"""

    response = client.models.generate_content(
        model=GEMINI_PRO_MODEL,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty workout plan."
        )

    return response.text.strip()