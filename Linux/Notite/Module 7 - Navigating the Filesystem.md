### 7.1-7.2 — Structura sistemului de fișiere

**Principiu fundamental Linux:** „everything is a file" — totul (inclusiv directoarele) e considerat fișier.

**Diferența față de Windows** (posibilă întrebare de examen):

|Windows|Linux|
|---|---|
|Top level = "My Computer"|Top level = **root directory**, simbolizat prin `/`|
|Fiecare device are literă de drive (C:, D:, E:)|Nu există litere de drive — fiecare device e montat **sub** un director|

### 7.2.1 — Home Directory

- Se află la `/home/nume_user` (ex: `/home/sysadmin`)
- Când userul deschide un shell, e plasat automat aici
- E unul dintre puținele directoare unde userul are control total (creare/ștergere fișiere), fără restricții de permisiuni ca în restul filesystem-ului

⚠️ **Capcană de examen — simbolul tilde `~`:**

- `~` = home directory-ul userului curent (ex: `~` = `/home/sysadmin`)
- `~bob` = home directory-ul altui user (echivalent cu `/home/bob`)

### 7.2.2 — `pwd` (Print Working Directory)

```
pwd [OPTIONS]
```

Arată **locația curentă** exactă în filesystem (calea absolută).

### 7.2.3 — `cd` (Change Directory)

```
cd [options] [path]
```

⚠️ **Capcane importante:**

- `cd` fără argumente → te duce **direct la home directory**, indiferent unde ești
- Comandă reușită = **fără output** (no news is good news)
- Director inexistent → eroare: `-bash: cd: Junk: No such file or directory`
- Prompt-ul (`~/Documents$`) arată directorul curent, cu `~` = home

### 7.3 — Paths (Căi)

Două tipuri, diferența e **frecvent testată**:

#### 7.3.1 Absolute Paths

- Încep **întotdeauna** cu `/` (root)
- Specifică locația exactă, indiferent unde te afli
- Ex: `cd /home/sysadmin`

#### 7.3.2 Relative Paths

- **NU** încep cu `/`
- Pornesc din directorul curent, folosind numele unui director conținut în el
- Ex: dacă ești în `Documents`, `cd School/Art` te duce direct în Art

### 7.3.3 — Shortcuts

⚠️ **Foarte important pentru examen:**

- **`..`** (două puncte) = directorul **părinte** (un nivel mai sus)
    - `cd ..` → urcă un nivel
    - `cd ../../Downloads` → urcă 2 niveluri, apoi intră în Downloads
- **`.`** (un punct) = directorul **curent**
    - Nu e util direct cu `cd`, dar apare la alte comenzi (ex: `ls -d .`)

### 7.4 — `ls` (Listing files)

```
ls [OPTION]... [FILE]...
```

Fără argumente → listează directorul curent. Cu path ca argument → listează acel director (ex: `ls /var`).

⚠️ **Capcană — culorile din `ls`:** nu sunt comportament implicit al comenzii, ci vin dintr-un **alias**: `ls` e de fapt `ls --color=auto`. Poți verifica asta cu `type ls`. Ca să rulezi comanda **fără** alias: `\ls`.

### 7.4.1 — Fișiere ascunse

- Fișier ascuns = orice fișier/director al cărui nume **începe cu punct** (`.`)
- `ls` **nu** le arată implicit
- `ls -a` → arată tot, inclusiv `.` (director curent) și `..` (părinte)
- De obicei sunt fișiere de configurare/customizare (ex: `.bashrc`, `.profile`)

### 7.4.2 — Long Listing (`ls -l`)

Afișează **metadata**. Foarte important — memorează structura unei linii:

```
-rw-r--r-- 1 root root 15322 Dec 10 21:33 alternatives.log
```

|Câmp|Descriere|
|---|---|
|Primul caracter|**tipul fișierului**|
|Următoarele 9 caractere|permisiuni (detaliate mai târziu)|
|Număr|hard link count|
|user|user owner|
|group|group owner|
|număr|dimensiune în bytes|
|dată|timestamp (ultima modificare a conținutului)|
|nume|numele fișierului|

**Tipuri de fișiere (primul caracter)** — clasic la examen:

|Simbol|Tip|
|---|---|
|`-`|fișier regular|
|`d`|director|
|`l`|symbolic link|
|`s`|socket|
|`p`|pipe|
|`b`|block file|
|`c`|character file|

⚠️ **Capcană:** pentru **directoare**, dimensiunea din `ls -l` **nu** reprezintă conținutul lor, ci spațiul rezervat pentru a ține evidența numelor fișierelor din acel director — se ignoră practic acea valoare.

⚠️ **Symbolic links** — în listare apar cu săgeată: `link -> /path/target`.

### 7.4.3 — Human-Readable Sizes

- `ls -l` → dimensiuni în **bytes**
- `ls -lh` → dimensiuni **human-readable** (K, M, G)

⚠️ **Capcană clasică de examen:** opțiunea `-h` **trebuie** folosită împreună cu `-l` — nu funcționează singură (nu există un mod human-readable fără long listing).

### 7.4.4 — `ls -d` (Listing Directories)

- `-d` = arată **directorul însuși**, nu conținutul lui
- Fără alte opțiuni e cam inutil: `ls -d` → arată doar `.`
- Devine util combinat cu `-l`: `ls -ld` → arată metadata **directorului curent**, nu a fișierelor din el (rezultatul se termină cu `.` la nume)

### 7.4.5 — Recursive Listing (`ls -R`)

- Listează directorul **și toate subdirectoarele** lui, recursiv
- ⚠️ **Atenție (subliniat explicit în curs):** rulat pe `/` (root) ar lista absolut tot sistemul, inclusiv USB-uri și DVD-uri montate — se recomandă folosirea doar pe structuri mai mici


### 7.4.6 — Sortarea listării

Implicit, `ls` sortează alfabetic după nume. Iată opțiunile de sortare — subiect clasic de examen pentru că literele mici se confundă ușor:

|Opțiune|Sortează după|Ordine implicită|
|---|---|---|
|`-S` (literă **mare**)|dimensiune|descrescător (cel mai mare primul)|
|`-t`|timp (data modificării)|cel mai recent modificat primul|
|`-r`|inversează sortarea curentă|—|

⚠️ **Capcană explicit menționată în curs:** opțiunea de sortare după dimensiune este **`-S` cu literă mare**, nu `-s` (small s ar putea fi confundat).

**Combinații uzuale:**

- `ls -lS` → listare detaliată, sortată descrescător după mărime
- `ls -lSh` → la fel, dar cu mărimi human-readable
- `ls -tl` → sortare după timp (cel mai recent primul), cu detalii
- `ls -lrS` → sortare după mărime, dar **inversată** (`-r`) → de la cel mai mic la cel mai mare
- `ls -lrt` → sortare după timp, inversată → de la cel mai vechi la cel mai nou (des folosită practic, pentru loguri)

⚠️ **Notă importantă:** pentru **directoare**, data de modificare reprezintă ultima dată când un fișier a fost **adăugat sau șters** din acel director (nu modificarea conținutului fișierelor din el).

**Timestamp detaliat:** `--full-time` afișează data completă (oră, minut, secundă) — util când mai multe fișiere au aceeași dată afișată în mod normal. Activează automat `-l`.