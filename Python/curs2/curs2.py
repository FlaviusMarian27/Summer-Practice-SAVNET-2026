'''
1.Creează o listă care să conțină 5 adrese IP la alegerea ta (ca șiruri de caractere). Folosește o buclă for pentru a parcurge lista și afișează fiecare adresă pe ecran, urmată de textul " -> este activ".

2.Folosind o buclă while, scrie un program care să afișeze numerele descrescător, de la 10 până la când numărătoarea se termină, programul trebuie să afișeze mesajul "Start!".

3. Sunteți responsabili cu alocarea unor adrese IP statice pentru un nou etaj dintr-o clădire. Rețeaua este 10.0.0.0/24.
* Scrieți un program care să genereze și să afișeze pe ecran adresele IP de la 10.0.0.50 până la 10.0.0.60 inclusiv.
* Hint: Folosiți funcția range() și concatenarea de string-uri.
4. Aveți următorul dicționar care reprezintă statusul porturilor de pe un switch: status_porturi = {'Fa0/1': 'up', 'Fa0/2': 'down', 'Fa0/3': 'up', 'Fa0/4': 'down', 'Gi0/1': 'up'}
* Scrieți un program care iterează prin acest dicționar și afișează un mesaj de alertă doar pentru porturile care sunt "down".
* Exemplu de output așteptat: ALERTA: Portul Fa0/2 este down!
5. Vrem să simulăm un mecanism simplu de securitate pe un router. Parola corectă este "cisco123".
* Creați o buclă care cere utilizatorului să introducă parola (folosind input()).
* Dacă introduce parola corectă, afișați mesajul "Acces permis" și opriți bucla.
* Dacă introduce altă parolă, afișați "Parolă greșită. Mai încearcă." și lăsați-l să bage din nou. (Pentru simplitate, momentan lăsăm bucla să ruleze la nesfârșit până ghicește, ca un while True).
6. Definiți o funcție numită configurare_bgp care primește doi parametri: as_number (un număr) și neighbor_ip (un string).
* Funcția trebuie să returneze (nu să dea print direct) următorul text formatat, simulând o configurare Cisco: "router bgp [as_number] \n neighbor [neighbor_ip] remote-as 65000"
* După ce ați definit funcția, apelați-o cu argumentele 65001 și "192.168.10.2" și dați print rezultatului.

   7.Creează un dicționar numit router care să conțină următoarele perechi: cheia hostname cu valoarea "R1", cheia ip cu valoarea "10.0.0.1" și cheia status cu valoarea "up". Afișează pe ecran doar valoarea asociată cheii ip. Adaugă o cheie nouă în dicționar numită vendor cu valoarea "Cisco" și afișează întregul dicționar la final.

   8.Scrie o funcție numită calculeaza_putere care primește doi parametri: baza și exponent. Funcția trebuie să calculeze și să returneze rezultatul (baza la puterea exponentului). Apelează funcția dându-i numerele 2 și 3, salvează rezultatul într-o variabilă și printează variabila.

9.Creează o funcție numită cauta_echipament care primește ca parametri o listă de nume de echipamente și un nume_cautat. Folosește o buclă for în interiorul funcției pentru a parcurge lista. Dacă numele căutat este găsit, returnează imediat "Echipament găsit!". Dacă bucla se termină și echipamentul nu a fost găsit, returnează "Nu există în rețea".
'''


print("Exercitiul 1:")
ip_uri = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5"]

for ip in ip_uri:
    print(f"{ip} -> este activ")


#Ex2
print("")
print("Exercitiul 2:")
print("Start")
numar = 10

while numar > 0:
    print(numar)
    numar = numar - 1


#Ex3
print("")
print("Exercitiul 3: ")
for i in range(50, 61):
    print(f"10.0.0.{i}")


#Ex4
print("")
print("Exercitiul 4: ")
status_porturi = {'Fa0/1': 'up', 'Fa0/2': 'down', 'Fa0/3': 'up', 'Fa0/4': 'down', 'Gi0/1': 'up'}

for port, status in status_porturi.items():
    if status == "down":
        print(f"Portul {port} este down!")