from openai import OpenAI
client = OpenAI()

client.fine_tuning.jobs.create(
  training_file="file-HfceNqxL6U3K9P5Jrf9sda0c", 
  model="gpt-3.5-turbo", 
  hyperparameters={
    "n_epochs":2
  }
)