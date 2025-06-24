import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Medicamento, Oferta, Farmacia

engine = create_engine("sqlite:///pharma.db")
Session = sessionmaker(bind=engine, future=True)

registro = st.session_state.get("med_selecionado", None)

if registro is None:
    st.warning("Nenhum medicamento selecionado.")
    st.stop()

with Session() as db:
    medicamento = db.query(Medicamento).filter_by(registro_ms=registro).first()
    st.title(medicamento.nome)
    st.image(medicamento.image_source)

    st.subheader("Ofertas disponíveis:")
    for oferta in medicamento.ofertas:
        st.write(f"- **{oferta.farmacia.nome}**: R$ {oferta.preco:.2f}")
        st.markdown(f"[Ver oferta]({oferta.url})")
