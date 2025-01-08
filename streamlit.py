import streamlit as st
import pandas as pd
import plotly.express as px
import logging

from Agent import query_agent, convert_response



def write_final_response(response_dict: dict):
    """
    Write the final response from the agent to the Streamlit app.

    Args:
        response_dict: The response dict from the agent.

    Returns:
        None.
    """


    # Check if the response is an answer.
    # if "answer" in response_dict:
    #     st.write(response_dict["answer"])

    # If the "answer" key doesn't exist, dynamically get the first available key and its value.
    # else:
    #     value = next(iter(response_dict.values()))
    #     st.write(value)


    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        x_label = "columns"  
        y_label = "data"     
        title = f"Bar Chart: {x_label} vs {y_label}"
        fig = px.bar(
            df, 
            x=x_label, 
            y=y_label, 
            title=title, 
            labels={x_label: x_label.capitalize(), y_label: y_label.capitalize()}
        )
        st.plotly_chart(fig, use_container_width=True)


    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        x_label = "columns"  
        y_label = "data"    
        title = f"Line Chart: {x_label} vs {y_label}"
        fig = px.line(
            df, 
            x=x_label, 
            y=y_label, 
            title=title, 
            labels={x_label: x_label.capitalize(), y_label: y_label.capitalize()}
        )
        st.plotly_chart(fig, use_container_width=True)



    # Check if the response is a pie chart.
    if "pie" in response_dict:
        data = response_dict["pie"]
        df = pd.DataFrame({"labels": data["labels"], "values": data["values"]})
        labels_key = "labels"
        values_key = "values"
        title = f"Pie Chart: {labels_key.capitalize()} Distribution"
        fig = px.pie(
            df, 
            names=labels_key, 
            values=values_key, 
            title=title
        )
        st.plotly_chart(fig, use_container_width=True)


    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)

    else:
        value = next(iter(response_dict.values()))
        st.write(value)    





st.set_page_config(page_title="CHATCSV 🤖📈")

st.title("CHATCSV 🤖📈")
st.header("Hi! I am your CSV bot.")


# Description to help users understand how to interact with the bot.
st.markdown("""
    I can help you answer questions related to the AI4I 2020 Predictive Maintenance Data along with tables and visualizations.

    **Example Queries:**
    - "What is the average of column X?"
    - "Show rows where 'Machine Type' is 'H'."
    - "Generate a bar chart for 'column Y'."
    - "What is the distribution of 'Column A'?"
""")


#Taking input
query = st.text_input("Enter your query:")


if st.button("Submit Query", type="primary"):
    if not query:
        st.warning("Please enter a query.")  # Warning if no query is entered.
    else:
        # Showing loading spinner while processing the query.
        with st.spinner('Processing your query...'):
            try:
                # Query the agent.
                response = query_agent(query)

                converted_response = convert_response(response)

                st.write("Your Answer:")

                # Write the final response to the Streamlit app.
                write_final_response(converted_response)

            except Exception as e:
                # Log the exception to the terminal for debugging
                logging.error("Error processing the response: %s", e)

                # Check if the error is a rate limit exceeded error (error code 413)
                if "Request too large" in str(e):
                    st.error("Your request is too large for the model's current token limit. Please try again with a smaller context.")
                
                # Check if the error is a rate limit exceeded error (error code 429)
                elif "Rate limit reached" in str(e):
                    st.error("You have exceeded the rate limit. Please try again later.")

                else:
                    # For other errors, show a general message
                    st.error("Oops! Something went wrong while processing your query. Please try again later.")