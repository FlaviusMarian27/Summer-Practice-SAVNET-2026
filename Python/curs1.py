'''
Exercițiul 1: Formularul de prezentare (Nivel: Foarte ușor)
* Cerință: Cere-i utilizatorului să introducă numele lui și băutura preferată folosind funcția input(). Salvează-le în două variabile. Folosește un f-string pentru a afișa un mesaj simpatic, de exemplu: "Salut, [nume]! Îți pregătim imediat un [băutura]!".
Exercițiul 2: Convertorul de vârstă (Nivel: Ușor)
* Cerință: Cere-i utilizatorului vârsta în ani. Transformă valoarea introdusă într-un număr întreg (typecasting) și calculează câte luni a trăit utilizatorul (înmulțind cu 12). Afișează rezultatul.
Exercițiul 3: Analiza textului (Nivel: Ușor spre Mediu)
* Cerință: Definește o variabilă care conține un text lung (ex: " python este super tare! "). Aplică pe acest șir de caractere trei metode învățate: elimină spațiile de la capete (folosind strip(), dacă le-ai arătat, sau extragere prin slicing), transformă totul în litere mari cu upper() și numără de câte ori apare litera "E".
Exercițiul 4: Par sau Impar? (Nivel: Ușor)
* Cerință: Cere utilizatorului un număr întreg. Folosește operatorul modulo (% - restul împărțirii) pentru a verifica dacă numărul este par sau impar. Dacă restul împărțirii la 2 este 0, afișează "Număr par", altfel afișează "Număr impar".
Exercițiul 5: Accesul interzis (Nivel: Ușor)
* Cerință: Cere utilizatorului să introducă vârsta. Dacă vârsta este mai mare sau egală cu 18, afișează mesajul "Acces permis. Bun venit!". Dacă este mai mică de 18, afișează "Acces interzis. Ești prea tânăr!".
Exercițiul 6: Generatorul de calificative (If-Elif-Else) (Nivel: Mediu)
* Cerință: Cere-i utilizatorului o notă de la 1 la 100.
    * Dacă nota este >= 90, afișează "Excelent (A)".
    * Dacă nota este >= 70, afișează "Bine (B)".
    * Dacă nota este >= 50, afișează "Treci clasa (C)".
    * Altfel, afișează "Ai picat (F)".
Exercițiul 7: Cafeneaua Inteligentă (Nivel: Dificil)
* Cerință: Oferă-le un dicționar cu produse și prețuri (ex: meniu = {"espresso": 10, "cappuccino": 15, "latte": 18}). Cere utilizatorului să introducă numele unei băuturi pe care o dorește. Verifică dacă băutura există în dicționar folosind operatorul in și metoda .keys(). Dacă există, afișează "Comanda va costa X lei". Dacă nu, afișează "Ne pare rău, nu avem acest produs."
Exercițiul 8: Minicalculator cu decizii (Nivel: Cel mai dificil)
* Cerință: Construiește un calculator simplu. Cere utilizatorului două numere (float). Apoi, cere utilizatorului să introducă o operație (un string): "+", "-", "*" sau "/". Folosește if-elif-else pentru a efectua operația corectă pe baza șirului introdus și afișează rezultatul. Cazul ideal este să adaugi o verificare suplimentară pentru a nu împărți la 0!

'''


#Ex1

print("Exercitiul 1:")
nume = input("Introduce un nume: ")
bautura = input("Introduce o bautura: ")

print(f"Salut, numele meu este {nume}! Bautura mea preferata este {bautura}!")

#Ex2
print("")
print("Exercitiul 2:")
varsta = input("Introduce varsta: ")
varsta = int(varsta)
luni = varsta * 12
print(f"Result: {luni} luni")

#Ex3
print("")
print("Exercitiul 3:")
text = "Python-ul este un limbaj de programare foarte frumos"

text1 = text.strip()
text_mare = text1.upper()
numar_e = text_mare.count("E")

print(f"Textul initial: {text}")
print(f"Textul dupa strip: {text1}")
print(f"Textul cu upper: {text_mare}")
print(f"Aparitile literei E: {numar_e}")


#Ex4
print("")
print("Exercitiul 4:")

numar = int(input("Alege un numar pentru a determina paritatea: "))
if numar % 2 == 0:
    print(f"{numar} este par!")
else:
    print(f"{numar} este impar!")


#Ex5
print("")
print("Exercitiul 5: ")

varsta = int(input("Alege varsta: "))

if(varsta >= 18):
    print("Acces permis. Bun venit!")
else:
    print("Acces interzis. Esti prea tanar!")


#Ex6
print("")
print("Exercitiul 6: ")

nota = int(input("Introduce nota de la 0 la 100: "))

if nota >= 90:
    print("Excelent (A)")
elif nota >= 70:
    print("Bile (B)")
elif nota >= 50:
    print("Treci clasa (c)")
else:
    print("Ai picat (F)")


#Ex7
print("")
print("Exercitiul 7: ")

meniu = {"espresso": 10, "cappuccino": 15, "latte": 18}
bautura1 = input("Introduce o bautura: ").lower()

if bautura1 in meniu:
    print(f"Comanda va costa {meniu[bautura]} lei")
else:
    print("Ne pare rău, nu avem acest produs.")


#Ex8
print("")
print("Exercitiul 8: ")

numar1 = float(input("Introdu primul numar: "))
numar2 = float(input("Introdu al doilea numar: "))
operatie = input("Introdu operatia (+, -, *, /): ")

if operatie == "+":
    print(f"Rezultat: {int(numar1 + numar2)}")
elif operatie == "-":
    print(f"Rezultat: {int(numar1 - numar2)}")
elif operatie == "*":
    print(f"Rezultat: {int(numar1 * numar2)}")
elif operatie == "/":
    if numar2 == 0:
        print("Eroare: nu se poate imparti la 0!")
    else:
        print(f"Rezultat: {int(numar1 / numar2)}")
else:
    print("Operatie necunoscuta.")