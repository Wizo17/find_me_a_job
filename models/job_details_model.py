from pydantic import BaseModel, Field

class JobDetailModel(BaseModel):
    # TODO : Write a docstring for the class

    job_name: str = Field(description="Name of the job")
    job_company: str = Field(description="Company of the job")
    job_location: str = Field(description="Location of the job")
    job_contract_type: str = Field(description="Contract type of the job")
    job_remote_status: str | None = Field(default=None, description="Remote status of the job")
    job_posted_time: str | None = Field(default=None, description="Posted time of the job")
    job_description: str | None = Field(default=None, description="Description of the job")
    job_profil_content: str | None = Field(default=None, description="Profil content of the job")
    job_required_skills: str | None = Field(default=None, description="Required skills of the job")
    job_salary: str | None = Field(default=None, description="Salary or Daily Rate of the job")
    job_url: str = Field(description="URL of the job")
