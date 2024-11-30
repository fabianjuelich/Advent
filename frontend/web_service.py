import streamlit as st

# prevent code leak
try:

    import re, xmlrpc.client
    from enum import StrEnum, Enum
    
    # validation of e-mail address
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    # XML-RPC server connection
    server = xmlrpc.client.ServerProxy('http://advent-backend:2413')

    # subscription types
    class Subscription(Enum):
        CREATED = 0
        UPTODATE = 1
        UPDATED = 2
        ERROR = 3
        EXCEPTION = 4

    # functions
    class Mode(StrEnum):
        SUB = 'Abonnieren'
        UNSUB = 'Deabonnieren'

    def reset():
        # not necessarily needed
        email = number = daily = mode = submit = None

    def feedback(message):
        st.markdown(message)

    st.set_page_config(page_icon=':santa:', page_title="Oma's Adventskalender", layout="wide")
    st.title("Oma's Adventskalender :christmas_tree:")

    with st.form('subscription'):
        # fields
        email = st.text_input(':email: E-Mail-Adresse `max.mustermann@mail.de`', key='email')
        number = st.number_input(':admission_tickets: Gewinnnummer `1234`', min_value=1, max_value=5000, step=1, value=None, key='number')
        daily = st.checkbox(':calendar: Tägliche Benachrichtigung', value=True, help='Falls deaktiviert, erhälst du lediglich eine Benachrichtigung bei einem Gewinn.', key='daily')
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
            if mode == Mode.SUB.value:
                result = Subscription(server.subscribe(valid_email, valid_number, daily))
                match(result):
                    case Subscription.CREATED:
                        feedback(f'__:green[Abonniert]__\n\nDu erhälst nun für diese Gewinnnummer Benachrichtigungen')
                        reset()
                    case Subscription.UPTODATE:
                        feedback(f'__:orange[Duplikat]__\n\nDu erhälst für diese Gewinnnummer bereits Benachrichtigungen')
                    case Subscription.UPDATED:
                        feedback(f'__:green[Aktualisiert]__\n\nDie Häufigkeit der Benachrichtigungen für diese Gewinnnummer wurde aktualisiert')
                        reset()
                    case Subscription.ERROR:
                        feedback('__:red[Fehler]__\n\nDas hat leider nicht geklappt')
                    case Subscription.EXCEPTION:
                        feedback('__:red[Ausnahme]__\n\nDas hat leider nicht geklappt')

            elif mode == Mode.UNSUB.value:
                if server.unsubscribe(valid_email, valid_number):
                    feedback(f'__:green[Deabonniert]__\n\nDu erhälst für diese Gewinnnummer nun __keine__ Benachrichtigungen mehr')
                    reset()
                else:
                    feedback('__:red[Ausnahme]__\n\nDas hat leider nicht geklappt')

except:
    feedback(':x: Versuche es später erneut')
