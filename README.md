# Conversational AI Assistant for SQL Data Management

The goal of this project was to develop a conversational AI application with two main functionalities: generating realistic synthetic data based on SQL schemas and enabling natural language querying through a “Talk to Your Data” interface.

The data generation component interprets SQL schemas (DDL) and produces a configurable amount of realistic, consistent synthetic data, while respecting all database integrity constraints. The querying component allows users to interact with the SQL data using natural language, executing queries and presenting the results as text, tables, and visualizations.

![App Demo](demo.gif)

## Functionalities

* **Schema Upload:** User can **upload a file** containing the DDL schema.
* **Data Generation:** The system must generate **consistent and valid data** for the provided DDL schema, respecting all database integrity constraints.
* **Generation Parameters:** User can set **additional generation parameters** (e.g., `temperature`).
* **Data Preview:** After generation, the user can check the **preview** for each of the generated tables.

* **Data Modification:** The system allow the user to **modify the generated data** through textual instructions.
* **Data Export & Storage:** Generated data be available for **download** as a `.csv` or `.zip` archive and **stored** within the system for access in the 'Talk to your data' module.
* **Conversational Interface:** The system provide a conversational interface for interacting with the data using **natural language text input**.
* **Conversation History:** The system display the **conversation history** and **stream system responses**.
* **SQL Generation and Execution:** The system **automatically generate and execute** relevant SQL queries against the underlying data source(s).
    * Support for **SQL JOINs** and **Aggregation functions**.
* **Data Visualization:** The system generate **data visualisations** using the Python **Seaborn** library and provide the results within the conversational interface.

#### Observability

* **Langfuse:** has been set up and connected to the application for **tracing**.
