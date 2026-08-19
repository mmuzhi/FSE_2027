from typing import List


class JobMarketplace:

    def __init__(self) -> None:
        self.job_listings: List["JobMarketplace.JobListing"] = []
        self.resumes: List["JobMarketplace.Resume"] = []

    def post_job(self, title: str, company: str, requirements: List[str]) -> None:
        self.job_listings.append(JobMarketplace.JobListing(title, company, requirements))

    def remove_job(self, job: "JobMarketplace.JobListing") -> None:
        try:
            self.job_listings.remove(job)
        except ValueError:
            pass

    def submit_resume(self, name: str, skills: List[str], experience: str) -> None:
        self.resumes.append(JobMarketplace.Resume(name, skills, experience))

    def withdraw_resume(self, resume: "JobMarketplace.Resume") -> None:
        try:
            self.resumes.remove(resume)
        except ValueError:
            pass

    def search_jobs(self, skill: str) -> List["JobMarketplace.JobListing"]:
        return [job for job in self.job_listings if skill in job.requirements]

    def get_job_applicants(self, job: "JobMarketplace.JobListing") -> List["JobMarketplace.Resume"]:
        return [resume for resume in self.resumes
                if self.matches_requirements(resume, job.requirements)]

    def matches_requirements(self, resume: "JobMarketplace.Resume", requirements: List[str]) -> bool:
        return (len(resume.skills) == len(requirements)
                and all(req in resume.skills for req in requirements))

    def get_job_listings(self) -> List["JobMarketplace.JobListing"]:
        return self.job_listings

    def get_resumes(self) -> List["JobMarketplace.Resume"]:
        return self.resumes

    class JobListing:
        def __init__(self, title: str, company: str, requirements: List[str]) -> None:
            self.title = title
            self.company = company
            self.requirements = requirements

        def get_title(self) -> str:
            return self.title

        def get_company(self) -> str:
            return self.company

        def get_requirements(self) -> List[str]:
            return self.requirements

        def __eq__(self, other: object) -> bool:
            if self is other:
                return True
            if type(other) is not type(self):
                return False
            that = other
            return (self.title == that.title
                    and self.company == that.company
                    and self.requirements == that.requirements)

        def __hash__(self) -> int:
            return hash((self.title, self.company, tuple(self.requirements)))

    class Resume:
        def __init__(self, name: str, skills: List[str], experience: str) -> None:
            self.name = name
            self.skills = skills
            self.experience = experience

        def get_name(self) -> str:
            return self.name

        def get_skills(self) -> List[str]:
            return self.skills

        def get_experience(self) -> str:
            return self.experience

        def __eq__(self, other: object) -> bool:
            if self is other:
                return True
            if type(other) is not type(self):
                return False
            that = other
            return (self.name == that.name
                    and self.skills == that.skills
                    and self.experience == that.experience)

        def __hash__(self) -> int:
            return hash((self.name, tuple(self.skills), self.experience))