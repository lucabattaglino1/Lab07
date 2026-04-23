import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):

        # faccio un controllo
        if self._mese is None or self._mese < 1 or self._mese > 12:
            self._view.create_alert("Seleziona un mese valido")
            return

        risultati = self._model.getUmidita(self._mese)

        # pulisco
        self._view.txt_result.controls.clear()

        # stampo i risultati
        for r in risultati:
            self._view.txt_result.controls.append(
                ft.Text(f"{r['Localita']}: {r['media']}")
            )

        self._view.update_page()


    def handle_sequenza(self, e):

        # 1. chiedo al model di calcolare la soluzione
        sol = self._model.calcola_sequenza()

        # 2. pulisco la lista risultati nella view
        self._view.lst_result.controls.clear()

        # 3. stampo ogni elemento della soluzione
        for s in sol:
            self._view.lst_result.controls.append(ft.Text(s))

        # 4. aggiorno la pagina (fondamentale!)
        self._view.update_page()


    # questo metodo per salvarmi il mese selezionato dall'utente
    def read_mese(self, e):
        self._mese = int(e.control.value)

