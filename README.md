# Conversational AI Assistant for SQL Data Management

The goal of this project was to develop a conversational AI application with two main functionalities: generating realistic synthetic data based on SQL schemas and enabling natural language querying through a “Talk to Your Data” interface.

The data generation component interprets SQL schemas (DDL) and produces a configurable amount of realistic, consistent synthetic data, while respecting all database integrity constraints. The querying component allows users to interact with the SQL data using natural language, executing queries and presenting the results as text, tables, and visualizations.

![App Demo](demo.gif)

## Features

### Schema Handling

* **Schema Upload:** Upload a DDL file to set up the database structure.
* **Data Generation:** Generate **consistent and valid data** respecting database constraints.
* **Generation Parameters:** Adjust settings:`temperature` and `max_tokens`.
* **Data Preview:** Preview generated data for each table before exporting.

### Data Modification & Export

* **Data Editing:** Modify generated data with **text instructions**.
* **Export & Storage:**
  * Download data as `.csv` or `.zip`.

### Conversational Interaction

* **Natural Language Queries:** Interact with data in plain English.
* **Conversation History:** Full history with streamed user and system responses.
* **Automatic SQL Generation:** Supports SQL queries including:
  * **JOINs**
  * **Aggregation functions**

### System Workflow
* **User Input:** The user submits a specific task or request.

* **Task Classification:** The system identifies the task as either a SQL Query or a Data Plot.

* **Specialized Routing:** The request is sent to a specialized model (by function calling) to generate the necessary Python (Seaborn) or SQL code.

* **Execution:** The application attempts to run the generated code.

* **Validation:** If the code runs successfully, the system displays the result and the code to the user.

* **Error Handling:** If the code fails, the system triggers a retry to regenerate and fix the output.


### Observability

* **Langfuse:** has been set up and connected to the application for **tracing**.
