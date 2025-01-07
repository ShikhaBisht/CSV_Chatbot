#importing all the dependencies
import os
import pandas as pd
import json
from langchain_groq import ChatGroq
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv

load_dotenv()
groq_api_key= os.getenv('GROQ_API_KEY')

    
def preprocess_csv_data(file_path):
    """Preprocess the CSV file to ensure clean and usable data."""
    
    df = pd.read_csv(file_path)

    # Removing leading/trailing whitespaces in column names
    df.columns = df.columns.str.strip()

    # Replacing spaces and special characters in column names with underscores
    df.columns = df.columns.str.replace(r"[^\w\s]", "_", regex=True).str.replace(r"\s+", "_", regex=True)

    # Convert all column names to lowercase for uniformity
    df.columns = df.columns.str.lower()

    return df




def query_agent(query):
    """
    Query the agent and return the response as a string.

    Args:
        query: The input query to ask the agent.

    Returns:
        The response from the agent as a string.
    """


    df=preprocess_csv_data('data.csv')

    #Initialising the llm
    llm= ChatGroq(api_key=groq_api_key, model="gemma2-9b-it", temperature=0.0)

    #Initialising the agent
    agent= create_pandas_dataframe_agent(
        llm,
        df,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        allow_dangerous_code=True
        )
    

    prompt = (
        """
    
            You are a helpful assistant trained to respond to the following query related to given dataframe. 
            Always be polite and ask for clarification if needed.

            For the following query, if it requires drawing a table, reply as follows:
            {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

            If the query requires creating a bar chart, reply as follows:
            {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires creating a line chart, reply as follows:
            {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires creating a pie chart, reply as follows:
            {"pie": {"labels": ["A", "B", "C", ...], "values": [25, 24, 10, ...]}}


            There can only be these types of chart: "bar", "line" and "pie".

            If it is just asking a question that requires neither, reply as follows:
            {"answer": "answer"}
            Example:
            {"answer": "The title with the highest rating is 'Gilead'"}

            Remember to strictly use double quotes("") only in the final answer and everywhere else. Do not use anything else.

            All strings in "columns" list and data list, should be in double quotes,

            For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

            Lets think step by step.

            Below is the query.
            Query: 
            """
        + query
    )


    # Passing the prompt through the agent.
    response = agent.run(prompt)

    # print("Raw response:", response)
    # print(type(response))

    return str(response)




def convert_response(response: str) -> dict:
    """This function converts the string response from the model/agent to a dictionary.

    Args:
        response (str): response from the model/agent

    Returns:
        dict: dictionary with response data
    """
    # print(response)
    # print(type(response))
    return json.loads(response)







