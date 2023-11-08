from operator import attrgetter
from queue import Queue
import sys
import Proceso

def RoundRobin(qp):    
    tiempoAnterior =0
    tiempoActual = 0
    intercambio = 1
    qpOrdenada = ordenarCola(qp)

    qpRoundRobin = Queue(cantidadProcesos)
      
    print("DIAGRAMA DE GANTT\n")
    while not qpRoundRobin.empty() or tiempoActual==0:
        if tiempoActual == 0: #Esto se realiza para que obtenga de la cola de procesos a la cola de listos la primera vez
            qpRoundRobin.put(qpOrdenada.get())  
        proceso = qpRoundRobin.get() #Se extrae el proceso a trabajar de la cola de listos
        
        tiempoAnterior = tiempoActual #Se actualiza el tiempo anterior
        tiempoActual = tiempoActual + (1*3 + intercambio ) #El 1*50 representa un quantum mulplicado por sus milisegundos respectivos
        
        #Llamar metodo para escribir cola de listos en un txt

        proceso.tiempoProcesador = proceso.tiempoProcesador -1 #Se le resta el quantum trabajado al proceso

        if not qpOrdenada.empty():  #Se revisa si hay mas procesos por entrar en la cola de procesos
            pEvaluar = qpOrdenada.get() #Se extrae el siguiente proceso en orden cronologico de la lista de procesos
            #Validar si entra proceso luego de trabajar con uno
            if(tiempoActual >= pEvaluar.tiempoLlegadaMS ): #and tiempoAnterior <= pEvaluar.tiempoLlegadaMS 
                        qpRoundRobin.put(pEvaluar)  #significa que el proceso llego y debe ser añadido a la cola de listos
            else:
                 qpOrdenada.put(pEvaluar)   #el proceso aun no ha llegado por lo cual se devuelve a la espera
                 qpOrdenada = ordenarCola(qpOrdenada)   #se ordena la cola en orden de llegada
        
        if (proceso.tiempoProcesador != 0): #se verifica si el proceso ya termino
            qpRoundRobin.put(proceso)   #si el proceso no ha terminado se vuelve a añadir a la cola de listos
            
                
        if(proceso.tiempoProcesador == 0):     
            if not proceso.colaEntradasSalidas.empty():
                entradaSalida =proceso.colaEntradasSalidas.get()
                tiempoDespertar = tiempoActual + entradaSalida.tiempoDormida*3
                
                proceso.tiempoLlegadaMS = tiempoDespertar
                proceso.tiempoProcesador = entradaSalida.tiempoProcesador

                qpOrdenada.put(proceso)
                qpOrdenada = ordenarCola(qpOrdenada)

        if(qpOrdenada.empty() and qpRoundRobin.empty()):    #Se evalua si ya todo el procedimiento termino para no poner intercambio
            tiempoActual = tiempoActual-intercambio
            intercambio = 0
        
        print("Proceso numero: "+ str(proceso.idProceso) +" "+str(tiempoActual- intercambio)+ " " +str(1))
        
        if not(qpOrdenada.empty() and qpRoundRobin.empty()):
            print("Intercambio: "+ str(1/intercambio))
    print("El algoritmo termina en el milisegundo: "+ str(tiempoActual))

def ordenarCola(qp):
    listCola = list(qp.queue)
    listaOrdenada = sorted(listCola, key=attrgetter('tiempoLlegadaMS'))
    qpOrdenada = Queue(cantidadProcesos)
    for proceso in listaOrdenada:
        qpOrdenada.put(proceso)
    return qpOrdenada

print("Ingrese la cantidad de procesos")
cantidadProcesos = int(input())

if (cantidadProcesos<=0):
    print("Programa finalizado")
    sys.exit()
else:
    qp = Queue(cantidadProcesos)
    for i in range(cantidadProcesos):

        print("Ingrese un tiempo de llegada para el proceso {} en MS ".format(i))
        tiempoLlegadaMS = int(input())
        print("Ingrese el tiempo que requiere en quantums el proceso",i)
        tiempoQ = int(input())
        print("cuantas entradas/salidas tiene el proceso ",i)
        entradaSalidaCant = int(input())
        if(entradaSalidaCant <=0 ):
            entradaSalidaCant = 0
   
        colaEntradasSalidas = Queue()        
        for j in range( entradaSalidaCant):
            entradaSalida = Proceso.EntradasSalidas()
            if(entradaSalidaCant > 0):
                print("Cuanto va a dormir el proceso ",i," en QUANTUM entrada y salida # ",j)
                dormidaPorProceso = int(input())
                print("Cuantos quantum va a requerir la entrada y salida del proceso", i)
                quantumEntradaSalida = int(input())
                          
                entradaSalida.idEntradaSalida = j                          
                entradaSalida.tiempoDormida = dormidaPorProceso
                entradaSalida.tiempoProcesador = quantumEntradaSalida

                colaEntradasSalidas.put(entradaSalida)
        proceso = Proceso.Proceso(i, tiempoLlegadaMS, tiempoQ, colaEntradasSalidas)
        qp.put(proceso)

    RoundRobin(qp)









#while not qpOrdenada.empty():
    #print(qpOrdenada.get().idProceso)


