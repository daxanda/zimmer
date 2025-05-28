import streamlit as st
import json

st.set_page_config(page_title="Zimmerkonfigurator", layout="centered")

st.title("🛏️ Zimmerbelegungskonfigurator")

# Eingaberegler
max_pax = st.slider("Maximale Gesamtbelegung (max_pax)", min_value=1, max_value=20, value=6)
max_kinder = st.slider("Maximale Kinderanzahl (max_kinder)", min_value=0, max_value=max_pax - 1, value=2)
min_pax = st.slider("Mindestbelegung (min_pax)", min_value=1, max_value=max_pax, value=3)

# Logik
feedback = ""
subcategories = []
json_output = []

if max_kinder >= max_pax:
    feedback = "❗ Das Zimmer muss mindestens einen Erwachsenen enthalten. max_kinder darf nicht ≥ max_pax sein."
elif min_pax > max_pax:
    feedback = "❗ Mindestbelegung darf max_pax nicht überschreiten."
else:
    for erwachsene in range(1, max_pax + 1):
        max_verbleibende_kinder = min(max_kinder, max_pax - erwachsene)
        valid_kinder_range = [k for k in range(0, max_verbleibende_kinder + 1) if erwachsene + k >= min_pax]

        if len(valid_kinder_range) > 1:
            kinder_min = valid_kinder_range[0]
            kinder_max = valid_kinder_range[-1]
            subcategories.append(f"{erwachsene} Erwachsener + {kinder_min}–{kinder_max} Kinder, min. Pax = {min_pax}")
            json_output.append({
                "erwachsene": erwachsene,
                "kinder_min": kinder_min,
                "kinder_max": kinder_max,
                "min_pax": min_pax
            })
        elif len(valid_kinder_range) == 1:
            kinder = valid_kinder_range[0]
            subcategories.append(f"{erwachsene} Erwachsener + {kinder} Kinder, min. Pax = {min_pax}")
            json_output.append({
                "erwachsene": erwachsene,
                "kinder_min": kinder,
                "kinder_max": kinder,
                "min_pax": min_pax
            })

# Ausgabe
if feedback:
    st.error(feedback)
else:
    st.subheader("✅ Gültige Subkategorien")
    for line in subcategories:
        st.markdown(f"- {line}")
    st.subheader("📦 JSON für Integration")
    st.code(json.dumps(json_output, indent=2), language="json")