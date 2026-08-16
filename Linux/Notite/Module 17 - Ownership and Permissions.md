### 17.2 File Ownership

- Fiecare fișier are un **user owner** și un **group owner**.
- Default: ownerul fișierului = userul care l-a creat; group ownerul = **grupul primar** al userului la momentul creării.
- Modificarea ownershipului necesită **privilegii administrative**.
- Ownershipul e stocat intern după **UID/GID** (numeric), nu după nume — dacă ștergi userul/grupul, iar UID-ul nu mai există în `/etc/passwd`, `ls -l` va afișa **UID-ul numeric** în loc de nume.

**Comanda `id`**:

```
id
uid=1001(sysadmin) gid=1001(sysadmin) groups=1001(sysadmin),4(adm),27(sudo),1005(research),1006(development)
```

- Arată UID + GID (grup primar) userului curent + **toate** grupurile din care face parte (inclusiv cel primar).
- În exemplu: UID = GID = 1001 și nume identic → semn de **UPG** (User Private Group).

```
ls -l /tmp/filetest1
-rw-r--r--. 1 sysadmin sysadmin 0 Oct 21 10:15 /tmp/filetest1
```

- `ls -l` funcționează la fel și pentru **fișiere ascunse** (cele care încep cu `.`), vizibile cu `ls -la`.

🔴 **Capcană examen**: `.` = directorul curent, `..` = directorul părinte — ambele apar în `ls -la` ca "fișiere" ascunse și au și ele ownership.

---

### 17.3 Changing Groups (grup primar temporar)

```
newgrp group_name
```

- Schimbă **grupul primar** al sesiunii curente (temporar).
- `groups` = listă simplă a tuturor grupurilor userului (mai puțin detaliat decât `id`).
- `id` arată explicit care e **gid** curent (grupul primar activ) — util pentru verificare după `newgrp`.

```
id                                    → gid=1001(sysadmin)
newgrp research
id                                    → gid=1005(research)
touch /tmp/filetest2
ls -l /tmp/filetest2                  → owner group = research
```

- `newgrp` deschide un **shell nou**; grupul primar rămâne schimbat **doar în acel shell**.
- Revenire la grupul original: `exit` (iese din shell-ul deschis de `newgrp`).

🔴 **Capcană examen**: `newgrp` = schimbare **temporară**, valabilă doar în sesiunea/shell-ul curent. Pentru schimbare **permanentă** a grupului primar, e nevoie de root:

```
usermod -g groupname username
```

---

### 17.4 Changing Group Ownership

```
chgrp group_name file
```

- **Root**: poate schimba group ownerul unui fișier la **orice** grup.
- **User obișnuit**: poate folosi `chgrp` doar dacă e deja **membru** al grupului țintă.

```
chgrp research sample     # OK dacă userul e membru research
chgrp development /etc/passwd
→ chgrp: changing group of '/etc/passwd': Operation not permitted
```

(eroare pentru că userul nu deține fișierul și/sau nu e root)

**Recursiv** (director + tot conținutul):

```
chgrp -R development test_dir
```

**Comanda `stat`** – detalii suplimentare față de `ls -l`:

```
stat /tmp/filetest1
```

- Arată UID/GID **atât numeric cât și ca nume** (`Uid: (1001/sysadmin)`), plus timestamps Access/Modify/Change.

---

### 17.5 Changing User Ownership

```
chown user /path/to/file
```

- Doar **root** poate schimba **user ownerul** unui fișier (spre deosebire de group owner, unde chiar userul obișnuit poate folosi `chgrp` dacă e membru al grupului țintă).

**3 variante de `chown`**:

1️⃣ Schimbă doar userul:

```
chown jane /tmp/filetest1
```

2️⃣ Schimbă user + grup simultan (separate prin `:` sau `.`):

```
chown user:group /path/to/file
chown user.group /path/to/file
chown jane:users /tmp/filetest2
```

3️⃣ Schimbă **doar grupul**, cu prefix `:` sau `.` (poate fi folosit și fără privilegii root, ca alternativă la `chgrp`, dar tot trebuie ca userul să fie membru al grupului țintă):

```
chown :group /path/to/file
chown .group /path/to/file
chown .users /tmp/filetest1
```

🔴 **Capcană examen**: `chown` cu variantele `:group` sau `.group` funcționează **identic** cu `chgrp` — ambele forme de separator (`:` sau `.`) sunt acceptate.

---

### 17.6 Permissions

`ls -l` afișează 10 caractere la începutul liniei = **tip fișier** (1 caracter) + **permisiuni** (9 caractere).

#### Tipuri de fișier (primul caracter)

|Caracter|Tip|
|---|---|
|`-`|fișier obișnuit (regular)|
|`d`|director|
|`l`|symbolic link|
|`b`|block device|
|`c`|character device|
|`p`|pipe file|
|`s`|socket file|

🔴 **Capcană examen**: în practică, la examen apar cel mai des `-`, `d`, `l`. Restul (b, c, p, s) sunt mai degrabă teoretice (`/dev`).

#### Cele 9 caractere = 3 grupuri x 3 permisiuni

```
-rw-r--r--. 1 root root 4135 May 27 21:08 /etc/passwd
```

- Caractere 2-4 = **User Owner** (rw-)
- Caractere 5-7 = **Group Owner** (r--)
- Caractere 8-10 = **Other** / "world" (r--)
- Dacă ești **ownerul** fișierului → se aplică DOAR permisiunile de User Owner (chiar dacă ai și fi membru al grupului owner, nu contează).
- Dacă nu ești owner dar ești **membru al grupului** owner → se aplică DOAR permisiunile Group Owner.
- Altfel → se aplică Other.

🔴 **Capcană majoră de examen**: sistemul verifică permisiunile în ordine **User → Group → Other**, se oprește la prima categorie potrivită și **nu combină** niciodată permisiuni din categorii diferite (ex: nu poți avea acces "or" între ce oferă user și ce oferă group — dacă ești ownerul, permisiunile de grup/other sunt **irelevante** pentru tine, chiar dacă ar fi mai permisive).

#### Semnificația r / w / x

|Permisiune|Pe fișier|Pe director|
|---|---|---|
|**r** (read)|citește conținutul fișierului|listează **numele** fișierelor din director (dar nu detalii — pt. `ls -l` e nevoie și de `x`)|
|**w** (write)|scrie/modifică conținutul (necesită și `r` ca să funcționeze corect)|adaugă/șterge fișiere din director (necesită și `x` ca să funcționeze corect)|
|**x** (execute)|execută fișierul ca program/script|**"intri"** în director (`cd`), condiție pentru a accesa fișiere/subdirectoare din el|

🔴 **Capcană foarte importantă**:

- `w` pe **fișier** are nevoie de `r` ca să funcționeze corect.
- `w` pe **director** are nevoie de `x` ca să funcționeze corect.
- Permisiunea **x pe director** e cea mai critică — fără ea, nu poți accesa NIMIC din director, indiferent de `r` sau `w`.

---

### 17.7 Understanding Permissions – Scenarii (esențiale pt. examen!)

Diagramă de bază folosită în toate scenariile:

```
drwxr-xr-x. 17 root root 4096 23:38 /
drwxr-xr--. 10 root root  128 03:38 /data
-rwxr-xr--.  1 bob  bob   100 21:08 /data/abc.txt
```

#### Scenariul #1 – Directory Access

**Întrebare**: ce acces are `bob` pe `/data/abc.txt`?  
**Răspuns: None.**

- Deși `bob` e ownerul fișierului cu `rwx`, permisiunile pe `/data` pentru `bob` (care nu e nici owner, nici în grupul `root`) sunt **Other** = `r--` → **fără `x`** → bob nu poate nici măcar `cd` în `/data`.

📌 **Lecție**: permisiunile tuturor directoarelor părinte trebuie verificate **înainte** de a te uita la permisiunile fișierului țintă.

#### Scenariul #2 – Viewing Directory Contents

**Întrebare**: cine poate rula `ls /data`?  
**Răspuns: Toți userii (all users).**

- `x` pe `/` pentru toți → toți pot "intra" până la `/data`.
- `r` pe `/data` pentru toți → toți pot lista conținutul cu `ls /data` (inclusiv `ls -a`).
- Dar pentru `ls -l /data` (detalii) ar fi nevoie și de `x` pe `/data` — doar root/grupul root îl au.

📌 **Lecție**: `r` pe director = poți vedea **lista** numelor. Pentru **detalii** (`ls -l`) ai nevoie și de `x`.

#### Scenariul #3 – Deleting Directory Contents

```
drwxrw-rw-. 10 root root 128 03:38 /data
```

**Întrebare**: cine poate șterge `/data/abc.txt`?  
**Răspuns: Doar root.**

- Ștergerea unui fișier necesită `w` **pe director** (nu pe fișier!) — toți au `w` pe `/data` acum.
- Dar necesită și `x` pe director ca să "intri" acolo — doar root are `x` pe `/data`.

📌 **Lecție**: `w` pe director permite ștergerea fișierelor din el, **dar numai** dacă ai și `x` pe acel director.

#### Scenariul #4 – Accessing Contents of a Directory

```
dr-xr-x--x. 10 root root 128 03:38 /data
```

**Întrebare**: poate `bob` executa `more /data/abc.txt`?  
**Răspuns: True.**

- `x` pe `/`, `x` pe `/data` (other), `r` pe `abc.txt` (owner) → toate condițiile îndeplinite.
- Nota bene: `/data` are `r-x` pentru owner root, dar Other are doar `--x` (fără `r`!) — și tot funcționează, pentru că **citirea fișierului nu necesită `r` pe director**, doar `x`.

📌 **Lecție**: `x` e obligatoriu pentru a "intra" în director; `r` pe director **nu** e necesar dacă doar vrei să accesezi un fișier cunoscut din el (nu să-l listezi).

#### Scenariul #5 – The Complexity of Users and Groups

```
dr-xr-x---. 10 sue payroll 128 03:38 /data
```

**Întrebare**: poate `bob` executa `more /data/abc.txt`?  
**Răspuns: Not enough information to determine.**

- Depinde dacă `bob` e membru al grupului `payroll`:
    - Dacă DA → permisiuni group `r-x` pe `/data` → funcționează.
    - Dacă NU → permisiuni Other `---` pe `/data` → eșuează.

📌 **Lecție**: trebuie verificată apartenența la grupuri, nu doar ownershipul afișat de `ls -l`.

#### Scenariul #6 – Permission Priority

```
----rw-rwx. 1 bob bob 100 21:08 /data/abc.txt
```

**Întrebare**: poate `bob` (ownerul!) executa `more /data/abc.txt`?  
**Răspuns: False.**

- `bob` e ownerul → se verifică **DOAR** permisiunile User Owner = `---` → **niciun** acces, deși grupul și Other au `rw-`/`rwx`.

📌 **Lecție**: cea mai importantă regulă din tot capitolul — dacă ești owner, contează **exclusiv** permisiunile de User Owner, chiar dacă grup/other au acces mai mare. Sistemul **nu alege** cea mai permisivă categorie, ci se oprește la prima potrivită (User → Group → Other, în ordine).


### 17.8 Changing Permissions – `chmod`

```
chmod new_permission file_name
```

- Două metode: **symbolic** și **numeric**.

🔴 **Capcană examen**: `chmod` poate fi rulat de **ownerul fișierului** SAU de **root** — nu e nevoie neapărat să fii root (spre deosebire de `chown`, care e doar pentru root).

Fișier de referință folosit în exemple:

```
-rw-r--r-- 1 root root 0 Dec 19 18:58 abc.txt
```

---

#### 17.8.1 Symbolic Method

Sintaxă: `[cui] [operator] [ce]`

**Cui** (permission group):

|Literă|Semnificație|
|---|---|
|`u`|user owner|
|`g`|group owner|
|`o`|others|
|`a`|all (u+g+o)|

**Operator**:

|Simbol|Efect|
|---|---|
|`+`|adaugă permisiunea|
|`-`|elimină permisiunea|
|`=`|setează exact (permisiunile nemenționate sunt **eliminate**)|

**Ce**: `r`, `w`, `x`

**Exemple**:

```
chmod g+w abc.txt          → doar group owner primește +w, restul rămâne neschimbat
chmod ug+x,o-r abc.txt     → adaugă x la user ȘI group, elimină r de la others (combinat, separat prin virgulă)
chmod u=rx abc.txt         → user owner devine EXACT r-x (elimină orice altă permisiune care nu e specificată, ex. w)
```

🔴 **Capcană majoră de examen**: `=` **înlocuiește complet** setul de permisiuni pentru grupul specificat — orice permisiune care nu e menționată explicit e **eliminată**, nu doar lăsată neschimbată. Diferența `+`/`-` (modifică doar ce specifici) vs. `=` (setează exact, restul dispare) e testată des.

- Metoda symbolic e utilă când vrei să schimbi **doar câteva** permisiuni, păstrând restul neschimbate.

---

#### 17.8.2 Numeric Method (Octal Method)

|Valoare|Permisiune|
|---|---|
|4|Read (r)|
|2|Write (w)|
|1|Execute (x)|

Combinații (sumă):

|Număr|Simbolic|
|---|---|
|7|rwx|
|6|rw-|
|5|r-x|
|4|r--|
|3|-wx|
|2|-w-|
|1|--x|
|0|---|

```
chmod 754 abc.txt   →  rwxr-xr--
```

(7=user rwx, 5=group r-x, 4=other r--)

🔴 **Capcane examen**:

- Metoda numerică cere **întotdeauna toate 3 cifre** (user, group, other) — nu poți specifica parțial ca la symbolic. De aceea, symbolic e mai bun pt. schimbări mici, numeric pt. schimbări drastice/complete.
- **Memorează**: 4=r, 2=w, 1=x — se **adună**, nu se combină altfel (ex. 6 = 4+2 = rw-, nu poate fi altă combinație).

**`stat`** arată permisiunile în **ambele** formate simultan:

```
Access: (0664/-rw-rw-r--)  Uid: (502/sysadmin)  Gid: (503/sysadmin)
```

(primul `0` = flag special octal, apoi cele 3 cifre reale de permisiuni: 664)

---

### 17.9 Default Permissions – `umask`

- `umask` determină permisiunile **implicite** la crearea unui fișier/director, prin **scădere** din maximul permis:

|Tip|Maxim implicit|
|---|---|
|Fișiere|`rw-rw-rw-` (666)|
|Directoare|`rwxrwxrwx` (777)|

🔴 **Capcană FOARTE importantă de examen**: fișierele **nu primesc niciodată** permisiune `x` la creare, indiferent de umask — maximul de bază pentru fișiere e 666 (fără x). Ca să aibă `x`, trebuie creat fișierul, apoi schimbate permisiunile explicit cu `chmod`.

**Structura output-ului `umask`**:

```
umask
0002
```

- Cifra 1 (`0`): indică faptul că valoarea e octală.
- Cifra 2: ce se scade din permisiunile **user owner**.
- Cifra 3: ce se scade din permisiunile **group owner**.
- Cifra 4: ce se scade din permisiunile **others**.
- Root are de obicei un umask **mai restrictiv** decât userii normali (dar în exemplul din curs, ambii au `0022` — depinde de distribuție).

#### Calcul umask — exemplu cu `027`

**Pentru fișiere**:

```
File Default:  666
Umask:        -027
Result:        640   → rw-r-----
```

**Pentru directoare**:

```
Directory Default: 777
Umask:             -027
Result:            750   → rwxr-x---
```

```
umask 027
touch sample
ls -l sample        → -rw-r-----  (640)

mkdir test-dir
ls -ld test-dir      → drwxr-x---  (750)
```

🔴 **Capcane examen**:

- Calculul e **scădere** (nu operație bit-cu-bit AND ca la subnetare!) — practic se scade cifra umask din cifra maximă (666/777), pe fiecare poziție.
- `umask` setat manual în shell e **valabil doar pentru sesiunea curentă** — la un shell nou, revine la valoarea implicită.
- Schimbare **permanentă** a umask-ului unui user → editezi fișierul `.bashrc` din home directory-ul acelui user.