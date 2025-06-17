from fastmcp import FastMCP
from models import PropertyInput
from extractor import fetch_properties
from analysis import analyze_property
import asyncio
from dotenv import load_dotenv
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp.server.auth.provider import AccessToken
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("TOKEN")
MY_NUMBER = os.getenv("MY_NUMBER")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RichToolDescription(BaseModel):
    description: str
    use_when: str
    side_effects: str | None

PropertyFinderDescription = RichToolDescription(
    description="Find properties based on user preferences like location, price, type, and category and provide a summary of the property and its lo.",
    use_when="Use this tool when the user asks for property listings, flats, houses, or wants to buy/rent something within a budget.",
    side_effects="Calls external sources to scrape property data. Might take a few seconds."
)

class SimpleBearerAuthProvider(BearerAuthProvider):
    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(public_key=k.public_key, jwks_uri=None, issuer=None, audience=None)
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(token=token, client_id="unknown", scopes=[], expires_at=None)
        return None

mcp = FastMCP("Property Finder MCP", auth=SimpleBearerAuthProvider(TOKEN))  

@mcp.tool
async def validate() -> str:
    """
    NOTE: This tool must be present in an MCP server used by puch.
    """
    return MY_NUMBER

@mcp.tool(description=PropertyFinderDescription.model_dump_json())
async def property_finder(input: PropertyInput):
    """
    MCP Tool: Find properties based on user preferences.
    """
    properties = await fetch_properties(input)
    print(properties)
    results = []
    for prop in properties:
        if prop.title == "N/A" or prop.city == "N/A":
            logger.warning(f"Skipping property due to insufficient details: {prop}")
            continue

        summary = await asyncio.to_thread(analyze_property, prop)
        print(summary)
        results.append({
            "title": prop.title,
            "price": prop.price,
            "area": prop.area,
            "city": prop.city,
            "url": prop.url,
            "ai_recommendation": summary
        })
    print(results)

    return results

async def main():
    await mcp.run_async("streamable-http", host="0.0.0.0", port=8085)

if __name__ == "__main__":
    asyncio.run(main())