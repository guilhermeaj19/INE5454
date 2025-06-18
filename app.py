import streamlit as st

# -----------------------  DATA  ----------------------- #
med_data = {
    "1037004870039": {
        "nome": "Cloridrato de Fluoxetina 20 mg – 30 cápsulas (Teuto – Genérico)",
        "registro_ms": 1037004870039,
        "categoria": "Remédios",
        "sub_categoria": "Antidepressivos",
        "principios_ativos": ["Cloridrato de Fluoxetina"],
        "image_source": "https://www.drogaraia.com.br/_next/image?url=https%3A%2F%2Fproduct-data.raiadrogasil.io%2Fimages%2F14966167.webp&w=1080&q=75",
        "is_generico": False,
        "necessita_prescricao": False,
        "farmacias": {
            "drogasil": {
                "preco": 13.39,
                "url": "https://www.drogasil.com.br/cloridrato-de-fluoxetina-20mg-teuto-generico-30-capsulas-c1.html?origin=search"
            },
            "drogaraia": {
                "preco": 13.39,
                "url": "https://www.drogaraia.com.br/cloridrato-de-fluoxetina-20mg-teuto-generico-30-capsulas-c1.html"
            }
        }
    }
}

# --------------------  SESSION STATE  ----------------- #
if 'selected_med' not in st.session_state:
    st.session_state.selected_med = None

# ---------------------  HOME PAGE  -------------------- #
def show_catalog_pretty(med_data):
    st.title("Catálogo de Medicamentos")
    st.caption("Clique em qualquer cartão para ver detalhes, preço e farmácias disponíveis.")

    # one column per medicine (change to st.columns(3) if you have many items)
    cols = st.columns(len(med_data))
    for col, (med_id, med) in zip(cols, med_data.items()):
        with col:
            # ---------- CARD ----------
            card_html = f"""
            <style>
            .med-card {{
                border-radius: 12px;
                overflow: hidden;              /* keeps name width = image width  */
                box-shadow: 0 2px 6px rgba(0,0,0,.08);
                cursor: pointer;
                transition: transform .15s ease;
            }}
            .med-card:hover {{ transform: translateY(-4px); }}

            .med-card img {{
                display: block;
                width: 100%;
                height: auto;
            }}

            .med-card-name {{
                background: #fafbfc;
                padding: 10px 8px;
                font-weight: 600;
                font-size: 0.9rem;
                color: #222;
                text-align: center;
                white-space: nowrap;           /* keep one line   */
                overflow: hidden;              /* hide long names */
                text-overflow: ellipsis;
            }}
            </style>

            <div class="med-card" onclick="window.parent.postMessage({{type: 'streamlit:click', id: '{med_id}'}}, '*')">
                <img src="{med['image_source']}" alt="{med['nome']}">
                <div class="med-card-name">{med['nome']}</div>
            </div>
            """
            # The postMessage trick lets Streamlit know which card was clicked
            # and is the recommended way to capture a click on custom HTML[1].

            st.markdown(card_html, unsafe_allow_html=True)

            # Handle the click coming from the iframe
            if "_EVENT" not in st.session_state:
                st.session_state._EVENT = None
            event = st.experimental_get_query_params().get("event")
            if event and event[0] == med_id and st.session_state._EVENT != event[0]:
                st.session_state._EVENT = event[0]
                st.session_state.selected_med = med_id
                st.rerun()


# ------------------  DETAIL PAGE  --------------------- #
def show_details(med_id: str):
    med = med_data[med_id]
    st.title(med["nome"])
    st.image(med["image_source"], width=300)

    st.markdown(f"**Categoria:** {med['categoria']}")
    st.markdown(f"**Sub-categoria:** {med['sub_categoria']}")
    st.markdown(f"**Princípio(s) ativo(s):** {', '.join(med['principios_ativos'])}")
    st.markdown(f"**Necessita prescrição:** {'Sim' if med['necessita_prescricao'] else 'Não'}")

    st.markdown("### Onde comprar")
    for farmacia, info in med["farmacias"].items():
        # pharma name is a hyperlink; price shown next to it
        st.markdown(f"- [{farmacia.capitalize()}]({info['url']}) — R$ {info['preco']:.2f}")

    if st.button("Voltar ao catálogo"):
        st.session_state.selected_med = None
        st.rerun()

# ---------------  APP ROUTING  ------------------------ #
if st.session_state.selected_med is None:
    show_catalog_pretty(med_data)
else:
    show_details(st.session_state.selected_med)
