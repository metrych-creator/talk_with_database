import streamlit as st
import pandas as pd
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt
from databse_operations import execute_given_sql_statement

def show_talk_to_your_data():
    st.title("Talk to your data")
    st.markdown("---")

def execute_seaborn_code(code, df, local_vars=None):
    if local_vars is None:
        local_vars = {}
    
    local_vars.update({
        "pd": pd,
        "sns": sns,
        "plt": plt,
        "df": df
    })
    exec(code, {}, local_vars)
    
    fig = plt.gcf()
    return fig


def view_talk_to_your_data_foo(model):
    st.set_page_config(layout="wide")
    show_talk_to_your_data()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["type"] == "TEXT":
                st.write(message["text"])
            elif message["type"] == "DATA":
                st.write(message["text"])
                st.code(message["sql"])
                st.table(message["content"])
            elif message["type"] == "PLOT":
                st.pyplot(message["plot_figure"])

    prompt = st.chat_input("Ask a question about your data...")

    if prompt:
        st.session_state.messages.append({"role": "user", "type": "TEXT", "text": prompt})
        safety_categories = model.check_prompt_safety(prompt)
    
        if safety_categories:
            print("SAFETY_PROBLEM_________________________________")
            st.error(f"Your prompt is blocked due to: {safety_categories}")
            return  
        print("NO SAFETY PROBLEMS")
        result_type, description, sql_query, python_code = model.generate_answer(st.session_state.ddl_schema, prompt, st.session_state.messages)
        
        if result_type == 'DATA' and sql_query:
            results = execute_given_sql_statement(sql_query)
            results_message = {"role": "assistant", "type": "DATA", "sql":sql_query, "content": results, "text": description}
            st.session_state.messages.append(results_message)
        elif result_type == 'PLOT' and sql_query and python_code:
            df = execute_given_sql_statement(sql_query)
            fig = execute_seaborn_code(python_code, df)
            results_message = {"role": "assistant", "type": "PLOT", "plot_figure": fig}
            st.session_state.messages.append(results_message)
        else:
            results_message = {"role": "assistant", "type": "TEXT", "text": description}
            st.error("Your prompt is not correct. {description}")
            st.session_state.messages.append(results_message)
        st.rerun()