#!.venv/bin/python3
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, inspect

# Les informations de base pour manipuler le LLM avec le BDD MySQL.
LLM = ChatOpenAI(temperature=0)
host = 'localhost'
port = '3306'
username = 'utilisateur0'
password = 'motdepasse0'
database_schema = 'employees'
mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"
BDD = SQLDatabase.from_uri(mysql_uri)
Chaine = SQLDatabaseChain.from_llm(LLM,BDD)

def listing_tables_sql():
    engine = create_engine(mysql_uri)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return tables

def preview_table(nom_table):
    pr = pd.read_sql("SELECT * FROM {};".format(nom_table),mysql_uri)
    return pr


def communication_langchain(message_entree):
    resultat = Chaine.invoke(message_entree)
    return resultat["result"]

if __name__ == "__main__":
    liste_des_tables = listing_tables_sql()
    print(liste_des_tables)
    preview = preview_table("salaries")
    print(preview)
