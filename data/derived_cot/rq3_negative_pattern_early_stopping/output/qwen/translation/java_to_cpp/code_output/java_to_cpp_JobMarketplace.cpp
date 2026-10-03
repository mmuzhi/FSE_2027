#include <vector>
#include <string>
#include <algorithm>

class JobMarketplace {
private:
    std::vector<JobListing> jobListings;
    std::vector<Resume> resumes;

public:
    JobMarketplace() = default;

    void postJob(const std::string& title, const std::string& company, const std::vector<std::string>& requirements) {
        jobListings.emplace_back(title, company, requirements);
    }

    void removeJob(const JobListing& job) {
        auto it = std::find(jobListings.begin(), jobListings.end(), job);
        if (it != jobListings.end()) {
            jobListings.erase(it);
        }
    }

    void submitResume(const std::string& name, const std::vector<std::string>& skills, const std::string& experience) {
        resumes.emplace_back(name, skills, experience);
    }

    void withdrawResume(const Resume& resume) {
        auto it = std::find(resumes.begin(), resumes.end(), resume);
        if (it != resumes.end()) {
            resumes.erase(it);
        }
    }

    std::vector<JobListing> searchJobs(const std::string& skill) const {
        std::vector<JobListing> result;
        for (const auto& job : jobListings) {
            if (std::find(job.requirements.begin(), job.requirements.end(), skill) != job.requirements.end()) {
                result.push_back(job);
            }
        }
        return result;
    }

    std::vector<Resume> getJobApplicants(const JobListing& job) const {
        std::vector<Resume> result;
        for (const auto& resume : resumes) {
            if (matchesRequirements(resume, job.requirements)) {
                result.push_back(resume);
            }
        }
        return result;
    }

    const std::vector<JobListing>& getJobListings() const { return jobListings; }
    const std::vector<Resume>& getResumes() const { return resumes; }

    static bool matchesRequirements(const Resume& resume, const std::vector<std::string>& requirements) {
        if (resume.skills.size() != requirements.size()) return false;
        return std::all_of(requirements.begin(), requirements.end(),
            [&resume](const std::string& req) { return std::find(resume.skills.begin(), resume.skills.end(), req) != resume.skills.end(); });
    }

    // Nested classes
    class JobListing {
    public:
        std::string title;
        std::string company;
        std::vector<std::string> requirements;

        JobListing(const std::string& title, const std::string& company, const std::vector<std::string>& requirements)
            : title(title), company(company), requirements(requirements) {}

        bool operator==(const JobListing& other) const {
            return title == other.title && company == other.company && requirements == other.requirements;
        }
    };

    class Resume {
    public:
        std::string name;
        std::vector<std::string> skills;
        std::string experience;

        Resume(const std::string& name, const std::vector<std::string>& skills, const std::string& experience)
            : name(name), skills(skills), experience(experience) {}

        bool operator==(const Resume& other) const {
            return name == other.name && skills == other.skills && experience == other.experience;
        }
    };
};