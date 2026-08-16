### 14.2-14.3 Terminologie de bază

Termeni rapizi (îi știi deja din CCNA, doar traducere de context LPI):

- **Host** = orice device care comunică în rețea (nu doar PC/laptop)
- **Router / Gateway** = termeni echivalenți în acest curs
- **Service** = o funcție oferită de un host altui host
- **Ethernet** — viteze: minim **10 Mbps**, maxim **100 Gbps**; cele mai comune: **100 Mbps și 1 Gbps**

⚠️ Nimic surprinzător aici pentru tine, dar reține exact formulările — LPI Essentials pune uneori întrebări literale pe definiții ("ce este un host?", "ce este DHCP?").

### 14.4 IP Addresses

- IPv4 = 32-bit (4×8 biți), IPv6 = 128-bit
- **NAT** și **Porting** = cele 2 motive pentru care IPv6 nu a înlocuit încă IPv4 global
- ⚠️ Capcană: procentul de dispozitive care încă folosesc IPv4 e citat ca **98-99%**

### 14.5.1.1-14.5.1.2 — Fișiere de configurare rețea (IMPORTANT pentru examen)

Pe **CentOS**, fișierul principal pentru configurare IPv4 static:

```
/etc/sysconfig/network-scripts/ifcfg-eth0
```

Parametri cheie din acest fișier (foarte testați):

|Parametru|Semnificație|
|---|---|
|`DEVICE="eth0"`|numele interfeței|
|`BOOTPROTO=none`|none/static = fără DHCP; `dhcp` = client DHCP|
|`ONBOOT=yes`|pornește interfața automat la boot|
|`IPADDR`|adresa IP|
|`PREFIX=24`|echivalent cu masca /24|
|`GATEWAY`|adresa gateway-ului|
|`DNS1`|server DNS|

⚠️ **Capcană:** dacă e configurat ca DHCP client, `IPADDR`, `GATEWAY`, `DNS1` **nu vor fi setate** în fișier (le primește dinamic).

**Pentru IPv6**, se adaugă în același fișier:

```
IPV6INIT=yes
IPV6ADDR=<IPv6 IP Address>
IPV6_DEFAULTGW=<IPv6 IP Gateway Address>
```

Pentru DHCP IPv6:

```
DHCPV6C=yes
```

Și obligatoriu în `/etc/sysconfig/network`:

```
NETWORKING_IPV6=yes
```

⚠️ **Capcană importantă — metoda corectă de a aplica schimbări:**

- Metodă **specifică/limitată** (preferată): `ifdown eth0` → editezi config → `ifup eth0`
- Metodă **radicală** (afectează TOATE interfețele): `service network restart`

Regula de examen: **folosește întotdeauna cea mai specifică comandă posibilă**, ca să nu perturbi alte interfețe.

### 14.5.1.3 DNS

- Adresa serverului DNS e stocată în **`/etc/resolv.conf`**

```
nameserver 127.0.0.1
```

- Comanda `host` — rezolvă un hostname în IP:

bash

```bash
host example.com
```

### 14.5.1.4 — Cele 3 fișiere critice pentru rezoluția de nume (FOARTE testat!)

|Fișier|Rol|
|---|---|
|`/etc/hosts`|tabel local hostname → IP|
|`/etc/resolv.conf`|adresele serverelor DNS de consultat|
|`/etc/nsswitch.conf`|ordinea în care sunt consultate sursele|

Linia cheie din `/etc/nsswitch.conf`:

```
hosts:    files dns
```

= caută întâi în `/etc/hosts`, apoi la DNS.

```
hosts:    dns files
```

= caută întâi DNS, apoi local.

⚠️ **Capcană critică de examen — ordinea exactă a procesului:**

1. Se consultă **`/etc/nsswitch.conf`** (ce ordine să folosească)
2. Dacă ordinea zice "files" primul → se consultă **`/etc/hosts`**
3. Dacă nu găsește potrivire → se consultă **`/etc/resolv.conf`** pentru serverele DNS

⚠️ **Capcană foarte importantă:** dacă `/etc/hosts` conține o intrare (chiar greșită/inexactă), sistemul **NU** trece mai departe la DNS — se oprește acolo cu rezultatul din `/etc/hosts`, chiar dacă e incorect!

`/etc/resolv.conf` ar trebui să aibă minim 2 servere `nameserver` — primul e încercat, al doilea e backup dacă primul nu răspunde/timeout.

Cuvinte cheie suplimentare posibile în `/etc/resolv.conf`:

- **`domain`** — completează automat un domeniu la hostname-uri scurte
- **`search`** — o listă de domenii încercate secvențial

### 14.6 Network Tools — Comenzi (secțiunea cea mai densă în comenzi)

#### 14.6.1 `ifconfig`

bash

```bash
ifconfig
```

Afișează config rețea. ⚠️ Capcană: comanda e considerată **deprecated** (învechită), înlocuită treptat de `ip addr show`.

Interfața **`lo`** = **loopback** device (folosit de sistem pentru a trimite date către el însuși).

#### 14.6.2 `ip` command — înlocuitorul modern

Sintaxă generală:

```
ip [OPTIONS] OBJECT COMMAND
```

bash

```bash
ip addr show     # echivalentul lui ifconfig
```

⚠️ Capcană de examen: `ip` înlocuiește **mai multe** comenzi vechi simultan — nu doar `ifconfig`, ci și `route` și `arp`.

#### 14.6.3 `route` command

bash

```bash
route          # tabelul de rutare, cu nume
route -n       # tabelul de rutare, doar cifre (fără rezoluție de nume)
```

⚠️ Capcană: `default` (în output cu nume) = **`0.0.0.0`** (în output cu `-n`) = "toate celelalte destinații".

Comandă modernă echivalentă (`route` e deprecated):

bash

```bash
ip route show
```

#### 14.6.4 `ping` command

bash

```bash
ping -c 4 192.168.1.2    # -c limitează la 4 pachete (implicit ping rulează la infinit!)
```

⚠️ Capcană: dacă `ping` eșuează, **NU înseamnă automat** că mașina e nedisponibilă — poate fi configurată explicit să ignore ping-urile, ca protecție împotriva **denial of service attacks**.

Recomandare practică din curs: dă ping cu **hostname** — dacă merge, confirmi și rezoluția de nume, și conectivitatea IP simultan.

#### 14.6.5 `netstat` command

bash

```bash
netstat -i       # statistici trafic (TX-OK, TX-ERR — procent mare de erori = problemă de rețea)
netstat -r       # tabel de rutare (similar cu route)
netstat -tln     # porturi deschise
```

⚠️ **Capcană — semnificația opțiunilor** (foarte testată):

- `-t` = **TCP**
- `-l` = **listening** (porturi care ascultă)
- `-n` = **show numbers, not names** (afișează IP/porturi numeric, nu hostname/nume de servicii)

Exemplu: dacă portul **22** apare cu status **LISTEN**, înseamnă serviciul **SSH** e activ și acceptă conexiuni.

⚠️ Capcană: `netstat` e de asemenea **deprecated** pe unele distribuții, înlocuit cu:

- `netstat` → **`ss`**
- `netstat -r` → **`ip route`**
- `netstat -i` → **`ip -s link`**
- `netstat -g` → **`ip maddr`**

---

**Rezumat capcane critice ale acestei părți:**

- Ordinea rezoluției de nume: `nsswitch.conf` → `hosts` → `resolv.conf`
- `/etc/hosts` cu intrare greșită → sistemul **nu** face fallback la DNS
- `ifdown`/`ifup` (specific) vs `service network restart` (global, riscant)
- Comenzi deprecated → înlocuitori: `ifconfig`→`ip addr`, `route`→`ip route`, `netstat`→`ss`
- `-t`, `-l`, `-n` la `netstat`
  
  

### 14.6.6 `ss` command

Menit ca **înlocuitor** pentru `netstat`, arată statistici despre socket-uri și conexiuni curent stabilite.

bash

```bash
ss          # output implicit
ss -s       # statistici sumarizate pe tip de socket (TCP/UDP/RAW/etc.)
```

**Coloane cheie ale output-ului `ss`:**

|Coloană|Semnificație|
|---|---|
|`Netid`|tipul de socket + protocolul de transport|
|`State`|conectat sau neconectat (depinde de protocol)|
|`Recv-Q`|date în coadă, primite, așteptând procesare|
|`Send-Q`|date în coadă, așteptând trimitere|
|`Local Address:Port`|adresa/portul local|
|`Peer Address:Port`|adresa/portul mașinii remote|

⚠️ Capcană practică: output-ul poate fi foarte lung — recomandare din curs: folosește `less` ca pager.

### 14.6.7 `dig` command

Testează funcționalitatea unui server DNS, interogându-l direct.

bash

```bash
dig example.com
```

Secțiuni de output importante:

- **QUESTION SECTION** — ce s-a interogat
- **ANSWER SECTION** — răspunsul (IP-ul găsit)
- **AUTHORITY SECTION** — serverul de nume autoritativ

⚠️ Dacă domeniul nu poate fi rezolvat (server-ul DNS nu are informația și niciun alt server contactat nu o are):

```
;; connection timed out; no servers could be reached
```

### 14.6.8 `host` command

Formă simplă — hostname → IP:

bash

```bash
host example.com
# example.com has address 192.168.1.2
```

⚠️ **Capcană — funcționează și invers** (IP → hostname, "reverse lookup"):

bash

```bash
host 192.168.1.2
# 2.1.168.192.in-addr.arpa domain name pointer example.com.
```

Notă formatul invers al octeților IP în interogarea reverse (`2.1.168.192.in-addr.arpa`).

Opțiuni utile:

bash

```bash
host -t CNAME example.com   # interoghează CNAME (alias)
host -t SOA example.com     # Start of Authority - server-ul primar al domeniului
host -a example.com         # TOATE informațiile DNS disponibile (-a = all)
```

### 14.6.9 `ssh` command

Conectare la altă mașină din rețea, autentificare și execuție de comenzi remote.

bash

```bash
ssh username@hostname
```

⚠️ Capcană: dacă specifici doar hostname-ul, fără username, `ssh` presupune automat că vrei să te loghezi cu **același username** cu care ești logat local.

Ieșire de pe mașina remote, înapoi la cea locală:

bash

```bash
exit
```

⚠️ **Capcană de examen — atenție la `exit` folosit repetat:** dacă apeși `exit` prea multe ori, riști să închizi complet fereastra de terminal (nu doar sesiunea SSH), pentru că la un moment dat ieși din shell-ul local însuși.

#### 14.6.9.1 RSA Key Fingerprint

- Prima dată când te conectezi la o mașină nouă prin SSH, ești întrebat să confirmi identitatea ei (RSA key fingerprint) — răspunzi de obicei `yes`.
- Fingerprint-ul e stocat local, pentru verificări viitoare.

⚠️ **Capcană critică de examen** — dacă la o conexiune ulterioară fingerprint-ul **nu se potrivește** cu cel stocat local, apare un avertisment sever:

```
WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
```

Acest lucru poate indica un **atac man-in-the-middle** — DAR poate fi și un motiv legitim (mașina remote a fost **reinstalată** și are cheie RSA nouă).

Fișierul unde sunt stocate fingerprint-urile cunoscute:

```
~/.ssh/known_hosts
```

Pentru a rezolva conflictul (dacă ești sigur că e legitim — server reinstalat):

bash

```bash
rm ~/.ssh/known_hosts     # șterge tot fișierul
# SAU elimină doar intrarea specifică indicată de eroare
```