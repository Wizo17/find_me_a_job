from pydantic import BaseModel, Field
from typing import List

class Job(BaseModel):
    job_name: str = Field(description="Name of the job")
    job_url: str = Field(description="URL of the job")

class JobSearchModel(BaseModel):
    """
    Model representing a job search result.

    Attributes:
        jobs (List[Job]): A list of jobs, each containing a job name and a job URL.
    """
    jobs: List[Job] = Field(description="List of jobs")
