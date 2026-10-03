class Job:
    def __init__(self, job_title, company, requirements):
        self.job_title = job_title
        self.company = company
        self.requirements = requirements

    def __eq__(self, other):
        if not isinstance(other, Job):
            return False
        return (self.job_title == other.job_title and
                self.company == other.company and
                self.requirements == other.requirements)


class Resume:
    def __init__(self, name, skills, experience):
        self.name = name
        self.skills = skills
        self.experience = experience

    def __eq__(self, other):
        if not isinstance(other, Resume):
            return False
        return (self.name == other.name and
                self.skills == other.skills and
                self.experience == other.experience)


class JobMarketplace:
    def __init__(self):
        self.job_listings = []
        self.resumes = []

    def post_job(self, job_title, company, requirements):
        self.job_listings.append(Job(job_title, company, requirements))

    def remove_job(self, job):
        self.job_listings = [j for j in self.job_listings if j != job]

    def submit_resume(self, name, skills, experience):
        self.resumes.append(Resume(name, skills, experience))

    def withdraw_resume(self, resume):
        self.resumes = [r for r in self.resumes if r != resume]

    def search_jobs(self, criteria):
        matching_jobs = []
        for job in self.job_listings:
            if criteria in job.job_title:
                matching_jobs.append(job)
                continue
            for req in job.requirements:
                if criteria in req:
                    matching_jobs.append(job)
                    break
        return matching_jobs

    def get_job_applicants(self, job):
        return [r for r in self.resumes if self.matches_requirements(r, job.requirements)]

    @staticmethod
    def matches_requirements(resume, requirements):
        for skill in resume.skills:
            if skill not in requirements:
                return False
        return True