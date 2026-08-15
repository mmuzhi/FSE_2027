#include <vector>
#include <string>
#include <algorithm>
#include <cctype>
#include <stdexcept>

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

class JobMarketplace {
public:
    std::vector<Job> job_listings;
    std::vector<Resume> resumes;

    void post_job(const std::string& job_title, const std::string& company,
                  const std::vector<std::string>& requirements) {
        job_listings.push_back({job_title, company, requirements});
    }

    void remove_job(const Job& job) {
        auto it = std::find(job_listings.begin(), job_listings.end(), job);
        if (it == job_listings.end()) {
            throw std::invalid_argument("list.remove(x): x not in list");
        }
        job_listings.erase(it);
    }

    void submit_resume(const std::string& name, const std::vector<std::string>& skills,
                       const std::string& experience) {
        resumes.push_back({name, skills, experience});
    }

    void withdraw_resume(const Resume& resume) {
        auto it = std::find(resumes.begin(), resumes.end(), resume);
        if (it == resumes.end()) {
            throw std::invalid_argument("list.remove(x): x not in list");
        }
        resumes.erase(it);
    }

    std::vector<Job> search_jobs(const std::string& criteria) const {
        std::vector<Job> matching_jobs;
        std::string lower_criteria = to_lower(criteria);

        for (const auto& job : job_listings) {
            if (contains_ignore_case(job.job_title, lower_criteria)) {
                matching_jobs.push_back(job);
                continue;
            }

            for (const auto& req : job.requirements) {
                if (to_lower(req) == lower_criteria) {
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

    static bool matches_requirements(const Resume& resume,
                                     const std::vector<std::string>& requirements) {
        for (const auto& skill : resume.skills) {
            if (std::find(requirements.begin(), requirements.end(), skill) == requirements.end()) {
                return false;
            }
        }
        return true;
    }

private:
    static std::string to_lower(std::string s) {
        std::transform(s.begin(), s.end(), s.begin(),
                       [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
        return s;
    }

    static bool contains_ignore_case(const std::string& text, const std::string& lower_criteria) {
        return to_lower(text).find(lower_criteria) != std::string::npos;
    }
};