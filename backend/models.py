from pydantic import BaseModel
from typing import List

class Finding(BaseModel):
    source_fragment: str
    identified_control: str
    nis2_pillar: str
    confidence: float
    reasoning: str


class AnalysisResponse(BaseModel):
    document_id: str
    findings: List[Finding]
    timestamp: str
