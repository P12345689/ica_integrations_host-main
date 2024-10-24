# -*- coding: utf-8 -*-
"""
Author: Andre Gheilerman
Description: Connection to an IBM DB2 Warehouse
This module provides routes for db2_integration, to an IBM DB2 Warehouse
Integration Development Guidelines:
1. Use Pydantic v2 models to validate all inputs and outputs.
2. All functions should be defined as async.
3. Ensure that all code has full docstring coverage in Google docstring format.
4. Implement full unit test coverage (can also use doctest).
5. Use Jinja2 templates for LLM prompts and response formatting.
6. Implement proper error handling and logging.
7. Use environment variables for configuration where appropriate.
8. Follow PEP 8 style guidelines.
"""

import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

import jaydebeapi
import pandas as pd

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set to INFO in production

# Set default model and max threads from environment variables
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("dev/app/routes/db2_integration/templates"))

# Set DB2 Variables
DB2_DATABASE = os.getenv("DB2_DATABASE")
DB2_HOSTNAME = os.getenv("DB2_HOSTNAME")
DB2_PORT = os.getenv("DB2_PORT")
DB2_UID = os.getenv("DB2_UID")
DB2_PWD = os.getenv("DB2_PWD")
DB2_SSL_CONN = os.getenv("DB2_SSL_CONN")
DB2_SSL_TRUST_STORE = os.getenv("DB2_SSL_TRUST_STORE")
DB2_SSL_PSS = os.getenv("DB2_SSL_PSS")
DB2_JDBC_DRIVER = os.getenv("DB2_JDBC_DRIVER")
DB2_DRIVER_JAR = os.getenv("DB2_DRIVER_JAR")

class DB2InputModel(BaseModel):
    """Model to validate input data for IBM DB2 SQL Query and Warehouse Connection."""
    query: str = Field(..., pattern=r"(?i)^\s*SELECT\s+.*", description="DB2 SQL Query")
    num_rows: int = Field(..., description="Number of Rows that output should have")

class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""
    data: str

class OutputModel(BaseModel):
    """Model to structure the output response."""
    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]

def db2_connect_with_truststore(db2_database, db2_hostname, db2_port, db2_uid, db2_pwd, db2_ssl_conn, db2_ssl_trust_store, db2_ssl_pss, db2_jdbc_driver_name, db2_driver_jar):
    """ IBM DB2 Connection with SSL Truststore.
    Args:
        db2_database (str): Name of the DB2 database.
        db2_hostname (str): Hostname or IP address of the DB2 database.
        db2_port (str): Port number of the DB2 database.
        db2_uid (str): Username for connecting to the DB2 database.
        db2_pwd (str): Password for connecting to the DB2 database.
        db2_ssl_conn (str): Type of SSL connection to use (e.g., SSL or NONSSL).
        db2_ssl_trust_store (str): Path to the .jks file for the DB2 SSL truststore.
        db2_ssl_pss (str): Password for the SSL truststore.
        db2_jdbc_driver_name (str): Name of the DB2 JDBC driver.
        db2_driver_jar (str): Path to the .jar file for the DB2 JDBC driver.
    Returns:
        db2_connection (DB2 Connection): An IBM DB2 Connection Object
    """
    DB2_url = (
        "jdbc:db2://" + db2_hostname + ":" + db2_port + "/" + db2_database + ":" + "useJDBC4ColumnNameAndLabelSemantics=false" + ";" + db2_ssl_conn + ";" + db2_ssl_trust_store + ";" + db2_ssl_pss + ";"
    )
    db2_connection = jaydebeapi.connect(
        jclassname=db2_jdbc_driver_name,
        url=DB2_url,
        driver_args=[db2_uid, db2_pwd],
        jars=db2_driver_jar,
    )
    return db2_connection

def db2_connect_without_truststore(db2_database, db2_hostname, db2_port, db2_uid, db2_pwd, db2_ssl_conn, db2_jdbc_driver_name, db2_driver_jar):
    """ IBM DB2 Connection with SSL Truststore.
    Args:
        db2_database (str): Name of the DB2 database.
        db2_hostname (str): Hostname or IP address of the DB2 database.
        db2_port (str): Port number of the DB2 database.
        db2_uid (str): Username for connecting to the DB2 database.
        db2_pwd (str): Password for connecting to the DB2 database.
        db2_ssl_conn (str): Type of SSL connection to use (e.g., SSL or NONSSL).
        db2_jdbc_driver_name (str): Name of the DB2 JDBC driver.
        db2_driver_jar (str): Path to the .jar file for the DB2 JDBC driver.
    Returns:
        db2_connection (DB2 Connection): An IBM DB2 Connection Object
    """
    DB2_url = (
        "jdbc:db2://" + db2_hostname + ":" + db2_port + "/" + db2_database + ":" + "useJDBC4ColumnNameAndLabelSemantics=false" + ";" + db2_ssl_conn + ";"
    )
    db2_connection = jaydebeapi.connect(
        jclassname=db2_jdbc_driver_name,
        url=DB2_url,
        driver_args=[db2_uid, db2_pwd],
        jars=db2_driver_jar,
    )
    return db2_connection

def fetch_db2_data(db2_credentials, query, num_rows):
    """Fetch data from a DB2 database using a SQL query.
    Args:
        db2_credentials (Connection): A connection object for the DB2 database.
        query (str): The SQL query to execute on the DB2 database.
        num_rows (int): The number of rows to return from the query.
    Returns:
        df (pd.Dataframe): A Pandas Dataframe containing the results of the query.
    Raises:
        HTTPException: If there is an error fetching data from the DB2 database.
    """
    query = query + f' limit {num_rows} for fetch only with ur;'
    log.info(f"Query: {query}")
    try:
        with db2_credentials as db2_conn:
            db2_cursor = db2_conn.cursor()
            db2_cursor.execute(query)
            columns = [desc[0] for desc in db2_cursor.description]
            df = pd.DataFrame(db2_cursor.fetchall(), columns=columns)
            return df.head(num_rows)
    except Exception as e:
            raise HTTPException(status_code=503, detail=str(e))
    
def db2_data_to_json(df):
    """
    Converts a Pandas DataFrame into a JSON string.
    Args:
        df (pd.DataFrame): The DataFrame to convert to JSON.
    Returns:
        A JSON string representation of the DataFrame.
    """
    try:
        df = df.to_json(orient="records")
        return df
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

def add_custom_routes(app: FastAPI):
    @app.post("/system/db2_integration/fetch_data_with_truststore/invoke")
    async def db2_fetch_request_with_truststore(request: Request) -> OutputModel:
        """
        Handle POST requests to an IBM DB2 Warehouse with an SSL Truststore. Fetches data based on a user query.
        Args:
            request (Request): The request object containing the input data.
        Returns:
            OutputModel: The structured output response.
        Raises:
            HTTPException: 422 for Input, Unprocessable Content. 503 for Fetching DB2 Data, For if DB2 is down.
        """
        log.info("Received request to fetch IBM DB2 Warehouse Data")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = DB2InputModel(**data)
            db2_credentials = db2_connect_with_truststore(DB2_DATABASE, DB2_HOSTNAME, DB2_PORT, DB2_UID, DB2_PWD, DB2_SSL_CONN, DB2_SSL_TRUST_STORE, DB2_SSL_PSS, DB2_JDBC_DRIVER, DB2_DRIVER_JAR)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))
        log.info(f"Connected to DB2 Warehouse")
        
        log.info(f"Fetching Data")
        try:
            db2_data = fetch_db2_data(db2_credentials, input_data.query, input_data.num_rows)
        except Exception as e:
            log.error(f"Unexpected error in connecting to IBM DB2 Data Warehouse: {str(e)}")
            raise HTTPException(status_code=503, detail={str(e)})
        
        if db2_data.empty:
            raise HTTPException(status_code=404, detail="Result of query is empty")
        
        log.info(f"Turning result into JSON")
        try:
            db2_data = db2_data_to_json(db2_data)
        except Exception as e:
            log.error(f"Error in converting result into JSON: {str(e)}")
            raise HTTPException(status_code=503, detail={str(e)})   

        log.info(f"Fetched Data")
        response_message = ResponseMessageModel(data=db2_data)
        return OutputModel(invocationId=invocation_id, response=[response_message])
    
    @app.post("/system/db2_integration/fetch_data_without_truststore/invoke")
    async def db2_fetch_request_without_truststore(request: Request) -> OutputModel:
        """
        Handle POST requests to an IBM DB2 Warehouse without an SSL Truststore. Fetches data based on a user query.
        Args:
            request (Request): The request object containing the input data.
        Returns:
            OutputModel: The structured output response.
        Raises:
            HTTPException: 422 for Input, Unprocessable Content. 503 for Fetching DB2 Data, For if DB2 is down.
        """
        log.info("Received request to fetch IBM DB2 Warehouse Data")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = DB2InputModel(**data)
            db2_credentials = db2_connect_without_truststore(DB2_DATABASE, DB2_HOSTNAME, DB2_PORT, DB2_UID, DB2_PWD, DB2_SSL_CONN, DB2_JDBC_DRIVER, DB2_DRIVER_JAR)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))
        log.info(f"Connected to DB2 Warehouse")
        
        log.info(f"Fetching Data")
        try:
            db2_data = fetch_db2_data(db2_credentials, input_data.query, input_data.num_rows)
        except Exception as e:
            log.error(f"Unexpected error in connecting to IBM DB2 Data Warehouse: {str(e)}")
            raise HTTPException(status_code=503, detail={str(e)})
        
        if db2_data.empty:
            raise HTTPException(status_code=404, detail="Result of query is empty")
        
        log.info(f"Turning result into JSON")
        try:
            db2_data = db2_data_to_json(db2_data)
        except Exception as e:
            log.error(f"Error in converting result into JSON: {str(e)}")
            raise HTTPException(status_code=503, detail={str(e)})   

        log.info(f"Fetched Data")
        response_message = ResponseMessageModel(data=db2_data)
        return OutputModel(invocationId=invocation_id, response=[response_message])