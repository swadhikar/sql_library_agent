import os
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy import create_engine

from dotenv import load_dotenv

if load_dotenv("./../.env"):
    print(f'Loaded env file')

# Initialize database
db = SQLDatabase.from_uri('sqlite:///library.db')

# OpenAI model
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
# llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0)

# toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# agent
agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)


def ask_question(question: str) -> str:
    try:
        return agent.run(question)
    except Exception as e:
        return f"error: {str(e)}"
