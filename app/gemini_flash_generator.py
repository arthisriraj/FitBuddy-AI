from app.config import DEMO_MODE, GOOGLE_API_KEY, GEMINI_FLASH_MODEL

from google import genai


def _get_client():

    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured. "
            "Add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=GOOGLE_API_KEY)


def _demo_tip(goal):

    tips = {
        "weight loss":
            "Prioritize protein and high-fiber foods, drink enough water, "
            "and avoid relying on extreme calorie restriction.",

        "muscle gain":
            "Include a protein source in each main meal, such as eggs, "
            "fish, chicken, beans, paneer, or Greek yogurt, and support "
            "training with adequate sleep.",

        "general wellness":
            "Build balanced meals around vegetables or fruit, a protein "
            "source, whole grains or other quality carbohydrates, and "
            "adequate hydration.",

        "flexibility":
            "Stay hydrated and include protein-rich foods plus fruits "
            "and vegetables that support balanced recovery.",

        "endurance":
            "Eat balanced meals containing carbohydrates and protein, "
            "stay hydrated, and give your body enough recovery time."
    }

    return tips.get(
        goal.lower().strip(),
        "Choose balanced meals with protein, vegetables or fruit, "
        "quality carbohydrates, and adequate hydration."
    )


def generate_nutrition_tip_with_flash(goal):

    if DEMO_MODE:
        return _demo_tip(goal)

    client = _get_client()

    prompt = f"""
Give one concise and practical nutrition or recovery tip
for a FitBuddy user whose fitness goal is:

{goal}

Requirements:

- Keep it to 3–5 sentences.
- Make it practical.
- Avoid extreme dieting advice.
- Do not make medical claims.
"""

    response = client.models.generate_content(
        model=GEMINI_FLASH_MODEL,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty nutrition tip."
        )

    return response.text.strip()