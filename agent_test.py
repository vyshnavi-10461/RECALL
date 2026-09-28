import os
from hindsight_client import Hindsight
from groq import Groq


# -----------------------------
# Configuration
# -----------------------------

hindsight = Hindsight(
    base_url="http://localhost:8888"
)

groq = Groq(
    api_key=os.environ["HINDSIGHT_API_LLM_API_KEY"]
)

BANK_ID = "recall-incidents"


# -----------------------------
# New production incident
# -----------------------------

new_incident = """
Service: Payment API

Severity: Critical

Error:
Database connection timeout

Symptoms:
Payment requests are failing intermittently.

The engineering team needs to identify
the likely root cause and determine
what resolution should be attempted.
"""


# -----------------------------
# 1. RECALL
# -----------------------------

results = hindsight.recall(
    bank_id=BANK_ID,
    query=new_incident
)


memories = []

for result in results.results[:5]:
    memories.append(result.text)


memory_text = "\n\n".join(memories)


print("\n===== RETRIEVED MEMORY =====\n")

print(memory_text)


# -----------------------------
# 2. REASON
# -----------------------------

prompt = f"""
You are RECALL, an AI incident response agent.

Your job is to analyze a new production incident
using historical incidents stored in long-term memory.

NEW INCIDENT:
{new_incident}

HISTORICAL INCIDENT MEMORIES:
{memory_text}

Analyze the incident and provide:

1. Likely Root Cause
2. Recommended Resolution
3. Why this resolution is recommended
4. Historical Evidence
5. Expected Recovery

Important:
Use the historical incidents as evidence.
Do not invent historical incidents.
If the evidence is uncertain, say so.
"""


response = groq.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": "You are a production incident response assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)


print("\n===== RECALL AI ANALYSIS =====\n")

print(response.choices[0].message.content)