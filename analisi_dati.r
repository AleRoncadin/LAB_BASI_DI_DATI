library(DBI)
library(RPostgres)

# Crea la cartella "grafici" se non esiste
if (!dir.exists("grafici")) {
  dir.create("grafici")
}

# Connessione al database PostgreSQL
con <- dbConnect(
  RPostgres::Postgres(),
  dbname = "postgres",
  host = "localhost",
  port = 5432,
  user = "postgres",
  password = "postgres"  # Sostituisci con la tua password
)

#############################
## ANALISI 1: Trend degli ordini nel tempo (grafico a linee)
#############################
query1 <- "SELECT date_trunc('month', dataordine) AS month, COUNT(*) AS orders FROM ordine GROUP BY month ORDER BY month;"
ordini_mese <- dbGetQuery(con, query1)
ordini_mese$month <- as.Date(ordini_mese$month)

png("grafici/1_trend_ordini_linee.png", width = 800, height = 600)
plot(ordini_mese$month, ordini_mese$orders, type = "o", col = "blue", pch = 19, 
     xlab = "Mese", ylab = "Numero di ordini", main = "N. di ordini per ogni mese")
dev.off()

#############################
## ANALISI 2: Distribuzione del prezzototale degli ordini (istogramma)
#############################
query2 <- "SELECT prezzototale FROM ordine;"
ordini_tot <- dbGetQuery(con, query2)

png("grafici/2_prezzototale_istogramma.png", width = 800, height = 600)
hist(ordini_tot$prezzototale, breaks = 30, col = "lightblue", border = "black", 
     main = "Prezzi degli ordini", xlab = "Prezzo Totale", ylab = "N. ordini")
dev.off()

#############################
## ANALISI 3: Clienti per tipo di mercato (grafico a barre)
#############################
query3 <- "SELECT m.tipo, COUNT(*) AS n_clienti FROM cliente c JOIN mercato m ON c.id_mercato = m.id_mercato GROUP BY m.tipo;"
clienti_mercato <- dbGetQuery(con, query3)

# Converti la colonna in numerico
clienti_mercato$n_clienti <- as.numeric(clienti_mercato$n_clienti)
clienti_mercato <- na.omit(clienti_mercato)

png("grafici/3_clienti_per_mercato.png", width = 800, height = 600)
barplot(clienti_mercato$n_clienti, names.arg = clienti_mercato$tipo, col = "lightgreen",
        main = "Numero di clienti per tipo di mercato", xlab = "Tipo di mercato", ylab = "Numero di clienti")
dev.off()


#############################
## ANALISI 4: Distribuzione delle partite per qualità (grafico a barre)
#############################
query4 <- "SELECT qualita, COUNT(*) AS num_partite FROM partita GROUP BY qualita;"
partite_qualita <- dbGetQuery(con, query4)

partite_qualita$num_partite <- as.numeric(partite_qualita$num_partite)
partite_qualita <- na.omit(partite_qualita)

png("grafici/4_partite_qualita_bar.png", width = 800, height = 600)
barplot(partite_qualita$num_partite, names.arg = partite_qualita$qualita, col = "orange", 
        main = "Numero di partite per qualità", xlab = "Qualità", ylab = "Numero di partite")
dev.off()

#############################
## ANALISI 5: Dot chart - Ranking degli agenti per numero di clienti
#############################
query5 <- "SELECT a.nome AS agente, COUNT(c.id_cliente) AS num_clienti FROM agente a JOIN cliente c ON a.id_agente = c.id_agente GROUP BY a.nome ORDER BY num_clienti DESC;"
agenti_clienti <- dbGetQuery(con, query5)

png("grafici/5_agenti_ranking_dot.png", width = 800, height = 600)
dotchart(agenti_clienti$num_clienti, labels = agenti_clienti$agente, pch = 19, 
         main = "Ranking degli agenti per numero di clienti", xlab = "Numero di clienti")
dev.off()

# Chiusura della connessione
dbDisconnect(con)
