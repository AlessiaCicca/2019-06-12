import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_grafo(self, e):
        numeroMinimo=self._view.txt_goal.value
        if numeroMinimo=="":
            self._view.create_alert("Inserisci un numero minimo di goal fatti")
            return
        grafo = self._model.creaGrafo(float(numeroMinimo))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        self._view.update_page()

    def handle_top(self, e):
        giocatore,avversari=self._model.getTop()
        self._view.txt_result.controls.append(ft.Text(f"TOP PLAYER: {giocatore}."))
        self._view.txt_result.controls.append(ft.Text("AVVERSARI BATTUTI:"))
        for (giocatore, peso) in avversari:
            self._view.txt_result.controls.append(ft.Text(f"{giocatore} | {peso}"))
        self._view.update_page()
    def handle_dream(self,e):
        ngiocatori = self._view.txt_giocatori.value
        if ngiocatori == "":
            self._view.create_alert("Inserire un numero di giocatori")
            return
        costo, listaNodi = self._model.getBestPath( int(ngiocatori))
        self._view.txt_result.controls.append(ft.Text(f"La soluzione migliore ha grado di titolarità pari a {costo}"))
        for nodo in listaNodi:
            self._view.txt_result.controls.append(ft.Text(f"{nodo}"))
        self._view.update_page()


