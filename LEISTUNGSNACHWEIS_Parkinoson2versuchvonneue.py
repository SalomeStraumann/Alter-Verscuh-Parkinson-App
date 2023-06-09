# Import der benÃ¶tigten Bibliotheken
import streamlit as st
import pandas as pd
import json
import datetime
from PIL import Image
from jsonbin import load_key, save_key
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import matplotlib.pyplot as plt

# -------- load secrets for jsonbin.io --------
jsonbin_secrets = st.secrets["jsonbin"]
api_key_med = jsonbin_secrets["api_key_med"]
bin_id_med = jsonbin_secrets["bin_id_med"]
api_key_sick = jsonbin_secrets["api_key_sick"]
bin_id_sick = jsonbin_secrets["bin_id_sick"]

# -------- user login --------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)
fullname, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == True:   # login successful
    show_logout_button = True
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()

# Hauptseite
severity_level = {"Kribbeln in den Armen": 7, "Kribbeln in den Beinen": 4}

# Ausgabe der Symptome und Schweregrade ohne geschweifte Klammern und Anführungszeichen
for symptom, level in severity_level.items():
    st.write(f"- {symptom}: {level}")

# Titel der App
st.title("Parkinson Tracker")
# Begrüssung
text_before = "Hallo,"
text_after = "!"
st.header("{} {}{}".format(text_before, username, text_after))
# Information für den Nutzer
st.warning("Bitte beantworte die Fragen in der Seitenleiste")

if show_logout_button:
    # Logout-Button am Ende des Codes platzieren
    authenticator.logout('Logout', 'main')

# Seitenleiste
# Eingabefelder für Datum und Uhrzeit
date = st.sidebar.date_input("Datum", datetime.date(2023, 5, 20))
time = st.sidebar.time_input("Uhrzeit", datetime.time(12, 00))
# Kombination von Datum und Uhrzeit zu einem Datetime-Objekt
datetime_obj = datetime.datetime.combine(date, time)
# Formation des Datetime-Objekts zum String
datetime_string = datetime_obj.strftime('%Y-%m-%d, %H:%M')




# Untertitel Seitenleiste - Befinden
st.sidebar.header(':blue[Befinden]')
# Liste der verfügbaren Symptome
symptoms = [
    'Taubheitsgefühl in den Beinen',
    'Taubheitsgefühl in den Armen',
    'Kribbeln in den Beinen',
    'Kribbeln in den Armen',
    'Tremor (Zittern)',
    'Steifheit der Muskeln',
    'Langsame Bewegungen',
    'Rasche Erschöpfung',
    'Probleme bei der Darmentleerung',
    'Probleme bei der Blasenentleerung',
    'Gangstörungen',
    'Gleichgewichtsstörungen',
    'Sehstörungen',
    'Lähmungserscheinungen',
    'Globale Schmerzen',
    'Keine Symptome'
]
# Multiselect-Widget für die verfügbaren Symptome
selected_symptoms = st.sidebar.multiselect('Symptome', symptoms)
# Eingabefelder für die Schweregrade der ausgewählten Symptome
severity_levels = {}
for symptom in selected_symptoms:
    severity_level = st.sidebar.number_input(
        f'Wie stark ist das Symptom "{symptom}" auf einer Skala? 0 = Nicht vorhanden, 10 = Extrem stark.', 
        min_value=0, 
        max_value=10, 
        value=5
    )
    severity_levels[symptom] = severity_level
# Einschub auf der Hauptseite
# Anzeige der ausgewählten Symptome und Schweregrade auf der Hauptseite, falls Eingabefeld ausgefüllt
if selected_symptoms:
    st.write(':blue[Ausgewählte Symptome und Schweregrade]')
    for symptom in selected_symptoms:
        severity_level = severity_levels[symptom]
        st.write(f'- {symptom}: {severity_level}')
# Speichern der ausgewählten Symptome und Schweregrade in einem Dictionary
    symptoms_and_severity = dict((symptom, severity_levels[symptom]) for symptom in selected_symptoms)
else:
    st.write('Keine Symptome ausgewählt')





    
    
    
    
# Seitenleiste
# Slider fÃ¼r StÃ¤rke der Limitation in der Gesamtheit
feeling = st.sidebar.slider('Wie stark limitieren dich die Symptome gerade im Alltag?', 0, 10, 1)
# Dictionary, das jedem Schweregrad eine Beschreibung zuordnet
severity_levels_lim = {
    0: 'Überhaupt nicht',
    1: 'Kaum',
    2: 'Geringfügig',
    3: 'Leicht',
    4: 'Etwas',
    5: 'MÃ¤ssig',
    6: 'Deutlich',
    7: 'Stark',
    8: 'Sehr stark',
    9: 'Äusserst',
    10:'Extrem'
}
# Beschreibungen der Schweregrade werden unter dem Slider angezeigt
st.sidebar.write(severity_levels_lim[feeling])
# Untertitel Seitenleiste - Kommentare
st.sidebar.header(':blue[Kommentare]')
# Eingabefeld, um Kommentare hinzuzufÃ¼gen
comment = st.sidebar.text_input('Hast du noch weitere relevante Bemerkungen?')
# Einschub auf der Hauptseite
# Anzeige der Kommentare auf der Hauptseite, falls Eingabefeld ausgefÃ¼llt
if comment:
    st.write('Kommentar:')
    st.write(comment)
else:
    st.write('Kein Kommentar hinzugefügt')
# Untertitel Seitenleiste - Medikamente
st.sidebar.header(':blue[Medikamente]')
# Eingabefeld, um einmalige Medikamenteneinnahme hinzuzufÃ¼gen
add_medication = st.sidebar.text_input(
    'Medikament inklusive Dosierung hinzufügen :blue[einmalige Einnahme]'
    )

# Button zum Speichern der Daten
submit = st.sidebar.button('Speichern')
delete = st.sidebar.button("Lezter Eintrag löschen")


# Darstellung der Daten auf der Hauptseite - Daten aus dem Abschnitt "Befinden" und "Medikamente"

# Funktion, um Daten der Tabelle "Krankheitsverlauf" hizuzufÃ¼gen
if submit:
    st.sidebar.write('Deine Daten wurden gespeichert.')
    st.balloons()   
    new_feeling = {
        "Datum und Zeit" : datetime_string,
        "Stärke der Limitation": feeling,
        "Symptome und Schweregrade" : severity_level,
        "Medikament und Dosierung" : add_medication,
        "Kommentare" :comment
    }
    feeling_list = load_key(api_key_sick, bin_id_sick, username)
    feeling_list.append(new_feeling)
    record_sick = save_key(api_key_sick, bin_id_sick, username, feeling_list)
    if 'message' in record_sick:
        st.error(record_sick['message'])

else:
    st.sidebar.write('Deine Daten wurden noch nicht gespeichert.')
 
    
    
 
# Löschen des letzten Eintrags
if delete:
    # delete last entry
    feeling_list = load_key(api_key_sick, bin_id_sick, username)
    feeling_list.pop()
    record_sick = save_key(api_key_sick, bin_id_sick, username, feeling_list)
    if 'message' in record_sick:
        st.error(record_sick['message'])

 
    
# Ãœberschrift  Diagram
st. header(':blue[Limitation im Verlauf der Zeit]')

# Lade die Daten und konvertiere sie in ein DataFrame
#feeling_list = load_key(api_key_sick, bin_id_sick, username)
#new_feeling_data = pd.DataFrame(feeling_list)

# Lade die Daten und konvertiere sie in ein DataFrame
feeling_list = load_key(api_key_sick, bin_id_sick, username)

if feeling_list:
    new_feeling_data = pd.DataFrame(feeling_list)
    # Ausgabe des DataFrames
    st.write(new_feeling_data)
else:
    st.warning('Es sind keine Daten vorhanden.')
    st.stop()

# Index auf Datum setzen
new_feeling_data = new_feeling_data.set_index('Datum und Zeit')

# Benutzereingabe für die Zeitspanne
time_periods = ['Heute', 'Letzte Woche', 'Letzter Monat']
selected_time_period = st.selectbox('Zeitspanne auswählen:', time_periods)

# Filtere die Daten basierend auf der ausgewählten Zeitspanne
if selected_time_period == 'Heute':
    filtered_data = new_feeling_data.tail(5)  # Filtert die letzten 7 Einträge
elif selected_time_period == 'Letzte Woche':
    filtered_data = new_feeling_data.tail(35)  # Filtert die letzten 30 Einträge
elif selected_time_period == 'Letzter Monat':
    filtered_data = new_feeling_data.tail(140)  # Filtert die letzten 90 Einträge
else:
    filtered_data = new_feeling_data  # Kein Filter angewendet

# Darstellung der Daten in einem Diagramm
# Liniendiagramm "Limitation durch die Symptome im Verlauf der Zeit" anzeigen
st.line_chart(filtered_data['Stärke der Limitation'])



# Einschub auf der Seitenleiste - Medikamente zur regelmÃ¤ssigen Einnahme

# Eingabefeld, um regelmÃ¤ssig einzunehmende Medikamente hinzuzufÃ¼gen
add_current_medication = st.sidebar.text_input(
    "Medikament hinzufügen :blue[regelmÃ¤ssige Einnahme]"
    )


# Eingabefeld, um Einnahmezeiten der regelmÃ¤ssig einzunehmenden Medikamente hinzuzufÃ¼gen
add_current_medication_dose = st.sidebar.text_input(
     "Dosierung"
     )


# Eingabefeld, um Einnahmezeiten der regelmÃ¤ssig einzunehmenden Medikamente hinzuzufÃ¼gen
add_current_medication_time = st.sidebar.text_input(
     "Einnahmezeiten"
     )
    

# Zweiter Button zum Speichern der Medikamente
submit_med = st.sidebar.button("zur aktuellen Medikamentenliste hinzufÃ¼gen")
delete_med = st.sidebar.button("Leztes Medikament löschen")




# Darstellung der Daten auf der Hauptseite - Daten aus dem Abschnitt "Medikamente hinzufÃ¼gen regelmÃ¤ssige Einnahme"

# Funktion, um Daten der Tabelle "Medikamente" hizuzufÃ¼gen
if submit_med:
    st.sidebar.write('Das Medikament wurde zur Liste hinzugefÃ¼gt.')
    st.balloons()   
    current_medication = {
    "Medikament" : add_current_medication,
    "Dosierung" : add_current_medication_dose,
    "Einnahmezeiten" : add_current_medication_time
    }
    medi_list = load_key(api_key_med, bin_id_med, username)
    medi_list.append(current_medication)
    record_med = save_key(api_key_med, bin_id_med, username, medi_list)
    if 'message' in record_med:
        st.error(record_med['message'])

else:
    st.sidebar.write('Deine Daten wurden noch nicht gespeichert.')
 
    
 
# Löschen des letzten Eintrags
if delete_med:
    # delete last entry
    medi_list = load_key(api_key_med, bin_id_med, username)
    medi_list.pop()
    record_med = save_key(api_key_med, bin_id_med, username, medi_list)
    if 'message' in record_med:
        st.error(record_med['message'])
        

# Konvertieren der Daten in ein Pandas DataFrame - Daten aus dem Abschnitt "Medikamente hinzufÃ¼gen regelmÃ¤ssige Einnahme"

medi_list = load_key(api_key_med, bin_id_med, username)
medi_list_data = pd.DataFrame(medi_list)


# Index auf Medikament setzen
medi_list_data = medi_list_data.set_index('Medikament')


# Anpassung der Darstellung auf der Hauptseite

# Ãœberschrift
st. header(":blue[Deine Daten auf einen Blick]")

# Darstellung der Daten auf der Hauptseite in zwei Tabs
tab1, tab2 = st.tabs(["Krankheitsverlauf", "Medikamente"])

with tab1:
   st.header("Krankheitsverlauf")
   st.write(new_feeling_data)

with tab2:
    st.header("Medikamente")
    st.write(medi_list_data)
