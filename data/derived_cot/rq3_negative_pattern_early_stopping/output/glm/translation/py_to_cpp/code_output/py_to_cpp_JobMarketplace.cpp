#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <stdexcept>

class JobMarketplace {
public:
    struct Job {
        std::string job_title;
        std::string company;
        std::vector<std::string> requirements;

        bool operator==(const Job& other) const {
            return job_title == other.job_title &&
                   company == other.company &&
                   requirements == other.requirements;
        }
    };

    struct Resume {
        std::string name;
        std::vector<std::string> skills;
        std::string experience;

        bool operator==(const Resume& other) const {
            return name == other.name &&
                   skills == other.skills &&
                   experience == other.experience;
        }
    };

private:
    static std::string to_lower(const std::string& s) {
        std::string result = s;
        for (char& c : result) {
            c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        }
        return result;
    }

public:
    std::vector<Job> job_listings;
    std::vector<Resume> resumes;

    void post_job(const std::string& job_title, const std::string& company, const std::vector<std::string>& requirements) {
        job_listings.push_back({job_title, company, requirements});
    }

    void remove_job(const Job& job) {
        auto it = std::find(job_listings.begin(), job_listings.end(), job);
        if (it == job_listings.end()) {
            throw std::runtime_error("list.remove(x): x not in list");
        }
        job_listings.erase(it);
    }

    void submit_resume(const std::string& name, const std::vector<std::string>& skills, const std::string& experience) {
        resumes.push_back({name, skills, experience});
    }

    void withdraw_resume(const Resume& resume) {
        auto it = std::find(resumes.begin(), resumes.end(), resume);
        if (it == resumes.end()) {
            throw std::runtime_error("list.remove(x): x not in list");
        }
        resumes.erase(it);
    }

    std::vector<Job> search_jobs(const std::string& criteria) {
        std::vector<Job> matching_jobs;
        std::string criteria_lower = to_lower(criteria);
        for (const auto& job_listing : job_listings) {
            // substring match on job_title (case-insensitive)
            bool match = to_lower(job_listing.job_title).find(criteria_lower) != std::string::npos;
            // exact match in requirements list (case-insensitive), matching Python's `in` on a list
            if (!match) {
                for (const auto& r : job_listing.requirements) {
                    if (to_lower(r) == criteria_lower) {
                        match = true;
                        break;
                    }
                }
            }
            if (match) {
                matching_jobs.push_back(job_listing);
            }
        }
        return matching_jobs;
    }

    std::vector<Resume> get_job_applicants(const Job& job) {
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