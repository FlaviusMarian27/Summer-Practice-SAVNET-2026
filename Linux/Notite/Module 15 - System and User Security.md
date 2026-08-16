### 15.2 Administrative Accounts

⚠️ **Capcană conceptuală:** login direct ca **root** e periculos și **nerecomandat**. Motive:

- Riști să rulezi comenzi periculoase din greșeală
- În mediul grafic, procesele de login rulează ca root, ceea ce e un risc suplimentar (browsere/email clients rulând fără restricții)
- Ubuntu, notabil, are contul root **dezactivat implicit**

**Cele 2 metode de a obține privilegii administrative:**

- `su` — dacă root e activat
- `sudo` — dacă root e dezactivat (metoda standard pe Ubuntu)

#### 15.2.1 `su` command

```
su [options] [username]
```

⚠️ **Capcană critică — `login shell`:** e recomandat să folosești opțiunea de login shell, altfel noul shell **schimbă UID-ul dar nu configurează complet** mediul noului user.

3 moduri echivalente de a specifica login shell:

bash

```bash
su -
su -l
su --login
```

Fără username specificat → implicit devine **root**:

bash

```bash
su - root    # echivalent cu
su -
```

⚠️ Capcană: `su` cere parola contului **destinație** (root), nu a userului curent.

Revenire la shell-ul original: `exit`

#### 15.2.2 `sudo` command

```
sudo [options] command
```

⚠️ **Diferență critică `su` vs `sudo`:** `sudo` cere **parola userului curent**, NU parola root-ului!

bash

```bash
sudo head /etc/shadow
[sudo] password for sysadmin: ...
```

Avantaje `sudo` (foarte testate):

1. **Nu trebuie să cunoști parola root** — poți acorda acces admin fără să divulgi parola de root
2. **Logging/accountability** — fiecare execuție `sudo` e înregistrată în log, cu utilizator + comandă + timp
3. **Reduce riscul** de a rula accidental o comandă ca root — intenția e clară doar când prefixezi cu `sudo`

⚠️ Notă: după prima autentificare `sudo` reușită, parola nu mai e cerută pentru o perioadă (sesiune curentă) — feature de securitate: dacă lași calculatorul nesupravegheat cu sesiunea activă, riscul e mai mic decât dacă ai fi logat direct ca root.

### 15.3 User Accounts — `/etc/passwd`

Fișier cu date despre conturi, câmpuri separate prin `:`. Exemplu:

```
sysadmin:x:1001:1001:System Administrator,,,,:/home/sysadmin:/bin/bash
```

**Cele 7 câmpuri (memorează ordinea, e testată direct!):**

|#|Câmp|Exemplu|Detalii|
|---|---|---|---|
|1|Name/username|`sysadmin`|numele contului|
|2|Password placeholder|`x`|`x` = parola reală e în `/etc/shadow`|
|3|UID|`1001`|user ID — sistemul folosește UID intern, nu username|
|4|Primary Group ID (GID)|`1001`|grupul primar|
|5|Comment|`System Administrator,,,,`|info liberă (ex: nume real)|
|6|Home Directory|`/home/sysadmin`|pentru useri normali; **root** are `/root`|
|7|Shell|`/bin/bash`|shell-ul folosit la login; `bash` e cel mai comun|

Căutare utilizator specific:

bash

```bash
grep sysadmin /etc/passwd
```

### 15.3.1 Passwords — `/etc/shadow`

⚠️ Accesibil **doar** cu privilegii admin (`su`/`sudo`), nu de useri obișnuiți.

```
sysadmin:$6$...hash...:16874:5:30:7:60::
```

**Cele 9 câmpuri (foarte testate — ordinea exactă și semnificația fiecăruia!):**

|#|Câmp|Semnificație|
|---|---|---|
|1|Username|trebuie să corespundă cu `/etc/passwd`|
|2|Password (criptată)|criptare **one-way**, nereversibilă; conturile de sistem au `*` în loc de hash|
|3|Last Change|zile de la 1 ianuarie 1970 (**Epoch**) de la ultima schimbare de parolă|
|4|Minimum|zile minime între schimbări de parolă; `0` = poate schimba oricând|
|5|Maximum|zile maxime de valabilitate a parolei; `99999` = practic niciodată (≈274 ani)|
|6|Warn|câte zile înainte de expirare userul e avertizat (doar la login)|
|7|Inactive|perioadă de grație după expirare, în care parola mai poate fi schimbată (doar la login)|
|8|Expire|ziua (Epoch) la care contul expiră complet|
|9|Reserved|rezervat, neutilizat|

⚠️ **Capcană importantă de logică:** dacă `minimum` e `0` dar `maximum` e setat (ex: 30), userul poate schimba imediat parola înapoi la cea veche, anulând scopul politicii de expirare. De aceea, când `maximum` e setat, e recomandat să fie setat și `minimum`.

⚠️ **Capcană — cont expirat ≠ cont șters:** un cont expirat e doar **blocat** (locked), nu șters. Adminul poate reseta parola pentru a-l debloca. Frecvent folosit pentru angajați temporari/contractori.

**Comanda `getent`** — alternativă la `grep`, funcționează atât cu fișiere locale, cât și cu servere de directoare din rețea:

bash

```bash
getent database record
getent passwd sysadmin
```

### 15.4 System Accounts

- Conturi normale de utilizator: UID de obicei **>500** (uneori **>1000**, în funcție de distribuție)
- **root** = UID **0**
- **System accounts**: UID de la **1 la 499** — pentru servicii, nu pentru login uman

Diferențe caracteristice ale system accounts:

- **shell** = `/usr/sbin/nologin` (nu pot face login interactiv)
- **parolă** în `/etc/shadow` = `*` (nu au parolă utilizabilă)

⚠️ Recomandare: nu ștergi conturi de sistem fără să știi exact ce fac — pot afecta funcționarea serviciilor.

### 15.5 Group Accounts — `/etc/group`

⚠️ Capcană istorică: tradițional UNIX limita userii la maxim **16 grupuri**; kernel-urile Linux moderne suportă peste **65.000**.

- **Primary group** — definit în `/etc/passwd`
- **Secondary/supplemental groups** — definite în `/etc/group`

Format `/etc/group`:

```
mail:x:12:mail,postfix
```

**4 câmpuri:**

|#|Câmp|Exemplu|
|---|---|---|
|1|Group Name|`mail`|
|2|Password placeholder|`x` (parolele de grup rar folosite; dacă există, sunt în `/etc/gshadow`)|
|3|GID|`12`|
|4|User List|`mail,postfix` — membri **secundari** ai grupului|

⚠️ Capcană: userii listați aici sunt doar membrii **secundari**; membrii **primari** ai grupului sunt cei ale căror GID din `/etc/passwd` se potrivește, dar **nu apar** în lista din `/etc/group`.

### 15.6 Viewing User Information — comanda `id`

```
id [options] username
```

bash

```bash
id                    # info despre userul curent
id root               # info despre un user specific
id -g                 # doar GID-ul grupului primar
id -G                 # toate grupurile (primar + secundare)
```

Output exemplu:

```
uid=1001(sysadmin) gid=1001(sysadmin) groups=1001(sysadmin),4(adm),27(sudo)
```

### 15.7 Viewing Current Users — comanda `who`

bash

```bash
who
```

**Coloane:**

|Coloană|Semnificație|
|---|---|
|Username|userul logat|
|Terminal|`tty` = login local; `pts` = pseudo-terminal (ex: SSH sau alt proces care acționează ca terminal)|
|Date|când s-a logat|
|Host|dacă apare hostname/IP → login **remote**; dacă apare `(:0)` → login **grafic local**; fără nimic → login local prin linia de comandă|

Opțiuni utile:

bash

```bash
who -b     # ultima pornire (boot) a sistemului
who -r     # runlevel-ul curent
```

#### Comanda `w` — informații extinse

bash

```bash
w
```

Combină output-ul `who` cu detalii suplimentare + prima linie identică cu `uptime`.

**Coloane suplimentare față de `who`:**

|Coloană|Semnificație|
|---|---|
|IDLE|de cât timp userul nu a mai rulat nicio comandă|
|JCPU|timp CPU total folosit de toate procesele de la login|
|PCPU|timp CPU folosit de procesul curent|
|WHAT|procesul curent rulat de user|

⚠️ Capcană: caracterul `s` din output reprezintă **secunde**.

### 15.8 Viewing Login History — comanda `last`

bash

```bash
last
```

⚠️ **Capcană critică — diferența `who` vs `last` (foarte testată!):**

- `who` citește din **`/var/log/utmp`** — doar sesiunile **curente**
- `last` citește din **`/var/log/wtmp`** — **istoricul complet** de login-uri (inclusiv reboot-uri)

Particularitate: la reboot-uri, `last` afișează **versiunea kernelului** care a fost pornit, în loc de locația de login.

Output posibil:

- `still logged in` — dacă userul e încă logat
- interval de timp — dacă s-a delogat deja