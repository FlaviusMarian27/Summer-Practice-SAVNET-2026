### 16.1 Introduction

- La instalare, majoritatea distribuțiilor creează un user normal + fie permisiuni `sudo`, fie parolă root configurată separat.
- Fiecare user are propriul home directory, inaccesibil altor useri by default.
- **User Private Group (UPG)** – pe unele distribuții (Red Hat-based), la crearea unui user se creează automat un grup cu **același nume** ca userul, iar acel user e singurul membru.
- Pe distribuțiile fără UPG, userii noi primesc grupul `users` ca grup primar.
- **Recomandare de workflow**: dacă știi deja ce useri/grupuri vrei, e mai eficient să creezi întâi grupurile, apoi userii (altfel trebuie să modifici userii ulterior ca să-i adaugi în grupuri).

🔴 **Capcană examen**: UPG = grup cu numele identic cu userul, nu un tip special de grup din `/etc/group`.

---

### 16.2 Groups

- Comenzi de verificare:

```
grep pattern filename
getent database record
```

- `grep root /etc/group` și `getent group root` → aceleași rezultate pentru grupuri **locale**.
- `getent` funcționează și pentru surse **network-based** (ex: LDAP), `grep` doar pentru fișiere locale.

#### 16.2.1 Creating a Group

```
groupadd -g 1005 research
```

- `-g` = specifici GID manual.
- Dacă nu dai `-g`, `groupadd` alege automat următorul GID liber (ultimul GID din `/etc/group` + 1).

#### 16.2.1.1 Group ID Considerations

- Pe distribuții Red Hat-like: UID-ul userului = GID-ul UPG-ului asociat → **evită să creezi GID-uri manual în același interval unde vor exista UID-uri**, ca să nu ai conflicte.
- GID-uri sub **500 (RedHat)** sau **1000 (Debian)** sunt rezervate pentru uz de sistem.
- Opțiunea `-r` la `groupadd` = creează grup cu GID sub limita standard (grup de sistem):

```
groupadd -r sales   →   sales:x:999:
```

🔴 **Capcană examen**: 500 = prag RedHat, 1000 = prag Debian pentru GID/UID sistem vs normal. Se confundă des la examen.

#### 16.2.1.2 Group Naming Considerations

- Primul caracter: `_` sau literă mică `a-z`.
- Max 32 caractere acceptate de majoritatea distribuțiilor, dar >16 poate cauza probleme de compatibilitate.
- După primul caracter: alfanumerice, `-` sau `_`.
- **Ultimul caracter NU poate fi `-`**.
- Aceste reguli **nu sunt mereu impuse** de `groupadd` — poate accepta un nume "greșit", dar alte comenzi/servicii pot să nu funcționeze corect cu el.

#### 16.2.2 Modifying a Group

```
groupmod -n clerks sales     # schimbă NUMELE grupului (sales → clerks)
groupmod -g 10003 clerks     # schimbă GID-ul grupului
```

- **Schimbarea numelui** grupului: fișierele rămân accesibile, pentru că sistemul le leagă de GID, nu de nume.
- **Schimbarea GID-ului**: fișierele care aveau acel GID **nu mai sunt asociate cu niciun nume de grup** → devin **orphaned files** (fișiere orfane), afișate doar cu GID numeric în `ls -l`.
- Găsirea fișierelor orfane:

```
find / -nogroup
```

🔴 **Capcană examen**: `groupmod -n` (nume) = safe, nu creează orfani. `groupmod -g` (GID) = creează orfani pentru fișierele vechi.

#### 16.2.3 Deleting a Group

```
groupdel clerks
```

- Se pot șterge doar grupuri **supplementare** (secundare).
- Un grup care e grup **primar** pentru vreun user **nu poate fi șters** direct — trebuie mai întâi schimbat grupul primar al userilor respectivi.
- Ștergerea unui grup → fișierele asociate devin orfane.

---

### 16.3 Users

- Info user → `/etc/passwd`
- Info autentificare (parolă) → `/etc/shadow`
- Se recomandă folosirea comenzii `useradd`, nu editare manuală a fișierelor (risc de erori care blochează login-ul tuturor userilor).
- Înainte de a crea useri, verifică valorile default din fișierele de configurare folosite de `useradd`.

#### 16.3.1 User Configuration Files – `/etc/default/useradd`

```
useradd -D
```

afișează/modifică valorile default:

|Setare|Valoare implicită|Semnificație|
|---|---|---|
|`GROUP=100`|grup primar implicit (dacă nu se folosește UPG) — de obicei `users`||
|`HOME=/home`|director de bază pt. home directories||
|`INACTIVE=-1`|zile după expirarea parolei până se dezactivează contul; `-1` = dezactivat||
|`EXPIRE=`|dată expirare cont (gol = fără expirare)||
|`SHELL=/bin/bash`|shell implicit la login||
|`SKEL=/etc/skel`|director "schelet" copiat în home-ul noului user||
|`CREATE_MAIL_SPOOL=yes`|creează fișier mail spool pt. user||

- Fiecare valoare are o opțiune corespunzătoare la `useradd` pentru a fi suprascrisă per-user: `-g`, `-b`, `-f` (inactive), `-e` (expire), `-s`, `-k`, etc.
- Modificare permanentă a valorilor default:

```
useradd -D -f 30    # setează INACTIVE=30 ca implicit
```

🔴 **Capcană examen**: `useradd -D` **fără alte opțiuni** = afișează valorile curente. `useradd -D -opțiune valoare` = **schimbă** valoarea default.

#### 16.3.2 User Configuration Files – `/etc/login.defs`

- Conține valori suplimentare aplicate default userilor noi, editat direct de admin (spre deosebire de `/etc/default/useradd`, care poate fi editat și prin `useradd -D`).

```
grep -Ev '^#|^$' /etc/login.defs
```

(afișează doar liniile care nu sunt comentarii sau goale)

|Setare|Valoare tipică|Semnificație|
|---|---|---|
|`MAIL_DIR`|`/var/mail/spool`|unde se creează mail spool-ul|
|`PASS_MAX_DAYS`|99999|zile max valabilitate parolă (practic = fără expirare)|
|`PASS_MIN_DAYS`|0|zile minime înainte de a putea schimba parola din nou|
|`PASS_MIN_LEN`|5|lungime minimă parolă|
|`PASS_WARN_AGE`|7|cu câte zile înainte de expirare începe avertismentul|
|`UID_MIN` / `UID_MAX`|500 / 60000|interval UID-uri pentru useri normali|
|`GID_MIN` / `GID_MAX`|500 / 60000|interval GID-uri pentru grupuri normale|
|`CREATE_HOME`|yes|creează automat home directory (⚠️ pe mașina virtuală a cursului, **NU** e setat by default → home NU se creează automat dacă nu specifici!)|
|`UMASK`|077|permisiuni implicite pe home directory (doar ownerul are acces)|
|`USERGROUPS_ENAB`|yes/no|`yes` = distribuția folosește UPG|
|`ENCRYPT_METHOD`|SHA512|metoda de criptare a parolelor|
|`MD5_CRYPT_ENAB`|no|**deprecated**, suprascris de `ENCRYPT_METHOD`|

🔴 **Capcane examen frecvente**:

- Organizațiile cu politici de securitate serioase schimbă `PASS_MAX_DAYS` la **60 sau 30 zile** (nu lasă 99999).
- Recomandare pentru UID_MAX modern: **60000** e valoarea safe/recomandată pentru compatibilitate maximă, deși tehnic un UID poate depăși 4 miliarde.
- `GID_MAX` ar trebui setat **egal cu `UID_MAX`** pentru a suporta UPG corect.
- Pe VM-ul cursului, `CREATE_HOME` nu e setat → **home directory NU se creează automat** decât dacă folosești explicit `-m`.

---

### 16.3.3 Account Considerations

**Username**: aceleași reguli ca la grupuri (start cu `_` sau literă mică, max 32 caractere/recomandat ≤16, ultim caracter ≠ `-`). Recomandat să fie **unic** și **identic pe toate sistemele** dacă userul accesează mai multe mașini.

**UID**:

```
useradd -u 1000 jane
```

- UID `0` = root (privilegii speciale).
- Conturi de sistem (daemons) au de obicei UID-uri în **range-ul rezervat**; excepție: `nfsnobody` are UID **65534**.
- Range-ul rezervat s-a extins istoric: inițial 1-99, apoi 1-499; trend actual: 1-999 (dar 1-499 tot folosit).
- La setup nou, e bună practică să începi userii de la UID **1000+**.

**Primary Group**:

```
useradd -g users jane
```

- Cu UPG: grup creat automat, GID = UID, nume = username.
- Fără UPG: grup primar implicit = `users` (GID 100).

**Supplementary Group** (`-G`, literă mare, listă separată prin virgulă):

```
useradd -G sales,research jane
```

🔴 **Capcană clasică examen**: `-g` (literă mică) = grup **primar** (unul singur). `-G` (literă mare) = grupuri **supplementare** (mai multe, separate prin virgulă).

**Home Directory**:

```
useradd -m jane              # creează home dir conform HOME din /etc/default/useradd
useradd -mb /test jane       # -b: alt director de bază (/test/jane)
useradd -md /test/jane jane  # -d: cale completă custom pentru home
```

- Dacă `CREATE_HOME=no` (sau lipsă) → home NU se creează automat, trebuie `-m`.
- Dacă `CREATE_HOME=yes` → home se creează automat fără `-m`.

🔴 **Capcană**: `-b` = director de bază (se adaugă username la final). `-d` = cale **completă**, custom, pentru home.

**Skeleton Directory**:

```
useradd -mk /home/sysadmin jane
```

- `-k` schimbă directorul skeleton folosit (implicit `/etc/skel`).
- ⚠️ **`-k` necesită obligatoriu și `-m`**, altfel `useradd` dă eroare.

**Shell**:

```
useradd -s /bin/bash jane
```

- Pentru conturi de sistem, e comun `/sbin/nologin`.

**Comment (GECOS field)**:

```
useradd -c 'Jane Doe' jane
```

- Numele complet al userului, afișat de multe aplicații grafice de login.

---

### 16.3.4 Creating a User – exemplu complet

```
useradd -u 1009 -g users -G sales,research -m -c 'Jane Doe' jane
```

- Creează UID 1009, grup primar `users`, grupuri supl. `sales` și `research`, home dir creat, comment "Jane Doe".
- Automat actualizate: `/etc/passwd`, `/etc/shadow` (pentru user), `/etc/group`, `/etc/gshadow` (pentru apartenența la grupuri).

🔴 **Foarte important pentru examen**: după `useradd`, contul **NU are parolă validă** — userul nu se poate loga până nu i se setează parola cu `passwd`!

- Dacă `CREATE_MAIL_SPOOL=yes` → se creează `/var/spool/mail/jane`.
- Cu `-m`: home dir creat cu permisiuni doar pentru user, conținutul din `/etc/skel` e copiat înăuntru.

---

### 16.3.5 Passwords

Factori de considerat la o parolă bună:

- **Length**: nu neapărat "mai lungă = mai bine" — parole prea lungi tind să fie scrise pe hârtie (risc de compromitere).
- **Composition**: combinație de caractere alfabetice, numerice și simbolice.
- **Lifetime**: expirare periodică → limitează fereastra de atac (brute-force), dar schimbarea prea frecventă poate duce la parole slabe/scrise pe hârtie/conturi neutilizate expirate.

#### 16.3.5.1 Setting a User Password

```
passwd jane
```

- Adminul poate seta parola oricărui user cu `passwd username`.
- Userul obișnuit rulează doar `passwd` (fără argument) → i se cere parola veche + parola nouă de 2 ori.

🔴 **Capcană majoră de examen**: **root este singurul cont care poate avea parolă goală** fără să fie blocat — dar toate celelalte reguli de parolă (lungime, complexitate) **nu se aplică strict la root**; dacă root le încalcă, primește doar un **warning**, nu e blocat.

- User normal are (de obicei) **3 încercări** să introducă o parolă validă înainte ca `passwd` să dea eroare.
- Doar root poate vedea conținutul `/etc/shadow`.

#### 16.3.5.2 Managing Password Aging – comanda `chage`

|Opțiune scurtă|Opțiune lungă|Descriere|
|---|---|---|
|`-l`|`--list`|listează info aging cont|
|`-d LAST_DAY`|`--lastday`|setează data ultimei schimbări de parolă|
|`-E EXPIRE_DATE`|`--expiredate`|setează data expirării contului|
|`-h`|`--help`|ajutor|
|`-I INACTIVE`|`--inactive`|zile în care login e permis după expirarea parolei|
|`-m MIN_DAYS`|`--mindays`|zile minime înainte de a putea schimba parola|
|`-M MAX_DAYS`|`--maxdays`|zile maxime de valabilitate parolă|
|`-W WARN_DAYS`|`--warndays`|zile înainte de expirare când începe avertismentul|

```
chage -M 60 jane
grep jane /etc/shadow | cut -d: -f1,5
→ jane:60
```

🔴 **Capcană examen**: reține litera mică vs. mare! `-I` = inactive, `-m` = min days, `-M` = max days — foarte ușor de confundat între ele la examen.



#### 16.3.6 Modifying a User

- Unele modificări **nu funcționează dacă userul e logat** (ex: schimbarea numelui de login).
- Alte modificări (ex: apartenența la grupuri) se fac, dar **nu au efect** decât după ce userul se delogează și se reloghează.
- De aceea e util să știi cine e logat pe sistem:

|Comandă|Ce arată|
|---|---|
|`who`|userii logați curent|
|`w`|mai verboasă decât `who` — arată și uptime, load, ce proces rulează fiecare user|
|`last`|sesiuni de login curente **și anterioare**, cu dată/oră. Poate fi filtrată după username sau `tty`|

**Opțiuni `usermod`** (multe identice ca la `useradd`):

|Scurt|Lung|Descriere|
|---|---|---|
|`-c COMMENT`|`--comment`|setează GECOS/comment|
|`-d HOME_DIR`|`--home`|setează HOME_DIR ca nou home directory|
|`-e EXPIRE_DATE`|`--expiredate`|data expirare cont|
|`-f INACTIVE`|`--inactive`|zile de login permise după expirarea parolei|
|`-g GROUP`|`--gid`|setează GROUP ca grup **primar**|
|`-G GROUPS`|`--groups`|setează grupurile **supplementare** = lista GROUPS (**înlocuiește** lista veche)|
|`-a`|`--append`|adaugă la grupurile supl. existente, fără să șteargă ce era deja acolo|
|`-h`|`--help`|help|
|`-l NEW_LOGIN`|`--login`|schimbă numele de login|
|`-L`|`--lock`|blochează contul|
|`-s SHELL`|`--shell`|schimbă shell-ul|
|`-u NEW_UID`|`--uid`|schimbă UID-ul|
|`-U`|`--unlock`|deblochează contul|

🔴 **Capcane clasice de examen**:

- **Schimbarea UID-ului** (`-u`) e problematică: fișierele pe care userul le deținea **nu se actualizează automat** → pot rămâne "legate" de vechiul UID (practic devin orfane dacă nu le actualizezi manual cu `chown`).
- **Schimbarea numelui de login** (`-l`) **NU** orfanizează fișierele (fișierele sunt legate de UID, nu de username).
- `usermod -G` **fără** `-a` → **înlocuiește complet** lista de grupuri supplementare (userul iese din orice grup vechi care nu e în noua listă!).
- `usermod -aG` (append + groups) → **adaugă** grupuri noi, păstrându-le pe cele vechi. **Aproape mereu vrei `-aG`, nu doar `-G`.**

Exemplu din curs — jane e deja în `sales` și `research`, vrei s-o adaugi și în `development` fără să o scoți din celelalte:

```
usermod -aG development jane
```

⚠️ Dacă ai fi scris doar `usermod -G development jane` (fără `-a`), jane ar fi rămas **doar** în `development` și ar fi ieșit din `sales` și `research`!

- `usermod -L` = **lock** cont (nu se poate loga, dar fișierele/contul rămân). `usermod -U` = **unlock**.
- Deosebire `userdel` vs `usermod -L`: `userdel` poate șterge/orfaniza fișierele; `usermod -L` doar blochează accesul, fără să atingă fișierele — variantă mai sigură/reversibilă decât ștergerea contului.

---

#### 16.3.7 Deleting a User

```
userdel jane
```

- Șterge userul, **dar NU șterge home directory-ul**.
- ⚠️ Fișierele din home directory rămân, dar devin **orphaned** (asociate doar cu UID/GID-ul fostului user, fără nume).

```
userdel -r jane
```

- Șterge userul **+ home directory + mail spool**.

🔴 **WARNING important pentru examen**: `userdel -r` șterge **doar** fișierele din home directory și mail spool. Dacă userul deținea fișiere **în afara** home directory-ului (ex: pe alt disk, alt path), acelea **rămân ca fișiere orfane** — `-r` nu le atinge!

- Ștergerea userului + fișierelor e **ireversibilă** dacă nu ai backup — se recomandă multă atenție înainte de a rula `userdel -r`, mai ales dacă există cerințe legale de păstrare a datelor.