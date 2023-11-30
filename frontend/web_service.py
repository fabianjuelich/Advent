import streamlit as st

# for safety reasons
try:
    import re, xmlrpc.client
    from enum import StrEnum

    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    class Mode(StrEnum):
        SUB = 'Abonnieren'
        UNSUB = 'Deabonnieren'

    def reset():
        # not necessarily needed
        email = number = daily = mode = submit = None

    def feedback(message):
        st.markdown(message)

    st.set_page_config(page_icon=':santa:', page_title="Oma's Adventskalender")
    st.title('Benachrichtigungsabo für Lions-Club-Adventsgewinnkalender :christmas_tree:')

    with st.form('subscription'):
        # fields
        email = st.text_input(':email: E-Mail-Adresse `max.mustermann@mail.de`', key='email')
        number = st.number_input(':admission_tickets: Gewinnnummer `1234`', min_value=1, max_value=5000, step=1, value=None, key='number')
        daily = not st.checkbox(':gift: Benachrichtige mich nur bei einem Gewinn', value=True, help='Falls deaktiviert, erhält man jeden Tag eine Benachrichtigung darüber, ob man gewonnen hat oder nicht.', key='daily')
        mode = st.radio('Modus', [Mode.SUB.value, Mode.UNSUB.value], 0, horizontal=True, label_visibility='collapsed', key='mode')
        # confirmation
        submit = st.form_submit_button('Okay')

    if submit:
        # validate
        valid_email = email if EMAIL_REGEX.fullmatch(email) else False
        valid_number = number if number in range(1, 5001) else False
        # warnings
        if not valid_email:
            feedback('__:orange[Fehler]__ :warning:\n\nUngültige E-Mail-Adresse')
        if not valid_number:
            feedback('__:orange[Fehler]__ :warning:\n\nUngültige Gewinnnummer')

        if valid_email and valid_number:
            # send data to server
            server = xmlrpc.client.ServerProxy('http://advent-backend:2413')

            if mode == Mode.SUB.value:
                if server.subscribe(valid_email, valid_number, daily):
                    feedback(f'__:green[Erfolgreich]__ :white_check_mark:\n\n{valid_email} erhält nun Benachrichtigungen für die Gewinnnummer _{valid_number}_ :bell:')
                    reset()
                else:
                    feedback(':exclamation: Das hat leider nicht geklappt')

            elif mode == Mode.UNSUB.value:
                if server.unsubscribe(valid_email, valid_number):
                    feedback(f'__:green[Erfolgreich]__ :white_check_mark:\n\n{valid_email} erhält nun __keine__ Benachrichtigungen mehr für die Gewinnnummer _{valid_number}_ :no_bell:')
                    reset()
                else:
                    feedback(':exclamation: Das hat leider nicht geklappt')
except:
    feedback(':x: Versuche es später erneut')