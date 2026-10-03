class JobListing:
    def __init__(self, title: str, company: str, requirements: list):
        self.title = title
        self.company = company
        self.requirements = requirements

    def get_title(self):
        return self.title

    def get_company(self):
        return self.company

    def get_requirements(self):
        return self.requirements

    def __eq__(self, other):
        if not isinstance(other, JobListing):
            return False
        return (self.title == other.title and
                self.company == other.company and
                self.requirements == other.requirements)

    def __hash__(self):
        result = hash(self.title)
        result = 31 * result + hash(self.company)
        result = 31 * result + hash(tuple(self.requirements))
        return result


class Resume:
    def __init__(self, name: str, skills: list, experience: str):
        self.name = name
        self.skills = skills
        self.experience = experience

    def get_name(self):
        return self.name

    def get_skills(self):
        return self.skills

    def get_experience(self):
        return self.experience

    def __eq__(self, other):
        if not isinstance(other, Resume):
            return False
        return (self.name == other.name and
                self.skills == other.skills and
                self.experience == other.experience)

    def __hash__(self):
        result = hash(self.name)
        result = 31 * result + hash(tuple(self.skills))
        result = 31 * result + hash(self.experience)
        return result


class JobMarketplace:
    def __init__(self):
        self.job_listings = []
        self.resumes = []

    def post_job(self, title: str, company: str, requirements: list):
        self.job_listings.append(JobListing(title, company, requirements))

    def remove_job(self, job: JobListing):
        self.job_listings.remove(job)

    def submit_resume(self, name: str, skills: list, experience: str):
        self.resumes.append(Resume(name, skills, experience))

    def withdraw_resume(self, resume: Resume):
        self.resumes.remove(resume)

    def search_jobs(self, skill: str):
        return [job for job in self.job_listings if skill in job.get_requirements()]

    def get_job_applicants(self, job: JobListing):
        return [resume for resume in self.resumes if self.matches_requirements(resume, job.get_requirements())]

    def matches_requirements(self, resume: Resume, requirements: list):
        return len(resume.get_skills()) == len(requirements) and set(resume.get_skills()).issuperset(requirements)

    def get_job_listings(self):
        return self.job_listings

    def get_resumes(self):
        return self.resumes