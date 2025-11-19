import hashlib
from psycopg2 import IntegrityError
import streamlit as st
from databse_operations import add_data_to_database, check_if_possible_update, create_database, get_schema_from_db, select_table
import io, zipfile


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def show_generation_prompt():
    st.title("Data Generation")
    st.text("Prompt")
    prompt = st.text_input("Prompt", placeholder="Enter your prompt here...", label_visibility="collapsed")
    return prompt


def show_file_uploader():
    uploaded_file = st.file_uploader(
        "Upload DDL Schema", 
        type=['sql', 'json', 'txt', 'ddl'], 
        label_visibility="collapsed"
    )
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        st.session_state.ddl_schema = uploaded_file.read().decode("utf-8")
        st.markdown("---")
        return st.session_state.ddl_schema
    st.markdown("---")
    return None


def show_advanced_parameters():
    # advanced parameters
    st.subheader("Advanced Parameters")
    col3, col4 = st.columns([0.7, 0.3])
    with col3:
        st.text("Temperature")
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.01, label_visibility="collapsed")
    with col4:
        st.text("Max Tokens")
        max_tokens = st.number_input("Max Tokens", min_value=1, value=10000, step=1, label_visibility="collapsed")
    st.markdown("")
    generate_clicked_state = st.button("Generate", type="secondary")
    return temperature, max_tokens, generate_clicked_state



def show_save_buttons(session_state):
    col_save1, col_save2, _ = st.columns([0.2, 0.2, 0.6])

    # ================= CSV =================
    with col_save1:
        clicked_csv = st.button("Save to CSV", type="secondary", icon=":material/save:", width='stretch')

        if clicked_csv:
            all_tables = get_schema_from_db(session_state)
            if not all_tables:
                st.error("No tables found in the database. Please add any data first.")
            else:
                tables_dict = {}
                for table in all_tables:
                    df = select_table(table)
                    if df is not None:
                        tables_dict[table] = df

                output = io.StringIO()
                for table_name, df in tables_dict.items():
                    output.write(f"=== TABLE: {table_name} ===\n")
                    df.to_csv(output, index=False)
                    output.write("\n\n")
            
                st.download_button(label="Click to download CSV", data=output.getvalue().encode("utf-8"), file_name="all_tables.csv",
                                   mime="text/csv", key="download_all_tables_csv", use_container_width=True)

    # ================= ZIP =================
    with col_save2:
        clicked_zip = st.button("Save to ZIP", type="secondary", icon=":material/save:", width='stretch')

        if clicked_zip:
            all_tables = get_schema_from_db(session_state)
            if not all_tables:
                st.error("No tables found in the database. Please add any data first.")

            tables_dict = {}
            for table in all_tables:
                df = select_table(table)
                if df is not None:
                    tables_dict[table] = df

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for table_name, df in tables_dict.items():
                    csv_bytes = df.to_csv(index=False).encode("utf-8")
                    zip_file.writestr(f"{table_name}.csv", csv_bytes)

            st.download_button("Download ZIP", data=zip_buffer.getvalue(), file_name="all_tables.zip", 
                               type="secondary", icon=":material/save:", width='stretch')


def show_dropdown_list(tables):
    st.markdown("---")
    st.subheader("Data Preview")
    col5, col6 = st.columns([0.7, 0.3])
    list_options = tables if tables else ['NO TABLES FOUND']

    with col6:
        selected_data = st.selectbox(
            "Select Data", 
            list_options, 
            index=0, 
            label_visibility="collapsed",
            key="data_preview_selector"
        )
    return selected_data


def show_table(table):
    st.dataframe(table, width='stretch', hide_index=True)


def show_chat_interface():
    st.text("Specify which TABLE to update, the ROW ID to edit, and the NEW VALUES for the columns.")
    col7, col8 = st.columns([0.88, 0.12])
    with col7:
        quick_instructions = st.text_input("Quick Instructions", placeholder="Enter quick edit instructions...", label_visibility="collapsed")
    with col8:
        submit_clicked = st.button("Submit", type="secondary", icon=":material/send:", width='stretch')
    if submit_clicked:
        return quick_instructions
    else:
        return None



MAX_RETRIES = 3 

def safe_generate_and_add(model, ddl_schema, user_generation_prompt, temperature, max_tokens):
    for attempt in range(MAX_RETRIES):
        st.info(f"(Generating data, attempt: {attempt + 1}/{MAX_RETRIES})...")
        print(f"--- Attepmt {attempt + 1} ---")

        response = model.generate_database(
            ddl_schema=ddl_schema,
            prompt=user_generation_prompt,
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        
        if response is None:
            st.error("No model response received. Adjust parameters and try again.")
            return

        try:
            add_data_to_database(response, st.session_state) 
            st.success("Data successfully generated and added to the database.")
            return

        except IntegrityError as e:
            print(f"Error {attempt + 1}: {e.orig}")
            st.warning(f"Error has occured while inserting data: {e.orig}. Retrying...")
            continue 

        except Exception as e:
            st.error(f"Unexpected error has occured {e}")
            print(f"Unexpected error:  {e}")
            return
    st.error(f"Generating data failed after {MAX_RETRIES} attempts due to repeated integrity errors.")


def view_data_generation_foo(model):
    load_css("styles.css")

    st.set_page_config(layout="wide", page_title="Data Assistant Prototype")
    user_generation_prompt = show_generation_prompt()
    ddl_schema = show_file_uploader()

    if 'last_ddl_hash' not in st.session_state:
        st.session_state.last_ddl_hash = None
    if 'file_uploader_key' not in st.session_state:
        st.session_state.file_uploader_key = 0
    if 'engine' not in st.session_state:
        st.session_state.engine = None

    if ddl_schema:
        # hash of current DDL script to detect changes
        current_hash = hashlib.sha256(ddl_schema.encode('utf-8')).hexdigest()
        if current_hash != st.session_state.last_ddl_hash:
            try:
                st.session_state.update(create_database(ddl_schema))
                st.session_state.last_ddl_hash = current_hash
                st.session_state.file_uploader_key += 1
            except Exception as e:
                st.sidebar.error(f"Database creation failed: {e}")

    tables = get_schema_from_db(st.session_state)
    temperature, max_tokens, generate_clicked_state= show_advanced_parameters()
    show_save_buttons(st.session_state)

    if generate_clicked_state:
        if ddl_schema:
            safe_generate_and_add(
                model,
                ddl_schema=ddl_schema,
                user_generation_prompt=user_generation_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            st.warning("Please upload a DDL schema file before generating data.")

    # data preview
    selected_table = show_dropdown_list(tables)
    table_data = select_table(selected_table)
    show_table(table_data)

    # edit
    user_edit_prompt = show_chat_interface()
    if user_edit_prompt:
        extracted_info = model.extract_important_info_from_edit_prompt(user_edit_prompt)
        st.info(f"Extracted Info: {extracted_info}")

        if isinstance(extracted_info, tuple):
            if_possible, update_result = check_if_possible_update(st.session_state, extracted_info[0], extracted_info[1], extracted_info[2])
            if if_possible:
                st.success(update_result)
            else:
                st.error(update_result)