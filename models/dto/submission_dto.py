from dataclasses import dataclass

@dataclass
class SubmissionDto:
    id: str
    code_path: str
    created_date: str
