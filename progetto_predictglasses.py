import os.path
import PySimpleGUI as sg
#per leggere da file CSV importo csv
import csv
import glob
import matplotlib.pyplot as plt


#dati righe mi serve per inglobare le righe del file CSV scelto
dati_righe = []
#lista che contiene i nomi dei file CSV
nomi_file_csv = []
#conterrà il nome del file csv per elaborarlo
csv_scelto = ""
#user e password per effettuare login
user = ""
password = ""
def welcomeLayout():
    welcome_layout = [
        [sg.Text("Benvenuto! Selezionare l'opzione per iniziare...")],
        [sg.Button("Login")],
        [sg.Button("Registrati")]
    ]

    welcome_layout = sg.Window('Benvenuto', welcome_layout, size=(300, 300))
    while True:
        event, values = welcome_layout.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Login':
            login, user, password = doLogin()
            doDashboard(user, password)
            break
        elif event == 'Registrati':
            pass
        break


def doLogin():
    layout = [
        [sg.Text("Username")], [sg.InputText(key='-username-')],
        [sg.Text("Password")], [sg.InputText(key="-password-", password_char="*")],
        [sg.Button("Accedi")]
    ]

    login_window = sg.Window("Login username", layout, size=(300,300))

    login = False

    while True:
        event, values = login_window.read()

        if event == sg.WINDOW_CLOSED:
            main()
        if event == "Accedi":
            # Verifica delle credenziali inserite
            username = values["-username-"]
            password = values["-password-"]

            if username == "admin" and password == "password":
                login = True
                login_window.close()
                return login, username, password
            else:
                sg.popup("Credenziali non valide. Riprova.")


def findCSV():
    global csv_scelto
    #Leggo da directory corrente
    folder = os.path.dirname(os.path.abspath("PythonExam"))
    path_search = os.path.join(folder, '*.csv')
    for percorso_file in glob.glob(path_search):
        nome_file = os.path.basename(percorso_file)
        nomi_file_csv.append(nome_file)

    print("File trovati CSV da poter analizzare...\n")
    for nome_file in nomi_file_csv:
        print(nome_file)

    #creo una finestra che mi permette di vedere i csv nella cartella
    layout = [
        [sg.Button(nomi_file_csv[0])],[sg.Button(nomi_file_csv[1])],[sg.Button("Annulla")]
    ]

    loadCSV = sg.Window("Scegli CSV", layout, size=(300,300))
    load = False

    event, values = loadCSV.read()

    if event == "Annulla":
        loadCSV.close()

    if event == nomi_file_csv[0]:
        csv_scelto = nomi_file_csv[0]
        dati_righe = readCSV(nomi_file_csv[0])

    if event == nomi_file_csv[1]:
        csv_scelto = nomi_file_csv[1]
        dati_righe = readCSV(nomi_file_csv[1])

    loadCSV.close()
    return dati_righe

def readCSV(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        dati_righe = [riga for riga in reader]
    return dati_righe

def cercaArticoliID(ID):
    risultati = []
    indice_riga = None
    succ = False
    righe_filtrate = []
    for riga in dati_righe:
        if riga and riga[0] == ID:
            righe_filtrate.append(riga)

    if righe_filtrate :
        print("Righe trovate con ID : ",ID)
        for riga in righe_filtrate:
            risultati.append(riga)
            succ = True
    else:
        print("Nessuna riga trovata per l'ID cercato...\n")
    return succ, risultati


def cercaArticoliMarca(marca):
    risultati = []
    indice_riga = None
    succ = False
    righe_filtrate = []
    for riga in dati_righe:
        if riga and riga[1] == marca:
            righe_filtrate.append(riga)
    if righe_filtrate:
        print("Righe trovate con marca '", marca,"'")
        for riga in righe_filtrate:
            risultati.append(riga)
            succ = True
    else:
        print("Nessuna riga trovata per la marca cercata...\n")
    return succ, risultati


def GenerateGraficoQuality():
    count_passati = 0
    count_falliti = 0
    for riga in dati_righe:
        if riga and riga[9] == 'Passato':
            count_passati += 1
        elif riga and riga[9] == 'Fallito':
            count_falliti += 1

    print("Modelli Passati al Test Qualità : ",count_passati)
    print("Modelli Falliti al Test Qualità : ", count_falliti)

    totale = count_passati + count_falliti
    #Calcolo percentuale passati
    perc_pass = (count_passati / totale) * 100
    perc_fail = (count_falliti / totale) * 100
    #Creo i dati del diagramma a torta
    dati = [perc_pass, perc_fail]
    #Creo etichette per il diagramma
    etichette = ['Passato','Fallito']
    #Creo l'effettivo diagramma a torta
    plt.pie(dati, labels=etichette, autopct='%1.1f%%')
    #Aggiungo titolo
    plt.title('Risultati Test Qualità')
    #Mostro il diagramma
    plt.show()

#genero diagramma a barre che contiene tutte le marche per fascia di prezzo
def GenerateGraficoBestLabel():
    marche = []
    prezzi = []
    for riga in dati_righe:
        if len(riga) > 1 and len(riga) > 6:
            marca = riga[1]
            prezzo = riga[6]

            try:
                prezzo = float(prezzo)
                marche.append(marca)
                prezzi.append(prezzo)
            except ValueError:
                continue

    plt.bar(marche, prezzi)
    plt.xlabel('Marca')
    plt.ylabel('Prezzo')
    plt.title('Prezzi per Marca')
    plt.xticks(rotation=45)
    plt.show()

def showTableFromCSV(dati_righe):
    succ = False #succ è la variabile che indica il successo della ricerca
    #creo layout finestra tabella
    layout = [
        [sg.Table(values=dati_righe[1:], headings=dati_righe[0], key='Tabella', display_row_numbers=False, auto_size_columns=True,
                  justification='left', num_rows=30, size=(500,400))],
        [sg.Text("uguale a [ inserisci l'ID ]: ")], [sg.InputText(key='ID')], [sg.Button("Cerca per ID")],
        [sg.Text("contiene [ inserisci la marca ]: ")], [sg.InputText(key='Marca')], [sg.Button("Cerca per Marca")],
        [sg.Button("Ripristina Tabella")],
        [sg.Button("Genera Grafico Qualità")],[sg.Button("Genera Grafico Migliore Marca")]
    ]

    # Crea la finestra
    finestra = sg.Window('Tabella', layout, size=(1000, 900))

    # Leggi gli eventi della finestra
    while True:
        evento, valori = finestra.read()
        if evento == sg.WINDOW_CLOSED:
            break

        if evento == "Ripristina Tabella":
            finestra['Tabella'].update(values=dati_righe[1:]) #ripristino i valori con quelli caricati
                                                              #precedentemente

        if evento == "Cerca per Marca":
            marca = valori["Marca"]
            succ, risultati = cercaArticoliMarca(marca)
            if succ == True:
                finestra['Tabella'].update(values=risultati) #mostro cambiamento della vista della tabella con i risultati filtrati per marca
            else:
                sg.popup("Marca non trovata", title="Errore")
        if evento == "Cerca per ID":
            ID = valori["ID"]
            succ, risultati = cercaArticoliID(ID)
            if succ == True:
                finestra['Tabella'].update(values=risultati) #mostro cambiamento della vista dei risultati ricerca per ID
            else:
                sg.popup("Articolo non trovato!", title="Errore")

        #se l'evento è la generazione del grafico allora provvedo a chiamate GenerateGrafico
        #(vedo se istogramma, diagramma a torta o un semplice plot sulle vendite) dell'istantanea della tabella
        #visualizzata a video
        if evento == "Genera Grafico Qualità":
            GenerateGraficoQuality()

        if evento == "Genera Grafico Migliore Marca":
            GenerateGraficoBestLabel()
    finestra.close()

def viewDashLayout(user):
    dashboard_layout = [
        [sg.Text(f'Benvenuto {user}', key='-zzz-')],
        [sg.Text("Benvenuto nella dashboard!")],
        [sg.Button("Carica dati CSV")],
        [sg.Button("Esegui machine learning")],
        [sg.Button("Logout")],
        [sg.Button('Refresh')]
    ]
    return dashboard_layout

def doDashboard(usr, pwd):
    global user, dati_righe
    user = usr
    dashboard_layout = viewDashLayout(user)
    winDashboard = sg.Window('Dashboard', dashboard_layout, size=(300,300))

    while True:

        event, values = winDashboard.read()

        winDashboard['-zzz-'].update(usr)

        if event == "Carica dati CSV":
            dati_righe = findCSV() #trova file CSV
            doDashboard(user, pwd)
            break

        if event == "Esegui machine learning":
            showTableFromCSV(dati_righe)
            break

        if event == sg.WINDOW_CLOSED:
            break
        if event == "Logout":
            winDashboard.close()
            main()
            break

        if event == 'Refresh':
            winDashboard['-zzz-'].update(usr)

    winDashboard.close()


def showErrorMessage(error):
    if (error == 'BadLogin'):
        print('No data found')


def main():
    welcomeLayout()


# --- MAIN ---
if (__name__ == '__main__'):
    main()