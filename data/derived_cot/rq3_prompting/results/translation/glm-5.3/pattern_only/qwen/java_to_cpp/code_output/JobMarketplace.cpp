#include <algorithm>
#include <cstdint>
#include <string>
#include <utility>
#include <vector>

namespace org {
namespace example {

namespace {
// Java String#hashCode (32-bit wraparound semantics)
std::int32_t javaStringHashCode(const std::string& s) {
    std::uint32_t h = 0;
    for (char c : s) {
        h = 31u * h + static_cast<std::uint8_t>(c);
    }
    return static_cast<std::int32_t>(h);
}

// Java List#hashCode (result = 31 * result + element.hashCode())
std::int32_t javaListHashCode(const std::vector<std::string>& list) {
    std::uint32_t result = 1;
    for (const std::string& element : list) {
        result = 31u * result + static_cast<std::uint32_t>(javaStringHashCode(element));
    }
    return static_cast<std::int32_t>(result);
}
}  // namespace

class JobMarketplace {
public:
    class JobListing {
    public:
        JobListing(std::string title, std::string company, std::vector<std::string> requirements)
            : title(std::move(title)), company(std::move(company)), requirements(std::move(requirements)) {}

        const std::string& getTitle() const { return title; }
        const std::string& getCompany() const { return company; }
        const std::vector<std::string>& getRequirements() const { return requirements; }

        bool operator==(const JobListing& other) const {
            return title == other.title && company == other.company && requirements == other.requirements;
        }
        bool operator!=(const JobListing& other) const { return !(*this == other); }

        std::int32_t hashCode() const {
            std::uint32_t result = static_cast<std::uint32_t>(javaStringHashCode(title));
            result = 31u * result + static_cast<std::uint32_t>(javaStringHashCode(company));
            result = 31u * result + static_cast<std::uint32_t>(javaListHashCode(requirements));
            return static_cast<std::int32_t>(result);
        }

    private:
        std::string title;
        std::string company;
        std::vector<std::string> requirements;
    };

    class Resume {
    public:
        Resume(std::string name, std::vector<std::string> skills, std::string experience)
            : name(std::move(name)), skills(std::move(skills)), experience(std::move(experience)) {}

        const std::string& getName() const { return name; }
        const std::vector<std::string>& getSkills() const { return skills; }
        const std::string& getExperience() const { return experience; }

        bool operator==(const Resume& other) const {
            return name == other.name && skills == other.skills && experience == other.experience;
        }
        bool operator!=(const Resume& other) const { return !(*this == other); }

        std::int32_t hashCode() const {
            std::uint32_t result = static_cast<std::uint32_t>(javaStringHashCode(name));
            result = 31u * result + static_cast<std::uint32_t>(javaListHashCode(skills));
            result = 31u * result + static_cast<std::uint32_t>(javaStringHashCode(experience));
            return static_cast<std::int32_t>(result);
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

    void removeJob(const JobListing& job) {
        // java.util.List#remove(Object) removes only the first matching element.
        auto it = std::find_if(jobListings.begin(), jobListings.end(),
                               [&job](const JobListing& j) { return j == job; });
        if (it != jobListings.end()) {
            jobListings.erase(it);
        }
    }

    void submitResume(const std::string& name, const std::vector<std::string>& skills,
                      const std::string& experience) {
        resumes.emplace_back(name, skills, experience);
    }

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
        if (resume.getSkills().size() != requirements.size()) {
            return false;
        }
        // java.util.List#containsAll (per-element membership)
        for (const std::string& req : requirements) {
            const std::vector<std::string>& skills = resume.getSkills();
            if (std::find(skills.begin(), skills.end(), req) == skills.end()) {
                return false;
            }
        }
        return true;
    }

    std::vector<JobListing>& getJobListings() { return jobListings; }
    const std::vector<JobListing>& getJobListings() const { return jobListings; }

    std::vector<Resume>& getResumes() { return resumes; }
    const std::vector<Resume>& getResumes() const { return resumes; }

private:
    std::vector<JobListing> jobListings;
    std::vector<Resume> resumes;
};

}  // namespace example
}  // namespace org