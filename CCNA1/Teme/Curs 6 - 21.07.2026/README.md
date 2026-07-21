# Laborator Packet Tracer — Rutare Statică (Static Routing)

Topologie cu **2 rețele LAN** interconectate printr-o legătură punct-la-punct între două routere, cu server TFTP pentru backup de configurație.

## Topologie și adresare IP

|Rețea|Adresă rețea|Rol|
|---|---|---|
|LAN 1|`192.168.1.0/24`|PC-uri conectate la SW1 → R1|
|Legătură R1 ↔ R2|`10.10.10.0/24`|Link serial/Ethernet între routere|
|LAN 2|`192.168.2.0/24`|PC-uri + Server TFTP conectate la SW2 → R2|

|Dispozitiv|Interfață|Adresă IP|Gateway|
|---|---|---|---|
|PC1 (LAN 1)|—|`192.168.1.x`|`192.168.1.1`|
|Server TFTP (LAN 2)|—|`192.168.2.3`|`192.168.2.1`|
|R1|G0/0|`192.168.1.1/24`|—|
|R1|G0/1|`10.10.10.1/24`|—|
|R2|G0/0|`10.10.10.2/24`|—|
|R2|G0/1|`192.168.2.1/24`|—|

---

## Pasul 1 — Configurarea dispozitivelor finale

Pentru fiecare PC și pentru serverul TFTP: **Desktop → IP Configuration**, unde se introduc adresa IP, subnet mask-ul și gateway-ul conform tabelului de mai sus.

---

## Pasul 2 — Configurarea switch-urilor (LAN 1 și LAN 2)

Aceleași comenzi se aplică identic pe **SW1** și **SW2** (se schimbă doar hostname-ul).

### 2.1 SW1 (LAN 1)

```
enable
configure terminal
hostname SW1
enable secret ccna
line console 0
password userlogin
login
exit
line vty 0 4
password cisco
login
transport input telnet
exit
service password-encryption
banner motd $Authorization #2 Required$
end
write memory
```

### 2.2 SW2 (LAN 2)

```
enable
configure terminal
hostname SW2
enable secret ccna
line console 0
password userlogin
login
exit
line vty 0 4
password cisco
login
transport input telnet
exit
service password-encryption
banner motd $Authorization #2 Required$
end
write memory
```

---

## Pasul 3 — Configurarea routerelor (R1 și R2)

Fiecare router primește: setări standard de securitate (identice cu cele de pe switch-uri) + configurarea interfețelor + rută statică către rețeaua opusă.

### 3.1 R1

**Securitate + hostname**

```
enable
configure terminal
hostname R1
enable secret ccna
line console 0
password userlogin
login
exit
line vty 0 4
password cisco
login
transport input telnet
exit
service password-encryption
banner motd $Authorization #2 Required$
```

**Interfețe (LAN 1 + link spre R2)**

```
interface GigabitEthernet0/0
ip address 192.168.1.1 255.255.255.0
no shutdown
exit

interface GigabitEthernet0/1
ip address 10.10.10.1 255.255.255.0
no shutdown
exit
```

**Rută statică spre LAN 2 (prin R2)**

```
ip route 192.168.2.0 255.255.255.0 10.10.10.2
```

**Salvare**

```
end
write memory
```

### 3.2 R2

**Securitate + hostname**

```
enable
configure terminal
hostname R2
enable secret ccna
line console 0
password userlogin
login
exit
line vty 0 4
password cisco
login
transport input telnet
exit
service password-encryption
banner motd $Authorization #2 Required$
```

**Interfețe (link spre R1 + LAN 2)**

```
interface GigabitEthernet0/0
ip address 10.10.10.2 255.255.255.0
no shutdown
exit

interface GigabitEthernet0/1
ip address 192.168.2.1 255.255.255.0
no shutdown
exit
```

**Rută statică spre LAN 1 (prin R1)**

```
ip route 192.168.1.0 255.255.255.0 10.10.10.1
```

**Salvare**

```
end
write memory
```

---

## Pasul 4 — Backup configurație pe server TFTP

Pe R1 și R2, din CLI:

```
copy running-config tftp
```

La cerere se introduce adresa serverului TFTP (`192.168.2.3`) și numele fișierului de configurare.

---

## Explicația comenzilor (detaliat)

### Moduri de operare

**`enable`** Trece dispozitivul din **modul utilizator** (`>`, acces limitat, doar comenzi `show` de bază) în **modul privilegiat** (`#`), unde ai acces la toate comenzile de vizualizare și la comanda `configure terminal`. Fără acest mod nu poți intra în configurare.

**`configure terminal`** (prescurtat `conf t`) Trece din modul privilegiat (`#`) în **modul de configurare globală** (`(config)#`). Aici se fac toate modificările care afectează întregul dispozitiv: hostname, parole, interfețe, rutare etc. Fiecare sub-mod (interfață, linie) se accesează tot de aici.

**`exit`** Iese cu un nivel mai sus din modul curent (ex: din `(config-if)#` înapoi în `(config)#`). Diferă de `end`, care sare direct în modul privilegiat indiferent de cât de "adânc" ești.

**`end`** Iese complet din modul de configurare, din orice sub-mod te-ai afla, și revine direct în modul privilegiat (`#`). Se folosește de obicei la finalul configurării, înainte de `write memory`.

---

### Identificare și parole

**`hostname R1`** Schimbă numele dispozitivului afișat în prompt (ex: `Router>` devine `R1>`). Ajută la identificarea rapidă a echipamentelor într-o topologie cu mai multe routere/switch-uri.

**`enable secret ccna`** Setează parola pentru accesul în modul privilegiat. Spre deosebire de vechea comandă `enable password`, `enable secret` **criptează automat** parola în fișierul de configurare (folosind MD5), indiferent dacă `service password-encryption` e activă sau nu. Este comanda recomandată din motive de securitate.

---

### Securizarea accesului local (consolă)

**`line console 0`** Intră în modul de configurare al portului fizic de consolă (portul prin care te conectezi direct cu un cablu, nu prin rețea). `0` reprezintă numărul liniei — consola are o singură linie, deci mereu `0`.

**`password userlogin`** Setează parola care va fi cerută la conectarea prin acest port.

**`login`** Activează cererea de parolă la conectare. Fără această comandă, parola setată mai sus **nu este verificată** — oricine se conectează intră direct, fără autentificare.

---

### Securizarea accesului la distanță (Telnet)

**`line vty 0 4`** Intră în modul de configurare al liniilor virtuale (VTY), folosite pentru conexiuni de la distanță (Telnet/SSH). `0 4` înseamnă că se configurează simultan liniile de la 0 la 4 — adică **5 sesiuni** de la distanță pot fi active în paralel.

**`password cisco`** Setează parola cerută pentru conexiunile de la distanță.

**`login`** La fel ca la consolă — activează verificarea parolei pentru cei ce se conectează prin vty.

**`transport input telnet`** Specifică ce protocoale sunt acceptate pe liniile vty. Cu `telnet`, dispozitivul acceptă **doar** conexiuni Telnet (nu SSH, nu altceva). Dacă vrei să permiți ambele protocoale, comanda ar fi `transport input telnet ssh`.

---

### Criptare și banner

**`service password-encryption`** Criptează (cu un algoritm slab, tip XOR — nu e criptare puternică, dar ascunde parola din `show running-config`) **toate** parolele din configurație care altfel ar fi vizibile în text clar (de exemplu cele setate cu `password`, spre deosebire de `enable secret` care e deja criptată puternic).

**`banner motd $Authorization #2 Required$`** Setează un mesaj afișat **înainte** de ecranul de login (Message Of The Day) — util pentru avertismente legale ("acces neautorizat interzis" etc). Caracterul `$` este delimitatorul de început/sfârșit al mesajului; poate fi orice caracter care nu apare în text, atâta timp cât e folosit consecvent la ambele capete.

---

### Configurarea interfețelor

**`interface GigabitEthernet0/0`** Intră în modul de configurare al interfeței specifice `G0/0`. Numărul depinde de portul fizic folosit pe router (verifică în Packet Tracer denumirea exactă a interfeței conectate).

**`ip address 192.168.1.1 255.255.255.0`** Alocă interfeței adresa IP `192.168.1.1` cu masca de subrețea `255.255.255.0` (adică `/24`). Aceasta devine gateway-ul pentru dispozitivele din acea rețea.

**`no shutdown`** Activează interfața. Din fabrică, toate interfețele routerului sunt **oprite administrativ** (`shutdown`); fără această comandă, interfața rămâne "down" chiar dacă e cablată corect.

---

### Salvare și rutare

**`write memory`** (echivalent cu `copy running-config startup-config`) Salvează configurația curentă din memoria volatilă (RAM — `running-config`) în memoria nevolatilă (NVRAM — `startup-config`). **Esențial**: dacă router-ul se repornește fără acest pas, toată configurația se pierde.

**`ip route 192.168.2.0 255.255.255.0 10.10.10.2`** Adaugă o **rută statică**. Sintaxa este:

```
ip route <rețea destinație> <mască subrețea> <next-hop>
```

Îi spune routerului: "pentru a ajunge la rețeaua `192.168.2.0/24`, trimite pachetele către `10.10.10.2`" (interfața următorului router de pe traseu). Este necesară pe **ambele** routere, fiecare cu ruta către rețeaua LAN a celuilalt, altfel traficul între cele două LAN-uri nu poate fi rutat.

**`copy running-config tftp`** Trimite o copie a configurației curente (running-config) către un server TFTP din rețea, pentru backup extern. Se cere adresa IP a serverului și numele fișierului sub care va fi salvată configurația.