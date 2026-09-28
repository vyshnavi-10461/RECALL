from hindsight_client import Hindsight

client = Hindsight(
    base_url="http://localhost:8888"
)

BANK_ID = "recall-incidents"


# The engineer applied the recommended fix
# and confirmed that it worked.

feedback = """
Incident: NEW-001

Service: Payment API

Problem:
Database connection timeouts during peak traffic.

Recommended Resolution:
Increase the database connection pool.

Engineer Action:
Connection pool was increased from 50 to 100.

Outcome:
SUCCESSFUL

Recovery Time:
5 minutes.

Learning:
Increasing the connection pool successfully resolved
the Payment API database timeout incident.
"""


response = client.retain(
    bank_id=BANK_ID,
    content=feedback
)

print("===== LEARNING STORED =====")
print(response)