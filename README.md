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

### Data Visualization

* **Seaborn Visualizations:** Generate charts and visual analyses directly in the interface.


### Observability

* **Langfuse:** has been set up and connected to the application for **tracing**.
