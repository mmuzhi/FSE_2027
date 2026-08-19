#include <algorithm>
#include <cctype>
#include <stdexcept>
#include <string>
#include <vector>

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

    std::vector<Job> job_listings;
    std::vector<Resume> resumes;

    void post_job(const std::string& job_title, const std::string& company,
                  const std::vector<std::string>& requirements) {
        job_listings.push_back(Job{job_title, company, requirements});
    }

    // Mirrors list.remove(): erases the first equal element,
    // raises (throws) when the element is absent.
    void remove_job(const Job& job) {
        for (auto it = job_listings.begin(); it != job_listings.end(); ++it) {
            if (*it == job) {
                job_listings.erase(it);
                return;
            }
        }
        throw std::invalid_argument("list.remove(x): x not in job_listings");
    }

    void submit_resume(const std::string& name, const std::vector<std::string>& skills,
                       const std::string& experience) {
        resumes.push_back(Resume{name, skills, experience});
    }

    void withdraw_resume(const Resume& resume) {
        for (auto it = resumes.begin(); it != resumes.end(); ++it) {
            if (*it == resume) {
                resumes.erase(it);
                return;
            }
        }
        throw std::invalid_argument("list.remove(x): x not in resumes");
    }

    // Note: job_title match is case-insensitive substring;
    // requirements match is case-insensitive exact equality (Python `in` on a list).
    std::vector<Job> search_jobs(const std::string& criteria) const {
        std::vector<Job> matching_jobs;
        const std::string lowered = to_lower(criteria);
        for (const Job& job_listing : job_listings) {
            bool title_match =
                to_lower(job_listing.job_title).find(lowered) != std::string::npos;
            bool req_match = false;
            for (const std::string& r : job_listing.requirements) {
                if (to_lower(r) == lowered) {
                    req_match = true;
                    break;
                }
            }
            if (title_match || req_match) {
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

private:
    static std::string to_lower(std::string s) {
        std::transform(s.begin(), s.end(), s.begin(),
                       [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
        return s;
    }
};