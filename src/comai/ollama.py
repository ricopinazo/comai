import ollama


def get_ollama_model_names() -> list[str]:
    models = ollama.list()["models"]
    model_names = [model["name"] for model in models]
    cleaned_model_names = [name.replace(":latest", "") for name in model_names]
    return cleaned_model_names
