import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.choiceDDnode = None

    def handleCreaGrafo(self, e):
        self._view.txt_result.clean()
        store_id = self._view._ddStore.value
        if store_id is None:
            self._view.create_alert("Scegliere uno store")
            return
        else:
            store_id = int(store_id)
        days = self._view._txtIntK.value
        if days is None:
            self._view.create_alert("Scegliere un numero massimo di giorni")
            return
        try:
            days = int(days)
        except ValueError:
            self._view.create_alert("Scegliere un numero di giorni valido")
            return
        self._model.buildGraph(store_id, days)
        self.fillDDnode()
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente:\n"
                                                      f"Numero di nodi: {nNodes}\n"
                                                      f"Numero di archi: {nEdges}"))
        self._view.update_page()

    def handleCerca(self, e):
        node = self.choiceDDnode
        if node is None:
            self._view.create_alert("Scegliere un nodo di partenza")
            return
        path = self._model.percorsoMassimo(node)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {node.order_id}"))
        for o in path:
            self._view.txt_result.controls.append(ft.Text(f"{o.order_id}\n"))
        self._view.update_page()

    def handleRicorsione(self, e):
        self._view.txt_result.clean()
        start = self.choiceDDnode
        if start is None:
            self._view.create_alert("Scegliere un nodo di partenza")
            return
        bestPath, bestScore = self._model.cammino_ottimo(start)
        self._view.txt_result.controls.append(ft.Text(f"Punteggio massimo: {bestScore}\n"
                                                      f"Il percorso è formato dai nodi:"))
        for n in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{n.order_id}"))
        self._view.update_page()






    def fillDDstore(self):
        for i in self._model.getStoresID():
            self._view._ddStore.options.append(ft.dropdown.Option(i))
        self._view.update_page()

    def fillDDnode(self):
        nodes = self._model.getNodes()
        for n in nodes:
            self._view._ddNode.options.append(ft.dropdown.Option(text=n.order_id, data=n,
                                                                  on_click=self.readDDnode))
            self._view.update_page()

    def readDDnode(self, e):
        if e.control.data is None:
            self.choiceDDnode = None
        self.choiceDDnode = e.control.data
