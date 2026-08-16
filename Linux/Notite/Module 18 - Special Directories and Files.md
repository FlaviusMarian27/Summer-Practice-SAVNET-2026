### 18.1 Introduction

- Permisiunile de bază (r/w/x) sunt suficiente în majoritatea cazurilor, dar când **mai mulți useri** trebuie să lucreze împreună pe aceleași fișiere/directoare, apar limitări.
- **Permisiuni speciale**: `setuid`, `setgid`, `sticky bit` — rezolvă aceste limitări.

---

### 18.2 Setuid

- Se aplică pe **fișiere executabile binare**. Când e setat, programul rulează cu privilegiile **ownerului fișierului**, NU cu privilegiile userului care îl execută.
- Folosit pentru utilitare de sistem care trebuie să acceseze resurse root, dar executate de useri normali.

**Exemplu clasic**: `passwd`

- `sysadmin` NU poate citi/modifica direct `/etc/shadow` (permisiuni `rw-------`, owner root).
- Dar comanda `passwd` **are setuid** → când `sysadmin` o rulează, sistemul acționează ca și cum **root** ar accesa `/etc/shadow`.

```
ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 31768 Jan 28 2010 /usr/bin/passwd
```

🔴 **Capcană examen — literă mică vs. mare**:

- **`s` minusculă** (în poziția de execute a user ownerului) = **atât setuid, cât și execute** sunt setate.
- **`S` majusculă** = **doar setuid** e setat, dar execute (x) **lipsește** → practic problematic/inutil.

**Setare/eliminare** (`chmod`):

```
chmod u+s file         # symbolic - adaugă setuid
chmod 4775 file         # numeric - adaugă 4000 la permisiunile existente (775 → 4775)
chmod u-s file          # symbolic - elimină setuid
chmod 0775 file         # numeric - elimină (scade 4000)
```

🔴 **Capcană importantă**: dacă specifici doar **3 cifre** la `chmod` (ex: `775`), sistemul presupune automat că prima cifră (specială) e **0** → **elimină** orice permisiune specială existentă pe fișier! Pentru a păstra/seta o permisiune specială, trebuie **4 cifre**.

---

### 18.3 Setgid

Similar cu setuid, dar folosește **grupul owner**. Comportament diferit pe **fișiere** vs. **directoare**.

#### 18.3.1 Setgid pe fișiere

- Comanda rulează cu accesul **grupului** care deține fișierul (temporar, doar în timpul execuției).

**Exemplu**: `/usr/bin/wall`

```
-rwxr-sr-x 1 root tty 30800 May 16 2018 /usr/bin/wall
```

- `s` în poziția group execute → setgid activ.
- `wall` trebuie să scrie în `/dev/tty*`, fișiere deținute de grupul `tty` cu permisiuni `crw--w----` (doar owner și grup `tty` au acces).
- Fără setgid, comanda `wall` ar **eșua** pentru userii care nu sunt în grupul `tty`.

#### 18.3.2 Setgid pe directoare

- Comportament diferit și foarte important: fișierele create **într-un director cu setgid** sunt automat deținute de **grupul directorului**, nu de grupul primar al userului care le-a creat.
- **Directoarele** create în interior **moștenesc** și ele setgid automat.

```
ls -ld /tmp/data
drwxrwsrwx 2 root demo 4096 Oct 30 23:20 /tmp/data
```

- `s` (minusculă) în poziția group execute = setgid + execute grup ambele active.
- `S` (majusculă) = setgid setat, dar **fără** execute pe grup → setgid practic **nu funcționează** (grupul nu poate "intra" oricum).

**De ce e util** — scenariu clasic de examen:

- `bob` (grup `payroll`), `sue` (grup `staff`), `tim` (grup `acct`) trebuie să colaboreze.
- Adminul: creează grup `team` → adaugă toți 3 userii → creează `/home/team` → setează group owner = `team` → dă permisiuni `rwxrwx---`.
- **Fără setgid**: fișierele create de `bob` în `/home/team` au grup `payroll` (grupul lui primar) → `sue` și `tim` nu au acces (`others` = `---`).
- **Cu setgid pe `/home/team`**: fișierele create de `bob` primesc automat grupul `team` → `sue` și `tim` au acces prin permisiunile de grup.

📌 **Lecție-cheie**: setgid pe director elimină nevoia de a schimba manual grupul fiecărui fișier nou creat.

#### 18.3.3 Setarea setgid

```
chmod g+s <file|directory>    # symbolic - adaugă
chmod 2775 <file|directory>   # numeric - adaugă 2000
chmod g-s <file|directory>    # symbolic - elimină
chmod 0775 <file|directory>   # numeric - elimină (scade 2000)
```

🔴 **Capcană**: cod numeric special: **4000 = setuid**, **2000 = setgid**, (vezi mai jos **1000 = sticky bit**). Se pot **combina** (ex: 6775 = setuid+setgid+775).

---

### 18.4 Sticky Bit

- Se aplică pe **directoare**. Previne ștergerea fișierelor de către useri care **nu le dețin**, chiar dacă au permisiune `w` pe director.
- Normal: `w` pe director = poți crea/șterge orice fișier din el, indiferent cine e ownerul fișierului.
- Cu sticky bit: **doar ownerul fișierului sau root** pot șterge acel fișier specific, deși toți au `w` pe director.

**Exemplu clasic**: `/tmp` și `/var/tmp` — directoare scriabile de toți userii, dar fiecare user trebuie să-și poată șterge doar fișierele proprii.

```
ls -ld /tmp
drwxrwxrwt 1 root root 4096 Mar 14 2016 /tmp
```

🔴 **Capcană literă mică/mare**:

- `t` (minusculă) = sticky bit **+** execute pentru others, ambele setate.
- `T` (majusculă) = doar sticky bit setat, **fără** execute pentru others.
- ⚠️ Diferă de setuid/setgid: `T` majusculă **nu indică neapărat o problemă** — atâta timp cât **grupul** are execute, sticky bit funcționează normal (spre deosebire de `S` la setuid/setgid unde majuscula chiar indică o inconsistență).

**Setare/eliminare**:

```
chmod o+t <directory>      # symbolic - adaugă
chmod 1775 <file|directory> # numeric - adaugă 1000
chmod o-t <directory>      # symbolic - elimină
chmod 0775 <directory>     # numeric - elimină (scade 1000)
```

🔴 **Recapitulare coduri numerice permisiuni speciale (foarte testat!)**:

|Cod|Permisiune|
|---|---|
|4000|setuid|
|2000|setgid|
|1000|sticky bit|

---

### 18.5 Links

Scenariu motivant: fișier îngropat adânc în structura de directoare, actualizat frecvent de altcineva → nu poți face o copie (ar deveni desincronizată) → soluție: **link-uri**.

Două tipuri: **hard link** și **symbolic (soft) link** — ambele oferă același acces final, dar cu avantaje/dezavantaje diferite.

#### 18.5.1 Hard Links

- Fiecare fișier are un **inode** (bloc de metadata: permisiuni, ownership, timestamps — **NU** conține numele fișierului sau conținutul propriu-zis).

```
ls -i /tmp/file.txt
215220874 /tmp/file.txt
```

- Directorul păstrează o listă **nume fișier ↔ inode number**.
- **Hard link** = alt nume de fișier care indică **spre același inode**.

```
ln target link_name
ln file.original file.hard.1
```

- `ls -li` arată **link count** (numărul din a doua coloană) = câte nume (hard links) indică spre acel inode.

```
278772 -rw-rw-r--. 2 sysadmin sysadmin 5 Oct 25 15:53 file.hard.1
278772 -rw-rw-r--. 2 sysadmin sysadmin 5 Oct 25 15:53 file.original
```

(același inode 278772, link count = 2)

#### 18.5.2 Symbolic (Soft) Links

```
ln -s target link_name
ln -s /etc/passwd mypasswd
```

```
lrwxrwxrwx 1 sysadmin sysadmin 11 Oct 31 13:17 mypasswd -> /etc/passwd
```

- Primul caracter din `ls -l` e `l` = tip fișier link.
- Soft link e un fișier separat care doar **"indică"** (pathname) către target — nu partajează inode-ul.

#### 18.5.3 Comparație Hard vs. Symbolic Links

|Aspect|Hard Link|Symbolic Link|
|---|---|---|
|**Punct unic de eșec**|❌ NU are — dacă ștergi un nume, celelalte hard links tot funcționează (inode-ul rămâne valid cât timp există măcar un nume legat de el)|✅ ARE — dacă ștergi fișierul original, linkul rămâne "spart" (`No such file or directory`)|
|**Vizibilitate**|Greu de identificat — trebuie `ls -i` + `find / -inum NUMĂR` ca să găsești toate hard links|Ușor de văzut — `ls -l` arată direct `link -> target`|
|**Cross-filesystem**|❌ NU poate — fiecare partiție are propriul set de inode-uri, hard link **nu poate traversa** filesystem-uri (eroare: `Invalid cross-device link`)|✅ POATE — leagă prin pathname, funcționează între filesystem-uri diferite|
|**Link către director**|❌ INTERZIS (`hard link not allowed for directory`) — SO-ul folosește hard links intern pentru structura de directoare|✅ PERMIS|

🔴 **Capcane cheie de examen**:

- Ștergerea fișierului **original** → hard links rămân valide, symbolic links **se strică**.
- `find / -inum NUMĂR` = comanda pentru a găsi toate hard links ale unui inode (obții numărul cu `ls -i`).
- Hard link **NU** poate fi creat pentru un **director** — doar pentru fișiere.
- Hard link **NU** poate traversa **filesystem-uri/partiții** diferite — symbolic link poate.