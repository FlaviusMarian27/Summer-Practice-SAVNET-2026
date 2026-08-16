
### 11.1-11.2 Introducere + Shell Scripts in a Nutshell

Un **shell script** = fișier text cu comenzi executabile, salvate ca să fie rulate repetat. Scriptul are acces la toate comenzile shell-ului.

**Două moduri de a rula un script:**

```
sh test.sh          # rulat ca argument al shell-ului → merge direct
./test.sh           # rulat direct → dă "Permission denied" dacă nu e executabil
chmod +x ./test.sh  # îl faci executabil
./test.sh           # acum merge
```

⚠️ **Capcană de examen:** de ce trebuie `./` în față? Pentru că directorul curent, de regulă, **nu** este în `$PATH`, deci shell-ul nu-l caută acolo automat.

**Shebang** (`#!`) = primele două caractere ale scriptului, indică interpretorul:

bash

```bash
#!/bin/sh
#!/bin/bash
```

"Hash" + "bang" = **shebang** (uneori numit și "crunchbang"). Dacă rulezi scriptul direct (`./script`), interpretorul din shebang e cel folosit, indiferent ce shell ai deschis tu. Dacă îl dai ca argument (`sh script`), shebang-ul e ignorat.

⚠️ Capcană: editoarele de tip office (LibreOffice etc.) NU sunt potrivite pentru scripting — salvează formatare ascunsă în fișier. Se folosește un **editor de text simplu**.

### 11.3 Editing Shell Scripts

Editorul recomandat de LPI Essentials: **nano** (simplu). Alternativa: **vi/vim** (curba de învățare mai abruptă).

Comenzi esențiale în `nano` (**foarte des întrebate la examen**):

|Comandă|Efect|
|---|---|
|Ctrl+X|Exit (întreabă de salvare dacă ai modificări)|
|Ctrl+O|Salvează fără să ieși ("Write Out")|
|Ctrl+K|Taie linia curentă (cut)|
|Ctrl+U|Lipește (paste) ce a fost tăiat|
|Ctrl+W|Caută în document|
|Ctrl+W apoi Ctrl+R|Caută și înlocuiește|
|Ctrl+G|Afișează toate comenzile posibile (help)|
|Ctrl+C|Afișează poziția curentă și mărimea fișierului|

### 11.4 Scripting Basics — 3 concepte cheie

1. **Variabile**
2. **Condiționale**
3. **Bucle (Loops)**

#### 11.4.1 Variabile

bash

```bash
#!/bin/bash
ANIMAL="penguin"
echo "My favorite animal is a $ANIMAL"
```

**Reguli critice (capcane clasice de examen):**

- **NU pui spații** în jurul lui `=` la atribuire → `ANIMAL = "penguin"` dă eroare (`command not found`). Corect: `ANIMAL="penguin"`.
- Ca să **citești** conținutul unei variabile, pui `$` în față: `$ANIMAL`.
- Ca să **atribui**, folosești doar numele, fără `$`: `ANIMAL=...`.
- Numele variabilelor cu majuscule = convenție, nu obligație.

**Variabile speciale (foarte des la examen):**

- `$1`, `$2`, ... `$N` — argumentele trimise scriptului
- `$0` — numele scriptului însuși
- `$?` — codul de ieșire (**exit code**) al ultimei comenzi rulate

bash

```bash
grep -q root /etc/passwd
echo $?     # 0 = succes (găsit)
grep -q slartibartfast /etc/passwd
echo $?     # 1 = eșec (negăsit)
```

⚠️ **Capcană majoră:** exit code **0 = SUCCES** ("totul e OK"), orice altă valoare (1-255) = eroare. E contra-intuitiv față de logica obișnuită unde 0 = fals!

Poți seta manual exit code-ul scriptului tău cu `exit N`:

bash

```bash
exit 1
```

Poți lua rezultatul unei comenzi într-o variabilă cu **backticks**:

bash

```bash
CURRENT_DIRECTORY=`pwd`
```

Input de la utilizator cu `read`:

bash

```bash
echo -n "What is your name? "
read NAME
echo "Hello $NAME!"
```

#### 11.4.2 Conditionale (if/else/elif)

bash

```bash
if grep -q root /etc/passwd; then
  echo "root is in the password file"
else
  echo "root is missing from the password file"
fi
```

Structura obligatorie: **`if ... then ... fi`** (fi = if invers, închide blocul!).

Comanda **`test`** — verifică fișiere/directoare/numere/string-uri:

|Comandă|Descriere|
|---|---|
|`test -f /path`|0 dacă fișierul există|
|`test ! -f /path`|0 dacă fișierul NU există|
|`test -d /tmp`|0 dacă directorul există|
|`test -x \`which ls``|0 dacă userul poate executa|
|`test 1 -eq 1`|0 dacă egalitate numerică|
|`test 1 -ne 1`|inegalitate numerică|
|`test "a" = "a"`|0 dacă string-urile sunt egale|
|`test "a" != "a"`|0 dacă string-urile diferă|
|`-o`|OR (oricare poate fi adevărat)|
|`-a`|AND (ambele trebuie)|

⚠️ **Capcană importantă:** `test` tratează diferit numerele și string-urile! `01` și `1` sunt egale ca **numere**, dar diferite ca **string-uri**.

**`[ ]` este alias pentru `test`** — identice funcțional:

bash

```bash
if test -f /tmp/foo; then
if [ -f /tmp/foo ]; then     # echivalent, dar necesită paranteza de închidere ]
```

**elif** = "else if", pentru comparații multiple:

bash

```bash
if [ "$1" = "hello" ]; then
  echo "hello yourself"
elif [ "$1" = "goodbye" ]; then
  echo "nice to have met you"
else
  echo "didn't understand"
fi
```

Notă: la comparație de string-uri se folosește `=`, nu `-eq` (acela e pentru numere).

**`case`** — alternativă mai curată la if/elif/else lung:

bash

```bash
case "$1" in
hello|hi)
  echo "hello yourself"
  ;;
goodbye)
  echo "nice to have met you"
  ;;
*)
  echo "didn't understand"
esac
```

- se închide cu **`esac`** (case invers, la fel ca `fi`/`if`)
- fiecare bloc se termină cu **`;;`**
- `|` = OR între mai multe pattern-uri posibile
- `*` = "orice altceva" (echivalent cu `else`), trebuie să fie **ultimul**

#### 11.4.3 Bucle (Loops)

**`for`** — pentru o listă finită de elemente:

bash

```bash
SERVERS="servera serverb serverc"
for S in $SERVERS; do
  echo "Doing something to $S"
done
```

⚠️ Capcană: variabila de iterare (`S`) NU are `$` când e definită în `for S in...`, dar `$SERVERS` are `$` fiindcă se extinde lista.

Alte forme:

bash

```bash
for NAME in Sean Jon Isaac David; do    # listă directă, fără variabilă
  echo "Hello $NAME"
done

for S in *; do                          # * = file glob, toate fișierele din director curent
  echo "Doing something to $S"
done
```

**`while`** — rulează cât timp o condiție e adevărată (listă de mărime necunoscută):

bash

```bash
i=0
while [ $i -lt 10 ]; do
  echo $i
  i=$((i + 1))
done
echo "Done counting"
```

- `$(( ... ))` = expresie aritmetică (calcul matematic)
- bucla se oprește când `test` returnează fals

Bucla se închide cu **`done`** (atât la `for` cât și la `while`).

---

**Recapitulare rapidă a cuvintelor cheie asociate (foarte testate la examen):**

- `if ... then ... fi`
- `case ... in ... esac`
- `for ... do ... done`
- `while ... do ... done`