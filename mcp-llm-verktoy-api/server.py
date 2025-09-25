import logging
import os
from fastmcp import FastMCP
import httpx

from summary_generation import create_ai_summary

mcp = FastMCP("LLM Verktøy API")


async def get_all_consultants() -> list[dict]:
  """
  Fetch all consultants from Konsulent API
  """

  KONSULENT_API_URL = os.getenv("KONSULENT_API_URL", "http://localhost:8000")

  try:
    if not KONSULENT_API_URL:
      raise ValueError("KONSULENT_API_URL is not set")

    response = await httpx.AsyncClient().get(f"{KONSULENT_API_URL}/konsulenter", timeout=10.0)
    response.raise_for_status()
    return response.json()
  except Exception as e:
    logging.error(f"Error fetching consultants: {e}")
    return []
  

@mcp.tool()
async def get_consultants_summary(
  min_tilgjengelighet_prosent: int,
  paakrevd_ferdighet: str
) -> dict[str, str]:
  """
  Get a summary of available consultants based on minimum availability percentage and required skill
  """
  
  # get all consultants
  try:
    all_consultants = await get_all_consultants()
  except Exception as e:
    logging.error(f"Error fetching consultants: {e}")
    return {"sammendrag": "Kunne ikke hente konsulenter."}

  # filter based on availability
  available_consultants = [c for c in all_consultants if 100 - c.get("load_percent", 0) >= min_tilgjengelighet_prosent]

  # filter based on skill
  skilled_consultants = [c for c in available_consultants if paakrevd_ferdighet in c.get("skills", [])]

  if not skilled_consultants:
    return {"sammendrag": "Ingen konsulenter matcher kriteriene."}
  
  # create summary
  summary = await create_ai_summary(skilled_consultants, min_tilgjengelighet_prosent, paakrevd_ferdighet)

  return {"sammendrag": summary}


if __name__ == "__main__":
    mcp.run(transport="stdio")