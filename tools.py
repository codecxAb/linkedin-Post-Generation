from crewai_tools import ScrapeWebsiteTool

# Initialize the tool
tool = ScrapeWebsiteTool(website_url='https://jobs.apple.com/en-in/details/200524442/full-stack-developer')

# Extract the text from the site
text = tool.run()
print(text)

import os

from groq import Groq

client = Groq(
    api_key= "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"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "write a cold mail for the job post"+text+"according to the job post"
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)