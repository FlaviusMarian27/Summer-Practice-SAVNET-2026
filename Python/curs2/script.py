lista = ["SW1","SW2","SW3","SW4","SW5"]

for i in range(len(lista)):
    if lista[i] == "SW4":
        print(f"SW4 gasit la pozitia {i}")
    else:
        print(f"{i} {lista[i]}")