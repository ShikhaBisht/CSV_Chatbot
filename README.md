# CSV_Chatbot

CHATCSV: AI-Powered CSV Chatbot

Objective:
This project implements an AI-powered chatbot, CHATCSV, designed to assist users in querying CSV data (AI4I 2020 Predictive Maintenance Data in this case) interactively. The bot can answer questions related to CSV data, generate visualizations, and provide data insights in tabular format. The goal is to enhance user experience by allowing easy and insightful interactions with data stored in CSV files.


Step 1: Technology Overview
- **Frameworks and Libraries**:
  - **Python**: Programming language.
  - **LangChain**: For building the conversational agent.
  - **Pandas**: For data manipulation and processing.
  - **Plotly**: For creating interactive visualizations.
  - **Groq**: For using the Groq language model. (In this case -gemma2-9b-it)
  - **Streamlit**: For building the web interface.
  - **Python-dotenv**: For managing environment variables securely.


Step 2: Setup Instructions:
Prerequisites: - Python 3.12.5 or higher.



Step 3: Clone the Repository
1.	Clone the repository to your local machine using the URL:
    ```  https://github.com/ShikhaBisht/CSV_Chatbot.git    ```


Step 4: Create a new branch in your local out of the main branch.


Step 5: Create a Virtual Environment
1. Create and activate a virtual environment to manage dependencies:
    python -m venv myenv
    source myenv/bin/activate  
On Windows, use myenv\Scripts\activate

    
Step 6: Set Up Environment Variables
1. Create a `.env` file in the root directory.
2. Add your **Groq API Key** to the `.env` file:
    ```
    GROQ_API_KEY=your_groq_api_key
    ```


Step 7: Install Dependencies
1. Install the required Python libraries using `pip`:
    pip install -r requirements.txt


Step 8: Run the Application
1. Launch the application using Streamlit:
    ```
    streamlit run streamlit.py
    ```
2. Open the application in your browser, where you can interact with the chatbot and submit queries.



Limitations and Model Comparisons

GEMMA2-9B-IT Model-  Supports only an 8192-token context window, requiring short queries/context. However, it offers faster inferencing compared to other models.
Other Models Tried
1.	LLAMA-3.1-8B-Instant: Extremely slow inference speed.
2.	LLAMA-3.3-70B-Versatile: Frequent rate limit errors encountered.
3.	Mixtral-8x7B-32768: Offers a good context window but provides inconsistent responses.


Contribute:
Feel free to contribute or suggest improvements by opening a pull request!
