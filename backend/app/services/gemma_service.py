import os
import json

from google import genai

client = genai.Client(
    api_key=os.getenv("GEMMA_API_KEY")
)


class GemmaService:

    def analyze_image(self, metadata):

        prompt = f"""
You are an AI Privacy Analyst.

Analyze the following image metadata.

Faces Detected:
{metadata['faces']}

Resolution:
{metadata['width']} x {metadata['height']}

Face Region:
{metadata['region']}

Respond ONLY with valid JSON.

{{
    "risk_score": 0,
    "risk_level": "Low",
    "summary": "",
    "recommendation": ""
}}
"""

        response = client.models.generate_content(
            model="gemma-4-12b-it",
            contents=prompt
        )

        text = response.text.strip()

        # Remove Markdown code fences if present
        if text.startswith("```"):
            lines = text.splitlines()

            if lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        try:
            return json.loads(text)

        except Exception:
            return {
                "risk_score": 75,
                "risk_level": "Medium",
                "summary": "Unable to parse Gemma response.",
                "recommendation": "Review the image manually."
            }


gemma_service = GemmaService()