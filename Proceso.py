class Proceso:
    "Clase para los atributos de un proceso"

    def __init__(self, idProceso, tiempoLlegadaMS, tiempoProcesador, colaEntradasSalidas):
        self.idProceso = idProceso
        self.tiempoLlegadaMS = tiempoLlegadaMS
        self.tiempoProcesador = tiempoProcesador
        self.colaEntradasSalidas = colaEntradasSalidas

class EntradasSalidas: 
    def __init__(self):
        self.idEntradaSalida = 0
        self.tiempoLlegadaMS = 0
        self.tiempoProcesador = 0
        self.tiempoDormida = 0