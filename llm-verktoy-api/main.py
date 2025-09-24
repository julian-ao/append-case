from fastapi import FastAPI
import httpx

app = FastAPI(title="LLM Verktøy API", version="1.0.0")


KONSULENT_API_URL = "http://localhost:8000"


async def get_all_consultants() -> list[dict]:
  """
  Fetch all consultants from Konsulent API
  """
  try:
    response = await httpx.AsyncClient().get(f"{KONSULENT_API_URL}/konsulenter", timeout=10.0)
    response.raise_for_status()
    return response.json()
  except Exception as e:
    print(f"Error fetching consultants: {e}")
    return []
  

def calculate_availability(load_percent: int) -> int:
  """
  Calculate availability percentage from load percentage
  """
  return 100 - load_percent


async def create_summary(consultants: list[dict], min_tilgjengelighet_prosent: int, påkrevd_ferdighet: str) -> str:
  """
  Create a summary of consultants using LLM
  """
  # This is a placeholder for actual LLM integration
  # For now, we just return a dummy summary
  return f"Found {len(consultants)} consultants with at least {min_tilgjengelighet_prosent}% availability and skill '{påkrevd_ferdighet}'."


@app.get("/tilgjengelige-konsulenter/sammendrag")
async def get_consultants_summary(
  min_tilgjengelighet_prosent: int,
  påkrevd_ferdighet: str
) -> dict[str, str]:
  """
  Get a summary of available consultants based on minimum availability percentage and required skill
  """
  
  # get all consultants
  all_consultants = await get_all_consultants()

  # filter based on availability
  available_consultants = [c for c in all_consultants if calculate_availability(c.get("load_percent", 0)) >= min_tilgjengelighet_prosent]

  # filter based on skill
  skilled_consultants = [c for c in available_consultants if påkrevd_ferdighet in c.get("skills", [])]

  if not skilled_consultants:
    return {"sammendrag": "Ingen konsulenter matcher kriteriene."}
  
  # create summary
  summary = await create_summary(skilled_consultants, min_tilgjengelighet_prosent, påkrevd_ferdighet)

  return {"sammendrag": summary}
