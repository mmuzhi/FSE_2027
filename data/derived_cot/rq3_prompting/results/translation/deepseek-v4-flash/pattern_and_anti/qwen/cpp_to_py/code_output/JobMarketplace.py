class Job:
    def __init__(self, job_title, company, requirements):
        self.job_title = job_title
        self.company = company
        self.requirements = list(requirements)

    def __eq__(self, other):
        if not isinstance(other, Job):
            return NotImplemented
        return (self.job_title == other.job_title and
                self.company == other.company and
                self.requirements == other.requirements)


class Resume:
    def __init__(self, name, skills, experience):
        self.name = name
        self.skills = list(skills)
        self.experience = experience

    def __eq__(self, other):
        if not isinstance(other, Resume):
            return NotImplemented
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
        self.job_listings[:] = [j for j in self.job_listings if j != job]

    def submit_resume(self, name, skills, experience):
        self.resumes.append(Resume(name, skills, experience))

    def withdraw_resume(self, resume):
        self.resumes[:] = [r for r in self.resumes if r != resume]

    def search_jobs(self, criteria):
        matching_jobs = []
        for job_listing in self.job_listings:
            found = criteria in job_listing.job_title
            if not found:
                for requirement in job_listing.requirements:
                    if criteria in requirement:
                        found = True
                        break
            if found:
                matching_jobs.append(Job(job_listing.job_title, job_listing.company, job_listing.requirements))
        return matching_jobs

    def get_job_applicants(self, job):
        applicants = []
        for resume in self.resumes:
            if JobMarketplace.matches_requirements(resume, job.requirements):
                applicants.append(Resume(resume.name, resume.skills, resume.experience))
        return applicants

    @staticmethod
    def matches_requirements(resume, requirements):
        for skill in resume.skills:
            if skill not in requirements:
                return False
        return True