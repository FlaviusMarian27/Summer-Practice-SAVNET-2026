### 13.1 Introducere

- **GNU/Linux** = numele corect complet: GNU (software-ul liber din jurul kernelului) + Linux (kernelul propriu-zis)
- Funcțiile cheie ale kernelului: system call interface, process management, memory management, virtual filesystems, networking, device drivers
- **Pseudo filesystems** importante: `/proc` și `/sys` — nu conțin fișiere reale pe disk, ci există doar în memorie și oferă o "fereastră" către informațiile kernelului

### 13.2 Processes

⚠️ **Diferența cheie `/proc` vs `/dev` vs `/sys`:**

- `/proc` — informații despre procesele active + configurația kernelului
- `/dev` — device-uri hardware (fișiere speciale)
- `/sys` — informații despre device-urile hardware conectate

**Pseudo filesystem** = pare a fi fișiere reale pe disk, dar există doar în memorie.

Comenzi care folosesc informația din `/proc`: `top`, `free`, `mount`, `umount`.

⚠️ **Capcană de examen — permisiuni de scriere:**

- fișierele din `/proc` — **nu pot fi modificate**, nici de root
- fișierele din `/sys` — **pot fi modificate de root**, iar modificarea lor schimbă comportamentul kernelului **temporar** (până la reboot)
- pentru a face schimbările **permanente**, se editează `/etc/sysctl.conf`

Exemplu clasic din curs:

bash

```bash
cat /proc/sys/net/ipv4/icmp_echo_ignore_all   # 0 = răspunde la ping
echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all   # 1 = ignoră ping-urile
```

**Fișiere importante în `/proc`:**

|Fișier|Conținut|
|---|---|
|`/proc/cmdline`|parametrii trimiși kernelului la pornire|
|`/proc/meminfo`|informații despre folosirea memoriei|
|`/proc/modules`|module curent încărcate în kernel|

#### 13.2.1 Process Hierarchy

- Primul proces pornit de kernel = **init**, are întotdeauna **PID 1**
- Sistem **System V** → init e `/sbin/init`
- Sistem **systemd** → init e `/bin/systemd` (de obicei link către `/lib/system/systemd`)
- **Parent process** = procesul care pornește alt proces; **child process** = procesul pornit; PID-ul părintelui apare ca **PPID**
- Valoarea maximă de PID e configurabilă în `/proc/sys/kernel/pid_max`; când se atinge maximul, sistemul "se rotește" și refolosește valori mici disponibile

Comandă pentru vizualizarea arborelui de procese:

```
pstree
```

#### 13.2.2 Viewing Process Snapshot — comanda `ps`

⚠️ Capcană: `ps` fără opțiuni arată **doar procesele din shell-ul curent** (inclusiv `ps` însuși!).

|Comandă|Ce arată|
|---|---|
|`ps`|doar procesele shell-ului curent|
|`ps --forest`|ca `pstree`, arată relația parent/child|
|`ps aux`|toate procesele din sistem (stil BSD)|
|`ps -ef`|toate procesele din sistem (stil UNIX/System V), afișează și PPID|
|`ps -u root`|doar procesele unui user specific|

Filtrare utilă:

bash

```bash
ps -ef | grep firefox
ps -ef | head
```

#### 13.2.3 Viewing Processes in Real Time — comanda `top`

- `ps` = fotografie statică (un moment)
- `top` = interfață dinamică, actualizată constant, sortată implicit după **%CPU**

**Taste interactive importante (foarte testate!):**

|Tastă|Acțiune|
|---|---|
|`K`|termină procesul (cere PID + semnal; implicit trimite semnalul **9 = KILL**, care **forțează** oprirea)|
|`R`|schimbă **niceness** (prioritatea) procesului|
|`q`|ieșire din `top`|

⚠️ **Capcană niceness:** valorile merg de la **-20 la 19**.

- Valoare mai **mică** (chiar negativă) = prioritate mai **mare** — doar **root** poate seta valori negative sau poate scădea niceness-ul.
- Orice user poate **crește** niceness-ul (scade prioritatea) propriului proces.

**Load average** (afișat de `top`, `uptime`, sau `cat /proc/loadavg`):

```
0.12 0.46 0.25 1/254 3052
```

- primele 3 numere = media de încărcare pe ultimele **1, 5, 15 minute**
- al 4-lea = fracție: procese active/total procese
- al 5-lea = ultimul PID folosit

⚠️ Capcană interpretare load average: valoarea e **relativă la numărul de nuclee CPU**. Load = 1 pe un CPU single-core = 100% încărcat; pe un CPU cu 4 nuclee = doar 25% încărcat.

### 13.3 Memory

- Memoria e gestionată prin **virtual addressing** — permite mai multor procese să "creadă" că au acces la mai multă memorie decât există fizic
- **Kernel space** = zonă protejată, izolată, unde rulează codul kernelului
- **User space** = zonă disponibilă programelor obișnuite; comunică cu kernelul prin **system calls**

#### 13.3.1 Viewing Memory

bash

```bash
free           # output în bytes
free -m        # în megabytes
free -g        # în gigabytes
free -s 10     # actualizează la fiecare 10 secunde
```

Interpretare rânduri:

- **Mem:** memorie fizică (total/used/free/shared/buffers/cached)
- **-/+ buffers/cache:** valorile ajustate — memoria folosită de buffers/cache e considerată **recuperabilă** la nevoie
- **Swap:** memoria virtuală (pe disk), folosită când RAM-ul fizic e insuficient

⚠️ Capcană: dacă memoria (și swap-ul) devin foarte reduse, sistemul **termină automat procese**. Un admin poate interveni manual cu `top` sau `kill` pentru a alege ce proces se oprește, în loc să lase sistemul să decidă.


### 13.4 Log Files

Log-urile documentează activitatea kernelului și proceselor — esențiale pentru troubleshooting și detectarea accesului neautorizat.

⚠️ **Capcană terminologie:** "**Syslog**" e folosit generic pentru sistemul de logging din Linux, indiferent ce daemon rulează efectiv.

**Evoluția daemon-ilor de logging (foarte testată la examen):**

- Metodă veche: **2 daemoni separați** — `syslogd` + `klogd`
- Metodă modernă (majoritatea distribuțiilor): **1 daemon unificat** — `rsyslogd`
- Sisteme bazate pe **systemd**: daemon-ul se numește **`journald`**, logurile sunt în format binar, se vizualizează cu comanda **`journalctl`**

Toate log-urile (indiferent de daemon) ajung de obicei în **`/var/log/`**.

**Fișiere comune în `/var/log`:**

|Fișier|Conținut|
|---|---|
|`boot.log`|mesaje la pornirea serviciilor în timpul boot-ului|
|`cron`|mesaje generate de daemon-ul `crond`|
|`dmesg`|mesaje generate de kernel la boot|
|`maillog`|mesaje de la daemon-ul de mail|
|`messages`|mesaje generale de la kernel/procese (uneori numit `syslog`)|
|`secure`|mesaje de autentificare/autorizare (ex: login)|
|`journal`|mesaje din `systemd-journald.service`, configurabil în `/etc/journald.conf`|
|`Xorg.0.log`|mesaje de la serverul grafic X Windows|

**Vizualizare log-uri:**

bash

```bash
cat / less fisier_log      # pentru fișiere text
journalctl                 # pentru sisteme systemd (jurnal binar)
```

⚠️ **Capcană — log rotation:** fișierele log sunt **rotite** periodic — cel vechi e redenumit (sufix numeric sau dată, ex: `secure.0` sau `secure-20181103`), iar unul nou preia numele original.

⚠️ **Capcană — fișiere binare:** unele fișiere din `/var/log` (ex: `wtmp`, `btmp`) conțin date **binare**, nu text. Verifici tipul cu:

bash

```bash
file /var/log/wtmp    # → wtmp: data (adică binar)
```

Pentru a citi conținutul binar:

bash

```bash
last     # citește /var/log/wtmp
lastb    # citește /var/log/btmp (necesită root)
```

### 13.5 Kernel Messages

- `/var/log/dmesg` — mesaje kernel de la **boot**
- `/var/log/messages` — mesaje kernel din timpul funcționării, dar **amestecate** cu mesaje de la alte procese/daemoni

Kernelul nu are propriul fișier de log fix — poate fi configurat prin `/etc/syslog.conf` sau `/etc/rsyslog.conf`.

**Kernel ring buffer** = zonă de memorie unde kernelul ține mesajele generate. Comanda pentru vizualizare:

bash

```bash
dmesg
```

⚠️ Capcană: `dmesg` poate produce **până la 512 KB** de text — se recomandă filtrare cu pipe:

bash

```bash
dmesg | grep -i usb    # -i = ignoră case-sensitivity
```

⚠️ Capcană: mărimea ring buffer-ului e setată **la compilarea kernelului** — nu e trivial de schimbat. Pe un sistem foarte activ, buffer-ul se poate umple și mesaje vechi se **pierd**.

### 13.6 Filesystem Hierarchy Standard (FHS)

FHS = standard (nu lege strictă — poate fi încălcat) care organizează directoarele sistemului.

**Două criterii de clasificare a directoarelor (foarte testate!):**

1. **Shareable vs Not Shareable** — poate fi partajat pe rețea între mai multe mașini sau nu
2. **Static vs Variable** — conținutul fișierelor se schimbă sau rămâne fix

||Not Shareable|Shareable|
|---|---|---|
|**Variable**|`/var/lock`|`/var/mail`|
|**Static**|`/etc`|`/opt`|

⚠️ Capcană: `/var` ca întreg **nu poate fi clasificat** direct — trebuie analizate subdirectoarele lui individual (ex: `/var/lock` ≠ shareable, dar `/var/mail` = shareable).

**Cele 4 ierarhii principale ale FHS:**

1. **root filesystem** (`/`) — esențial pentru boot
2. `/usr` — a doua ierarhie, non-esențială pentru boot
3. `/usr/local` — a treia ierarhie, software care nu vine din distribuție
4. `/var` — a patra ierarhie, fișiere care se schimbă în timp

⚠️ **Capcană importantă de examen:** `/`, `/bin`, `/boot`, `/dev`, `/etc`, `/lib`, `/sbin` sunt **esențiale pentru boot**. În schimb, `/var`, `/usr`, `/usr/local` sunt **NON-esențiale** pentru boot — de aceea, în **single-user mode** (mediu de troubleshooting), doar root filesystem-ul poate fi disponibil.

**Tabel director → conținut (memorează-l bine, e testat masiv):**

|Director|Conținut|
|---|---|
|`/`|rădăcina, unifică toate directoarele|
|`/bin`|binare esențiale (`ls`, `cp`, `rm`)|
|`/boot`|fișiere necesare boot-ului (kernel + config)|
|`/dev`|fișiere device (`/dev/null`, `/dev/sda`)|
|`/etc`|configurări esențiale gazdă (`/etc/hosts`, `/etc/passwd`)|
|`/home`|directoare home ale userilor|
|`/lib`|librării pentru `/bin` și `/sbin`|
|`/lib64`|librării pentru arhitecturi 64-bit|
|`/media`|mount point automat pentru media removable|
|`/mnt`|mount point pentru montare manuală temporară|
|`/opt`|software third-party opțional|
|`/proc`|pseudo filesystem info procese|
|`/root`|home directory al root-ului|
|`/sbin`|binare esențiale root|
|`/sys`|pseudo filesystem info hardware|
|`/srv`|servicii specifice site-ului|
|`/tmp`|fișiere temporare (teoretic șterse la boot, dar nu mereu)|
|`/usr`|a doua ierarhie, non-esențial multi-user|
|`/usr/local`|a treia ierarhie, software non-distribuție|
|`/var`|a patra ierarhie, fișiere variabile|
|`/var/cache`|cache aplicații|
|`/var/log`|majoritatea log-urilor|
|`/var/lock`|lock files resurse partajate|
|`/var/spool`|spool pentru print/mail|
|`/var/tmp`|fișiere temporare **păstrate** între reboot-uri|

### 13.6.1 Organization Within the Filesystem Hierarchy

**User Home Directories:**

- `/home/username` — fiecare user primește un director
- Fără permisiuni speciale, userul poate scrie doar în: **propriul home**, `/tmp`, `/var/tmp`

**Binary Directories — separare user vs root:**

|Categorie|Directoare|
|---|---|
|Non-privileged (utilizatori normali)|`/bin`, `/usr/bin`, `/usr/local/bin`|
|Root-restricted (admin)|`/sbin`, `/usr/sbin`, `/usr/local/sbin`|

Third-party software poate avea propriile directoare bin/sbin:

```
/usr/local/application/bin
/opt/application/bin
```

Uneori chiar și userii au propriul `bin` în home: `/home/bob/bin`.

⚠️ Capcană: variabila **`$PATH`** nu conține automat toate directoarele bin/sbin — pentru a rula o comandă dintr-un director care nu e în `$PATH`, trebuie fie adăugat la `PATH`, fie specificată calea completă.

**Software Application Directories:**

⚠️ Capcană comparativă Windows vs Linux: pe Windows, o aplicație are toate fișierele într-un singur folder (`C:\Program Files`). Pe **Linux**, fișierele unei aplicații sunt **răspândite** în mai multe directoare.

Comenzi pentru a vedea unde sunt instalate fișierele unui pachet:

bash

```bash
dpkg -L packagename    # distribuții Debian-derivate
rpm -ql packagename    # distribuții Red Hat-derivate
```

Localizare tipică pentru componentele unei aplicații:

- **Executabil:** `/usr/bin` (dacă vine cu OS-ul) sau `/usr/local/bin`, `/opt/application/bin` (dacă e third-party)
- **Date aplicație:** `/usr/share`, `/usr/lib`, `/opt/application`, `/var/lib`
- **Documentație:** `/usr/share/doc`, `/usr/share/man`, `/usr/share/info`
- **Config globală:** de obicei în `/etc`
- **Config personalizată (per user):** de obicei într-un director ascuns din home-ul userului

**Library Directories:**

- **Library** = fișier cu cod partajat între mai multe programe
- Extensie tipică: **`.so`** (shared object)
- Pot exista **mai multe versiuni** ale aceleiași librării, compilate diferit pentru procesoare diferite (32-bit vs 64-bit)
- Librării pentru `/bin` și `/sbin` → în **`/lib`** sau **`/lib64`**
- Librării pentru `/usr/bin` și `/usr/sbin` → în **`/usr/lib`** sau **`/usr/lib64`**
- Librării pentru aplicații third-party → **`/usr/local/lib`**, **`/opt/application/lib`**

**Variable Data Directories:**

- `/var` și subdirectoarele sale conțin date care se schimbă frecvent
- `/var/mail` sau `/var/spool/mail` — date email
- `/var/spool/cups` — job-uri de printare, temporar
- `/var/log` — log-uri (pot crește mult pe sisteme active)

⚠️ **Capcană critică de examen:** dacă `/var` **NU e o partiție separată**, sistemul root poate deveni plin (din cauza log-urilor care cresc necontrolat) și **sistemul poate crăpa** (crash). Din acest motiv, pe servere e recomandat ca `/var` să fie pe o partiție proprie.