#include <vector>
#include <string>
#include <memory>
#include <algorithm>

class JobMarketplace {
public:
    class JobListing {
    private:
        std::string title;
        std::string company;
        std::vector<std::string> requirements;

    public:
        JobListing(const std::string& title, const std::string& company,
                   const std::vector<std::string>& requirements)
            : title(title), company(company), requirements(requirements) {}

        const std::string& getTitle() const { return title; }
        const std::string& getCompany() const { return company; }
        std::vector<std::string>& getRequirements() { return requirements; }
        const std::vector<std::string>& getRequirements() const { return requirements; }

        bool operator==(const JobListing& other) const {
            return title == other.title && company == other.company && requirements == other.requirements;
        }
    };

    class Resume {
    private:
        std::string name;
        std::vector<std::string> skills;
        std::string experience;

    public:
        Resume(const std::string& name, const std::vector<std::string>& skills,
               const std::string& experience)
            : name(name), skills(skills), experience(experience) {}

        const std::string& getName() const { return name; }
        std::vector<std::string>& getSkills() { return skills; }
        const std::vector<std::string>& getSkills() const { return skills; }
        const std::string& getExperience() const { return experience; }

        bool operator==(const Resume& other) const {
            return name == other.name && skills == other.skills && experience == other.experience;
        }
    };

private:
    std::vector<std::shared_ptr<JobListing>> jobListings;
    std::vector<std::shared_ptr<Resume>> resumes;

public:
    JobMarketplace() = default;

    void postJob(const std::string& title, const std::string& company,
                 const std::vector<std::string>& requirements) {
        jobListings.push_back(std::make_shared<JobListing>(title, company, requirements));
    }

    void removeJob(const JobListing& job) {
        auto it = std::find_if(jobListings.begin(), jobListings.end(),
            [&](const std::shared_ptr<JobListing>& ptr) { return *ptr == job; });
        if (it != jobListings.end()) {
            jobListings.erase(it);
        }
    }

    void submitResume(const std::string& name, const std::vector<std::string>& skills,
                      const std::string& experience) {
        resumes.push_back(std::make_shared<Resume>(name, skills, experience));
    }

    void withdrawResume(const Resume& resume) {
        auto it = std::find_if(resumes.begin(), resumes.end(),
            [&](const std::shared_ptr<Resume>& ptr) { return *ptr == resume; });
        if (it != resumes.end()) {
            resumes.erase(it);
        }
    }

    std::vector<std::shared_ptr<JobListing>> searchJobs(const std::string& skill) const {
        std::vector<std::shared_ptr<JobListing>> result;
        for (const auto& ptr : jobListings) {
            const auto& reqs = ptr->getRequirements();
            if (std::find(reqs.begin(), reqs.end(), skill) != reqs.end()) {
                result.push_back(ptr);
            }
        }
        return result;
    }

    std::vector<std::shared_ptr<Resume>> getJobApplicants(const JobListing& job) const {
        std::vector<std::shared_ptr<Resume>> result;
        for (const auto& ptr : resumes) {
            if (matchesRequirements(*ptr, job.getRequirements())) {
                result.push_back(ptr);
            }
        }
        return result;
    }

    bool matchesRequirements(const Resume& resume, const std::vector<std::string>& requirements) const {
        const auto& skills = resume.getSkills();
        if (skills.size() != requirements.size()) {
            return false;
        }
        for (const auto& req : requirements) {
            if (std::find(skills.begin(), skills.end(), req) == skills.end()) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::shared_ptr<JobListing>>& getJobListings() {
        return jobListings;
    }

    std::vector<std::shared_ptr<Resume>>& getResumes() {
        return resumes;
    }
};