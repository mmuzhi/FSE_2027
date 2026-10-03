#include <vector>
#include <string>
#include <algorithm>
#include <cctype>
#include <stdexcept>

struct Job {
    std::string job_title;
    std::string company;
    std::vector<std::string> requirements;
};

struct Resume {
    std::string name;
    std::vector<std::string> skills;
    std::string experience;
};

class JobMarketplace {
public:
    std::vector<Job> job_listings;
    std::vector<Resume> resumes;

    void post_job(const std::string& job_title, const std::string& company, const std::vector<std::string>& requirements) {
        Job job;
        job.job_title = job_title;
        job.company = company;
        job.requirements = requirements;
        job_listings.push_back(job);
    }

    void remove_job(const Job& job) {
        auto it = std::find(job_listings.begin(), job_listings.end(), job);
        if (it == job_listings.end()) {
            throw std::invalid_argument("Job not found");
        }
        job_listings.erase(it);
    }

    void submit_resume(const std::string& name, const std::vector<std::string>& skills, const std::string& experience) {
        Resume resume;
        resume.name = name;
        resume.skills = skills;
        resume.experience = experience;
        resumes.push_back(resume);
    }

    void withdraw_resume(const Resume& resume) {
        auto it = std::find(resumes.begin(), resumes.end(), resume);
        if (it == resumes.end()) {
            throw std::invalid_argument("Resume not found");
        }
        resumes.erase(it);
    }

    std::vector<Job> search_jobs(const std::string& criteria) const {
        std::vector<Job> matching_jobs;
        std::string criteria_lower = criteria;
        std::transform(criteria_lower.begin(), criteria_lower.end(), criteria_lower.begin(), ::tolower);
        for (const auto& job : job_listings) {
            std::string title_lower = job.job_title;
            std::transform(title_lower.begin(), title_lower.end(), title_lower.begin(), ::tolower);
            if (title_lower.find(criteria_lower) != std::string::npos) {
                matching_jobs.push_back(job);
                continue;
            }
            for (const auto& req : job.requirements) {
                std::string req_lower = req;
                std::transform(req_lower.begin(), req_lower.end(), req_lower.begin(), ::tolower);
                if (req_lower.find(criteria_lower) != std::string::npos) {
                    matching_jobs.push_back(job);
                    break;
                }
            }
        }
        return matching_jobs;
    }

    std::vector<Resume> get_job_applicants(const Job& job) const {
        std::vector<Resume> applicants;
        for (const auto& resume : resumes) {
            if (matches_requirements(resume, job.requirements)) {
                applicants.push_back(resume);
            }
        }
        return applicants;
    }

    static bool matches_requirements(const Resume& resume, const std::vector<std::string>& requirements) {
        for (const auto& skill : resume.skills) {
            if (std::find(requirements.begin(), requirements.end(), skill) == requirements.end()) {
                return false;
            }
        }
        return true;
    }
};

// Helper to allow std::find for Job and Resume (equality operators)
bool operator==(const Job& lhs, const Job& rhs) {
    return lhs.job_title == rhs.job_title &&
           lhs.company == rhs.company &&
           lhs.requirements == rhs.requirements;
}

bool operator==(const Resume& lhs, const Resume& rhs) {
    return lhs.name == rhs.name &&
           lhs.skills == rhs.skills &&
           lhs.experience == rhs.experience;
}