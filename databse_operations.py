from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from sqlalchemy.types import Integer, Float, String, Boolean, Date, DateTime
import datetime
from sqlalchemy import Table, MetaData, update
import pandas as pd


engine = create_engine("postgresql+psycopg2://monika:password@localhost:5432/databases")

def create_database(ddl_script):
    creation_statements = []
    fk_statements = []
    
    statements = [stmt.strip() for stmt in ddl_script.split(';') if stmt.strip()]

    for stmt in statements:
        if stmt.startswith('ALTER TABLE') and 'FOREIGN KEY' in stmt:
            fk_statements.append(stmt)
        else:
            creation_statements.append(stmt)
            
    creation_sql = ";\n".join(creation_statements)
    fk_sql = ";\n".join(fk_statements)

    with engine.connect() as conn:
        # 1. drop enums
        enum_query = """
            SELECT t.typname 
            FROM pg_type t 
            JOIN pg_namespace n ON n.oid = t.typnamespace
            WHERE n.nspname = 'public' 
            AND t.typtype = 'e'
        """
        result = conn.execute(text(enum_query))
        enums_to_drop = [row[0] for row in result]
        
        if enums_to_drop:
            drop_enum_statements = "; ".join([f"DROP TYPE IF EXISTS {enum} CASCADE" for enum in enums_to_drop])
            conn.execute(text(drop_enum_statements))
            conn.commit()

        # 2. drop tables
        tables_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
        tables_to_drop = [row[0] for row in conn.execute(text(tables_query))]
        if tables_to_drop:
            drop_statements = "; ".join([f"DROP TABLE IF EXISTS {table} CASCADE" for table in tables_to_drop])
            conn.execute(text(drop_statements))
            conn.commit()

        # 3. CREATE TABLE / CREATE TYPE
        conn.execute(text(creation_sql))
        conn.commit()
        
        # 4. adding foreign key constraints
        if fk_sql:
            conn.execute(text(fk_sql))
            conn.commit()
        print("Database schema created successfully.")
    return {'engine': engine}


def get_schema_from_db(session_state):
    if session_state.engine is None:
        return []
    
    query = """
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        """
    with session_state.engine.connect() as conn:
        result = conn.execute(text(query))
        tables = [row[0] for row in result] 
    return tables


def select_table(table_name):
    if st.session_state.engine is None:
        return None
    
    query = f"SELECT * FROM {table_name} LIMIT 10"
    with st.session_state.engine.connect() as conn:
        result = conn.execute(text(query))
        columns = result.keys()
        data = result.fetchall()
    
    df = pd.DataFrame(data, columns=columns)
    return df


def add_data_to_database(model_response, session_state):
    if model_response is None:
        print("No model response to insert.")
        return
    
    if session_state.engine is None:
        return
    
    try:
        with session_state.engine.connect() as conn:
            conn.execute(text(model_response))
            conn.commit()

    except SQLAlchemyError as e:
        print(f"Error inserting data to database: {e}")
        raise e 
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e



def check_if_possible_update(session_state, table_name, row_id, new_values):
    engine = session_state.engine
    if engine is None:
        return False, "Database engine is not initialized."

    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        return False, f"Table '{table_name}' does not exist."

    # get columns and their types
    columns_info = {col["name"]: col["type"] for col in inspector.get_columns(table_name)}

    # get primary key columns
    primary_key = inspector.get_pk_constraint(table_name)["constrained_columns"][0]

    # check if the row exists
    query = f"SELECT EXISTS (SELECT 1 FROM {table_name} WHERE {primary_key} = :row_id)"
    with engine.connect() as conn:
        result = conn.execute(text(query), {"row_id": row_id})
        exists = result.scalar()
        if not exists:
            return False, f"Row with {primary_key}={row_id} does not exist in table '{table_name}'."

    # validate new values (types)
    for col, value in new_values.items():
        if col not in columns_info:
            return False, f"Column '{col}' does not exist in table '{table_name}'."
        col_type = columns_info[col]
        try:
            if isinstance(col_type, Integer):
                int(value)
            elif isinstance(col_type, Float):
                float(value)
            elif isinstance(col_type, Boolean):
                if not isinstance(value, (bool, str, int)):
                    raise ValueError()
            elif isinstance(col_type, Date):
                if not isinstance(value, (datetime.date, str)):
                    raise ValueError()
            elif isinstance(col_type, DateTime):
                if not isinstance(value, (datetime.datetime, str)):
                    raise ValueError()
            elif isinstance(col_type, String):
                str(value)
            else:
                str(value)
        except Exception:
            return False, f"Value '{value}' for column '{col}' cannot be cast to {col_type}"

    # Update row in main table
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = Table(table_name, metadata, autoload_with=engine)
    
    try:
        with engine.begin() as conn:
            stmt = (
                update(table)
                .where(table.c[primary_key] == row_id)
                .values(**new_values)
            )
            conn.execute(stmt)
            return True, "Row updated successfully."
    except SQLAlchemyError as e:
        return False, f"Error updating row: {str(e)}"
    

def clean_sql_query(query):
    start_delimiter = "```sql"
    end_delimiter = "```"

    working_query = query.strip()

    if working_query.startswith(start_delimiter) and working_query.endswith(end_delimiter):
        cleaned_query = query[len(start_delimiter):]
        cleaned_query = cleaned_query[:-len(end_delimiter)]
        return cleaned_query.strip()
    return working_query


def execute_given_sql_statement(query):
    if st.session_state.engine is None:
        return []
    
    cleaned_query = clean_sql_query(query)
    
    with st.session_state.engine.connect() as conn:
        result = conn.execute(text(cleaned_query))
        columns = result.keys()
        data = result.fetchall()

        df = pd.DataFrame(data, columns=columns)
    return df