from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- App setup ---
app = FastAPI(title="Text Processor API")

# Allow frontend to access (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request model ---
class TextInput(BaseModel):
    text: str

# --- Routes ---
@app.post("/process")
async def process_text(input_data: TextInput):
    user_text = input_data.text

    # Placeholder logic — replace with AI or processing logic
    processed_text = f"Received: {user_text}"

    # Send back to frontend
    return {"response": processed_text}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Backend API", version="1.0")

# ===== CORS CONFIG =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== MODELS =====
class AnswerRequest(BaseModel):
    question: str
    answer: str

class LoginRequest(BaseModel):
    username: str
    password: str

class EmailConfig(BaseModel):
    email: str

# ===== BASIC ROUTES =====
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ===== CHAT-LIKE ENDPOINTS =====
@app.post("/answer")
async def handle_answer(payload: AnswerRequest):
    """
    Simplified version of the chat flow:
    Receives one question and one answer at a time.
    """
    q = payload.question
    a = payload.answer

    # Placeholder logic
    print(f"Q: {q}\nA: {a}")

    # TODO: You can call your AI service here if needed
    processed = f"Answer received for: '{q}'"

    return {"question": q, "answer": a, "status": "saved", "result": processed}


@app.get("/question")
async def get_question():
    return {
        "question_id": "q1",
        "question": "What is your business name?",
        "type": "freeform"
    }

# ===== FILE UPLOAD =====
@app.post("/uploads")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles file uploads.
    """
    contents = await file.read()
    # Save to local folder (optional)
    with open(f"./uploads/{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename, "size": len(contents), "status": "uploaded"}

# ===== AUTH =====
@app.post("/login")
async def login_user(payload: LoginRequest):
    """
    Dummy admin login - replace with real JWT later.
    """
    if payload.username == "admin" and payload.password == "password":
        return {"token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# ===== CONFIG =====
@app.put("/config/email-recipient")
async def update_email(config: EmailConfig):
    """
    Updates the recipient email (dummy logic for now).
    """
    new_email = config.email
    print(f"Updated recipient email to: {new_email}")
    return {"status": "success", "email": new_email}

# ===== ANALYTICS =====
@app.get("/kpis")
async def get_kpis(start_time: Optional[str] = None, end_time: Optional[str] = None):
    """
    Placeholder for KPI dashboard data.
    """
    return {"start": start_time, "end": end_time, "total_submissions": 12, "resolved": 11}

