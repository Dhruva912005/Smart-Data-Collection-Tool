import requests
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Skipping .env loading and utilizing fallback tokens natively.")

API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-small"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

def generate_keywords(topic):
    prompt = f"Give 20 keywords related to {topic}, comma separated"

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        
        if response.status_code != 200:
            return fallback_keywords(topic)

        result = response.json()
        if isinstance(result, dict) and "error" in result:
            return fallback_keywords(topic)

        text = result[0]["generated_text"]
        keywords = [k.strip().lower() for k in text.split(",") if k.strip()]
        return keywords[:20]

    except Exception:
        return fallback_keywords(topic)

def fallback_keywords(topic):
    """
    Fallback keyword generation function if API fails.
    """
    base = topic.lower()

    return [
        base,
        f"{base} news",
        f"{base} market",
        f"{base} trends",
        f"{base} analysis",
        f"{base} demand",
        f"{base} supply",
        f"{base} investment",
        f"{base} price",
        f"{base} forecast"
    ]