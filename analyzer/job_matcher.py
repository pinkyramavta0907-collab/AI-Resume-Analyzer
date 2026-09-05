from .skill_extractor import extract_skills


def calculate_match(resume_skills, job_description):

    job_skills = extract_skills(job_description)

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matching_skills = sorted(
        resume_set.intersection(job_set)
    )

    missing_skills = sorted(
        job_set - resume_set
    )

    if len(job_set) == 0:

        match_percentage = 0

    else:

        match_percentage = round(
            (len(matching_skills) / len(job_set)) * 100
        )

    return {
        "match_percentage": match_percentage,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "job_skills": sorted(job_set)
    }