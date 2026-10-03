from dataclasses import dataclass
from typing import List

@dataclass
class Job:
    job_title: str
    company: str
    requirements: List[str]

@dataclass
class Resume:
    name: str
    skills: List[str]
    experience: str

class JobMarketplace:
    def __init__(self):
        self.job_listings: List[Job] = []
        self.resumes: List[Resume] = []

    def post_job(self, job_title: str, company: str, requirements: List[str]) -> None:
        self.job_listings.append(Job(job_title, company, requirements))

    def remove_job(self, job: Job) -> None:
        self.job_listings = [j for j in self.job_listings if j != job]

    def submit_resume(self, name: str, skills: List[str], experience: str) -> None:
        self.resumes.append(Resume(name, skills, experience))

    def withdraw_resume(self, resume: Resume) -> None:
        self.resumes = [r for r in self.resumes if r != resume]

    def search_jobs(self, criteria: str) -> List[Job]:
        matching_jobs = []
        for job_listing in self.job_listings:
            found = criteria in job_listing.job_title
            if not found:
                found = any(criteria in requirement for requirement in job_listing.requirements)
            
            if found:
                matching_jobs.append(job_listing)
        return matching_jobs

    def get_job_applicants(self, job: Job) -> List[Resume]:
        applicants = []
        for resume in self.resumes:
            if JobMarketplace.matches_requirements(resume, job.requirements):
                applicants.append(resume)
        return applicants

    @staticmethod
    def matches_requirements(resume: Resume, requirements: List[str]) -> bool:
        return all(skill in requirements for skill in resume.skills)