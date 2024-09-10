import wandb

# prerequisites:
# login to wandb using `wandb login` command in the terminal
# create a project in wandb called "snippets"

# Start a W&B Run with wandb.init
run = wandb.init(
    project="snippets2", notes="description", tags=["tag1", "tag2"]
)

# Save model inputs and hyperparameters in a wandb.config object
config = run.config
config.learning_rate = 0.01
config.foo = "bar"

# Model training code here ...

# Log metrics over time to visualize performance with wandb.log
for i in range(10):
    run.log({"loss": 1 / (i + 1)})

# Mark the run as finished, and finish uploading all data
run.finish()
