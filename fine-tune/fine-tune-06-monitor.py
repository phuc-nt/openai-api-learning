from pprint import pprint

from openai import OpenAI
client = OpenAI()

# List 10 fine-tuning jobs
job_list = client.fine_tuning.jobs.list(limit=10)
pprint(vars(job_list))

# Retrieve the state of a fine-tune
# job_state = client.fine_tuning.jobs.retrieve("ftjob-bc6OqA3jcMTeR0OOVtUk9Hoq")
# pprint(vars(job_state))

# # Cancel a job
# client.fine_tuning.jobs.cancel("ftjob-abc123")

# # List up to 10 events from a fine-tuning job
# client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-abc123", limit=10)

# # Delete a fine-tuned model (must be an owner of the org the model was created in)
# client.models.delete("ft:gpt-3.5-turbo:acemeco:suffix:abc123")