import streamlit as st
import json

def generate_subcategories(max_pax, max_kinder, min_pax):
    subcategories = []

    for erwachsene in range(1, max_pax + 1):
        max_verbleibende_kinder = min(max_kinder, max_pax - erwachsene)
        kinder_range = [k for k in range(0, max_verbleibende_kinder + 1) if erwachsene + k >= min_pax]

        if not kinder_range:
            continue

        if len(kinder_range) > 1:
            kinder_text = f"{kinder_range[0]}-{kinder_range[-1]} Kinder"
            subcategories.append({
                'erwachsene': erwachsene,
                'kinder_text': kinder_text,
                'min_pax': min_pax
            })
        else:
            kinder_text = f"{kinder_range[0]} Kinder"
            subcategories.append({
                'erwachsene': erwachsene,
                'kinder_text': kinder_text,
                'min_pax': min_pax
            })

    return subcategories

# SessionState Initialisierung
if 'max_pax' not in st.session_state:
    st.session_state.max_pax = 8
if 'max_kinder' not in st.session_state:
    st.session_state.max_kinder = 3
if 'min_pax' not in st.session_state:
    st.session_state.min_pax = 2

# Slider
st.session_state.max_pax = st.slider("Maximale Gästezahl (max_pax)", 1, 20, st.session_state.max_pax)
st.session_state.max_kinder = st.slider("Maximale Kinderzahl (max_kinder)", 0, st.session_state.max_pax - 1, st.session_state.max_kinder)
st.session_state.min_pax = st.slider("Mindestbelegung (min_pax)", 1, st.session_state.max_pax, st.session_state.min_pax)

# Automatische Korrekturen
rerun = False
if st.session_state.max_kinder >= st.session_state.max_pax:
    st.session_state.max_kinder = st.session_state.max_pax - 1
    rerun = True

if st.session_state.min_pax > st.session_state.max_pax:
    st.session_state.min_pax = st.session_state.max_pax
    rerun = True

if st.session_state.min_pax < 1:
    st.session_state.min_pax = 1
    rerun = True

if rerun:
    st.rerun()

# Ausgabe
subcategories = generate_subcategories(
    st.session_state.max_pax,
    st.session_state.max_kinder,
    st.session_state.min_pax
)

if subcategories:
    st.markdown("### Gültige Subkategorien")
    for sub in subcategories:
        st.write(f"{sub['erwachsene']} Erwachsener + {sub['kinder_text']}, min. Pax = {sub['min_pax']}")

    st.markdown("### JSON Output")
    st.code(json.dumps(subcategories, indent=2), language="json")
else:
    st.info("Keine gültigen Kombinationen für die aktuelle Einstellung.")