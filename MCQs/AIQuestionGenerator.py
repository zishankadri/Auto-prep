from tika import parser
import openai
from django.conf import settings


# Configure OpenAI API key
openai.api_key = settings.API_KEY


# Function to get response from OpenAI GPT-3.5 engine 
def get_gpt_response(promt:str, engine="gpt-3.5-turbo-instruct"):
    return openai.Completion.create(
        engine=engine,  # text-davinci-003 Or another GPT-3.5 engine
        prompt=promt,
        max_tokens=50  # Maximum tokens in the response
    )

def summarize(content):
    response = get_gpt_response(f'''
        You are given a string variable containing a full chapter you need to impliment principals which make a great MCQ type question and generate 1 good question 
        questions and answers should preferably be under 10 words
        Return the result as a single string that I can split usinag the '|' character in Python.
        your output should strictly follow this following example without any \n (newline characters)
        format =  Question | option A | option B | option C | option D | Correct option                               
        example = what is the color of a chick? | Blue | Green | Yellow | Red | C

        string variable = "{content}"
    ''')

    return response['choices'][0]['text']


def get_question_from_pdf(file_url):
    raw = parser.from_file(file_url)
    summary = summarize(raw['content'])
    summary = summary.split('|')
    print("summary: ", summary)
    return summary
    
# get_question_from_pdf("/home/zishan/Documents/CIA-RDP96-00788R001200060018-5.pdf")