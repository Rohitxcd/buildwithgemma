from fastapi import APIRouter

router = APIRouter(
    prefix="/report",
    tags=["Reports"]
)


@router.get("/{report_id}")
async def get_report(report_id: str):

    return {
        "message": "Report endpoint coming soon.",
        "report_id": report_id
    }