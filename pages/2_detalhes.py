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
    med = db.query(Medicamento).filter_by(registro_ms=registro).first()
    st.title(med.nome)

    if med.categoria:
        categoria = med.categoria

        if med.sub_categoria:
            st.subheader(f"{categoria} -> {med.sub_categoria}")
        else:
            st.subheader(f"{categoria}")

    col1, col2 = st.columns(2)

    with col1:
        if med.image_source:
            st.image(med.image_source, width=300)

    with col2:
        st.subheader("Ofertas disponíveis:")

        # 1. Acha o menor preço
        precos = [oferta.preco for oferta in med.ofertas]
        menor_preco = min(precos) if precos else None

        # 2. Mostra ofertas, destacando a mais barata
        for oferta in med.ofertas:
            destaque = " - ✅ Melhor preço!" if oferta.preco == menor_preco else ""
            st.write(f"- **{oferta.farmacia.nome.capitalize()}**: R$ {oferta.preco:.2f}")
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;[Ver oferta]({oferta.url}){destaque}")   
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Detalhes:")
        st.write(f"Registro MS: {med.registro_ms}")
        if med.marca:
            st.write(f"Marca: {med.marca}")

        if med.quantidade:
            st.write(f"Quantidade: {med.quantidade}")

        st.write(f"Genérico? {'✅' if med.is_generico else '❌'}")
        st.write(f"Necessita prescrição? {'✅' if med.necessita_prescricao else '❌'}")
        
    with col2:
        if med.descricao:
            st.subheader("Descrição:")
            st.write(med.descricao)