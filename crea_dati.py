import csv
import random
import datetime
from faker import Faker

fake = Faker('it_IT')

# 1. CAPO_AREA (25 record)
capo_area = []
for i in range(1, 26):
    row = {
        "id_capoarea": i,
        "nome": fake.name()
    }
    capo_area.append(row)

# 2. AGENTE (50 record)
agenti = []
for i in range(1, 51):
    row = {
        "id_agente": i,
        "id_capoarea": random.randint(1, 25),
        "nome": fake.name()
    }
    agenti.append(row)

# 3. MERCATO (25 record)
mercati = []
regioni = ["Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna", 
           "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche", 
           "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana", 
           "Trentino-Alto Adige", "Umbria", "Valle d'Aosta", "Veneto"]
macrozoni = ["nord-ovest", "nord-est", "centro", "sud", "isole"]

# Aggiungo le 20 regioni
for i, reg in enumerate(regioni, start=1):
    row = {
        "id_mercato": i,
        "nome": reg,
        "tipo": "Regione"
    }
    mercati.append(row)

# Aggiungo le 5 macrozone
for j, macro in enumerate(macrozoni, start=21):
    row = {
        "id_mercato": j,
        "nome": macro,
        "tipo": "Macrozona"
    }
    mercati.append(row)

# 4. CLIENTE (2000 record)
clienti = []
for i in range(1, 2001):
    row = {
        "id_cliente": i,
        "id_mercato": random.randint(1, 25),
        "id_agente": random.randint(1, 50),
        "nome": fake.name(),
        "cap": str(random.randint(10000, 99999)),
        "provincia": fake.state(),
        "via": fake.street_name(),
        "numerocivico": str(random.randint(1, 200)),
        "paese": "Italia"
    }
    clienti.append(row)

# 5. LINEA_PRODOTTO (10 record)
linee = []
linea_descrizioni = [
    "Carne Bovina", "Carne Suina", "Pollo", "Agnello", "Tacchino",
    "Vitello", "Coniglio", "Maiale", "Anatra", "Pesce"
]
for i in range(1, 11):
    row = {
        "id_linea": i,
        "descrizione": linea_descrizioni[i - 1]
    }
    linee.append(row)

# 6. PARTITA (1000 record)
partite = []
for i in range(1, 1001):
    id_linea = random.randint(1, 10)
    qualita = random.choice(["Prima Scelta", "Seconda Scelta", "Terza Scelta"])
    num_articoli = random.randint(5, 15)  # Numero di articoli nella partita
    costo_acquisto = round(random.uniform(50, 200), 2)
    costo_stoccaggio = round(random.uniform(10, 50), 2)
    costo_spedizione = round(random.uniform(5, 30), 2)
    costo_totale = round(costo_acquisto + costo_stoccaggio + costo_spedizione, 2)
    row = {
        "codice_partita": i,
        "id_linea": id_linea,
        "qualita": qualita,
        "numeroarticoli": num_articoli,
        "acquisto": costo_acquisto,
        "stoccaggio": costo_stoccaggio,
        "spedizione": costo_spedizione,
        "costototale": costo_totale
    }
    partite.append(row)

# 7. ORDINE (5000 record)
ordini = []
# Generiamo date casuali tra il 2020 e il 2025
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2025, 2, 15)
for i in range(1, 5001):
    id_cliente = random.randint(1, 2000)
    random_date = fake.date_between_dates(date_start=start_date, date_end=end_date)
    num_articoli = 2  # per avere esattamente 10000 articoli in totale
    row = {
        "id_ordine": i,
        "id_cliente": id_cliente,
        "dataordine": random_date.strftime("%Y-%m-%d"),
        "numeroarticoli": num_articoli,
        "prezzototale": 0.0  # aggiornato in seguito
    }
    ordini.append(row)

# Creiamo un dizionario per accumulare il prezzo totale per ogni ordine (aggiornato durante la generazione degli articoli)
ordine_totali = {ordine["id_ordine"]: 0.0 for ordine in ordini}

# 8. ARTICOLO (10000 record)
articoli = []
articolo_id = 1
# Per ogni ordine, generiamo esattamente il numero di articoli indicato (2 per ordine)
for ordine in ordini:
    id_ordine = ordine["id_ordine"]
    for j in range(1, ordine["numeroarticoli"] + 1):
        partita = random.choice(partite)
        costo_articolo = round(partita["costototale"] / partita["numeroarticoli"], 2)
        ordine_totali[id_ordine] += costo_articolo
        row = {
            "id_articolo": articolo_id,
            "id_ordine": id_ordine,
            "id_linea": partita["id_linea"],
            "codice_partita": partita["codice_partita"],
            "numerosequenziale": j,
            "costo": costo_articolo
        }
        articoli.append(row)
        articolo_id += 1

# Aggiorniamo il campo PrezzoTotale in ORDINE in base al totale calcolato
for ordine in ordini:
    ordine["prezzototale"] = round(ordine_totali[ordine["id_ordine"]], 2)

# 9. FORNITORE (100 record)
fornitori = []
for i in range(1, 101):
    row = {
        "id_fornitore": i,
        "nome": "Fornitore " + fake.company(),
        "cap": str(random.randint(10000, 99999)),
        "indirizzo": fake.street_address(),
        "provincia": fake.state(),
        "via": fake.street_name(),
        "numerocivico": str(random.randint(1, 200)),
        "paese": "Italia"
    }
    fornitori.append(row)

# 10. FORNISCE (1000 record)
fornisce_set = set()
fornisce = []
while len(fornisce) < 1000:
    codice_partita = random.randint(1, 1000)
    id_fornitore = random.randint(1, 100)
    if (codice_partita, id_fornitore) not in fornisce_set:
        fornisce_set.add((codice_partita, id_fornitore))
        row = {
            "codice_partita": codice_partita,
            "id_fornitore": id_fornitore
        }
        fornisce.append(row)

# Funzione per scrivere i CSV
def write_csv(filename, fieldnames, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Scrittura dei file CSV
write_csv("dati/capo_area.csv", ["id_capoarea", "nome"], capo_area)
write_csv("dati/agente.csv", ["id_agente", "id_capoarea", "nome"], agenti)
write_csv("dati/mercato.csv", ["id_mercato", "nome", "tipo"], mercati)
write_csv("dati/cliente.csv", ["id_cliente", "id_mercato", "id_agente", "nome", "cap", "provincia", "via", "numerocivico", "paese"], clienti)
write_csv("dati/linea_prodotto.csv", ["id_linea", "descrizione"], linee)
write_csv("dati/partita.csv", ["codice_partita", "id_linea", "qualita", "numeroarticoli", "acquisto", "stoccaggio", "spedizione", "costototale"], partite)
write_csv("dati/ordine.csv", ["id_ordine", "id_cliente", "dataordine", "numeroarticoli", "prezzototale"], ordini)
write_csv("dati/articolo.csv", ["id_articolo", "id_ordine", "id_linea", "codice_partita", "numerosequenziale", "costo"], articoli)
write_csv("dati/fornitore.csv", ["id_fornitore", "nome", "cap", "indirizzo", "provincia", "via", "numerocivico", "paese"], fornitori)
write_csv("dati/fornisce.csv", ["codice_partita", "id_fornitore"], fornisce)
