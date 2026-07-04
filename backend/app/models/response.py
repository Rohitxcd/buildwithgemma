class RiskAnalysis(BaseModel):

    risk_score: int

    risk_level: str

    summary: str

    recommendation: str


class ProtectResponse(BaseModel):

    success: bool

    faces_detected: int

    image_width: int

    image_height: int

    original_image: str

    protected_image: str

    risk_analysis: RiskAnalysis