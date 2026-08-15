
# 5.1 Introduction

- CLI-ul ideal pentru putere, viteză și abilitatea de a face task-urile complexe cu o singură comandă.

--- 
## 5.2 Shell

- **Shell** = interpretorul de linie de comandă care traduce comenzile în acțiuni pe care le execută OS-ul
- Cel mai folosit shell pe distribuții Linux: **Bash**
- Funcții avansate Bash:
    - **Scripting** - pui comenzi într-un fișier și le execuți pe toate deodată; are elemente de programare (condiționale, funcții)
    - **Aliases** - porecle scurte pentru comenzi lungi
    - **Variables** - stochează informații pentru shell/user

**Structura promptului** - de reținut exact (posibil examen):

```
sysadmin@localhost:~$
```

- **sysadmin** = User Name
- **localhost** = System Name
- **~** = Current Directory (simbolul **~** = shorthand pentru home directory, de regulă `/home/nume_user`)

---
## 5.3 Commands

- **Command** = program software care, executat în CLI, face o acțiune
- Formatul tipic: `command [options] [arguments]`
- **Options** = modifică comportamentul de bază al comenzii
- **Arguments** = furnizează informații suplimentare (ex: un nume de fișier)
- ⚠️ **Linux e case-sensitive** — comenzi, opțiuni, argumente, variabile, nume de fișiere trebuie scrise exact


**5.3.1 Arguments** 
- ex: `ls /etc/ppp` listează conținutul acelui director; 
- poți da mai multe argumente: `ls /etc/ppp /etc/ssh`


**5.3.2 Options**
- `-l` = long listing (mnemonic: **l**ong) — arată permisiuni, dimensiune, dată
- `-r` = reverse order (mnemonic: **r**everse)
- Opțiunile se pot combina: `-l -r` = `-rl` = `-lr` (ordinea nu contează)
- Implicit, `-l` arată dimensiunea în **bytes**; adăugând `-h` (human-readable) arată în format ușor de citit (ex: 11K)
- ⚠️ De reținut: opțiunile scurte (o literă) sunt precedate de **un singur dash** `-h`; opțiunile complete (cuvinte) sunt precedate de **două dash-uri** `--human-readable`


**5.3.3 History**
- `history` = afișează lista comenzilor rulate în sesiunea curentă
- Săgeata **Up** = afișează comanda anterioară
- Pentru re-execuție: `!n` (execută comanda cu numărul n din listă), `!-n` (execută comanda a n-a **de la coadă**), `!!` (repetă ultima comandă), `!nume_comanda` (repetă ultima execuție a acelei comenzi specifice)
- `history 3` = afișează ultimele 3 comenzi



---

## 5.4 Variables

Două tipuri: **local** și **environment**

**5.4.1 Local Variables**

- Există doar în shell-ul curent, se pierd la închiderea terminalului
- Setare: `variable=value`
- Afișare: `echo $variable1`

**5.4.2 Environment Variables**

- Numite și **global variables**, disponibile system-wide, în toate shell-urile
- Exemple: `PATH`, `HOME`, `HISTSIZE` (definește câte comenzi anterioare se stochează în history)
- `env` = afișează toate variabilele de mediu (des combinat cu `grep` prin pipe `|` pentru filtrare)
- `export variable` = transformă o variabilă locală în variabilă de mediu
- `unset variable` = șterge o variabilă exportată

**5.4.3 PATH Variable** — foarte important de examen!

- **PATH** = lista de directoare în care shell-ul caută comenzi
- Dacă o comandă nu e găsită în niciun director din PATH → eroare **"command not found"**
- Directoarele din PATH sunt separate prin **`:`** (două puncte)
- Modificare PATH: `PATH=/usr/bin/custom:$PATH` — ⚠️ atenție: mereu incluzi `$PATH` la final ca să nu pierzi accesul la comenzile existente


---

## 5.5 Command Types

`type command` — identifică sursa unei comenzi

**5.5.1 Internal Commands** (built-in) — construite direct în shell, ex: `cd` (nu necesită program separat)

**5.5.2 External Commands** — executabile binare stocate în directoare căutate prin PATH

- `which command` — afișează calea completă a unei comenzi (caută prin PATH)
- Diferență importantă: `type` poate arăta diferit față de `which` — ex: `echo` e shell builtin (arătat de `type`), dar există și un `/bin/echo` extern (arătat de `which`)
- `type -a echo` — arată **toate** locațiile unei comenzi

**5.5.3 Aliases**

- Mapează comenzi lungi la secvențe scurte, ex: `ll` = alias pentru `ls -alF`
- `alias` (fără argumente) = afișează toate alias-urile setate
- Creare: `alias name=command`
- Alias-urile create manual persistă doar cât rămâne shell-ul deschis; se pierd la închidere; fiecare shell are propriile alias-uri

**5.5.4 Functions**

- Mai avansate decât alias-urile, folosite de obicei în scripturi Bash
- Sintaxă: `function_name () { commands }`
- Permit execuția mai multor comenzi printr-un singur nume

---
#### 5.6 Quoting

3 tipuri de quote-uri cu semnificație specială pentru Bash: 
 - **double quotes `"`**
 - **single quotes `'`**,
 - **back quotes `` ` ``** 
 - fiecare spune shell-ului să nu trateze textul din interior în mod normal.


---

#### 5.6.1 Double Quotes `"`

- Opresc shell-ul din a interpreta **glob characters** (metacaractere/wildcards): `*`, `?`, `[ ]`
- În interiorul double quotes, `*` rămâne literal `*`, `?` rămâne literal `?`
- **DAR** double quotes încă permit: **command substitution** și **variable substitution** — deci `$PATH` sau `` `date` `` tot se evaluează în interiorul lor

#### 5.6.2 Single Quotes `'`

- Blochează **complet** interpretarea caracterelor speciale — inclusiv globs, variabile, command substitution
- Exemplu clasic de examen: `echo The car costs $100` → output `The car costs 00` (fiindcă `$1` și `$0` sunt tratate ca variabile poziționale, goale) vs `echo 'The car costs $100'` → output `The car costs $100` (literal, nimic interpretat)

#### 5.6.3 Backslash Character `\`

- Alternativă pentru a "single-quote" un singur caracter, fără să pui tot textul între single quotes
- `\$` = previne interpretarea acelui `$` specific ca variabilă, restul textului rămâne interpretabil normal
- Exemplu: `echo The service costs \$1 and the path is $PATH` → `$1` rămâne literal, dar `$PATH` tot se expandează

#### 5.6.4 Backquotes `` ` `` (backticks)

- Realizează **command substitution** = execută o comandă și inserează output-ul ei într-o altă comandă
- Exemplu: `echo Today is` `date` `→`Today is Mon Nov 4 03:40:04 UTC 2018`(output-ul comenzii`date`e inserat direct în output-ul lui`echo`)

---
## 5.7 Control Statements

Permit rularea mai multor comenzi deodată, sau comenzi suplimentare condiționat de succesul comenzii anterioare. Folosite mai ales în scripturi, dar și direct în linia de comandă.

**5.7.1 Semicolon `;`**

- `command1; command2; command3` — rulează comenzile una după alta, **independent** — indiferent dacă prima reușește sau eșuează, a doua tot rulează
- Exemplu: `cal 1 2030; cal 2 2030; cal 3 2030` — afișează 3 calendare succesiv

**5.7.2 Double Ampersand `&&`** — logică "AND"

- `command1 && command2` — a doua comandă rulează **doar dacă** prima **reușește**
- Comenzile "succeed" (reușesc) când funcționează corect, "fail" (eșuează) când ceva merge greșit — ex: `ls` reușește dacă directorul e accesibil, eșuează dacă nu există
- Exemplu: `ls /etc/ppp && echo success` → rulează `echo success` fiindcă `ls` a reușit
- Exemplu: `ls /etc/junk && echo success` → `echo` **NU** rulează, fiindcă `/etc/junk` nu există (ls eșuează)

**5.7.3 Double Pipe `||`** — logică "OR"

- `command1 || command2` — a doua comandă rulează **doar dacă** prima **eșuează** (dacă prima reușește, a doua e sărită)
- Practic: "rulează prima comandă SAU a doua" — spui shell-ului să folosească una din ele
- Exemplu: `ls /etc/ppp || echo failed` → `echo` **NU** rulează (ls a reușit)
- Exemplu: `ls /etc/junk || echo failed` → `echo failed` rulează, fiindcă `ls` a eșuat