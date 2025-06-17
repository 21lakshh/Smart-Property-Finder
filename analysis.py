import base64
import requests
import io
from dotenv import load_dotenv
import os
import logging
import json
import pandas as pd
from models import Property

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ API KEY is not set in the .env file")

def analyze_property(prop: Property) -> str:
    query = (
        f"Analyze the property with available details: "
        f"Title: {prop.title}; Price: {prop.price}; Area: {prop.area}; "
        f"Bedrooms: {prop.bedrooms}; Bathrooms: {prop.bathrooms}; "
        f"Type: {prop.property_type}; Category: {prop.property_category}; City: {prop.city}. "
        f"If some values are missing, still try to provide a meaningful analysis based on what's present. "
        f"\nRespond with:\n1. Investment Potential\n2. Location Insights\n3. Buyer Advice"
    )
    messages = [
        {
            "role": "user",
            "content": query
        }
    ]

    # API Request
    response = requests.post(
        GROQ_API_URL,
        json={"model": "meta-llama/llama-4-maverick-17b-128e-instruct", "messages": messages, "max_tokens": 4000},
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        timeout=30
    )

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]

    else:
        return f"API Error: {response.status_code} - {response.text}"
