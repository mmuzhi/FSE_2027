#include <algorithm>
#include <cctype>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

std::string to_lower(const std::string& s) {
    std::string out(s.size(), '\0');
    std::transform(s.begin(), s.end(), out.begin(),
                   [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
    return out;
}

struct Job {
    std::string job_title;
    std::string company;
    std::vector<std::string> requirements;

    bool operator==(const Job& other) const {
        return job_title == other.job_title && company == other.company &&
               requirements == other.requirements;
    }
};

struct Resume {
    std::string name;
    std::vector<std::string> skills;
    std::string experience;

    bool operator==(const Resume& other) const {
        return name == other.name && skills == other.skills &&
               experience == other.experience;
    }
};

}  // namespace

class JobMarketplace {
public:
    std::vector<Job> job_listings;
    std::vector<Resume> resumes;

    void post_job(const std::string& job_title, const std::string& company,
                  const std::vector<std::string>& requirements) {
        Job job{job_title, company, requirements};
        job_listings.push_back(job);
    }

    void remove_job(const Job& job) {
        auto it = std::find(job_listings.begin(), job_listings.end(), job);
        if (it == job_listings.end()) {
            // Mirrors Python's ValueError from list.remove when not found
            throw std::invalid_argument("list.remove(x): x not in list");
        }
        job_listings.erase(it);
    }

    void submit_resume(const std::string& name, const std::vector<std::string>& skills,
                       const std::string& experience) {
        Resume resume{name, skills, experience};
        resumes.push_back(resume);
    }

    void withdraw_resume(const Resume& resume) {
        auto it = std::find(resumes.begin(), resumes.end(), resume);
        if (it == resumes.end()) {
            // Mirrors Python's ValueError from list.remove when not found
            throw std::invalid_argument("list.remove(x): x not in list");
        }
        resumes.erase(it);
    }

    std::vector<Job> search_jobs(const std::string& criteria) const {
        std::vector<Job> matching_jobs;
        const std::string lowered = to_lower(criteria);
        for (const Job& job_listing : job_listings) {
            // criteria.lower() in job_title.lower()  -> substring test
            bool in_title =
                to_lower(job_listing.job_title).find(lowered) != std::string::npos;
            // criteria.lower() in [r.lower() for r in requirements] -> equality membership
            bool in_requirements = false;
            for (const std::string& r : job_listing.requirements) {
                if (to_lower(r) == lowered) {
                    in_requirements = true;
                    break;
                }
            }
            if (in_title || in_requirements) {
                matching_jobs.push_back(job_listing);
            }
        }
        return matching_jobs;
    }

    std::vector<Resume> get_job_applicants(const Job& job) const {
        std::vector<Resume> applicants;
        for (const Resume& resume : resumes) {
            if (matches_requirements(resume, job.requirements)) {
                applicants.push_back(resume);
            }
        }
        return applicants;
    }

    static bool matches_requirements(const Resume& resume,
                                      const std::vector<std::string>& requirements) {
        for (const std::string& skill : resume.skills) {
            if (std::find(requirements.begin(), requirements.end(), skill) ==
                requirements.end()) {
                return false;
            }
        }
        return true;
    }
};