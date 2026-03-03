import json

from anthropic import Anthropic

from app.config import get_settings
from app.services.plant_data import get_plant_context
from app.models.requests import GardenPreferences
from app.models.responses import GardenPlanResponse

SYSTEM_PROMPT = """You are an expert gardener who specializes in companion planting and aesthetic garden design. You help users create beautiful, productive gardens by grouping plants that benefit each other and recommending appropriate containers.

Your recommendations should consider:
1. Companion planting benefits (pest control, pollination, nutrient sharing)
2. Plants that should NOT be planted together
3. Similar sun, water, and soil requirements for grouped plants
4. Container sizing based on plant spacing needs
5. Aesthetic arrangement with flowers as borders and focal points
6. Bloom times for continuous color throughout the season
7. Mix flowers as companions directly into all beds for pest control, pollination, and beauty — never isolate flowers into their own separate group

Always provide practical, actionable advice."""


def create_user_prompt(
    selected_seeds: list[str],
    plant_context: str,
    preferences: GardenPreferences,
) -> str:
    seeds_list = "\n".join(f"- {seed}" for seed in selected_seeds)
    bed_types_list = ", ".join(preferences.bed_types)

    return f"""Based on the following plant data and the user's selected seeds, create a garden plan with companion plant groupings and container recommendations.

{plant_context}

## Garden Setup:
- Yard size: {preferences.yard_width}ft x {preferences.yard_depth}ft
- Sun exposure: {preferences.sun_exposure}
- Available bed types: {bed_types_list}

## User's Selected Seeds:
{seeds_list}

Please provide your response as JSON with this exact structure:
{{
  "plant_groups": [
    {{
      "name": "Group name (e.g., 'Tomato & Basil Bed')",
      "plants": [
        {{"name": "Plant 1", "category": "veggies"}},
        {{"name": "Plant 2", "category": "herbs"}}
      ],
      "container": {{
        "type": "One of the available bed types listed above",
        "size": "Recommended size (e.g., 4ft x 4ft)",
        "depth": "Required depth"
      }},
      "reason": "Why these plants work well together",
      "placement": "Where to place in the garden"
    }}
  ],
  "aesthetic_tips": [
    "Tip for visual arrangement"
  ],
  "bloom_schedule": {{
    "spring": ["Plants that bloom in spring"],
    "summer": ["Plants that bloom in summer"],
    "fall": ["Plants that bloom in fall"]
  }}
}}

IMPORTANT RULES:
- Create exactly 2 to 4 plant groups (beds). Combine plants into fewer, well-planned beds.
- Mix flowers directly into other groups as companions. Do NOT create a flowers-only group unless the user selected ONLY flowers.
- The "category" field for each plant must be one of: "fruits", "veggies", "herbs", "flowers".
- Only use bed types from the available bed types listed above.
- Beds must fit within the {preferences.yard_width}ft x {preferences.yard_depth}ft yard.
- Group all selected plants into appropriate beds. Ensure every selected plant appears in exactly one group.
- Only include plants from the selected seeds in the bloom_schedule."""


async def generate_garden_plan(
    selected_seeds: list[str],
    preferences: GardenPreferences,
) -> GardenPlanResponse:
    settings = get_settings()
    client = Anthropic(api_key=settings.anthropic_api_key)

    plant_context = get_plant_context()
    user_prompt = create_user_prompt(selected_seeds, plant_context, preferences)

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    response_text = message.content[0].text

    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    plan_data = json.loads(response_text.strip())
    return GardenPlanResponse(**plan_data)
