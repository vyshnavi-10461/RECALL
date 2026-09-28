from hindsight_client import Hindsight

# Connect to our local Hindsight server
client = Hindsight(
    base_url="http://localhost:8888"
)

BANK_ID = "recall-incidents"

# -----------------------------
# RETAIN - Store an old incident
# -----------------------------

incident = """
Incident ID: INC-001

Service: Payment API

Problem:
The Payment API started returning database connection timeout errors.

Root Cause:
The database connection pool was exhausted because traffic suddenly increased.

Resolution:
The engineering team increased the database connection pool size from 50 to 100.

Outcome:
The fix worked successfully.

Recovery Time:
4 minutes.
"""

response = client.retain(
    bank_id=BANK_ID,
    content=incident
)

print("RETAIN completed!")
print(response)

# -----------------------------
# RECALL - Search the memory
# -----------------------------

results = client.recall(
    bank_id=BANK_ID,
    query="Have we seen a database connection pool exhaustion issue before?"
)

print("\nRECALL results:")
print(results)