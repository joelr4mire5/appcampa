import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DATETIME
from sqlalchemy.orm import sessionmaker
import datetime




dbname = "postgres"

user = "postgres"
password = "Exomeza1995"
host = "legendarios-rds.cn4ckqii4e2h.us-east-1.rds.amazonaws.com"
port = "5432"


# Create a SQLAlchemy engine
engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")


# Example: Query a table and load the data into a Pandas DataFrame
table_name = "campistas"
query = f"SELECT * FROM {table_name};"


table_name2="puntajes"

# Use the engine to execute the query and fetch data into a DataFrame
data = pd.read_sql_query(query, engine)


lista_equipos=data["equipo"].unique().tolist()



st.title("Campamento Legionarios Invencibles 2024")
equipo_seleccionado=st.selectbox("Seleccionar Equipo",lista_equipos)

data=data[data["equipo"]==equipo_seleccionado]
lista_nombres=data["nombrecompleto"].tolist()

nombre_selecccionado=st.selectbox("Seleccionar al campista",lista_nombres)

lista_categorias=["Versiculo","Capitulo Grande","Capitulo Pequeño"]


categorias=st.selectbox("Seleccionarla categoria a contabilizar",lista_categorias)

# Initialize a total value




metadata = MetaData()

your_table = Table('puntajes', metadata,
                   Column('nombrecompleto', String),
                   Column('categoria', String),
                   Column('puntaje', Integer),
                   Column('timestamp',DATETIME)
                   )

Session = sessionmaker(bind=engine)
session = Session()




col1,col2 = st.columns(2)

# Create a button to increment the total value
if col1.button("Añadir"):
    timestamp = datetime.datetime.now()
    values_to_insert = {'nombrecompleto': nombre_selecccionado, 'categoria': categorias, 'puntaje': 1,'timestamp':timestamp}
    insert_statement = your_table.insert().values(values_to_insert)
    session.execute(insert_statement)

    # Commit the transaction
    session.commit()

    st.write(f" Se agregó un punto a {nombre_selecccionado} en la categoria de {categorias} a las {timestamp}")


    # Increment the total value by 1 when the button is clicked



if col2.button("Restar"):
    timestamp=datetime.datetime.now()
    values_to_insert = {'nombrecompleto': nombre_selecccionado, 'categoria': categorias, 'puntaje': -1,'timestamp':timestamp        }
    insert_statement = your_table.insert().values(values_to_insert)
    session.execute(insert_statement)

    # Commit the transaction
    session.commit()

    st.write(f" Se restó un punto a {nombre_selecccionado} en la categoria de {categorias} a las {timestamp}")



# Update the session state to store the current total value




