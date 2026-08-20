from typing import List


def _list_hash(items) -> int:
    # Mirrors java.util.List#hashCode()
    result = 1
    for item in items:
        result = 31 * result + hash(item)
    return result


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

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if other is None or type(other) is not type(self):
            return False
        if self.title != other.title:
            return False
        if self.company != other.company:
            return False
        return self.requirements == other.requirements

    def __hash__(self) -> int:
        result = hash(self.title)
        result = 31 * result + hash(self.company)
        result = 31 * result + _list_hash(self.requirements)
        return result


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

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if other is None or type(other) is not type(self):
            return False
        if self.name != other.name:
            return False
        if self.skills != other.skills:
            return False
        return self.experience == other.experience

    def __hash__(self) -> int:
        result = hash(self.name)
        result = 31 * result + _list_hash(self.skills)
        result = 31 * result + hash(self.experience)
        return result


class JobMarketplace:
    def __init__(self) -> None:
        self.job_listings: List[JobListing] = []
        self.resumes: List[Resume] = []

    def post_job(self, title: str, company: str, requirements: List[str]) -> None:
        self.job_listings.append(JobListing(title, company, requirements))

    def remove_job(self, job: JobListing) -> None:
        # Java's List.remove(Object) is a silent no-op when the element is absent;
        # Python's list.remove raises ValueError, so it is suppressed here.
        try:
            self.job_listings.remove(job)
        except ValueError:
            pass

    def submit_resume(self, name: str, skills: List[str], experience: str) -> None:
        self.resumes.append(Resume(name, skills, experience))

    def withdraw_resume(self, resume: Resume) -> None:
        try:
            self.resumes.remove(resume)
        except ValueError:
            pass

    def search_jobs(self, skill: str) -> List[JobListing]:
        return [job for job in self.job_listings if skill in job.requirements]

    def get_job_applicants(self, job: JobListing) -> List[Resume]:
        return [
            resume
            for resume in self.resumes
            if self.matches_requirements(resume, job.requirements)
        ]

    def matches_requirements(self, resume: Resume, requirements: List[str]) -> bool:
        skills = resume.skills
        return len(skills) == len(requirements) and all(
            requirement in skills for requirement in requirements
        )

    def get_job_listings(self) -> List[JobListing]:
        return self.job_listings

    def get_resumes(self) -> List[Resume]:
        return self.resumes