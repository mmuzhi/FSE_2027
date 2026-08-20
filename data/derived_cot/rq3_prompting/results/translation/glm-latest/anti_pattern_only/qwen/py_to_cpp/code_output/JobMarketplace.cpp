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
            return job_title == other.job_title
                && company == other.company
                && requirements == other.requirements;
        }
    };

    struct Resume {
        std::string name;
        std::vector<std::string> skills;
        std::string experience;

        bool operator==(const Resume& other) const {
            return name == other.name
                && skills == other.skills
                && experience == other.experience;
        }
    };

    std::vector<Job> job_listings;
    std::vector<Resume> resumes;

    // Publish a position: appends it to job_listings.
    void post_job(const std::string& job_title, const std::string& company,
                  const std::vector<std::string>& requirements) {
        Job job{job_title, company, requirements};
        job_listings.push_back(job);
    }

    // Remove the first job equal to `job` from job_listings.
    // Throws if not present (mirrors Python's ValueError from list.remove).
    void remove_job(const Job& job) {
        auto it = std::find(job_listings.begin(), job_listings.end(), job);
        if (it == job_listings.end()) {
            throw std::invalid_argument("list.remove(x): x not in list");
        }
        job_listings.erase(it);
    }

    // Submit a resume: appends it to resumes.
    void submit_resume(const std::string& name, const std::vector<std::string>& skills,
                       const std::string& experience) {
        Resume resume{name, skills, experience};
        resumes.push_back(resume);
    }

    // Remove the first resume equal to `resume` from resumes.
    // Throws if not present (mirrors Python's ValueError from list.remove).
    void withdraw_resume(const Resume& resume) {
        auto it = std::find(resumes.begin(), resumes.end(), resume);
        if (it == resumes.end()) {
            throw std::invalid_argument("list.remove(x): x not in list");
        }
        resumes.erase(it);
    }

    // Return job listings whose title contains `criteria` (case-insensitive)
    // or whose requirements contain an entry equal to `criteria` (case-insensitive).
    std::vector<Job> search_jobs(const std::string& criteria) const {
        std::vector<Job> matching_jobs;
        const std::string criteria_lower = to_lower(criteria);
        for (const Job& job_listing : job_listings) {
            bool matches = to_lower(job_listing.job_title).find(criteria_lower)
                           != std::string::npos;
            if (!matches) {
                for (const std::string& r : job_listing.requirements) {
                    if (to_lower(r) == criteria_lower) {
                        matches = true;
                        break;
                    }
                }
            }
            if (matches) {
                matching_jobs.push_back(job_listing);
            }
        }
        return matching_jobs;
    }

    // Return resumes whose skills all appear in the job's requirements.
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
            if (std::find(requirements.begin(), requirements.end(), skill)
                    == requirements.end()) {
                return false;
            }
        }
        return true;
    }

private:
    static std::string to_lower(const std::string& s) {
        std::string result(s);
        std::transform(result.begin(), result.end(), result.begin(),
                       [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
        return result;
    }
};