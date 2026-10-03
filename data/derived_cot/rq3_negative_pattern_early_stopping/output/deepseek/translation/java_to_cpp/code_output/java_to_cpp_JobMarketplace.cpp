#include <vector>
#include <string>
#include <algorithm>
#include <iterator>
#include <functional>

class JobMarketplace {
public:
    // ----- JobListing -----
    class JobListing {
    public:
        JobListing() = default;
        JobListing(const std::string& title, const std::string& company, const std::vector<std::string>& requirements)
            : title_(title), company_(company), requirements_(requirements) {}

        const std::string& getTitle() const { return title_; }
        const std::string& getCompany() const { return company_; }
        const std::vector<std::string>& getRequirements() const { return requirements_; }

        bool operator==(const JobListing& other) const {
            return title_ == other.title_ &&
                   company_ == other.company_ &&
                   requirements_ == other.requirements_;
        }

        bool operator!=(const JobListing& other) const { return !(*this == other); }

    private:
        std::string title_;
        std::string company_;
        std::vector<std::string> requirements_;
    };

    // ----- Resume -----
    class Resume {
    public:
        Resume() = default;
        Resume(const std::string& name, const std::vector<std::string>& skills, const std::string& experience)
            : name_(name), skills_(skills), experience_(experience) {}

        const std::string& getName() const { return name_; }
        const std::vector<std::string>& getSkills() const { return skills_; }
        const std::string& getExperience() const { return experience_; }

        bool operator==(const Resume& other) const {
            return name_ == other.name_ &&
                   skills_ == other.skills_ &&
                   experience_ == other.experience_;
        }

        bool operator!=(const Resume& other) const { return !(*this == other); }

    private:
        std::string name_;
        std::vector<std::string> skills_;
        std::string experience_;
    };

    // ----- JobMarketplace -----
    JobMarketplace() = default;

    void postJob(const std::string& title, const std::string& company, const std::vector<std::string>& requirements) {
        jobListings_.emplace_back(title, company, requirements);
    }

    void removeJob(const JobListing& job) {
        auto it = std::find(jobListings_.begin(), jobListings_.end(), job);
        if (it != jobListings_.end()) {
            jobListings_.erase(it);
        }
    }

    void submitResume(const std::string& name, const std::vector<std::string>& skills, const std::string& experience) {
        resumes_.emplace_back(name, skills, experience);
    }

    void withdrawResume(const Resume& resume) {
        auto it = std::find(resumes_.begin(), resumes_.end(), resume);
        if (it != resumes_.end()) {
            resumes_.erase(it);
        }
    }

    std::vector<JobListing> searchJobs(const std::string& skill) const {
        std::vector<JobListing> result;
        std::copy_if(jobListings_.begin(), jobListings_.end(), std::back_inserter(result),
            [&skill](const JobListing& job) {
                const auto& reqs = job.getRequirements();
                return std::find(reqs.begin(), reqs.end(), skill) != reqs.end();
            });
        return result;
    }

    std::vector<Resume> getJobApplicants(const JobListing& job) const {
        std::vector<Resume> result;
        std::copy_if(resumes_.begin(), resumes_.end(), std::back_inserter(result),
            [&job](const Resume& resume) {
                return matchesRequirements(resume, job.getRequirements());
            });
        return result;
    }

    static bool matchesRequirements(const Resume& resume, const std::vector<std::string>& requirements) {
        const auto& skills = resume.getSkills();
        if (skills.size() != requirements.size()) return false;
        // Check that every requirement appears in skills (order does not matter)
        return std::all_of(requirements.begin(), requirements.end(),
            [&skills](const std::string& req) {
                return std::find(skills.begin(), skills.end(), req) != skills.end();
            });
    }

    const std::vector<JobListing>& getJobListings() const { return jobListings_; }
    const std::vector<Resume>& getResumes() const { return resumes_; }

private:
    std::vector<JobListing> jobListings_;
    std::vector<Resume> resumes_;
};

// ----- Hash specializations (optional, for compatibility if unordered containers are used later) -----
namespace std {
    template<>
    struct hash<JobMarketplace::JobListing> {
        size_t operator()(const JobMarketplace::JobListing& j) const noexcept {
            size_t h1 = hash<string>{}(j.getTitle());
            size_t h2 = hash<string>{}(j.getCompany());
            size_t h3 = 0;
            for (const auto& req : j.getRequirements()) {
                h3 ^= hash<string>{}(req) + 0x9e3779b9 + (h3 << 6) + (h3 >> 2);
            }
            return h1 ^ (h2 << 1) ^ (h3 << 2);
        }
    };

    template<>
    struct hash<JobMarketplace::Resume> {
        size_t operator()(const JobMarketplace::Resume& r) const noexcept {
            size_t h1 = hash<string>{}(r.getName());
            size_t h2 = 0;
            for (const auto& skill : r.getSkills()) {
                h2 ^= hash<string>{}(skill) + 0x9e3779b9 + (h2 << 6) + (h2 >> 2);
            }
            size_t h3 = hash<string>{}(r.getExperience());
            return h1 ^ (h2 << 1) ^ (h3 << 2);
        }
    };
}