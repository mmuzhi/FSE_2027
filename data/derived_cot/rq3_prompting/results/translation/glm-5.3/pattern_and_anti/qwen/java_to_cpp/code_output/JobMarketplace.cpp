#include <string>
#include <vector>
#include <algorithm>
#include <cstddef>

class JobMarketplace {
public:
    class JobListing {
    public:
        JobListing(std::string title, std::string company, std::vector<std::string> requirements)
            : title_(std::move(title)), company_(std::move(company)), requirements_(std::move(requirements)) {}

        const std::string& getTitle() const { return title_; }
        const std::string& getCompany() const { return company_; }
        std::vector<std::string>& getRequirements() { return requirements_; }
        const std::vector<std::string>& getRequirements() const { return requirements_; }

        bool operator==(const JobListing& other) const {
            return title_ == other.title_
                && company_ == other.company_
                && requirements_ == other.requirements_;
        }

        bool operator!=(const JobListing& other) const {
            return !(*this == other);
        }

    private:
        std::string title_;
        std::string company_;
        std::vector<std::string> requirements_;
    };

    class Resume {
    public:
        Resume(std::string name, std::vector<std::string> skills, std::string experience)
            : name_(std::move(name)), skills_(std::move(skills)), experience_(std::move(experience)) {}

        const std::string& getName() const { return name_; }
        std::vector<std::string>& getSkills() { return skills_; }
        const std::vector<std::string>& getSkills() const { return skills_; }
        const std::string& getExperience() const { return experience_; }

        bool operator==(const Resume& other) const {
            return name_ == other.name_
                && skills_ == other.skills_
                && experience_ == other.experience_;
        }

        bool operator!=(const Resume& other) const {
            return !(*this == other);
        }

    private:
        std::string name_;
        std::vector<std::string> skills_;
        std::string experience_;
    };

    JobMarketplace() = default;

    void postJob(std::string title, std::string company, std::vector<std::string> requirements) {
        jobListings.emplace_back(std::move(title), std::move(company), std::move(requirements));
    }

    // Mirrors java.util.List#remove(Object): removes only the FIRST element equal to `job`.
    void removeJob(const JobListing& job) {
        auto it = std::find_if(jobListings.begin(), jobListings.end(),
                               [&job](const JobListing& j) { return j == job; });
        if (it != jobListings.end()) {
            jobListings.erase(it);
        }
    }

    void submitResume(std::string name, std::vector<std::string> skills, std::string experience) {
        resumes.emplace_back(std::move(name), std::move(skills), std::move(experience));
    }

    // Mirrors java.util.List#remove(Object): removes only the FIRST element equal to `resume`.
    void withdrawResume(const Resume& resume) {
        auto it = std::find_if(resumes.begin(), resumes.end(),
                               [&resume](const Resume& r) { return r == resume; });
        if (it != resumes.end()) {
            resumes.erase(it);
        }
    }

    std::vector<JobListing> searchJobs(const std::string& skill) const {
        std::vector<JobListing> result;
        for (const JobListing& job : jobListings) {
            const std::vector<std::string>& reqs = job.getRequirements();
            if (std::find(reqs.begin(), reqs.end(), skill) != reqs.end()) {
                result.push_back(job);
            }
        }
        return result;
    }

    std::vector<Resume> getJobApplicants(const JobListing& job) const {
        std::vector<Resume> result;
        for (const Resume& resume : resumes) {
            if (matchesRequirements(resume, job.getRequirements())) {
                result.push_back(resume);
            }
        }
        return result;
    }

    bool matchesRequirements(const Resume& resume, const std::vector<std::string>& requirements) const {
        const std::vector<std::string>& skills = resume.getSkills();
        if (skills.size() != requirements.size()) {
            return false;
        }
        // Mirrors List#containsAll: every element of `requirements` must be contained in `skills`.
        for (const std::string& req : requirements) {
            if (std::find(skills.begin(), skills.end(), req) == skills.end()) {
                return false;
            }
        }
        return true;
    }

    // Java getters return the live, mutable list; expose both mutable and const views.
    std::vector<JobListing>& getJobListings() { return jobListings; }
    const std::vector<JobListing>& getJobListings() const { return jobListings; }

    std::vector<Resume>& getResumes() { return resumes; }
    const std::vector<Resume>& getResumes() const { return resumes; }

private:
    std::vector<JobListing> jobListings;
    std::vector<Resume> resumes;
};