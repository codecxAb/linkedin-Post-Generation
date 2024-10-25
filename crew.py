from crewai import Crew, Process
from tasks import scrape_job_task, match_cv_task, write_email_task

# Creating the crew with agents and tasks
crew = Crew(
    agents=[scrape_job_task.agent, match_cv_task.agent, write_email_task.agent],
    tasks=[scrape_job_task, match_cv_task, write_email_task],
    process=Process.sequential  # Tasks will be executed one after another
)

# Start the process with a sample job post URL
result = crew.kickoff(inputs={'job_post_url': 'https://www.linkedin.com/jobs/view/123456789'})
