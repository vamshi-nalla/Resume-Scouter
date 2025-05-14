import yaml

def load_prompts(path="prompts.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
