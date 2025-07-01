import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Medicamento

engine = create_engine("sqlite:///pharma.db")
Session = sessionmaker(bind=engine, future=True)

st.title("Lista de Medicamentos")

with Session() as db:
    medicamentos = db.query(Medicamento).all()

PAGE_SIZE = 30

if "page_num" not in st.session_state:
    st.session_state.page_num = 0

start = st.session_state.page_num * PAGE_SIZE
end = start + PAGE_SIZE
medicamentos_page = medicamentos[start:end]

cols = st.columns(3)
for i, med in enumerate(medicamentos_page):
    with cols[i % 3]:
        if med.image_source:
            st.image(med.image_source, width=150)
        if st.button(med.nome, key=med.registro_ms):
            st.session_state["med_selecionado"] = med.registro_ms
            st.switch_page("pages/2_detalhes.py")

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.session_state.page_num > 0:
        if st.button("⬅️ Anterior"):
            st.session_state.page_num -= 1
            st.rerun()  # força reload

with col3:
    if end < len(medicamentos):
        if st.button("Próximo ➡️"):
            st.session_state.page_num += 1
            st.rerun()  # força reload
