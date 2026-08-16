### 10.1.1 — `cat` (concatenate)

```
cat fisier
```

Afișează conținutul unui fișier text. Poate combina și fișiere multiple, sau redirecționa output-ul.

⚠️ **Dezavantaj important:** `cat` afișează tot fișierul dintr-o dată, fără posibilitate de pauză — de asta e nepotrivit pentru fișiere mari.

### 10.1.2 — Pageri (`less` și `more`)

|Comandă|Caracteristici|
|---|---|
|`less`|mai avansat, folosit implicit de `man`|
|`more`|mai vechi, mai puține funcții, dar **întotdeauna disponibil** (spre deosebire de `less`, care nu e inclus în toate distribuțiile)|

⚠️ **Capcană de examen:** `less` a fost construit **pe baza** funcționalității lui `more`, deci toate comenzile de la `more` funcționează și în `less` — dar nu neapărat invers.

**Navigare de bază (comune la ambele):**

|Tastă|Acțiune|
|---|---|
|`Spacebar`|o fereastră înainte|
|`B`|o fereastră înapoi|
|`Enter`|o linie înainte|
|`Q`|ieșire|
|`H` (sau `Shift+H`)|help|

**Căutare în `less`:**

- `/pattern` + Enter → caută **înainte**
- `?pattern` + Enter → caută **înapoi**
- `n` → următoarea potrivire
- `Shift+N` → potrivirea anterioară

⚠️ **Notă din curs:** termenii de căutare sunt de fapt **regular expressions** (detaliate mai târziu în curs).

### 10.1.3 — `head` și `tail`

```
head fisier      → primele 10 linii (implicit)
tail fisier      → ultimele 10 linii (implicit)
```

**Specificarea numărului de linii:**

```
tail -5 fisier         (stil vechi)
head -n 3 fisier        (stil modern, cu -n)
```

⚠️ **Capcană majoră de examen — Negative vs Positive Value:**

|Opțiune|`tail`|`head` (versiune GNU)|
|---|---|---|
|`-3` sau `-n 3`|arată **ultimele 3 linii**|arată **primele 3 linii**|
|`-n -3`|tot ultimele 3 linii|arată **TOT în afară de ultimele 3 linii** (comportament diferit!)|

Deci `head -n -3` **NU** înseamnă „primele 3 linii" — înseamnă „toate liniile, mai puțin ultimele 3". Asta e o capcană clasică de examen.

**Positive Value Option (doar la `tail`):**

```
tail -n +25 fisier
```

`+` înainte de număr = afișează **de la linia specificată până la final** (nu ultimele N linii, ci începând cu linia N).

⚠️ **Opțiune utilă practică:** `tail -f fisier` → urmărește fișierul **live**, în timp real (util pentru log-uri, ex: `/var/log/mail.log`).

### 10.2 — Pipes (`|`)

Pipe-ul trimite output-ul unei comenzi ca **input** pentru comanda următoare, în loc să-l afișeze pe ecran.

```
ls /etc | head              → primele 10 fișiere din /etc
ls /etc/ssh | nl              → numerotează liniile (comanda nl)
ls /etc/ssh | nl | tail -5    → numerotează, apoi arată ultimele 5
```

⚠️ **Capcană foarte importantă:** **ordinea contează!** Fiecare comandă vede doar output-ul comenzii precedente.

Exemplu din curs:

- `ls /etc/ssh | nl | tail -5` → numerotare **întâi**, apoi ultimele 5 → numerele rămân cele originale (6-10)
- `ls /etc/ssh | tail -5 | nl` → ultimele 5 **întâi**, apoi numerotare → numerele devin 1-5

Acest exemplu chiar apare explicit ca demonstrație — foarte probabil să fie testat conceptul la examen.

### 10.3 — I/O Redirection

**Cele 3 stream-uri standard:**

|Stream|Nume|Channel #|
|---|---|---|
|STDIN|Standard Input|—|
|STDOUT|Standard Output|#1|
|STDERR|Standard Error|#2|

#### STDOUT (`>` și `>>`)

|Operator|Efect|
|---|---|
|`>`|redirecționează output, **suprascrie** conținutul fișierului existent|
|`>>`|redirecționează output, **adaugă** la finalul fișierului (append)|

⚠️ **Capcană clasică:** `>` **șterge** conținutul anterior al fișierului fără avertisment!

#### STDERR (`2>`)

⚠️ **Foarte important:** implicit, `>` redirecționează doar STDOUT (stream #1). Pentru STDERR, trebuie specificat explicit numărul **2** înainte de `>`:

```
ls /fake 2> error.txt
```

#### Redirecționare simultană a ambelor stream-uri

|Sintaxă|Efect|
|---|---|
|`comanda &> fisier`|STDOUT **și** STDERR în același fișier|
|`comanda > out.txt 2> err.txt`|STDOUT și STDERR în fișiere **separate**|

⚠️ **Capcană de examen:** cu `&>`, în fișierul rezultat, toate mesajele STDERR apar **primele**, urmate de toate mesajele STDOUT — nu în ordinea cronologică a comenzilor. De asemenea, **ordinea în care specifici stream-urile în comandă nu contează**.

#### STDIN (`<`)

- Redirecționare rar folosită direct, pentru că majoritatea comenzilor acceptă nume de fișier ca argument
- Unele comenzi (ex: `tr`) **nu acceptă** fișier ca argument și **necesită** STDIN redirecționat:

```
tr 'a-z' 'A-Z' < example.txt
```

⚠️ Dacă încerci `tr 'a-z' 'A-Z' example.txt` (fără `<`) → eroare `extra operand`, pentru că `tr` nu știe să citească direct dintr-un fișier ca argument.

Poți combina: `tr 'a-z' 'A-Z' < example.txt > newexample.txt`

### 10.4 — `sort`

```
sort fisier
```

Sortează liniile alfabetic (dicționar) implicit.

### 10.4.1 — Field-uri și opțiuni de sortare

|Opțiune|Rol|
|---|---|
|`-t:`|field delimiter (ex: `:` pentru `/etc/passwd`)|
|`-k3`|sortează după câmpul al **3**-lea|
|`-n`|sortare **numerică** (nu alfabetică)|
|`-r`|sortare **inversă**|

Exemplu complet:

```
sort -t: -n -k3 mypasswd
```

⚠️ **Capcană:** fără `-n`, sortarea numerică se comportă ca text (`10` ar veni înaintea lui `2`, alfabetic).


### 10.4.1 (continuare) — Sortare pe câmpuri multiple

```
sort -t, -k2 -k1n -k3 os.csv
```

⚠️ **Capcană de examen:** poți combina **mai multe `-k`** pentru sortare pe câmp primar, apoi secundar, apoi terțiar (în ordinea specificată în comandă). În exemplu: sortează întâi după câmpul 2, apoi (la egalitate) după câmpul 1 numeric, apoi după câmpul 3.

Notă sintaxă: `-k1n` = sortează câmpul 1, numeric (`n` lipit de numărul câmpului).

### 10.5 — `wc` (word count)

```
wc fisier
```

Output cu **4 coloane**:

1. Number of lines
2. Number of words
3. Number of bytes
4. File name

**Opțiuni individuale:**

|Opțiune|Arată doar|
|---|---|
|`-l`|numărul de linii|
|`-w`|numărul de cuvinte|
|`-c`|numărul de bytes|

⚠️ **Uz practic frecvent la examen:** `ls /etc/ | wc -l` → numără câte fișiere sunt într-un director (foarte comun combinat cu pipe).

### 10.6 — `cut`

Extrage **coloane** de text dintr-un fișier delimitat.

```
cut -d: -f1,5-7 mypasswd
```

|Opțiune|Rol|
|---|---|
|`-d`|delimiter (implicit e **tab**, nu spațiu!)|
|`-f`|ce câmpuri să afișeze — range (`5-7`) sau listă (`1,5,6,7`)|
|`-c`|extrage pe baza **poziției caracterelor**, nu a câmpurilor|

⚠️ **Capcană de examen:** delimiter-ul implicit al `cut` e **tab**, nu spațiul — de asta trebuie specificat explicit `-d:` sau `-d,` pentru fișiere separate prin altceva.

Exemplu cu `-c` (poziții fixe, util la output de comandă):

```
ls -l | cut -c1-11,50-
```

`-c1-11` = primele 11 caractere (tip fișier + permisiuni + spațiu), `50-` = de la caracterul 50 până la final (numele fișierului).

### 10.7 — `grep`

Filtrează linii care se potrivesc unui pattern.

```
grep pattern fisier
```

**Opțiuni esențiale — foarte testate:**

|Opțiune|Efect|
|---|---|
|`--color`|evidențiază potrivirea (pe VM e alias-uit automat)|
|`-c`|numără **câte linii** se potrivesc (nu le afișează)|
|`-n`|arată **numărul liniei** originale din fișier|
|`-v`|**inversează** potrivirea — arată liniile care NU conțin pattern-ul|
|`-i`|ignoră majuscule/minuscule (case-insensitive)|
|`-w`|potrivire doar pe **cuvinte întregi**|

⚠️ **Capcană de examen cu `-w`:** `grep are fisier` ar potrivi și „bathrooms" sau „Beware" (pentru că „are" apare ca substring), dar `grep -w are fisier` potrivește **doar** cuvântul „are" de sine stătător.

### 10.8 — Basic Regular Expressions (regex)

⚠️ **Distincție fundamentală de examen:** există **Basic Regular Expressions** (BRE) și **Extended Regular Expressions** (ERE) — comenzi diferite/opțiuni diferite le suportă.

**Basic Regular Expressions — tabel de reținut:**

|Caracter|Semnificație|
|---|---|
|`.`|orice caracter (unul singur)|
|`[ ]`|un caracter din listă/interval|
|`[^ ]`|un caracter care **NU** e în listă|
|`*`|caracterul precedent, repetat de **zero sau mai multe ori**|
|`^`|ancoră — începutul liniei (doar dacă e primul caracter din pattern)|
|`$`|ancoră — sfârșitul liniei (doar dacă e ultimul caracter din pattern)|

⚠️ **Bună practică menționată explicit în curs:** folosește ghilimele simple `'pattern'` în jurul regex-urilor, ca shell-ul să nu le interpreteze greșit.

#### 10.8.1 — Punctul `.`

Matches orice caracter (exact unul), cu excepția newline.

```
grep 'r..f' red.txt    → reef, roof
```

#### 10.8.2 — Parantezele `[ ]`

```
grep '[0-9]' fisier      → linii care conțin o cifră
grep '[^0-9]' fisier     → linii care conțin cel puțin un caracter NON-cifră
```

⚠️ **Capcană majoră explicit subliniată în curs:** `[^0-9]` **NU** înseamnă „linii care nu conțin cifre" — înseamnă „linii care conțin cel puțin un caracter care nu e cifră". O linie compusă **doar** din cifre nu se potrivește cu `[^0-9]`.

⚠️ **Intervalele se bazează pe tabela ASCII**, nu pe alfabet intuitiv: `[a-d]` e valid pentru că `a`(97) < `d`(100), dar `[d-a]` dă eroare (`Invalid range end`).

#### 10.8.3 — Asteriscul `*`

Repetă caracterul precedent de **zero sau mai multe ori**.

⚠️ **Capcană clasică de examen:** un singur caracter urmat de `*` (ex: `e*`) matches **orice linie**, chiar și liniile fără acel caracter — pentru că „zero ori" e valid. Pattern-ul `z*` potrivește toate liniile, chiar dacă niciuna nu conține `z`.

Pentru a fi util, `*` trebuie combinat cu un caracter obligatoriu înainte:

```
grep 'ee*' fisier    → cel puțin un 'e' (primul e obligatoriu, al doilea e* poate repeta)
```

Poate fi combinat și cu paranteze: `[oe]*` = zero sau mai multe apariții din `o` sau `e`.

#### 10.8.4 — Ancore (`^` și `$`)

```
grep '^root' /etc/passwd    → linii care ÎNCEP cu "root"
grep 'r$' fisier             → linii care SE TERMINĂ cu "r"
```

⚠️ **Capcană:** `^` și `$` funcționează ca ancore **doar** dacă sunt poziționate la începutul, respectiv finalul pattern-ului. Altfel sunt tratate ca și caractere literale.

#### 10.8.5 — Backslash `\`

Pentru a căuta un caracter special ca literal (ex: un asterisc real `*`), se pune `\` înainte:

```
grep 're\*' fisier    → caută litera "e" urmată de un asterisc LITERAL
```

### 10.8.6 — Extended Regular Expressions (ERE)

Necesită opțiunea **`-E`** la `grep` (comanda separată `egrep` e deprecated).

|Caracter|Semnificație|
|---|---|
|`?`|caracterul precedent apare **zero sau o dată** (opțional)|
|`+`|caracterul precedent apare **una sau mai multe** ori|
|`\|`|alternare, ca „SAU" logic|

```
grep -E 'colou?r' fisier      → matches "color" SAU "colour"
grep -E 'e+' fisier           → cel puțin un 'e'
grep -E 'gray|grey' fisier    → matches "gray" SAU "grey"
```

⚠️ **Capcană de examen — diferența `*` (BRE) vs `+` (ERE):**

- `*` = zero sau mai multe (deci poate să nu existe deloc caracterul)
- `+` = **una** sau mai multe (caracterul trebuie să existe măcar o dată)

---

**Rezumat rapid — tabel BRE vs ERE (foarte probabil la examen):**

|Simbol|Tip|Înseamnă|
|---|---|---|
|`.`|BRE|orice caracter|
|`[ ]`|BRE|un caracter din set|
|`[^ ]`|BRE|un caracter NU din set|
|`*`|BRE|zero+ repetări|
|`^` `$`|BRE|ancore linie|
|`?`|ERE|0 sau 1|
|`+`|ERE|1+ repetări|
|`\|`|ERE|SAU logic|