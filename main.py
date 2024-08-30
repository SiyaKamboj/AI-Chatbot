#to run this, cd into LinkedinChatbot and type ' source langchain-env/bin/activate '. Then, run python3 main.py
import os
from langchain_openai import OpenAI
#import openai
from langchain.prompts import PromptTemplate
import time
from flask import Flask, render_template, request, jsonify

openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

prompt = open('pdf-text.txt', 'r').read()

chatbot_template = prompt + """
You are a chatbot for Triton Teleivison (aka TTV), UC San Diego's student-run film studio". 
Your expertise is exclusively in providing information and advice about anything related to Triton Teleivsion. 
This includes any general TTV related queries. In this case, I have only trained you on information about the positional hierarchy of TTV and how to get involved; however, in the future, I will train you information on our equipment inventory so that you can assist people who have questions about what equipment to check out.
You do not provide information outside of this scope. 
If a question is not about TTV, respond with, "I can't assist you with that, sorry! Please only ask me about TTV." 
Question: {question} 
Answer: 
"""

chatbot_prompt_template = PromptTemplate( 
    input_variables=["question"], 
    template=chatbot_template 
    ) 

llm = OpenAI(api_key=openai_api_key, model='gpt-3.5-turbo-instruct', temperature=0)

llm_chain = chatbot_prompt_template | llm 

def query_llm(question): 
    try:
        response = llm_chain.invoke({'question': question})
        #print(response)
        return response
    except OpenAI.error.RateLimitError as e:
        print("Rate limit exceeded. Retrying after a delay...")
        time.sleep(60)  # Wait for 60 seconds before retrying
        query_llm(question)
    except Exception as e:
        print(f"An error occurred: {e}")

# while True:
#     user_input = input("Enter your question: ")
#     query_llm(user_input)

app=Flask(__name__)

#define route for root URL
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data=request.get_json()
    question=data["question"]
    response=query_llm(question)
    return jsonify({"response" : response})

if __name__=="__main__":
    app.run(debug=True)