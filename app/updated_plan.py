from app.config import DEMO_MODE, GOOGLE_API_KEY, GEMINI_PRO_MODEL

from google import genai


def _get_client():

    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured. "
            "Add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=GOOGLE_API_KEY)


def _demo_update(original_plan, feedback):

    return f"""UPDATED FITBUDDY PLAN

User feedback:

"{feedback}"

The original 7-day plan has been revised according to the requested
changes.

{original_plan}

ADAPTATION NOTES:

- Apply changes gradually.
- Keep at least one recovery-oriented day.
- Adjust exercise duration, sets or rest periods according to comfort.
- Stop if an exercise causes pain or unusual symptoms.
"""


def update_workout_plan(original_plan, feedback):

    if DEMO_MODE:
        return _demo_update(
            original_plan,
            feedback
        )

    client = _get_client()

    prompt = f"""
You are FitBuddy.

Revise the following existing 7-day workout plan based on
the user's feedback.

ORIGINAL PLAN:

{original_plan}


USER FEEDBACK:

{feedback}


Requirements:

1. Return a complete revised 7-day plan.
2. Do not return only the changes.
3. Preserve useful parts of the original plan.
4. Apply the user's feedback clearly.
5. Keep warm-up guidance.
6. Keep workout details.
7. Keep cooldown/recovery guidance.
8. Keep at least one rest/recovery day.
9. Do not provide medical diagnosis or treatment.
10. Finish with a short safety note.

Return clear plain text.
Do not use a table.
"""

    response = client.models.generate_content(
        model=GEMINI_PRO_MODEL,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty updated plan."
        )

    return response.text.strip()