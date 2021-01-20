
# Sparkify Airflow Data Pipeline

## About this project
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

We will be building data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. Data quality plays a big part when analyses are executed on top the data warehouse so we will be implementing some of them. 

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Prerequisites
Before running this pipeline, the following steps must be completed:
1. Set up an Amazon Web Services connection inside of the airflow UI with your credentials
2. Set up a PostgreSQL connection inside of airflow UI that points to your Redshift Cluster (You need to create one)

## Apache Airflow in this project
In a regular not advanced data ETL project we would have a script that runs in a certain order some queries for the data warehouse to be populated. The issue with this approach is that it can really slow some tasks that can be run in parallel, for example:
Lets say we need to insert records in five independent tables that have nothing to do with each other. In a regular approach we will need to wait for a query to be finished in order to start executing the next one. In Apache Airflow, we can run each query at the same time with different workers inside the Redshift Cluster, this speeds the task for at least 5x assuming every table is populated in the same time.

![Airflow Schema](images/airflow_schema.PNG)

This is the data pipeline design. We first create the tables, then move data from S3 into staging tables, then fact tables, then dimension tables, run some tests and the pipeline is over.
Having Airflow not only speeds up the ETL, it also allows us to identify which part of the pipeline is broken and why, this is pretty good practice for teamwork.

## Usage

 - ```dag.py```: This script is the orchestrator of the project, in this file we define the DAG and the pipeline architecture. 
 - ```create_tables.sql```: This sql script deletes tables if they exist and creates the tables of the data warehouse.
 - ```sql_queries.py```: In this script we define the insert queries of the fact and dimesion tables- <code>stage_redshift.py</code>: Defines a class that reads from S3 and writes to staging tables in AWS Redshfit
 - ```load_fact.py```: Defines a class that extracts data from staging table into the fact table
 - ```load_dimension.py```: Defines a class that extracts data from the staging tables into the dimesion tables
 - ```data_quality.py```: Defines a class that counts the rows in each table to ensure data has been written to RedShift. We can include more tests, but these are ok in this project.