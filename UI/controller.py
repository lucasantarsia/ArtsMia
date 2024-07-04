import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.creaGrafo()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo creato correttamente."))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi."))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumEdges()} archi."))
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()

    def handleCompConnessa(self,e):
        self._view._txt_result.controls.clear()

        # Verifico prima che quello che inserisce l'utente e un intero
        idAdded = self._view._txtIdOggetto.value
        try:
            intId = int(idAdded)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Il valore inserito non è un intero!"))
            self._view.update_page()

        # Verifico se l'id inserito esiste, cioè se fa parte del grafo
        if self._model.checkExistence(intId):
            self._view._txt_result.controls.append(ft.Text(f"L'oggetto {intId} è presente nel grafo."))
        else:
            self._view._txt_result.controls.append(ft.Text(f"L'oggetto {intId} non è presente nel grafo."))

        sizeConnessa = self._model.getConnessa(intId)

        self._view._txt_result.controls.append(ft.Text(f"La componente connessa che contiene {intId} ha dimensione {sizeConnessa}."))

        self._view._ddLun.disabled = False
        self._view._btnCercaPercorso.disabled = False

        # RIEMPIO IL DROPDOWN ddLun
        for i in range(2, sizeConnessa):
            self._view._ddLun.options.append(ft.dropdown.Option(i))

        # Altro modo per riempire il dropdown:
        # myOptsNum = list(range(2, sizeConnessa))
        # myOptsDD = list(map(lambda x: ft.dropdown.Option(x), myOptsNum))
        # self._view._ddLun.options = myOptsDD

        self._view.update_page()

    def handleCercaPercorso(self,e):
        path, peso = self._model.getBestPath(int(self._view._ddLun.value),
                     self._model.getObjectFromId(int(self._view._txtIdOggetto.value)))
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Percorso trovato con peso migliore uguale a {peso}"))
        self._view._txt_result.controls.append(ft.Text(f"Percorso:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()
