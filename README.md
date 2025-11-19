# Conversational AI Assistant for SQL Data Management

## Project Overview

The goal of this project was to implement a conversational AI application with two core functionalities: generating realistic synthetic data based on SQL schemas and enabling natural language querying (Talk-to-your-data) against that data.

The project is structured around two main functional areas: **Data Generation** and **Chat with Your Data**.

## Functionalities

### Synthetic Data Generation

#### Goal
To develop a core data generation engine that interprets SQL schemas (DDL) and creates a configurable amount of realistic, consistent synthetic data while respecting all database integrity constraints.

#### Functional Requirements
* **Schema Upload:** User can **upload a file** containing the DDL schema (.sql, .txt or .ddl).
* **Data Generation:** The system must generate **consistent and valid data** for the provided DDL schema, respecting all database integrity constraints.
* **Generation Parameters:** User can set **additional generation parameters** (e.g., `temperature`).
* **Data Preview:** After generation, the user can check the **preview** for each of the generated tables.


* **Data Modification:** The system must allow the user to **modify the generated data** through textual instructions.
* **Data Export & Storage:** Generated data must be available for **download** as a `.csv` or `.zip` archive and **stored** within the system for access in the 'Talk to your data' module.

---

### Chat with Your Data (Talk-to-your-data)

#### Goal
To implement a conversational core module that allows users to query SQL data using natural language, executing queries and presenting results as text, tables, and plots.

#### Functional Requirements

* **Conversational Interface:** The system shall provide a conversational interface for interacting with the data using **natural language text input**.
* **Conversation History:** The system must display the **conversation history** and **stream system responses**.
* **SQL Generation and Execution:** The system must **automatically generate and execute** relevant SQL queries against the underlying data source(s).
    * Support for **SQL JOINs** and **Aggregation functions** is required.
* **Data Visualization:** The system must generate **data visualisations** using the Python **Seaborn** library and provide the results within the conversational interface.
* **Guardrails:**
    * Detect **Prompt Injection / Jailbreaks attempts**.
    * Ensure the AI assistant **stays on topic**.

#### Observability

* **Langfuse:** Set up and connect **Langfuse** to the application for **tracing**.
