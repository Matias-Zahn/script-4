import csv
import pprint
from datetime import datetime

ENCABEZADO = ['NroCheque','CodigoBanco','CodigoSucursal','NumeroCuentaOrigen','NumeroCuentaDestino','Valor','FechaOrigen','FechaPago','DNI','Estado']

# Solicitar datos al usuario
def solicitar_datos():
    dni = input("Por favor ingrese el DNI del cliente: ")

    while len(dni) < 8 or len(dni) > 8:
        dni = input("Por favor ingrese correctamente el dni (8 digitos): ").lower()

    cheque_tipo = input("¿Qué tipo de cheque desea buscar (Depositado o Emitido)?: ").lower()
    
    while cheque_tipo != 'emitido' and cheque_tipo != 'depositado':
        cheque_tipo = input("Por favor, ingrese una respuesta valida: ").lower()
    
    estado = input("Desea filtrar por estados? (s/n): ").lower()
    
    while estado != 's' and estado != 'n':
        estado = input("Por favor, ingrese una respuesta valida: ").lower()

    return dni, cheque_tipo, estado


#AQUI SE GUARDA LA RESPUESTA DEL USUARIO
DNI,CHEQUE_TIPO, ESTADO = solicitar_datos()



# Función para buscar cheques por DNI y tipo
def dni_buscador(dni, cheque):
    with open('ejemplo.csv', 'r') as file:
        listado = csv.DictReader(file)
        
        clientes = []

        # Filtrar cheques según el DNI y el tipo de cheque solicitado solicitado
        for fila in listado:
            if dni == fila["DNI"]:
                if(cheque == 'emitido' and fila['NumeroCuentaOrigen'] == dni):
                    clientes.append(fila)
                elif cheque == 'depositado' and fila['NumeroCuentaDestino'] == dni:
                    clientes.append(fila)
        mostrar_resu(clientes, dni)


def mostrar_resu(clientes, dni):
    
    #Si no existe datos que coincida con el dni solicitado, se le permitira volver a ingresar nuevamente el dni
    if len(clientes) == 0:
        print("NO HAY COINCIDENCIAS CON EL DNI SOLICITADO")
        print("Volveremos a solicitar los datos")
        dniNuevo, cheque = solicitar_datos()
        dni_buscador(dniNuevo, cheque)
    else:
        #SI encuentra algun dato que coincida con el dni, se preguntara como desea visualizar dichos datos
        pref = consitir_res()

        #EN CSV
        if(pref == 'csv'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f'{dni}_{timestamp}.csv', 'w') as file:
                writer = csv.DictWriter(file, fieldnames=ENCABEZADO)
                writer.writeheader()
                writer.writerows(clientes)
                print(f"{dni}_{timestamp}.CSV creado con exito.")
        else:
            #EN PANTALLA
            for cliente in clientes:
                pprint.pprint(cliente)


#PERMITE AL USUARIO VOLVER A INGRESAR UNA RESPUESTA VALIDA
def consitir_res():
    res = input("Mostrar datos por PANTALLA o crear archivo CSV: ").lower()
    while res != "pantalla" and res != "csv":
        res = input("Su respuesta es invalida por favor intentelo de nuevo (Pantalla / Csv): ")
    return res


# Llamada a la función para buscar
dni_buscador(DNI, CHEQUE_TIPO)
