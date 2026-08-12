from datetime import timedelta
from temporalio import workflow

# In Temporal, workflows execute activities, which contain the actual side-effects.
# Here is the workflow declaration:
@workflow.defn
class CustomerOnboardingWorkflow:
    @workflow.run
    async def run(self, user_id: str) -> str:
        # Executes an agent activity reliably. If the system crashes mid-execution,
        # Temporal remembers that the activity was running and resumes it.
        parsed_doc = await workflow.execute_activity(
            "run_doc_parser_agent",
            user_id,
            schedule_to_close_timeout=timedelta(minutes=5)
        )
        return f"Completed onboarding for {user_id}"

if __name__ == "__main__":
    print("[Temporal Setup] Declared CustomerOnboardingWorkflow.")
    print("To run this successfully, ensure you have temporal SDK installed:")
    print("  pip install temporalio")
    print("And run a Temporal local server along with a registered Worker to process activities.")
