renglones_columnas_finales = ['','','']
sigma = []
finales = []
tabla_transiciones = []
def ObtenerDatos(archivo):
    txt = open(archivo, 'r')
    contenido = txt.read();
    txt.close
    saltos = 0
    FILA = -1
    COLUMNA = 0
    captura = 0
    for i, caracter in enumerate(contenido):
        if (saltos <= 2 and caracter.isnumeric()):
            renglones_columnas_finales[saltos] += caracter
        if (saltos <= 2 and (caracter == '\n')):
            saltos += 1
        if (saltos == 3):
            X = int(renglones_columnas_finales[1])
            Y = int(renglones_columnas_finales[0])
            tabla_transiciones = []
            for i in range(Y):
                a = ['']*X
                tabla_transiciones.append(a)
        if (saltos == 3 and caracter == 'S'):
            saltos += 1
        if (saltos == 4 and caracter == '{'):
            saltos += 1
        if (saltos == 5 and caracter != '}'):
            if (caracter != ' ' and caracter != ',' and caracter != '{' and caracter != '\n'):
                sigma.append(caracter)
        if (saltos == 5 and caracter == '}'):
            saltos += 1    
        if (saltos == 6 and caracter == 'F'):
            saltos += 1
        if (saltos == 7 and caracter == '{'):
            saltos += 1
        if (saltos == 8 and caracter != '}'):
            if (caracter.isnumeric()):
                finales.append(caracter)
        if (saltos == 8 and caracter == '}'):
            saltos += 1
        if (saltos == 9):
            if (caracter == '>'):
                captura = 1
                FILA += 1
                COLUMNA = 0
            if (caracter == '|'):
                COLUMNA += 1
            if (caracter == ','):
                captura = 0
            if (captura == 1 and caracter != '>' and caracter != ' ' and caracter != '|' and caracter != ',' and caracter != '}' and caracter != '\n'):
                tabla_transiciones[FILA][COLUMNA] = tabla_transiciones[FILA][COLUMNA]+caracter 
            if (captura == 1 and (caracter == 'N' or caracter == 'U' or caracter == 'L')):
                tabla_transiciones[FILA][COLUMNA] = ''
    return tabla_transiciones

def calcular_funciones(estado_a_calcular,estadoAFND, AFND):
    trans = AFND[0].copy()
    for x in trans:
        trans[trans.index(x)] = '' 
    for x in estado_a_calcular:
        indiceRen=(estadoAFND.index(x))
        contY = 0
        for y in AFND[indiceRen]:
            trans[contY] += y
            contY += 1
    for tran in trans:
        Ordenar = set(sorted(list(map(int, tran))))
        trans[trans.index(tran)] = ''.join(map(str, Ordenar))
    return trans
def main():
    archivo = input('Ingrese el automata: ')
    AFND = (ObtenerDatos(archivo))
    contador=0
    EstadoAFND=[]
    for renglon in AFND:
        EstadoAFND.append(str(contador))
        contador+=1
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXTabla XXXXXXXXXXXXXXXXXXXX')
    for q in EstadoAFND:
        print('q',q,AFND[int(q)])
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Estados AFD XXXXXXXXXXXXXXXXXXXX')
    AFD=[AFND[0]]
    estadosAFD=[EstadoAFND[0]]
    nEstado = True
    while nEstado == True:
        nEstado = False
        for renglon in AFD:
            for columna in renglon:
                if columna not in estadosAFD:
                    nEstado = True
                    estadosAFD.append(columna)     
        AFD = []
        for estado in estadosAFD:
            AFD.append('')
        for estado in estadosAFD:
            AFD[estadosAFD.index(estado)] = calcular_funciones(estado, EstadoAFND, AFND)
    for q in estadosAFD:
        print ('q',q, AFD[estadosAFD.index(q)])
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Estados Minimizado XXXXXXXXXXXXXXXXXXXX')
    gFinales = []
    gNoFinales = []
    for estado in estadosAFD:
        for caracter in estado:
            if caracter in finales and estado not in gFinales:
                gFinales.append(estado)
    for estado in estadosAFD:
        if estado not in gFinales:
            gNoFinales.append(estado)
    todosGrupos = [gFinales,gNoFinales]
    isNuevoGrupo = False
    while isNuevoGrupo != True:
        isNuevoGrupo = True
        for grupo in todosGrupos:
            if len(grupo) > 1:
                for estado in grupo:
                    for trans in AFD[estadosAFD.index(estado)]:
                        if trans not in grupo and [estado] not in todosGrupos:
                            isNuevoGrupo = False
                            nuevoGrupo = []
                            nuevoGrupo.append(estado)
                            todosGrupos.append(nuevoGrupo) 
                            grupo.remove(estado)                    
    estadosMinAFD = []
    minAFD = []
    for grupo in todosGrupos:
        if grupo != []:
            estadosMinAFD.append(grupo[0])
    for estado in estadosMinAFD:
        minAFD.append(AFD[estadosAFD.index(estado)])
    for columna in minAFD:
        for trans in columna:
            if trans not in estadosMinAFD:
                minAFD[minAFD.index(columna)][columna.index(trans)] = estadosMinAFD[0]
    for q in estadosMinAFD:
        print ('q',q, minAFD[estadosMinAFD.index(q)])
main()