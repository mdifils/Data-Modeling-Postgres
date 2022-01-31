# Data Modeling with PostgreSQL

## Description

The dataset used in this project has been collected from songs and users activities
on a streaming music app. The purpose is to analyze data and understand what
songs users are listening to. Data has been collected in JSON format. Those
`.json` files are located in different directories and doesn't make it easy to
perform data analysis:  

![dataset structure](./images/dataset_structure.png)

For this reason, I'm going to build an ETL pipeline that will transfer data
from JSON files in those seven directories into a postgres database using python
and SQL. The data will then be ready for data analysis from Sparkify analytics
team (Sparkify is a startup who owns the streaming music app mentionned above). 
But before writting the ETL pipeline, I'm going to define fact and dimension 
tables for a star schema. Then I'm going to build an entity relationship diagram
that represents my data model.

## Data Model

![data model](./images/sparkifydb.png)
