## 1.1 Networks Affect our Lives

### 1.1.1 Networks Connect Us

#### Ideea centrală:

- Comunicarea este una dintre nevoile fundamentale ale omului, aproape la fel de importantă ca aerul, apa, mâncarea și adăpostul. Rețelele moderne au transformat modul în care comunicăm, permițându-ne să fim conectați ca niciodată înainte.

#### Puncte de susținere:

1. **Idei → realitate instant** - oamenii cu idei pot comunica instant cu alții pentru a le transforma în realitate (colaborare globală, în timp real)
2. **Informație globală, instant** - știri și descoperiri devin cunoscute la nivel mondial în câteva secunde
3.  **Conectare socială la distanță** - oamenii se pot conecta și juca jocuri cu prieteni aflați la mii de kilometri distanță (oceane, continente)

#### Concluzii:

- Rețelele nu mai sunt doar o unealtă tehnică - au devenit parte din infrastructura care susține interacțiunea umană globală, indiferent de distanță.

---

## 1.2 Networks Components

### 1.2.1 Host Roles

![Structura Host](HostRoles.png)

#### Ce este un host?

- orice device conectat la o rețea care participă direct la comunicare (ex: calculator, telefon, laptop etc).
- Tehnic: **host = device care are o adresă IP, adresă care identifică host-ul și rețeaua din care face parte host-ul respectiv.**

#### Cele două roluri:

-  Server = rulează software-ul care oferă servicii sau informații altor device-uri (ex: web server, email server, file server).
- Client = este cel care inițializează comunicarea cu server-ul. Clientul rulează software-ul care cere și afișează informația primită de la server (ex: browser, Outlook).

#### Reguli importante

- un server poate deservi mai mulți clienți simultan.
- un singur calculator poate să fie client și server în același timp.
- un calculator poate rula mai multe tipuri de client software deodată(ex: email + browser + streaming, simultan).

#### Tipuri de server software

| Tip   | Ce face                   | Exemplu client  |
| ----- | ------------------------- | --------------- |
| Email | Găzduiește email          | Outlook         |
| Web   | Găzduiește pagini web     | Chrome, Firefox |
| File  | Stochează fișiere central | File Explorer   |

#### Protocoalele din spatele fiecărui tip de server:

| Tip server          | Protocol                                 | Rol                                                 |
| ------------------- | ---------------------------------------- | --------------------------------------------------- |
| **Web**             | **HTTP** (HyperText Transfer Protocol)   | transferă pagini web necriptat                      |
| **Web (securizat)** | **HTTPS** (HTTP Secure)                  | la fel ca HTTP, dar criptat (SSL/TLS)               |
| **Email**           | **SMTP** (Simple Mail Transfer Protocol) | trimite email-uri (client-server sau server-server) |
| **Email (primire)** | **POP3 / IMAP**                          | primesc/citesc email-uri de pe server               |
| **File**            | **FTP** (File Transfer Protocol)         | transferă fișiere                                   |

- Fiecare protocol funcționează pe un **port** specific (ex: HTTP = port 80, HTTPS = port 443, SMTP = port 25 (server-server), SMTP = port 587(client-server), FTP = port 21).

---

### 1.2.2 Peer-to-peer

![Structura PeerToPeer](PeerToPeer.png)

- **Într-o rețea P2P, fiecare calculator poate fi simultan și client și server** nu există o ierarhie fixă ca la client-server, unde serverul e dedicat doar să ofere servicii. Aici toate device-urile sunt "egale" (peers) și pot atât oferi, cât și cere resurse (fișiere, imprimante etc.) unele de la altele.

#### PeerToPeer = o rețea în care device-urile partajează resurse direct între ele, fără server dedicat, fiecare device fiind simultan client și server
#### Practic reține 3 lucruri:

1. **Definiția**: rețea în care nu există server dedicat, toate PC-urile pot juca ambele roluri (client + server) în același timp.
2. **Când se folosește**: potrivit pentru **case și rețele mici de birou** nu pentru business-uri mari.
3. **Trade-off-ul principal**: e simplu și ieftin de configurat, dar **sacrifică securitatea, administrarea centralizată și scalabilitatea**.

#### Avantaje:

- Ușor de configurat (**easy to set up**)
- Mai puțin complex
- Cost mai mic, nu ai nevoie de device-uri de rețea dedicate/servere dedicate
- Bun pentru task-uri simple (transfer fișiere, partajare imprimantă)

#### Dezavantaje:

- **Fără administrare centralizată** - nu există un punct central de control
- **Mai puțin sigur** - nu există autentificare/securitate centralizată
- **Nu e scalabil** - nu funcționează bine când crește numărul de device-uri
- **Toate device-urile pot fi și client și server simultan** → asta le poate **încetini performanța** (fac dublă treabă)

---
### 1.2.3 End Devices

![Structura End Devices](EndDevice.png)

#### **End devices = orice device cu care interacționează direct utilizatorul final** și care generează sau consumă date în rețea.

#### Exemple:

- **Laptopuri, PC-uri, desktop-uri**
- **Telefoane mobile / smartphone-uri**
- **Tablete**
- **Printere** (de rețea)
- **Servere** (web server, file server, mail server - da, și serverele sunt end devices!)
- **Telefoane IP** (cum vezi în figură)
- **Camere de securitate/rețea**
- Practic orice **device "smart"** conectat la rețea care trimite/primește date (IoT - smart TV, smart thermostat, etc.)

#### Atenție: Routerele și switch-urile NU sunt end devices. Ele doar **transportă** date de la un end device la altul, nu generează și nu consumă ele datele.

---
### 1.2.4 Intermediary Devices

![Structura intermediary devices](IntermediaryDevices.png)

- Device-urile intermediare **conectează end device-urile la rețea** și pot conecta mai multe rețele individuale între ele, formând un **internetwork**. Rolul lor: asigură **conectivitatea** și garantează că datele **circulă corect** prin rețea.

#### **Exemple de device-uri intermediare** (din figură):

- **Wireless Router** - router wireless
- **LAN Switch** - switch de rețea locală
- **Router**
- **Multilayer Switch** - switch multi-layer (funcționează și la nivel de rețea, nu doar data link)
- **Firewall Appliance** - dispozitiv de firewall dedicat

---

### 1.2.5 Network Media

![Tipuri de cabluri](NetworkMedia.png)

### **Media** (mediul de transmisie) e canalul prin care mesajul călătorește **de la sursă la destinație**. Practic, e "drumul fizic" pe care circulă datele.

### Cele 3 tipuri principale de media (rețelele moderne):

| Tip                                                      | Cum e codificat datele                                       | Exemplu                               |
| -------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------- |
| **Cupru (Copper)** — fire metalice                       | **Impulsuri electrice**                                      | Cabluri UTP/Ethernet (RJ45)           |
| **Fibră optică (Fiber-optic)** — fibre de sticlă/plastic | **Pulsuri de lumină**                                        | Cabluri fiber cu conectori SC, ST, LC |
| **Wireless** — transmisie fără fir                       | **Modulația undelor electromagnetice** (frecvențe specifice) | Router wireless, Wi-Fi                |


---
## 1.3 Network Representations and Topologies

### 1.3.1 Network Representations

### **Cele 3 categorii de simboluri**

| Categorie                | Exemple                                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------------------- |
| **End Devices**          | Desktop computer, Laptop, Printer, IP Phone, Wireless tablet, TelePresence endpoint             |
| **Intermediary Devices** | Wireless router, LAN switch, Router, Multilayer switch, Firewall appliance                      |
| **Network Media**        | Wireless media (linie ondulată), LAN media (linie continuă), WAN media (linie cu fulger/zigzag) |

### **Termen nou important: Topology Diagram**

- O diagramă care arată cum se conectează device-urile într-o rețea mare se numește **topology diagram** (diagramă de topologie)
- Abilitatea de a recunoaște **reprezentările logice** ale componentelor fizice de rețea e esențială pentru a înțelege organizarea și funcționarea unei rețele


### **3 termeni tehnici noi, de reținut clar (apar des la quiz):**

1. **NIC (Network Interface Card)** — placa de rețea care conectează **fizic** un end device la rețea
2. **Physical Port** — conectorul/priza de pe un device de rețea unde se conectează mediul (cablul) la un end device sau alt device de rețea
3. **Interface** — porturi **specializate** de pe un device de rețea care se conectează la rețele individuale. La routere, aceste porturi se numesc specific **network interfaces** (pentru că routerele conectează rețele diferite între ele)

---
### 1.3.2 Topology Diagrams

Diagramele de topologie sunt **documentație obligatorie** pentru oricine lucrează cu o rețea, oferă o **hartă vizuală** a modului în care e conectată rețeaua. Există **două tipuri**: fizică și logică.

### Physical Topology Diagram

**Ce arată:** **locația fizică** a device-urilor intermediare și **instalarea cablurilor**, practic, unde sunt device-urile în realitate (camere, rack-uri, shelf-uri)

![Fizic](PTD.png)

### Logical Topology Diagram

**Ce arată:** **device-urile, porturile, și schema de adresare** a rețelei, vezi ce end devices sunt conectate la ce device-uri intermediare și ce media se folosește

![Logic](LTD.png)


---
## 1.4 Common Types of Networks

### 1.4.1 Networks of Many Sizes

Rețelele se clasifică după **mărime și scop**: de la rețele mici de casă (partajare resurse locale), la SOHO (muncă de la distanță/afaceri mici), la rețele business mari (colaborare, servere), până la Internet (rețeaua globală, "rețea de rețele")

#### 1. Small Home Networks

![Small Home Network](SmallHome.png)

- Conectează **câteva calculatoare** între ele și la internet
- Permit partajarea resurselor: **printere, documente, poze, muzică** — între câteva end devices locale

#### 2. Small Office and Home Office (SOHO)

![Small Office and Home Office](HomeOffice.png)

- Permit oamenilor să **lucreze de acasă** sau dintr-un birou la distanță
- Folosite mult de **lucrători independenți (self-employed)** — pentru a face reclamă/vinde produse, a comanda materiale, a comunica cu clienții

#### 3. Medium to Large Networks (business-uri/organizații mari)

![Medium to Large Networks](MediumToLarge.png)

- Folosite de business-uri și organizații mari pentru: **consolidare, stocare, și acces la informații** pe servere de rețea
- Oferă **email, mesagerie instant, colaborare** între angajați
- Multe organizații își folosesc conexiunea la internet ca să ofere **produse și servicii clienților**

#### 4. World Wide Networks (Internetul)

![World Wide Networks](WorldWide.png)

- **Internetul** = cea mai mare rețea existentă — termenul "internet" înseamnă literal **"network of networks"** (rețea de rețele)
- E o **colecție de rețele private și publice interconectate**

---
### 1.4.2 LANs and WANs

### LAN = rețea mică, locală, administrată de o singură entitate, viteză mare. 
### WAN = conectează LAN-uri aflate la distanță mare, administrat de mai mulți provideri, viteză mai mică.

### LAN (Local Area Network)

![LAN](LAN.png)

### WAN (Wide Area Network)

![WAN](WAN.png)

---
### 1.4.3 The Internet

![Internet](Internet.png)

- Internetul = colecție globală de LAN-uri interconectate prin WAN-uri, fără un proprietar unic, funcționând datorită unor standarde comune menținute de organizații precum IETF, ICANN și IAB.

### !**Internetul nu este deținut de niciun individ sau grup.** Nimeni nu "deține" Internetul ca întreg!

---
### 1.4.4 Intranets and Extranets

![Intranet and Extranet](IntraExtra.png)

| Nivel        | Cine are acces                                    | Domeniu                 |
| ------------ | ------------------------------------------------- | ----------------------- |
| **Intranet** | Doar angajații companiei                          | Cel mai restrictiv      |
| **Extranet** | Compania + parteneri externi (furnizori, clienți) | Restrictiv, dar extins  |
| **Internet** | Oricine, la nivel mondial                         | Public, nerestricționat |

---

## 1.5 Internet Connections

### 1.5.1 Internet Access Technologies

- Utilizatorii casnici/mici folosesc conexiuni ISP standard (cable, DSL, wireless, mobil), în timp ce business-urile au nevoie de conexiuni mai rapide și mai fiabile (business DSL, leased lines, Metro Ethernet) pentru a susține servicii critice ca telefonie IP și videoconferințe.
### 1.5.2 Home and Small Office Internet Connections

![Connections](Con.png)

| Tip                   | Cum funcționează                                                             | Caracteristici cheie                                                                                                                                        |
| --------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cable**             | Semnalul de internet circulă pe **același cablu** ca televiziunea prin cablu | Bandwidth mare, disponibilitate mare, conexiune **always-on**                                                                                               |
| **DSL**               | Rulează pe **linie telefonică**                                              | Bandwidth mare, always-on. Varianta comună pentru case/birouri mici = **ADSL** (Asymmetrical) → **download mai rapid decât upload**                         |
| **Cellular**          | Folosește **rețeaua de telefonie mobilă**                                    | Disponibil oriunde ai semnal celular; performanța depinde de telefon și de turnul celular la care ești conectat                                             |
| **Satellite**         | Conexiune prin **satelit**                                                   | Util în zone **fără altă opțiune** de internet; dish-ul are nevoie de **linie clară către satelit** (fără obstacole)                                        |
| **Dial-up Telephone** | Folosește **orice linie telefonică + modem**                                 | Opțiune **ieftină**, dar bandwidth foarte mic — insuficient pentru transfer de date mari; util totuși pentru acces mobil în călătorii (variantă de urgență) |

### 1.5.3 Businesses Internet Connections

![Businesses](Buss.png)

| Tip                       | Cum funcționează                                                                                                                         | Caracteristici cheie                                                                                                                                      |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dedicated Leased Line** | **Circuite rezervate** în rețeaua furnizorului de servicii, care conectează sedii **separate geografic** pentru voce și/sau date private | Închiriate la o rată **lunară sau anuală**; conexiune dedicată doar pentru compania ta                                                                    |
| **Metro Ethernet**        | Cunoscut și ca **Ethernet WAN**                                                                                                          | **Extinde tehnologia LAN (Ethernet) în WAN** — practic aduci viteza/simplitatea Ethernet-ului la scară mai mare, între sedii                              |
| **Business DSL**          | Disponibil în mai multe formate                                                                                                          | Popular: **SDSL** (Symmetric DSL) — similar cu DSL consumer, dar **upload și download la aceeași viteză mare** (spre deosebire de ADSL, care e asimetric) |
| **Satellite**             | Conexiune prin satelit                                                                                                                   | Oferă conectivitate **acolo unde nu există soluție prin cablu** (wired)                                                                                   |

### 1.5.4 The Converging Network

**Convergență** = combinarea rețelelor separate de date, voce și video într-**o singură infrastructură de rețea**, capabilă să transporte toate tipurile de trafic simultan, folosind un singur set de standarde.

![.](Traditional.png)

![.](Converged.png)

---

## 1.6 Reliable Networks

### 1.6.1 Network Architecture

- O rețea modernă trebuie construită pe o **arhitectură standard** ca să susțină eficient conectarea oamenilor, device-urilor și informației într-un mediu convergent — iar asta se măsoară prin 4 piloni: toleranță la erori, scalabilitate, QoS, și securitate.

1. **Fault Tolerance** — toleranța la erori
2. **Scalability** — scalabilitate
3. **Quality of Service (QoS)** — calitatea serviciului
4. **Security** — securitate

### 1.6.2 Fault Tolerance

![Tolerance](Tolerance.png)

**Fault tolerance** = capacitatea rețelei de a continua să funcționeze chiar dacă un link/device cade, datorită **redundanței** (căi multiple) și **packet switching** (pachetele își găsesc singure alt drum, dinamic, fără ca userul să simtă ceva).

### 1.6.3 Scalability

**Scalability** = capacitatea rețelei de a crește (mai mulți useri, mai multe aplicații) **fără să afecteze** performanța pentru cei deja conectați — posibilă datorită **standardelor comune** pe care le respectă toți producătorii de echipamente/software.

### 1.6.4 Quality of Service

![QOS](QOS.png)

**QoS prioritizează traficul time-sensitive** (sensibil la timp) — **tipul de trafic contează, nu conținutul lui**. Adică routerul nu se uită la _ce_ se transmite exact, ci la _ce fel_ de trafic e (voce vs date vs video) ca să decidă prioritatea.

### 1.6.5 Network Security

Securitatea rețelei nu înseamnă doar protejarea datelor (information security) — înseamnă și protejarea **fizică** a echipamentelor și a accesului la managementul lor (**infrastructure security**). Sunt **două concerns distincte**, ambele importante.

# CIA

---

## 1.7 Network Trends

### 1.7.1 Recent Trends

- rețelele evoluează continuu pe măsură ce apar tehnologii noi și device-uri noi de utilizator, business-urile și consumatorii trebuie să se adapteze constant.

1. **BYOD** (Bring Your Own Device) — aduci propriul device
2. **Online Collaboration** — colaborare online
3. **Video Communications** — comunicații video
4. **Cloud Computing** — computing în cloud

### 1.7.2 BYOD

- BYOD e trendul prin care oamenii își folosesc propriile device-uri personale (nu doar echipamente oferite de companie) pentru a se conecta și lucra pe rețeaua organizației ridică probleme de securitate pentru că device-urile nu sunt neapărat controlate/deținute de organizație.

# any device, with any ownership, used anywhere

### 1.7.3 Online Collaboration

- Rețelele moderne nu mai servesc doar la accesarea de informații (citit date), ci facilitează **colaborarea în timp real**, întâlniri video, partajare de ecran, lucru pe proiecte comune, indiferent de locația fizică a participanților.

### 1.7.4 Video Communications

- Video-ul e o altă componentă critică pentru comunicare și colaborare. E folosit pentru **3 scopuri**: **comunicații, colaborare, și divertisment**.

### 1.7.6 Cloud Computing

- Cloud computing e una din metodele prin care **accesăm și stocăm date** permite stocarea fișierelor personale, chiar backup la un întreg drive, pe servere prin internet. Aplicații ca procesare de text sau editare foto pot fi accesate direct din cloud.

| Tip           | Descriere                                                                                                                                                                                                                                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Public**    | Aplicații/servicii oferite **populației generale** — gratuite sau pay-per-use (ex: stocare online). Folosește **internetul** pentru livrare                                                                                                                                                                       |
| **Private**   | Destinat unei **organizații/entități specifice** (ex: guvern). Poate fi construit pe rețeaua privată a organizației (scump) sau administrat de o companie externă cu **securitate strictă de acces**                                                                                                              |
| **Hybrid**    | Combinație de **2 sau mai multe clouds** (ex: parte privat, parte public) — fiecare parte rămâne distinctă, dar conectate printr-o **arhitectură unică**. Accesul diferă în funcție de drepturile utilizatorului                                                                                                  |
| **Community** | Creat pentru **uz exclusiv** de entități/organizații specifice cu nevoi similare. Ex: organizații medicale care trebuie să respecte reglementări (ca **HIPAA**) — necesită autentificare și confidențialitate speciale. E similar cu public cloud, dar cu niveluri de securitate/conformitate ca la private cloud |

- **Public** = oricine, prin internet
- **Private** = o singură organizație
- **Hybrid** = mix de public + private
- **Community** = mai multe organizații cu nevoi/reglementări similare (ex: sănătate, guvernamental)

### 1.7.7 Technology Trends in the Home

Smart home technology va deveni tot mai comună pe măsură ce **networking-ul de acasă și internetul de mare viteză** se extind, se dezvoltă pentru **toate camerele** casei, nu doar bucătărie.

### 1.7.8 Powerline Networking

Powerline = alternativă la cablurile Ethernet sau la Wi-Fi, ideală când vrei semnal de rețea într-o zonă unde Wi-Fi-ul nu ajunge bine, dar ai prize electrice disponibile.

### 1.7.9 Wireless Broadband

**WISP** = soluția wireless pentru zone rurale fără cable/DSL — antenă pe acoperișul clientului conectată wireless la un punct de access aflat pe o structură înaltă din apropiere.

![Wireless Broadband](WirelessBroadband.png)

---

## 1.8 Network Security

### 1.8.1 Security Threats

Securitatea rețelei e o **prioritate de top** pentru administratori, atât pentru o rețea de casă (o singură conexiune), cât și pentru o corporație cu mii de useri.

| Tip                               | Descriere                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------- |
| **Viruses, worms, Trojan horses** | Software/cod malițios care rulează pe device-ul utilizatorului                      |
| **Spyware and adware**            | Software instalat pe device care **colectează secret informații** despre utilizator |
| **Zero-day attacks**              | (zero-hour) Ataca **prima zi** în care o vulnerabilitate devine cunoscută           |
| **Threat actor attacks**          | O persoană malițioasă atacă direct device-uri sau resurse de rețea                  |
| **Denial of service (DoS)**       | Încetinește sau blochează aplicații/procese de pe un device de rețea                |
| **Data interception and theft**   | Capturează informații private din rețeaua unei organizații                          |
| **Identity theft**                | Fură **credențialele de login** ale unui utilizator pentru a accesa date private    |

### 1.8.2 Security Solutions

Nicio soluție unică nu poate proteja rețeaua de toate amenințările → securitatea trebuie implementată **în mai multe straturi (layers)**, cu mai multe soluții — dacă una eșuează, altele pot reuși.

---
## 1.9 The IT Professional

---

## 1.10 Module Practice and Quiz