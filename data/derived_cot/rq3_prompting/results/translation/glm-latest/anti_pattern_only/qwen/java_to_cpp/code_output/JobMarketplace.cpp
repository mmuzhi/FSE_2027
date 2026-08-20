#include <algorithm>
#include <string>
#include <utility>
#include <vector>

namespace org {
namespace example {

class JobMarketplace {
public:
    class JobListing {
    public:
        JobListing(std::string title, std::string company, std::vector<std::string> requirements)
            : title(std::move(title)),
              company(std::move(company)),
              requirements(std::move(requirements)) {}

        const std::string& getTitle() const {
            return title;
        }

        const std::string& getCompany() const {
            return company;
        }

        std::vector<std::string>& getRequirements() {
            return requirements;
        }

        const std::vector<std::string>& getRequirements() const {
            return requirements;
        }

        bool operator==(const JobListing& other) const {
            return title == other.title
                && company == other.company
                && requirements == other.requirements;
        }

        bool operator!=(const JobListing& other) const {
            return !(*this == other);
        }

    private:
        std::string title;
        std::string company;
        std::vector<std::string> requirements;
    };

    class Resume {
    public:
        Resume(std::string name, std::vector<std::string> skills, std::string experience)
            : name(std::move(name)),
              skills(std::move(skills)),
              experience(std::move(experience)) {}

        const std::string& getName() const {
            return name;
        }

        std::vector<std::string>& getSkills() {
            return skills;
        }

        const std::vector<std::string>& getSkills() const {
            return skills;
        }

        const std::string& getExperience() const {
            return experience;
        }

        bool operator==(const Resume& other) const {
            return name == other.name
                && skills == other.skills
                && experience == other.experience;
        }

        bool operator!=(const Resume& other) const {
            return !(*this == other);
        }

    private:
        std::string name;
        std::vector<std::string> skills;
        std::string experience;
    };

    JobMarketplace() = default;

    void postJob(const std::string& title, const std::string& company,
                 const std::vector<std::string>& requirements) {
        jobListings.emplace_back(title, company, requirements);
    }

    // Mirrors Java's List.remove(Object): removes the FIRST element equal to `job`.
    void removeJob(const JobListing& job) {
        auto it = std::find(jobListings.begin(), jobListings.end(), job);
        if (it != jobListings.end()) {
            jobListings.erase(it);
        }
    }

    void submitResume(const std::string& name, const std::vector<std::string>& skills,
                      const std::string& experience) {
        resumes.emplace_back(name, skills, experience);
    }

    // Mirrors Java's List.remove(Object): removes the FIRST element equal to `resume`.
    void withdrawResume(const Resume& resume) {
        auto it = std::find(resumes.begin(), resumes.end(), resume);
        if (it != resumes.end()) {
            resumes.erase(it);
        }
    }

    std::vector<JobListing> searchJobs(const std::string& skill) const {
        std::vector<JobListing> result;
        for (const JobListing& job : jobListings) {
            const std::vector<std::string>& requirements = job.getRequirements();
            if (std::find(requirements.begin(), requirements.end(), skill) != requirements.end()) {
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

    // Exact equivalent of:
    // skills.size() == requirements.size() && skills.containsAll(requirements)
    // (per-element containment, NOT set equality, so duplicate handling matches Java)
    bool matchesRequirements(const Resume& resume,
                             const std::vector<std::string>& requirements) const {
        const std::vector<std::string>& skills = resume.getSkills();
        if (skills.size() != requirements.size()) {
            return false;
        }
        for (const std::string& requirement : requirements) {
            if (std::find(skills.begin(), skills.end(), requirement) == skills.end()) {
                return false;
            }
        }
        return true;
    }

    std::vector<JobListing>& getJobListings() {
        return jobListings;
    }

    const std::vector<JobListing>& getJobListings() const {
        return jobListings;
    }

    std::vector<Resume>& getResumes() {
        return resumes;
    }

    const std::vector<Resume>& getResumes() const {
        return resumes;
    }

private:
    std::vector<JobListing> jobListings;
    std::vector<Resume> resumes;
};

}  // namespace example
}  // namespace org