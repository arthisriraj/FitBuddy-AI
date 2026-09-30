from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import (
    init_db,
    save_user,
    get_user,
    get_original_plan,
    update_plan,
    get_all_users,
    delete_user,
)
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app.schemas import UserInput, FeedbackRequest

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
router = APIRouter()

init_db()


def _error_context(request, message):
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"error_message": message},
        status_code=400,
    )


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    try:
        user = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
        existing = get_user(user.user_id)
        if existing:
            return _error_context(
                request,
                f"User ID '{user.user_id}' already exists. Use a different User ID or open the existing result from the admin page.",
            )

        workout_plan = generate_workout_gemini(
            user.username, user.age, user.weight, user.goal, user.intensity
        )
        nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

        save_user(
            user.user_id,
            user.username,
            user.age,
            user.weight,
            user.goal,
            user.intensity,
            workout_plan,
            nutrition_tip,
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user.model_dump(),
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "updated_plan": None,
                "message": "Your personalized plan has been generated successfully.",
            },
        )
    except Exception as exc:
        return _error_context(request, str(exc))


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
):
    try:
        data = FeedbackRequest(user_id=user_id, feedback=feedback)
        user = get_user(data.user_id)
        if not user:
            return _error_context(request, f"No user found for User ID '{data.user_id}'.")

        original_plan = get_original_plan(data.user_id)
        revised_plan = update_workout_plan(original_plan, data.feedback)
        updated = update_plan(data.user_id, revised_plan, data.feedback)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": {
                    "username": user.username,
                    "user_id": user.user_id,
                    "age": user.age,
                    "weight": user.weight,
                    "goal": user.goal,
                    "intensity": user.intensity,
                },
                "workout_plan": user.original_plan,
                "nutrition_tip": user.nutrition_tip,
                "updated_plan": updated.updated_plan if updated else revised_plan,
                "message": "Your feedback was processed and the workout plan was updated.",
            },
        )
    except Exception as exc:
        return _error_context(request, str(exc))


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    users = get_all_users()
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": users},
    )


@router.post("/delete-user")
def remove_user(user_id: str = Form(...)):
    delete_user(user_id)
    return RedirectResponse(url="/view-all-users", status_code=303)


# JSON API endpoints for testing through /docs or external clients.

@router.post("/api/generate")
def api_generate(user: UserInput):
    if get_user(user.user_id):
        return JSONResponse(
            status_code=409,
            content={"detail": f"User ID '{user.user_id}' already exists."},
        )

    workout_plan = generate_workout_gemini(
        user.username, user.age, user.weight, user.goal, user.intensity
    )
    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)
    saved = save_user(
        user.user_id,
        user.username,
        user.age,
        user.weight,
        user.goal,
        user.intensity,
        workout_plan,
        nutrition_tip,
    )
    return {
        "user_id": saved.user_id,
        "workout_plan": workout_plan,
        "nutrition_tip": nutrition_tip,
    }


@router.post("/api/feedback")
def api_feedback(data: FeedbackRequest):
    user = get_user(data.user_id)
    if not user:
        return JSONResponse(status_code=404, content={"detail": "User not found."})

    revised = update_workout_plan(user.original_plan, data.feedback)
    updated = update_plan(data.user_id, revised, data.feedback)
    return {
        "user_id": updated.user_id,
        "updated_plan": updated.updated_plan,
        "feedback": updated.feedback,
    }


@router.get("/api/users")
def api_users():
    users = get_all_users()
    return {
        "users": [
            {
                "id": u.id,
                "user_id": u.user_id,
                "username": u.username,
                "age": u.age,
                "weight": u.weight,
                "goal": u.goal,
                "intensity": u.intensity,
                "original_plan": u.original_plan,
                "updated_plan": u.updated_plan,
                "nutrition_tip": u.nutrition_tip,
                "feedback": u.feedback,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ]
    }


@router.get("/api/users/{user_id}")
def api_user(user_id: str):
    user = get_user(user_id)
    if not user:
        return JSONResponse(status_code=404, content={"detail": "User not found."})
    return {
        "id": user.id,
        "user_id": user.user_id,
        "username": user.username,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
        "original_plan": user.original_plan,
        "updated_plan": user.updated_plan,
        "nutrition_tip": user.nutrition_tip,
        "feedback": user.feedback,
    }
