from openai import OpenAI
import os


def get_openai_model_names() -> list[str]:
    # FIXME: this piece of code is duplicated
    default_key = os.environ.get("OPENAI_API_KEY")
    comai_key = os.environ.get("COMAI_OPENAI_API_KEY")
    api_key = comai_key if comai_key is not None else default_key

    client = OpenAI(api_key=api_key)
    return [model.id for model in client.models.list() if model.id.startswith("gpt-")]
