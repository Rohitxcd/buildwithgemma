from typing import Any


class ReportService:
    def generate(
        self,
        before_protection: dict[str, Any],
        after_protection: dict[str, Any],
        strategy_used: dict[str, Any],
        metadata: dict[str, Any],
        protected_image: str,
    ) -> dict[str, Any]:
        return {
            "success": True,
            "before_protection": before_protection,
            "after_protection": after_protection,
            "strategy_used": strategy_used,
            "protected_image": protected_image,
            "metadata": metadata,
        }


report_service = ReportService()
