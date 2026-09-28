import json
import time
from hindsight_client import Hindsight

client = Hindsight(
    base_url="http://localhost:8888"
)

BANK_ID = "recall-incidents"

with open("incidents.json", "r") as file:
    incidents = json.load(file)

for incident in incidents[2:]:

    content = f"""
Incident ID: {incident["incident_id"]}

Service: {incident["service"]}

Severity: {incident["severity"]}

Error: {incident["error"]}

Symptoms:
{incident["symptoms"]}

Root Cause:
{incident["root_cause"]}

Resolution:
{incident["resolution"]}

Outcome:
{incident["outcome"]}

Recovery Time:
{incident["recovery_time_minutes"]} minutes.
"""

    while True:
        try:
            response = client.retain(
                bank_id=BANK_ID,
                content=content
            )

            print(
                f'{incident["incident_id"]} stored successfully'
            )

            # Give Groq some time before processing
            # the next incident.
            time.sleep(30)

            break

        except Exception as e:

            error_text = str(e)

            if "429" in error_text or "quota exhausted" in error_text:
                print(
                    f'{incident["incident_id"]}: Groq rate limit reached.'
                )

                print("Waiting 40 seconds before retrying...")
                time.sleep(40)

            else:
                print(
                    f'{incident["incident_id"]} failed: {e}'
                )
                break

print("\nFinished loading incidents!")