import streamlit as st
from ai_model import GeminiModel
from view_side_bar import show_side_bar
from view_data_generation import view_data_generation_foo
from view_talk_to_your_data import view_talk_to_your_data_foo


script = None
tables = None
model = GeminiModel()

if "page" not in st.session_state:
    st.session_state.page = "Data Generation"

show_side_bar()

if st.session_state.page == 'Data Generation':
    view_data_generation_foo(model)
elif st.session_state.page == 'Talk to your data': 
    view_talk_to_your_data_foo(model)

