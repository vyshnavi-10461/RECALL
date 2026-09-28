from hindsight_client import Hindsight

client = Hindsight(
    base_url="http://localhost:8888"
)

BANK_ID = "recall-incidents"

new_incident = """
A new incident has occurred.

Service: Payment API

Error:
Database connection timeout

Symptoms:
Payment requests are failing intermittently.

The engineering team wants to know whether
similar incidents happened before and what
solutions worked previously.
"""

results = client.recall(
    bank_id=BANK_ID,
    query=new_incident
)

print("\n===== RECALL RESULTS =====\n")

for result in results.results:
    print("Memory:")
    print(result.text)
    print("\n-------------------------\n")