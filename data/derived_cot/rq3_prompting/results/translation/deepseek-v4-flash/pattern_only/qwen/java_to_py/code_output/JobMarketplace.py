def _to_signed32(x):
    x &= 0xffffffff
    return x if x < 0x80000000 else x - 0x100000000

def _java_string_hash(s):
    if s is None:
        raise AttributeError("'NoneType' object has no attribute 'hashCode'")
    h = 0
    encoded = s.encode('utf-16-be', errors='surrogatepass')
    for i in range(0, len(encoded), 2):
        code_unit = (encoded[i] << 8) | encoded[i + 1]
        h = (31 * h + code_unit) & 0xffffffff
    return _to_signed32(h)

def _java_list_hash(lst):
    if lst is None:
        raise AttributeError("'NoneType' object has no attribute 'hashCode'")
    h = 1
    for e in lst:
        if e is None:
            elem_hash = 0
        else:
            elem_hash = _java_string_hash(e)
        h = (31 * h + elem_hash) & 0xffffffff
    return _to_signed32(h)

def _java_equals(a, b):
    if a is None:
        raise AttributeError("'NoneType' object has no attribute 'equals'")
    return a == b

class JobMarketplace:
    def __init__(self):
        self._jobListings = []
        self._resumes = []

    def postJob(self, title, company, requirements):
        self._jobListings.append(JobMarketplace.JobListing(title, company, requirements))

    def removeJob(self, job):
        for i, existing in enumerate(self._jobListings):
            if job == existing:
                del self._jobListings[i]
                return

    def submitResume(self, name, skills, experience):
        self._resumes.append(JobMarketplace.Resume(name, skills, experience))

    def withdrawResume(self, resume):
        for i, existing in enumerate(self._resumes):
            if resume == existing:
                del self._resumes[i]
                return

    def searchJobs(self, skill):
        return [job for job in self._jobListings if skill in job.getRequirements()]

    def getJobApplicants(self, job):
        return [resume for resume in self._resumes if self.matchesRequirements(resume, job.getRequirements())]

    def matchesRequirements(self, resume, requirements):
        return len(resume.getSkills()) == len(requirements) and all(skill in resume.getSkills() for skill in requirements)

    def getJobListings(self):
        return self._jobListings

    def getResumes(self):
        return self._resumes

    class JobListing:
        def __init__(self, title, company, requirements):
            self._title = title
            self._company = company
            self._requirements = requirements

        def getTitle(self):
            return self._title

        def getCompany(self):
            return self._company

        def getRequirements(self):
            return self._requirements

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(self) is not type(other):
                return False
            return (_java_equals(self._title, other._title) and
                    _java_equals(self._company, other._company) and
                    _java_equals(self._requirements, other._requirements))

        def __hash__(self):
            result = _java_string_hash(self._title)
            result = (31 * result + _java_string_hash(self._company)) & 0xffffffff
            result = (31 * result + _java_list_hash(self._requirements)) & 0xffffffff
            return _to_signed32(result)

    class Resume:
        def __init__(self, name, skills, experience):
            self._name = name
            self._skills = skills
            self._experience = experience

        def getName(self):
            return self._name

        def getSkills(self):
            return self._skills

        def getExperience(self):
            return self._experience

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(self) is not type(other):
                return False
            return (_java_equals(self._name, other._name) and
                    _java_equals(self._skills, other._skills) and
                    _java_equals(self._experience, other._experience))

        def __hash__(self):
            result = _java_string_hash(self._name)
            result = (31 * result + _java_list_hash(self._skills)) & 0xffffffff
            result = (31 * result + _java_string_hash(self._experience)) & 0xffffffff
            return _to_signed32(result)