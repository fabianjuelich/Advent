import streamlit as st
from streamlit_lottie import st_lottie
import requests
import re

lion = requests.get('https://lottie.host/1cb7141e-90c2-424f-ada9-afa5441e602e/zikRRfxK2P.json').json()

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

st.set_page_config(page_icon=':santa:', page_title="Oma's Adventskalender")
col1,col2 = st.columns([7,1])
col1.title('Benachrichtigungsabo für Lions-Club-Adventsgewinnkalender :christmas_tree:')
with col2:
    st_lottie(lion, height=128)

with st.form('subscription'):
    email = st.text_input(':email: E-Mail-Adresse `max.mustermann@mail.de`', key='email')
    number = st.number_input(':admission_tickets: Gewinnnummer `1234`', min_value=1, max_value=5000, step=1, value=None, key='number')
    onlyWin = st.checkbox(':gift: Benachrichtige mich nur bei einem Gewinn', value=True, help='Falls deaktiviert, erhält man jeden Tag eine Benachrichtigung darüber, ob man gewonnen hat oder nicht.', key='onlyWin')
    submit = st.form_submit_button('Abonnieren')

if submit:
    valid_email = EMAIL_REGEX.fullmatch(email)
    valid_number = number in range(1, 5001)
    
    if not valid_email:
        st.markdown('__:orange[Fehler]__ :warning:\n\nUngültige E-Mail-Adresse')
    if not valid_number:
        st.markdown('__:orange[Fehler]__ :warning:\n\nUngültige Gewinnnummer')

    if valid_email and valid_number:
        #subscribe()
        st.markdown(f'__:green[Erfolgreich]__ :white_check_mark:\n\n{email} erhält nun Benachrichtigungen für die Gewinnnummer __{number}__ :bell:')
        email = number = onlyWin = submit = None