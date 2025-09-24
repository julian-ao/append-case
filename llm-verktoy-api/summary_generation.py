import os
import httpx
import json


async def call_openrouter_api(prompt: str) -> str:
  """
  Calls OpenRouter API to get a response based on the prompt
  """

  OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
  MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

  try:
    if not OPENROUTER_API_KEY:
      raise ValueError("OPENROUTER_API_KEY is not set")

    response = await httpx.AsyncClient().post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
      },
      data=json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You respond concisely and professionally."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
      }),
      timeout=15.0
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
  except Exception as e:
    print(f"Error calling OpenRouter: {e}")
    return "Error calling OpenRouter."


def build_prompt(consultants: list[dict], min_availability: int, required_skill: str) -> str:
    """
    Builds a prompt for OpenRouter to generate a consultant summary
    """

    prompt = (
        f"You are an assistant that summarizes consultant availability professionally and concisely.\n\n"
        f"Requirements:\n"
        f"- Minimum availability: {min_availability}%\n"
        f"- Required skill: '{required_skill}'\n\n"
        f"Consultants data:\n"
    )
    for c in consultants:
        availability = 100 - c.get("load_percent", 0)
        skills = ", ".join(c.get("skills", []))
        prompt += f"- {c['name']}: {availability}% available, skills: {skills}\n"

    prompt += (
        "\nPlease provide a short, human-readable summary of matching consultants. "
        "Example: 'Found 2 consultants with at least 50% availability and skill python. "
        "Anna K. has 60% availability. Leo T. has 80% availability.'"
    )
    return prompt


async def create_ai_summary(consultants: list[dict], min_tilgjengelighet_prosent: int, påkrevd_ferdighet: str) -> str:
    """
    AI-generated summary using OpenRouter
    """
    
    prompt = build_prompt(consultants, min_tilgjengelighet_prosent, påkrevd_ferdighet)
    summary = await call_openrouter_api(prompt)
    return summary


def create_manual_summary(consultants: list[dict], min_tilgjengelighet_prosent: int, påkrevd_ferdighet: str) -> str:
  """
  Create a text summary of consultants available
  """

  summary = ""

  if len(consultants) == 0:
    return "Ingen konsulenter matcher kriteriene."
  if len(consultants) == 1:
    summary += f"Fant 1 konsulent med minst {min_tilgjengelighet_prosent}% tilgjengelighet og ferdigheten '{påkrevd_ferdighet}'."
  else:
    summary += f"Fant {len(consultants)} konsulenter med minst {min_tilgjengelighet_prosent}% tilgjengelighet og ferdigheten '{påkrevd_ferdighet}'."
  
  for c in consultants:
    summary += f" {c['name']} har {100 - c.get('load_percent', 0)}% tilgjengelighet."

  return summary
