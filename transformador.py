settings = {
    # Cabecalho
    "projectName": "Transformador",
    "version": "BETA 2.11",
    "Author": "André Lara",
    # Configurações
    "width": 50,
    "precisao": 2, # Número de casas decimais
    # Informações base
    "transformadorPrimario": "", # Y: Y-Monofásico, D: D-Trifásico
    "transformadorSecundario": "", # Y: Y-Monofásico, D: D-Trifásico
    "carga": "",
    "fatorReducao": 0, # Fator de transformação KT
    "potencia": 0, 
    "req" : 0,
    # Tensões base
    "tl1": 0,
    "tl2": 0,
    "tf1": 0,
    "tf2": 0,
    # Correntes base
    "il1": 0,
    "if1": 0,
    "il2": 0,
    "if2": 0,
    # Cargas
    "cargas": []
}



#Transformador monofasico

def tensaoMonofasica(tl1, fatorReducao, typeTransformation):
    response = {
        "tl1": tl1,
        "tl2": tl1 / fatorReducao,
        "typeTransformation": typeTransformation,
        "fatorReducao": fatorReducao,
        "req": 0
    }
    return response

def correnteMonofasica(dictionary):
    response = {
        "req": 0
    }
    req = float(input("Valor da resistência da carga"))
    response["req"] = dictionary["tl2"] / req

    return merge_two_dicts(dictionary, response)



#Transformador trifásico

def tensaoTrifasica():
    tl1 = settings["tl1"]
    fatorReducao = settings["fatorReducao"]
    
    printLine()
    tipo = input("Tipo de circuito primário Y: Estrela, D: Triângulo\n")
    settings["transformadorPrimario"] = tipo
    printLine()
    tipoSec = input("Tipo de circuito secundário Y: Estrela, D: Triângulo\n")
    settings["transformadorSecundario"] = tipoSec

    if (tipo.upper() == "Y"):
        settings["tf1"] = tl1 / 3**0.5

        if (tipoSec.upper() == "Y"):
            settings["tl2"] = settings["tl1"] / fatorReducao
            settings["tf2"] = settings["tl2"] / 3**0.5
            
        elif (tipoSec.upper() == "D"):
            settings["tf2"] = settings["tf1"] / fatorReducao
            settings["tl2"] = settings["tf2"]
            
        else:
            print("Valor inválido")

    elif (tipo.upper() == "D"):
        settings["tf1"] = tl1
        settings["tl2"] = settings["tl1"] / fatorReducao

        if (tipoSec.upper() == "Y"):
            settings["tf2"] = settings["tl2"] * 3 ** 0.5
            
            
        elif (tipoSec.upper() == "D"):
            settings["tf2"] = settings["tl2"]

def correnteTrifasica():

    for charge in settings["cargas"]:
        settings["il2"] += charge["ilc"]
    
    if(settings["transformadorSecundario"].upper() == "Y"):
        settings["if2"] = settings["il2"]
        settings["if1"] = settings["if2"]/settings["fatorReducao"]

    elif (settings["transformadorSecundario"].upper() == "D"):
        settings["if2"] = settings["il2"] / 3**0.5
        settings["if1"] = settings["if2"]/settings["fatorReducao"]

    if (settings["transformadorPrimario"].upper() == "Y"):
        settings["il1"] = settings["if1"]

    else:
        settings["il1"] = settings["if1"] * 3 ** 0.5



#Funções estruturais
def addCharge():
    print("Adicionando Cargas".upper())
    printDoubleLine()
    tipoCarga = input("Tipo de carga: D: Triangulo, Y: Estrela, F-SAIR\n")
    settings["carga"] = tipoCarga

    tlc = settings["tl2"]

    if (tipoCarga.upper() == "D"):
        tfc = tlc

    elif (tipoCarga.upper() == "Y"):
        tfc = tlc / 3 ** 0.5
        
    elif (tipoCarga.upper() == "F"):
        return False
    else :
        print("Valor inválido")
        return False

    printLine()
    req = float(input("Valor da resistência da carga:\n"))

    if (tipoCarga.upper() == "Y"):
        ifc = tfc / req
        ilc = ifc

    elif (tipoCarga.upper() == "D"):
        ifc = tfc / req
        ilc = ifc * 3 ** 0.5
        
    response = {
        "tipoCarga": tipoCarga,
        "tlc": tlc,
        "tfc": tfc,
        "ifc": ifc,
        "ilc": ilc,
    }

    settings["cargas"].append(response)
    return True

def printResult():
    
    tensoes = ["tl1", "tl2", "tf1", "tf2"]
    correntes = ["il1", "il2", "if1", "if2"]
    
    print("TENSOES".center(settings["width"]))
    printLine()
    
    for i in tensoes:
        print(i + " : " + str(round(settings[i], settings["precisao"])) + " V")
    
    printLine()
    print("CORRENTES".center(settings["width"]))
    printLine()
    
    for i in correntes:
        print(i + " : " + str(round(settings[i], settings["precisao"])) + " A")
        
    printLine()
    print("CARGAS".center(settings["width"]))
    printLine()

    for carga in settings["cargas"]:
        print("\nCarga "+ str(settings["cargas"].index(carga) + 1) + carga["tipoCarga"].upper() + " : ")
        print("\ntlc" + carga["tipoCarga"].lower() + " : " + str(round(carga["tlc"], settings["precisao"])))
        print("tfc" + carga["tipoCarga"].lower() + " : " + str(round(carga["tfc"], settings["precisao"])))
        print("ilc" + carga["tipoCarga"].lower() + " : " + str(round(carga["ilc"], settings["precisao"])))
        print("ifc" + carga["tipoCarga"].lower() + " : " + str(round(carga["ifc"], settings["precisao"])))
        printLine()



#Funções Logicas e cálculo
def typeOfTransformation(n1, n2):
    typeTransformation = ""
    if (n1 < n2):
        typeTransformation = "Increase"

    else:
        typeTransformation = "Decrease"

    if (n1 != "null"):
        settings["fatorReducao"] = n1/n2

    return typeTransformation


def selectTransformator():
    printDoubleLine()
    type = input("Tipo de transformador: M: Monofásico T: Trifásico\n")

    response = {}
    tl1 = settings["tl1"]
    fatorReducao = settings["fatorReducao"]

    if (type.upper() == "M"):
        response = tensaoMonofasica(tl1, fatorReducao)
        response = correnteMonofasica(response)
        response = potencia(response)
        printDoubleLine()
        print(response)

    elif (type.upper() == "T"):
        tensaoTrifasica()

        running = True
        while (running):
            printDoubleLine()
            running = addCharge()
            printDoubleLine()
            choice = input("Continuar adicionando? S/N\n")
            if(choice.upper() == "N"):
                running = False

        correnteTrifasica()
        potencia()
        printDoubleLine()


def potencia():
    settings["potencia"] = settings["tl1"] * settings["req"]



#Utilidades
def printLine():
    print("-" * settings["width"])


def printDoubleLine():
    print("="*settings["width"])


def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z


def Header():
    printDoubleLine()
    print("{} & {}".format(settings["projectName"], settings["version"]))
    print("AUTHOR: {}".format(settings["Author"]))
    printDoubleLine()



#Função Principal
def main():
    Header()
    n1 = float(input("Quantidade de voltas no primário: \n"))
    printLine()
    n2 = float(input("Quantidade de voltas no secundário: \n"))
    printLine()
    settings["tl1"] = float(input("Tensão de linha no primário: \n"))
    
    settings["fatorReducao"] = n1/n2

    selectTransformator()
    printResult();


main()