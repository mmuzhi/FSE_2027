class JobMarketplace:
    def __init__(self):
        self.jobListings = []
        self.resumes = []

    def postJob(self, title, company, requirements):
        self.jobListings.append(JobListing(title, company, requirements))

    def removeJob(self, job):
        for i in range(len(self.jobListings) - 1, -1, -1):
            if self.jobListings[i] == job:
                del self.jobListings[i]
                break

    def submitResume(self, name, skills, experience):
        self.resumes.append(Resume(name, skills, experience))

    def withdrawResume(self, resume):
        for i in range(len(self.resumes) - 1, -1, -1):
            if self.resumes[i] == resume:
                del self.resumes[i]
                break

    def searchJobs(self, skill):
        return [job for job in self.jobListings if skill in job.requirements]

    def getJobApplicants(self, job):
        return [resume for resume in self.resumes if self.matchesRequirements(resume, job.requirements)]

    def matchesRequirements(self, resume, requirements):
        return len(resume.skills) == len(requirements) and all(skill in resume.skills for skill in requirements)

    def getJobListings(self):
        return self.jobListings

    def getResumes(self):
        return self.resumes

class JobListing:
    def __init__(self, title, company, requirements):
        self.title = title
        self.company = company
        self.requirements = requirements

    def __eq__(self, other):
        if not isinstance(other, JobListing):
            return False
        return (self.title == other.title and
                self.company == other.company and
                self.requirements == other.requirements)

    def __hash__(self):
        h_title = hash(self.title)
        h_company = hash(self.company)
        h_requirements = hash(tuple(self.requirements))
        return hash((h_title, h_company, h_requirements))

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

    def __hash__(self):
        h_name = hash(self.name)
        h_skills = hash(tuple(self.skills))
        h_experience = hash(self.experience)
        return hash((h_name, h_skills, h_experience))