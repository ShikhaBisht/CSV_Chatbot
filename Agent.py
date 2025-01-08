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
        allow_dangerous_code=True,
        agent_executor_kwargs={"handle_parsing_errors": True}
        )
    

    prompt = (
        """
    
            You are a Chatbot assistant trained to respond to the following query related to given dataframe in an interactive manner. 
            Always be polite and ask for clarification if needed.

            If the query requires creating a bar chart then do the same and follow the below format:
            {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires creating a line chart then do the same and follow the below format:
            {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires creating a pie chart then do the same and follow the below format:
            {"pie": {"labels": ["A", "B", "C", ...], "values": [25, 24, 10, ...]}}


            There can only be these types of chart: "bar", "line" and "pie".

            else for any query related to the dataframe, if it can be displyed in a table then do the same and follow the below format:
            {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}


            If it is just asking a question that requires none of the above, follow the below format:
            {"answer": "answer"}
            Example:
            {"answer": "The correlation between torque and machine failure is 0.12."}


            All strings in "keys" list and "data" list, should be in double quotes,

            For example: {"columns": ["uid", "type"], "data": [[1, "L"], [2, "M"]]}

            Lets think step by step: Thoughts, Action and then Final Answer. Remember to strictly use only double quotes("") in the final answer and everywhere else. Do not use anything else.


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







