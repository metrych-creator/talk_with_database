import streamlit as st


def show_side_bar():
    # sidebar
    with st.sidebar:
        st.title("Data Assistant")
        st.header("")
        if st.sidebar.button("Data Generation", icon=":material/database:"):
            st.session_state.page = "Data Generation"
        if st.sidebar.button("Talk to your data", icon=":material/chat:"):
            st.session_state.page = "Talk to your data"
        st.markdown("---")
    return st.session_state.page