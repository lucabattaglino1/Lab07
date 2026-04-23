from database import meteo_dao


class Model:
    def __init__(self):
        self._situazioni = meteo_dao.MeteoDao.get_all_situazioni()

        self._best = None
        self._best_cost = float("inf")

        # costruisco un dizionario
        self._umidita = {
            "Torino": [],
            "Milano": [],
            "Genova": []
        }

        # lo vado a riempire con città e umidità per ogni giorno
        for s in self._situazioni:
            self._umidita[s.localita].append(s.umidita)

    def getUmidita(self, mese):
        return meteo_dao.getUmidita(mese)

    def calcola_sequenza(self):
        self._best = None
        self._best_cost = float("inf")

        self._ricorsione([], 0)

        return self._best

    # FUNZIONE PRINCIPALE
    # parziale è la sequenza che sto costruendo
    # giorno sarebbe quale giorno sto riempiendo da 0 a 14
    def _ricorsione(self, parziale, giorno):

        # caso base (quando ho finito) --> ho costruito una sequenza completa
        if len(parziale) == 15:
            costo = self.calcola_costo(parziale) # calcolo quanto costa

            if costo < self._best_cost: # se è la migliore la salvo
                self._best_cost = costo
                self._best = list(parziale)
            return

        # caso ricorsivo, dove per ogni giorno provo tutte le città
        for città in ["Torino", "Milano", "Genova"]:

            # VINCOLO 1 --> max 6 giorni per città
            # se ho già usato quella città 6 volte non posso più usarla
            if parziale.count(città) >= 6:
                continue

            # VINCOLO 2 --> min 3 giorni consecutivi prima di cambiare città
            # qui significa che sto cambiando città perchè diversa dall'ultima
            if len(parziale) > 0 and città != parziale[-1]:

                # devo avere almeno 3 giorni già fatti se no non ha senso il vincolo
                if len(parziale) < 3:
                    continue

                # controllo gli ultimi 3 giorni
                if parziale[-1] != parziale[-2] or parziale[-1] != parziale[-3]:
                    continue

            # aggiungo la scelta
            parziale.append(città)

            # ricorsione, vado avanti con il giorno successivo
            self._ricorsione(parziale, giorno + 1)

            # backtrack, torno indietro
            parziale.pop()

    # funzione per andare a calcolare il costo
    def calcola_costo(self, sequenza):

        costo = 0

        for i in range (len(sequenza)): # scorri i giorni
            città = sequenza[i]

            # aggiungo l'umidità di quel giorno
            costo += self.get_umidità(città, i)

            # se cambio città aggiungo 100
            if i > 0 and sequenza[i] != sequenza[i - 1]:
                costo += 100

            return costo

    def get_umidità(self, città, giorno):

        # mi da la lista umidità di quella città per il giorno
        return self._umidita[città][giorno]



