import streamlit as st
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db.models import Medicamento

engine = create_engine("sqlite:///pharma.db")
Session = sessionmaker(bind=engine, future=True)

st.title("Lista de Medicamentos")

if "busca" not in st.session_state:
    st.session_state.busca = ""
busca = st.text_input("Buscar medicamento por nome:", value=st.session_state.busca)
st.session_state.busca = busca

if "min_ofertas" not in st.session_state:
    st.session_state.min_ofertas = 1
min_ofertas = st.slider("Quantidade mínima de farmácias com oferta:", 1, 5, value=st.session_state.min_ofertas)
st.session_state.min_ofertas = min_ofertas

with Session() as db:
    medicamentos = (
        db.query(Medicamento)
        .join(Medicamento.ofertas)
        .group_by(Medicamento.id)
        .having(func.count(Medicamento.ofertas) >= min_ofertas)
        .filter(Medicamento.nome.ilike(f"%{busca}%"))
        .all()
    )

PAGE_SIZE = 30

if "page_num" not in st.session_state:
    st.session_state.page_num = 0

max_paginas = len(medicamentos) // PAGE_SIZE + 1
st.session_state.page_num = min(st.session_state.page_num, max_paginas - 1)
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
