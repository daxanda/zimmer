import streamlit as st
import json
from collections import defaultdict

def generate_subcategories(max_pax, max_kinder, min_pax):
    subcategories = []
    json_groups = defaultdict(list)

    for erwachsene in range(1, max_pax + 1):
        max_verbleibende_kinder = min(max_kinder, max_pax - erwachsene)
        kinder_range = [k for k in range(0, max_verbleibende_kinder + 1) if erwachsene + k >= min_pax]

        if not kinder_range:
            continue

        for k in kinder_range:
            subcategories.append({
                'erwachsene': erwachsene,
                'kinder': k,
                'min_pax': min_pax
            })
            json_groups[erwachsene].append(k)

    return subcategories, json_groups

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
subcategories, json_groups = generate_subcategories(
    st.session_state.max_pax,
    st.session_state.max_kinder,
    st.session_state.min_pax
)

if subcategories:
    st.markdown("### Gültige Subkategorien")
    for sub in subcategories:
        st.write(f"{sub['erwachsene']} Erwachsener + {sub['kinder']} Kinder, min. Pax = {sub['min_pax']}")

    # Zusammengefasster JSON-Output für Programmierer
    compressed_json = [
        {
            "erwachsene": erwachsene,
            "kinder": f"{min(kinder)}-{max(kinder)}" if len(set(kinder)) > 1 else f"{kinder[0]}",
            "min_pax": st.session_state.min_pax
        }
        for erwachsene, kinder in json_groups.items()
    ]

    st.markdown("### JSON Output (komprimiert)")
    st.code(json.dumps(compressed_json, indent=2), language="json")
else:
    st.info("Keine gültigen Kombinationen für die aktuelle Einstellung.")
