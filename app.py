import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DATETIME
from sqlalchemy.orm import sessionmaker
import datetime
import numpy as np


#online

dbname = "campamento"

user = "science"
password = "D4t4.Science"
host = "campamento-legendarios-rds.cn4ckqii4e2h.us-east-1.rds.amazonaws.com"
port = "5432"

# #local
# dbname = "campamento"
#
# user = "postgres"
# password = "Team.Lead#2023"
# host = "localhost"
# port = "5432"


# Create a SQLAlchemy engine
engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")


# Example: Query a table and load the data into a Pandas DataFrame
table_name = "campistas"
query = f"SELECT * FROM {table_name};"


table_name2="puntajes"

# Use the engine to execute the query and fetch data into a DataFrame


data = pd.read_sql_query(query, engine)

data_campistas=data
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




if col2.button("Restar"):
    timestamp=datetime.datetime.now()
    values_to_insert = {'nombrecompleto': nombre_selecccionado, 'categoria': categorias, 'puntaje': -1,'timestamp':timestamp        }
    insert_statement = your_table.insert().values(values_to_insert)
    session.execute(insert_statement)

    # Commit the transaction
    session.commit()

    st.write(f" Se restó un punto a {nombre_selecccionado} en la categoria de {categorias} a las {timestamp}")






#dashboard

query_puntajes = f"SELECT * FROM {table_name2};"
data_puntajes = pd.read_sql_query(query_puntajes, engine)


dashboard_data=pd.merge(data_campistas,data_puntajes)



conditions=[
    (dashboard_data['categoria']=="Versiculo"),
    (dashboard_data['categoria']=="Capitulo Grande"),
    (dashboard_data['categoria']=="Capitulo Pequeño"),
]
values=[10,150,230]

dashboard_data['puntos'] = np.select(conditions, values)

dashboard_data['total_puntaje']=dashboard_data["puntos"]*dashboard_data["puntaje"]

dashboard_data.rename(columns={"puntaje":"cantidad_versiculos"},inplace=True)




resumen_equipo_total_puntaje= dashboard_data.groupby(by='equipo')['total_puntaje'].sum()
resumen_equipo_total_puntaje=resumen_equipo_total_puntaje.to_frame()
resumen_equipo_total_puntaje=resumen_equipo_total_puntaje.reset_index()


resumen_equipo_cantidad_versiculos= dashboard_data.groupby(by='equipo')['cantidad_versiculos'].sum()
resumen_equipo_cantidad_versiculos=resumen_equipo_cantidad_versiculos.to_frame()
resumen_equipo_cantidad_versiculos=resumen_equipo_cantidad_versiculos.reset_index()


resumenparticipantes=dashboard_data.groupby(by=['nombrecompleto','equipo','categoria'])['cantidad_versiculos'].sum()







st.title("Total de puntaje por equipos")
st.bar_chart(resumen_equipo_total_puntaje, x="equipo", y="total_puntaje", color='equipo')


st.title("Total cantidad versiculos")

st.bar_chart(resumen_equipo_cantidad_versiculos, x="equipo", y="cantidad_versiculos", color='equipo')



st.title("Resumen por participante")
st.dataframe(resumenparticipantes)



