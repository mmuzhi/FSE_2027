#include <vector>
#include <string>
#include <cctype>
#include <algorithm>
#include <stdexcept>

// Helper function to convert string to lowercase
static std::string toLower(const std::string& s) {
    std::string result;
    for (char c : s) {
        result += std::tolower(static_cast<unsigned char>(c));
    }
    return result;
}

struct JobListing {
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
    std::vector<JobListing> job_listings;
    std::vector<Resume> resumes;

    void post_job(const std::string& job_title, const std::string& company, const std::vector<std::string>& requirements) {
        JobListing job = {job_title, company, requirements};
        job_listings.push_back(job);
    }

    void remove_job(const JobListing& job) {
        auto it = std::find(job_listings.begin(), job_listings.end(), job);
        if (it == job_listings.end()) {
            throw std::runtime_error("Job not found");
        }
        job_listings.erase(it);
    }

    void submit_resume(const std::string& name, const std::vector<std::string>& skills, const std::string& experience) {
        Resume resume = {name, skills, experience};
        resumes.push_back(resume);
    }

    void withdraw_resume(const Resume& resume) {
        auto it = std::find(resumes.begin(), resumes.end(), resume);
        if (it == resumes.end()) {
            throw std::runtime_error("Resume not found");
        }
        resumes.erase(it);
    }

    std::vector<JobListing> search_jobs(const std::string& criteria) {
        std::vector<JobListing> matching_jobs;
        std::string lower_criteria = toLower(criteria);
        for (const auto& job : job_listings) {
            std::string lower_job_title = toLower(job.job_title);
            if (lower_job_title.find(lower_criteria) != std::string::npos || 
                std::any_of(job.requirements.begin(), job.requirements.end(),
                            [&lower_criteria](const std::string& req) {
                                std::string lower_req = toLower(req);
                                return lower_req.find(lower_criteria) != std::string::npos;
                            })) {
                matching_jobs.push_back(job);
            }
        }
        return matching_jobs;
    }

    std::vector<Resume> get_job_applicants(const JobListing& job) {
        std::vector<Resume> applicants;
        for (const auto& resume : resumes) {
            bool matches = true;
            for (const auto& skill : resume.skills) {
                bool found = false;
                for (const auto& req : job.requirements) {
                    if (skill == req) {
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    matches = false;
                    break;
                }
            }
            if (matches) {
                applicants.push_back(resume);
            }
        }
        return applicants;
    }
};