from langsmith import Client
from evaluation_dataset import evaluation_data
from dotenv import load_dotenv

load_dotenv()

def main():
    client = Client()

    # Programmatically create a dataset in LangSmith
    dataset = client.create_dataset(
    dataset_name="dispatch-agent-evaluation-v1",
    description=(
        "Evaluation dataset for trucking LangGraph dispatch agent. "
        "Tests driver availability, load status, tool selection, "
        "tool arguments, and equipment compatibility using dummy data."
    )
)

    # Create examples
    examples = evaluation_data
    # Add examples to the dataset
    client.create_examples(dataset_id=dataset.id, examples=examples)
    print("Created dataset:", dataset.name)

if __name__ == "__main__":
    main()