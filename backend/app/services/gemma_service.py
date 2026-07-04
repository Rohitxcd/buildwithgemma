import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMMA_API_KEY"))


class GemmaService:

    def analyze_image(self, metadata):

        prompt = f"""
You are an AI Privacy Analyst.

Image Data:
- Faces: {metadata['faces']}
- Resolution: {metadata['width']}x{metadata['height']}

Return ONLY JSON:
{{
  "risk_score": int,
  "risk_level": "Low | Medium | High",
  "summary": string,
  "recommendation": string
}}
"""

        response = client.models.generate_content(
            model="gemma-4-12b-it",
            contents=prompt
        )

        return response.text


gemma_service = GemmaService()