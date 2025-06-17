import httpx
import os 
from models import Property, PropertyInput
from typing import List
from firecrawl import AsyncFirecrawlApp, JsonConfig
import json
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
app = AsyncFirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

async def extract_property_details(url: str, prompt: str) -> List[Property]:

    json_cfg = JsonConfig(                     
        prompt=prompt
    )

    response = await app.scrape_url(
        url,
        formats=["json"],                      
        json_options=json_cfg                  
    )
    raw = response.json
    print(raw)
    if isinstance(raw, dict) and "properties" in raw:
        raw = raw["properties"]
   
    items = raw if isinstance(raw, list) else [raw]

    props = []
    for obj in items:
      
        if isinstance(obj, str):
            try:
                obj = json.loads(obj)         
            except json.JSONDecodeError:
                continue                       
        props.append(Property(
            title=obj.get("title", "N/A"),
            price=str(obj.get("price", "N/A")),
            area=str(obj.get("area", "N/A")),
            bedrooms=str(obj.get("bedrooms", "N/A")),
            bathrooms=str(obj.get("bathrooms", "N/A")),
            property_type=obj.get("property_type", "N/A"),
            property_category=obj.get("property_category", "N/A"),
            city=obj.get("city", "N/A"),
            url=obj.get("url", "N/A")
        ))

    return props


async def fetch_properties(input: PropertyInput) -> List[Property]:
    urls = [
        # f"https://www.squareyards.com/sale/property-for-sale-in-{input.city}",
        f"https://www.99acres.com/property-in-{input.city}-ffid"
    ]

    all_properties = []
    prompt = f"""
Extract 3 to 10 properties from this page with the following criteria:
- City: {input.city}
- Category: {input.property_category}
- Type: {input.property_type}
- Maximum price: {input.max_budget} crores

Return each property with:
- title
- price 
- area
- bedrooms
- bathrooms
- property_type
- property_category
- city
- url

Do not include any other text or comments, please keep only the JSON objects in string format.
"""

    for url in urls:
        props = await extract_property_details(url, prompt)
        all_properties.extend(props)

    return all_properties


