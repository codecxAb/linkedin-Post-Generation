from crewai import Agent
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from tools import scraping_tool, cv_matching_tool, email_tool

# Google Gemini LLM Configuration
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Agent 1: Scraping agent for job posts
scraping_agent = Agent(
    role="Job Scraper",
    goal="Extract job details (title, company, skills) from job post {job_post_url}.",
    verbose=True,
    memory=False,
    backstory="You are a skilled web scraper that extracts detailed job post data efficiently.",
    tools=[scraping_tool],  # Ensure scraping_tool is provided
    llm=llm,
    allow_delegation=True
)

# Agent 2: CV Matching agent
matching_agent = Agent(
    role="CV Matcher",
    goal="Match relevant CV skills and projects to the job post.",
    verbose=True,
    memory=False,
    backstory="You are an expert in analyzing CVs and matching them with job descriptions to identify key strengths.",
    tools=[cv_matching_tool],  # Ensure cv_matching_tool is provided
    llm=llm,
    allow_delegation=True
)

# Agent 3: Cold Email Writer agent
email_agent = Agent(
    role="Email Writer",
    goal="Compose a professional cold email tailored to the job post using matched skills and projects.",
    verbose=True,
    memory=False,
    backstory="You are a skilled writer, specializing in crafting professional and personalized emails for job applications.",
    tools=[email_tool],  # Ensure email_tool is provided
    llm=llm,
    allow_delegation=False
)
