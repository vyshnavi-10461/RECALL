# RECALL — AI Incident Response Agent

> **Every incident teaches the next one.**

RECALL is an AI-powered incident response agent that uses persistent memory to help engineers diagnose production incidents.

Instead of treating every incident as a completely new problem, RECALL remembers previous incidents, their root causes, resolutions, and outcomes. It retrieves relevant historical experiences and uses them as evidence when analyzing a new incident.

The core learning loop is:

**RETAIN → RECALL → REASON → RESOLVE → LEARN**

---

## Problem

Production incidents often repeat similar patterns.

An engineer may have previously solved a database timeout, queue failure, API error, or service outage, but that knowledge can be difficult to retrieve when a new incident occurs.

Traditional AI assistants can analyze the current incident, but without persistent memory they may not remember how similar incidents were handled previously.

This creates a gap between:

- What happened before
- What worked before
- What is happening now

RECALL addresses this gap by giving the AI agent long-term incident memory.

---

## Solution

RECALL combines an AI reasoning layer with **Hindsight persistent memory**.

For every new incident, RECALL:

1. Receives the current incident details.
2. Searches Hindsight for relevant historical incidents.
3. Retrieves previous root causes, resolutions, and outcomes.
4. Provides the historical evidence to the AI model.
5. Generates a likely root cause.
6. Recommends a practical resolution.
7. Shows the historical incidents supporting the recommendation.
8. Allows the engineer to provide the actual outcome.
9. Stores the outcome back into Hindsight.
10. Uses that new experience for future incidents.

This creates a continuous learning cycle rather than a one-time AI response.

---

## How RECALL Works

```text
                 NEW INCIDENT
                      │
                      ▼
              ┌───────────────┐
              │     RECALL    │
              │    Incident   │
              │    Analysis   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    HINDSIGHT  │
              │    RECALL     │
              │               │
              │ Historical    │
              │ Incidents     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   AI REASONING│
              │               │
              │ Root Cause    │
              │ Resolution    │
              │ Evidence      │
              └───────┬───────┘
                      │
                      ▼
                 RESOLUTION
                      │
                      ▼
             ENGINEER FEEDBACK
                      │
                      ▼
              ┌───────────────┐
              │    HINDSIGHT  │
              │    RETAIN     │
              │               │
              │ Outcome +     │
              │ Recovery Time │
              └───────┬───────┘
                      │
                      ▼
                FUTURE INCIDENT
## Core Learning Loop

### 1. RETAIN

Incident information and resolution outcomes are stored in Hindsight.

### 2. RECALL

When a new incident occurs, RECALL searches historical memory for relevant experiences.

### 3. REASON

The AI analyzes the current incident using the retrieved historical evidence.

### 4. RESOLVE

RECALL recommends a resolution based on previous incidents and their outcomes.

### 5. LEARN

After the engineer reports whether the resolution worked, the outcome is stored back into Hindsight.

The next incident can then benefit from this newly learned experience.
Architecture
┌──────────────────────┐
│      React UI        │
│                      │
│ Incident Input       │
│ AI Analysis          │
│ Memory Timeline      │
│ Engineer Feedback    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     FastAPI Backend  │
│                      │
│ Incident Analysis    │
│ Feedback Handling    │
│ Hindsight Client     │
└───────┬─────────┬────┘
        │         │
        ▼         ▼
┌────────────┐ ┌─────────────┐
│ Hindsight  │ │    Groq     │
│            │ │             │
│ Long-term  │ │ AI Reasoning│
│ Memory     │ │             │
└────────────┘ └─────────────┘
Components

Frontend

React
Vite
CSS

Backend

Python
FastAPI
Hindsight Client

AI

Groq
openai/gpt-oss-20b

Memory

Hindsight        
Key Features
Historical Incident Recall

RECALL retrieves similar incidents from Hindsight instead of relying only on the current incident.

AI Root Cause Analysis

The AI identifies the most likely root cause using the current incident and historical evidence.

Evidence-Based Recommendations

Recommendations are connected to previously observed incidents.

Memory Timeline

The UI displays the historical memories retrieved for the current incident.

Engineer Feedback

Engineers can report whether the recommended resolution worked or failed.

Continuous Learning

Resolution outcomes and recovery times are retained in Hindsight so future incidents can benefit from them.
Hindsight Memory

Hindsight is the persistent memory layer of RECALL.

It allows the system to retain information beyond a single AI interaction.

RECALL uses Hindsight for two important operations:

Recall historical experience
New Incident
     ↓
Search Hindsight
     ↓
Relevant historical incidents
     ↓
AI reasoning
Retain new learning
Incident Resolution
       ↓
Engineer Feedback
       ↓
Outcome + Recovery Time
       ↓
Hindsight
       ↓
Future incidents

This makes Hindsight a central part of the learning loop rather than simply an external database.
Sample Historical Incidents

The project includes synthetic incident data covering multiple production scenarios, including:

Payment API database connection timeouts
Authentication service timeouts
Order service HTTP 500 errors
Notification delays
Search service 503 errors
User profile API performance issues
Payment gateway latency
Inventory update delays
Database migration locking

These incidents provide the historical experience used during the demonstration.
Project Structure
RECALL/
│
├── backend/
│   ├── main.py
│   ├── agent_test.py
│   ├── recall_test.py
│   ├── feedback_test.py
│   ├── test_hindsight.py
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── incidents.json
├── README.md
└── .gitignore
How to Run
Prerequisites

Make sure the following are installed:

Python
Node.js
Docker
Git

You also need:

A running Hindsight instance
A Groq API key
1. Clone the repository
git clone https://github.com/vyshnavi-10461/RECALL.git
cd RECALL
2. Start Hindsight

Run the Hindsight service using Docker according to the Hindsight setup used for the project.

The local Hindsight API should be available at:

http://localhost:8888

The Hindsight Swagger documentation can be accessed at:

http://localhost:8888/docs
3. Set up the backend

Navigate to the backend:

cd backend

Create and activate a Python virtual environment:

Windows
python -m venv venv
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Configure the required environment variables in .env.

Do not commit API keys or secrets to GitHub.
4. Start the FastAPI backend

From the backend directory:

uvicorn main:app --reload

The API will be available at:

http://127.0.0.1:8000

FastAPI Swagger documentation:

http://127.0.0.1:8000/docs
5. Start the frontend

Open another terminal and navigate to:

cd frontend

Install dependencies:

npm install

Start the React application:

npm run dev

The frontend will run locally through Vite
Demo Flow

The intended demonstration follows this sequence:

Step 1 — Create an incident

Enter a production incident such as:

Service: Payment API
Severity: Critical
Problem: Database connection timeout during peak traffic
Step 2 — Analyze

RECALL searches Hindsight for historical incidents.

Step 3 — Recall

The interface displays relevant historical memories.

Step 4 — Reason

The AI analyzes the incident using the retrieved historical evidence.

Step 5 — Recommend

RECALL provides:

Likely root cause
Recommended resolution
Reason for the recommendation
Historical evidence
Expected recovery time when supported by historical data
Step 6 — Resolve

The engineer applies the recommended action.

Step 7 — Provide feedback

The engineer records whether the resolution worked and provides the recovery time.

Step 8 — Learn

The outcome is retained in Hindsight.

Step 9 — Recall again

A future similar incident can retrieve the newly stored learning.

This demonstrates the complete:

RETAIN → RECALL → REASON → RESOLVE → LEARN

cycle.
Why Persistent Memory Matters

Without persistent memory:

Incident → AI Analysis → Response

With RECALL:

Incident
   ↓
Historical Experience
   ↓
AI Analysis
   ↓
Resolution
   ↓
Outcome
   ↓
Persistent Memory
   ↓
Better Context for Future Incidents

The system therefore treats previous incidents as reusable operational knowledge.
Future Scope

Potential future extensions include:

Integration with real monitoring systems
Automatic incident ingestion
Slack or Microsoft Teams integration
Integration with observability platforms
Automated runbook execution
Incident severity prediction
More advanced incident similarity detection
Human approval workflows for automated remediation
Tech Stack
Layer	Technology
Frontend	React + Vite
Backend	Python + FastAPI
AI Model	Groq / GPT-OSS
Memory	Hindsight
Containerization	Docker
Data	Synthetic Production Incidents
Project Status

RECALL currently demonstrates a complete incident-response learning loop:

Incident → Recall → AI Analysis → Recommendation → Engineer Feedback → Retained Learning → Future Recall

The project uses synthetic incident data to demonstrate how persistent memory can improve an AI-powered incident response workflow.
Contributors

Built as a collaborative project focused on applying persistent AI memory to production incident response.


### After pasting

Save it:

**`Ctrl + S`**

Then **don't push yet**.

Next we'll quickly check the README visually in VS Code and make sure there are **no wrong commands, secrets,         