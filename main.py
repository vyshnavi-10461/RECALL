from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hindsight_client import Hindsight
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="RECALL API",
    description="AI Incident Response Agent with Hindsight memory"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Connections
# -----------------------------

hindsight = Hindsight(
    base_url="http://localhost:8888"
)

groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

BANK_ID = "recall-incidents"


# -----------------------------
# Incident input
# -----------------------------

class Incident(BaseModel):
    service: str
    severity: str
    problem: str
class Feedback(BaseModel):
    service: str
    problem: str
    recommended_resolution: str
    engineer_action: str
    outcome: str
    recovery_time_minutes: int

# -----------------------------
# Basic endpoints
# -----------------------------

@app.get("/")
def home():
    return {"message": "RECALL API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# -----------------------------
# Analyze incident
# -----------------------------

@app.post("/incidents/analyze")
async def analyze_incident(incident: Incident):

    # 1. Build search query
    query = (
        f"Service: {incident.service}. "
        f"Severity: {incident.severity}. "
        f"Problem: {incident.problem}"
    )

    # 2. Recall historical incidents from Hindsight
    response = await hindsight.arecall(
        bank_id=BANK_ID,
        query=query,
        max_tokens=2000,
        budget="mid"
    )

    memories = []

    for result in response.results[:5]:
        memories.append(result.text)

    # 3. Prepare historical evidence for Groq
    historical_context = "\n\n".join(
        f"MEMORY {i + 1}:\n{memory}"
        for i, memory in enumerate(memories)
    )

    # 4. Ask Groq to reason about the incident
    prompt = f"""
You are an AI incident response assistant.

Analyze the current production incident using ONLY the
historical evidence provided below.

CURRENT INCIDENT:
Service: {incident.service}
Severity: {incident.severity}
Problem: {incident.problem}

HISTORICAL EVIDENCE:
{historical_context}

Rules:
- Identify the most likely root cause.
- Recommend a practical resolution.
- Explain why the recommendation is supported by historical incidents.
- Mention the incident IDs that support the recommendation.
- Give an estimated recovery time ONLY if historical evidence supports it.
- NEVER invent historical actions or outcomes.
- If the evidence is insufficient, clearly say so.

Return your answer in this format:

LIKELY ROOT CAUSE:
<root cause>

RECOMMENDED RESOLUTION:
<recommended resolution>

WHY THIS RECOMMENDATION:
<explanation>

HISTORICAL EVIDENCE:
<incident IDs and relevant evidence>

EXPECTED RECOVERY:
<time or "Insufficient historical evidence">
"""

    # 5. Send incident + memories to Groq
    try:
        completion = groq.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are RECALL, an AI incident response assistant.

Use the retrieved Hindsight memories as historical evidence.

Your job:
1. Identify the likely root cause.
2. Recommend a practical resolution.
3. Explain why the recommendation is supported by historical incidents.
4. Mention relevant incident IDs.
5. Estimate recovery time only when historical evidence supports it.

IMPORTANT:
- Never invent historical actions, outcomes, or recovery times.
- Only claim something happened if it is explicitly present in the retrieved memories.
- If the evidence is insufficient, say so clearly.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

    except Exception as e:
        error_text = str(e)

        if "429" in error_text or "rate_limit" in error_text.lower():
            return {
                "error": "AI rate limit reached",
                "message": "Groq has temporarily reached its token limit. Hindsight memories are still available."
            }

        raise

    # 6. Extract AI analysis
    analysis = completion.choices[0].message.content

    # 7. Return complete result
    return {
        "incident": {
            "service": incident.service,
            "severity": incident.severity,
            "problem": incident.problem
        },
        "memories_found": len(memories),
        "historical_memories": memories,
        "ai_analysis": analysis
    }
# -----------------------------
# Incident feedback / learning
# -----------------------------
@app.post("/incidents/feedback")
async def incident_feedback(feedback: Feedback):

    # Store the important learning from the incident.
    learning = f"""
Incident outcome learning:

Service: {feedback.service}
Problem: {feedback.problem}

Recommended Resolution:
{feedback.recommended_resolution[:500]}

Engineer Action:
{feedback.engineer_action}

Outcome:
{feedback.outcome}

Recovery Time:
{feedback.recovery_time_minutes} minutes
"""

    try:
        # Try to save the learning into Hindsight
        result = await hindsight.aretain(
            bank_id=BANK_ID,
            content=learning,
            context="incident resolution feedback"
        )

        return {
            "message": "Incident outcome learned successfully",
            "outcome": feedback.outcome,
            "recovery_time_minutes": feedback.recovery_time_minutes,
            "hindsight_saved": True
        }

    except Exception as e:
        error_text = str(e)

        # Groq quota exhausted inside Hindsight
        if "ProviderRateLimitResetError" in error_text or "rate_limit" in error_text.lower():
            return {
                "message": "Feedback recorded, but Hindsight learning is temporarily delayed because the AI provider quota is exhausted.",
                "outcome": feedback.outcome,
                "recovery_time_minutes": feedback.recovery_time_minutes,
                "hindsight_saved": False,
                "learning_pending": True
            }

        # Any other unexpected error should still be visible
        raise