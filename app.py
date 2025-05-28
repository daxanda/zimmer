import streamlit as st

# Initialwerte setzen (nur beim ersten Laden)
if 'max_pax' not in st.session_state:
    st.session_state.max_pax = 8
if 'max_kinder' not in st.session_state:
    st.session_state.max_kinder = 3
if 'min_pax' not in st.session_state:
    st.session_state.min_pax = 2

# Sliders anzeigen
st.session_state.max_pax = st.slider("Maximale Gästezahl (max_pax)", 1, 20, st.session_state.max_pax)
st.session_state.max_kinder = st.slider("Maximale Kinderzahl (max_kinder)", 0, st.session_state.max_pax - 1, st.session_state.max_kinder)
st.session_state.min_pax = st.slider("Mindestbelegung (min_pax)", 1, st.session_state.max_pax, st.session_state.min_pax)

# Logik überprüfen und korrigieren
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
