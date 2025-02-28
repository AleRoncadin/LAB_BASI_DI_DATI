library(DBI)
library(RPostgres)

# Connessione al database PostgreSQL
con <- dbConnect(
  RPostgres::Postgres(),
  dbname = "postgres",
  host = "localhost",
  port = 5432,
  user = "postgres",
  password = "postgres"  # Sostituisci con la tua password
)

# Funzione per caricare un CSV in una tabella PostgreSQL
carica_csv <- function(file_path, table_name) {
  df <- read.csv(file_path, header=TRUE)
  dbWriteTable(con, table_name, df, append=TRUE, row.names=FALSE)
  cat(paste("Dati caricati in", table_name, "da", file_path, "/n"))
}

# Caricamento dei file CSV nelle rispettive tabelle
carica_csv("D:/Universita/3_ANNO/BASI/LABORATORIO/codici/dati/capo_area.csv", "capo_area")
carica_csv("D:/Universita/3_ANNO/BASI/LABORATORIO/codici/dati/mercato.csv", "mercato")
carica_csv("D:/Universita/3_ANNO/BASI/LABORATORIO/codici/dati/agente.csv", "agente")
carica_csv("D:/Universita/3_ANNO/BASI/LABORATORIO/codici/dati/cliente.csv", "cliente")
carica_csv("D:/Universita/3_ANNO/BASI/LABORATORIO/codici/dati/ordine.csv", "ordine")
carica_csv("D:/Universita/3_ANNO/BASI/LABORATORIO/codici/dati/linea_prodotto.csv", "linea_prodotto")
carica_csv("D:/Universita/3_ANNO/BASI/LABORATORIO/codici/dati/partita.csv", "partita")
carica_csv("D:/Universita/3_ANNO/BASI/LABORATORIO/codici/dati/articolo.csv", "articolo")
carica_csv("D:/Universita/3_ANNO/BASI/LABORATORIO/codici/dati/fornitore.csv", "fornitore")
carica_csv("D:/Universita/3_ANNO/BASI/LABORATORIO/codici/dati/fornisce.csv", "fornisce")

# Chiudere la connessione al database
dbDisconnect(con)
