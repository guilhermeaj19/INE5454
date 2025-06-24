import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Medicamento, Base

# Conexão com o banco
engine = create_engine("sqlite:///pharma.db")
Session = sessionmaker(bind=engine, future=True)

st.title("Lista de Medicamentos")

with Session() as db:
    medicamentos = db.query(Medicamento).all()
    for med in medicamentos:
        if st.button(med.nome, key=med.registro_ms):
            st.session_state["med_selecionado"] = med.registro_ms
            st.switch_page("pages/2_detalhes.py")
