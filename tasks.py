from crewai import Task
from agents import scraping_agent, matching_agent, email_agent
from tools import scraping_tool, cv_matching_tool, email_tool

# Task 1: Scrape job post data
scrape_job_task = Task(
    description=(
        "Scrape job post details from {job_post_url}."
        "Extract job title, company, skills required, and description."
    ),
    expected_output='Job post data (title, company, skills, etc.)',
    tools=[scraping_tool],
    agent=scraping_agent,
    async_execution=False  # Synchronous task execution
)

# Task 2: Match CV with job post
match_cv_task = Task(
    description=(
        "Match the relevant skills and projects from the CV with the job post."
        "Use the scraped data and CV to find skill matches."
    ),
    expected_output='Matched skills and projects from CV',
    tools=[cv_matching_tool],
    agent=matching_agent,
    async_execution=False
)

# Task 3: Write cold email
write_email_task = Task(
    description=(
        "Generate a cold email using the matched skills and projects."
        "The email should highlight the candidate's qualifications for the job."
    ),
    expected_output='Cold email content',
    tools=[email_tool],
    agent=email_agent,
    async_execution=False
)
