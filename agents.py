import os
from dotenv import load_dotenv
from groq import Groq
from crewai_tools import ScrapeWebsiteTool

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key and website URL from environment variables
groq_api = os.getenv("GROQ_API_KEY")

# Initialize the tool
tool = ScrapeWebsiteTool(website_url='https://jobs.apple.com/en-in/details/200524442/full-stack-developer')

# Extract the text from the site
text = tool.run()

client = Groq(api_key=groq_api)
cv_summery= """cv content"""

chat_completion = client.chat.completions.create(
    #
    # Required parameters
    #
    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": "scrape the data from the job post"+text+"and write a cold mail for the job post according to the job post"+"according to the cv summery"+cv_summery,
        }
        
    ],


    # The language model which will generate the completion.
    model="llama3-8b-8192",

    #
    # Optional parameters
    #

    # Controls randomness: lowering results in less random completions.
    # As the temperature approaches zero, the model will become deterministic
    # and repetitive.
    temperature=0.5,

    # The maximum number of tokens to generate. Requests can use up to
    # 32,768 tokens shared between prompt and completion.
    max_tokens=1024,

    # Controls diversity via nucleus sampling: 0.5 means half of all
    # likelihood-weighted options are considered.
    top_p=1,

    # A stop sequence is a predefined or user-specified text string that
    # signals an AI to stop generating content, ensuring its responses
    # remain focused and concise. Examples include punctuation marks and
    # markers like "[end]".
    stop=None,

    # If set, partial message deltas will be sent.
    stream=False,
)

# Print the completion returned by the LLM.
print(chat_completion.choices[0].message.content)