import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import streamlit as st
from langfuse import get_client, observe
import ast

class GeminiModel:
    def __init__(self, modelID="gemini-2.5-flash"):
        load_dotenv() 
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.langfuse_api_key = os.getenv("LANGFUSE_API_KEY")

        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
        
        if not self.langfuse_api_key:
            raise ValueError("LANGFUSE_API_KEY is not set in environment variables.")
        
        self.client = genai.Client(api_key=self.google_api_key)
        langfuse = get_client()
        self.modelID = modelID
        self.safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_MEDIUM_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_MEDIUM_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_MEDIUM_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_MEDIUM_AND_ABOVE",
            ),
        ]


    def check_prompt_safety(self, contents):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0,
                max_output_tokens=1,
                safety_settings=self.safety_settings,
            )
        )
        safety_categories = []
        candidate = response.candidates[0]
        if candidate.finish_reason == types.FinishReason.SAFETY:
            for rating in candidate.safety_ratings:
                if rating.blocked:
                    safety_categories.append(rating.category)
        
        return safety_categories


    @observe()
    def generate_response(self, contents, temperature=0.1, max_output_tokens=10000):
        response = self.client.models.generate_content(
            model=self.modelID,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                safety_settings=self.safety_settings,
            )
        )

        return response.text
        

    def generate_database(self, ddl_schema, prompt="", temperature=0.5, max_output_tokens=10000):
        generate_database_prompt = [
            "Generate a SQL database data based on the following DDL schema."
            "Include data types, null values, date and time formats, primary and foreign keys, unique, etc. "
            "Respond ONLY with the SQL INSERT statements. Do not include any explanation or commentary.",
            "--- DDL SCHEMA ---",           
            ddl_schema,                     
            "--- USER INSTRACTION/CONTEXT ---",  
            prompt                          
        ]
        return self.generate_response(generate_database_prompt)
        
    

    def extract_important_info_from_edit_prompt(self, user_instructions):
        contents = [
            "Used to extract important information from user instructions for editing a database row.",
            "User instructions: ",
            user_instructions,
            "Given a table name, row data, and user instructions, extract the important information needed to perform an edit on the row.",
            "Respond with a tuple in the format (table_name, row_id, updated_values).",
            "If there are not all three elements in the user instructions, respond with 'INSUFFICIENT INFORMATION' and write which elements are missing.",
            "Do not include any explanation or commentary.",
        ]

        response = self.generate_response(contents)

        try:
            result = ast.literal_eval(response.text)
            if isinstance(result, tuple) and len(result) == 3:
                return result
            else:
                return "INSUFFICIENT INFORMATION: Response is not a valid tuple of (table_name, row_id, updated_values). " + response.text
        except:
            return "INSUFFICIENT INFORMATION: Unable to parse the response. " + response.text
    

    def generate_answer(self, ddl_schema, query, context):
        contents = contents = f"""
            You are an assistant that decides whether the user's request requires DATA or a PLOT. 
            You also generate SQL to retrieve the data. 
            If RESULT_TYPE is PLOT, ALWAYS generate Python code using pandas and seaborn to visualize the result.

            Your response must strictly follow this python tuple format:
            (DATA|PLOT, short description for the user, sql query, python code if PLOT, otherwise None)

            Rules:
            1. RESULT_TYPE must be either DATA or PLOT or TEXT.
            2. Choose PLOT when the user asks about trends, comparisons, relationships, or visualizations.
            3. Choose DATA when the user asks for specific numbers or tables.
            4. Choose TEXT if user asks about something not connected with database.
            4. SQL must be valid and executable.
            5. If RESULT_TYPE is PLOT:
                - Do NOT execute SQL in the Python code.
                - Use the variable `df` which contains the result of the SQL query as a pandas DataFrame.
                - Use seaborn and matplotlib for plotting.
                - Do NOT include plt.show(). The Streamlit app will handle plotting.
            6. Python code must be a single string using \n for line breaks.
            7. Do not include any extra text outside the tuple.

            EXAMPLES:

            ('PLOT',
            "Showing the trend of sales over the last 12 months.",
            "SELECT month, revenue FROM sales ORDER BY month;",
            'import seaborn as sns
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8, 4))
            sns.barplot(data=df, x='project_year', y='num_projects', palette='viridis')
            plt.title('Number of Projects Started Each Year')
            plt.xlabel('Start Year')
            plt.ylabel('Number of Projects')
            plt.xticks(rotation=45)')

            User: "How many orders were placed in January?"
            Assistant:
            ('DATA',
            "Returning the number of orders in January.",
            "SELECT COUNT(*) AS orders FROM orders WHERE date >= '2024-01-01' AND date < '2024-02-01';",
            None)

            User: "What is the weather"
            Assistant:
            ('TEXT',
            "This request is outside my domain of generating SQL queries and plots.",
            None,
            None)


            DATABASE:
            {ddl_schema}

            Stay on topic. Do not answer questions outside your domain.
            CONTEXT:
            {context}

            USER QUERY:
            {query}
            """

        response = self.generate_response(contents)
        print(response)
        if response[2] or response[3]:
            return ast.literal_eval(response)           
        return response[1]     