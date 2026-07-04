import json
import mimetypes
import os
import re
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types

from app.gemma.prompts import (
    build_post_protection_verification_prompt,
    build_privacy_analysis_prompt,
)

GEMMA_MODEL = os.getenv("GEMMA_MODEL", "gemma-4-12b-it")
VALID_STRENGTHS = {"low", "medium", "high"}


def _fallback_strategy() -> dict[str, Any]:
    return {
        "landmark_perturbation": True,
        "frequency_mask": True,
        "texture_shift": False,
        "strength": "medium",
    }


def _fallback_initial_analysis(message: str) -> dict[str, Any]:
    return {
        "risk_score": 50,
        "risk_level": "Medium",
        "summary": message,
        "privacy_risks": [
            "Automated Gemma analysis was unavailable; default protection was applied."
        ],
        "strategy": _fallback_strategy(),
    }


def _fallback_verification(message: str) -> dict[str, Any]:
    return {
        "risk_score": 50,
        "risk_level": "Medium",
        "summary": message,
        "face_still_identifiable": None,
        "privacy_improved": None,
        "remaining_risks": [
            "Automated Gemma verification was unavailable."
        ],
        "recommendations": [
            "Review the protected image manually before sharing."
        ],
    }


class GemmaService:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMMA_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def analyze_image(self, image_path: str) -> dict[str, Any]:
        prompt = build_privacy_analysis_prompt()
        fallback = _fallback_initial_analysis(
            "Gemma privacy analysis could not be completed; using a conservative default strategy."
        )

        result = self._generate_json(image_path, prompt, fallback)
        result["strategy"] = self._normalize_strategy(result.get("strategy"))
        result.setdefault("privacy_risks", [])

        return result

    def verify_protection(self, image_path: str) -> dict[str, Any]:
        prompt = build_post_protection_verification_prompt()
        fallback = _fallback_verification(
            "Gemma post-protection verification could not be completed."
        )

        result = self._generate_json(image_path, prompt, fallback)
        result.setdefault("remaining_risks", [])
        result.setdefault("recommendations", [])

        return result

    def _generate_json(
        self,
        image_path: str,
        prompt: str,
        fallback: dict[str, Any],
    ) -> dict[str, Any]:
        if self.client is None:
            return fallback

        path = Path(image_path)
        if not path.exists():
            return {
                **fallback,
                "summary": f"Image not found for Gemma analysis: {image_path}",
            }

        try:
            response_text = self._call_gemma(path, prompt)
            parsed = self._parse_json(response_text)
        except Exception as exc:
            return {
                **fallback,
                "summary": f"{fallback['summary']} Error: {exc}",
            }

        if parsed is None:
            return {
                **fallback,
                "summary": "Gemma returned malformed JSON; using fallback response.",
            }

        return parsed

    def _call_gemma(self, image_path: Path, prompt: str) -> str:
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
        )

        try:
            uploaded_file = self.client.files.upload(file=str(image_path))
            response = self.client.models.generate_content(
                model=GEMMA_MODEL,
                contents=[prompt, uploaded_file],
                config=config,
            )
            return getattr(response, "text", "") or ""
        except Exception:
            mime_type = mimetypes.guess_type(image_path.name)[0] or "image/jpeg"
            image_part = types.Part.from_bytes(
                data=image_path.read_bytes(),
                mime_type=mime_type,
            )
            response = self.client.models.generate_content(
                model=GEMMA_MODEL,
                contents=[prompt, image_part],
                config=config,
            )
            return getattr(response, "text", "") or ""

    def _parse_json(self, text: str) -> dict[str, Any] | None:
        cleaned = text.strip()

        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"```$", "", cleaned).strip()

        try:
            value = json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
            if not match:
                return None
            try:
                value = json.loads(match.group(0))
            except json.JSONDecodeError:
                return None

        return value if isinstance(value, dict) else None

    def _normalize_strategy(self, strategy: Any) -> dict[str, Any]:
        fallback = _fallback_strategy()

        if not isinstance(strategy, dict):
            return fallback

        strength = str(strategy.get("strength", fallback["strength"])).lower()
        if strength not in VALID_STRENGTHS:
            strength = fallback["strength"]

        return {
            "landmark_perturbation": bool(
                strategy.get(
                    "landmark_perturbation",
                    fallback["landmark_perturbation"],
                )
            ),
            "frequency_mask": bool(
                strategy.get("frequency_mask", fallback["frequency_mask"])
            ),
            "texture_shift": bool(strategy.get("texture_shift", fallback["texture_shift"])),
            "strength": strength,
        }


gemma_service = GemmaService()
