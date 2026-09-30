import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

templates = Jinja2Templates(directory="templates")

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/generate")
def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    if client:
        prompt = f"""
Create a safe 7-day beginner-friendly fitness plan.

User:
Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Workout intensity: {intensity}

Give:
1. Day-by-day workout plan
2. Simple nutrition tips
3. Recovery tips

Keep the response clear and practical.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        plan = response.text
    else:
        plan = "Gemini API key is not configured yet."

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "name": name,
            "plan": plan
        }
    )


@app.get("/users")
def users(request: Request):
    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "users": []
        }
    )


@app.get("/health")
def health():
    return {"status": "FitBuddy is running"}
