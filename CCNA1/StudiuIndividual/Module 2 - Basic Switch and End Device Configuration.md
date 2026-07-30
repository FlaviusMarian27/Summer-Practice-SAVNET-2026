

## 2.1 Cisco IOS Access

### 2.1.1 Operating Systems

![OS](../Image/OS.png)

Toate device-urile (end devices și network devices) au nevoie de un OS.

- **Shell** – interfața cu utilizatorul, permite cereri de task-uri specifice de la calculator. Poate fi CLI sau GUI.
- **Kernel** – comunică între hardware și software, gestionează cum sunt folosite resursele hardware pentru cerințele software-ului.
- **Hardware** – partea fizică a calculatorului, inclusiv electronica de bază.

Structura e concentrică: Hardware (în centru) → Kernel → Shell (exterior), iar utilizatorul interacționează cu Shell-ul prin CLI sau GUI.

**CLI** (command-line interface): utilizatorul interacționează direct cu sistemul într-un mediu text-based, introducând comenzi de la tastatură la un prompt. Sistemul execută comanda și de obicei dă output textual. CLI necesită overhead foarte mic, dar necesită cunoașterea structurii de comenzi.



### 2.1.2 GUI

GUI (Windows, macOS, Linux KDE, Apple iOS, Android) — utilizatorul interacționează prin icoane grafice, meniuri, ferestre. E mai user-friendly, necesită mai puțină cunoaștere a structurii de comenzi → de aceea majoritatea utilizatorilor preferă GUI.

Totuși, GUI-urile pot să nu ofere toate funcțiile disponibile prin CLI, pot să pice/crash-uiască sau să nu funcționeze cum trebuie. **De aceea network device-urile sunt de obicei accesate prin CLI** — CLI e mai puțin resource-intensive și mult mai stabil decât GUI.

- Familia de OS-uri de rețea folosită pe multe device-uri Cisco = **Cisco IOS (Internetwork Operating System)**.
- Cisco IOS e folosit pe multe routere și switch-uri Cisco, indiferent de tip/mărime.
- Fiecare tip de router/switch folosește o versiune diferită de IOS.
- Alte OS-uri Cisco: **IOS XE, IOS XR, NX-OS**.
- **Notă:** OS-ul de pe routerele de acasă se numește de obicei **firmware**. Cea mai comună metodă de configurare a unui router de acasă = printr-un GUI bazat pe browser web.



### 2.1.3 Purpose of an OS

Network OS-urile sunt similare cu OS-ul de PC.

Printr-un GUI, un OS de PC permite utilizatorului să:

- folosească mouse-ul pentru selecții și rulare de programe
- introducă text și comenzi text-based
- vadă output pe un monitor

Un network OS bazat pe CLI (ex: Cisco IOS pe switch/router) permite unui tehnician de rețea să:

- folosească tastatura pentru a rula programe CLI-based
- folosească tastatura pentru a introduce text și comenzi text-based
- vadă output pe un monitor

Device-urile Cisco rulează versiuni particulare de IOS, dependente de tipul de device și feature-urile necesare. Toate device-urile vin cu un IOS default și un set de feature-uri default, dar poate fi făcut upgrade la versiunea de IOS sau la feature set pentru capabilități suplimentare.



### 2.1.4 Access Methods

Un switch va forward-ui trafic by default, fără să fie explicit configurat — ex: două host-uri conectate la un switch nou pot comunica direct. Totuși, **toate switch-urile trebuie configurate și securizate**.

|Metodă|Descriere|
|---|---|
|**Console**|Port fizic de management, oferă acces **out-of-band** (canal de management dedicat, doar pentru mentenanță device). Avantaj: device-ul e accesibil chiar dacă nu sunt configurate servicii de rețea (ex: la configurarea inițială). Necesită un calculator cu software de terminal emulation + cablu console special.|
|**SSH (Secure Shell)**|Metodă **in-band**, recomandată, pentru stabilirea securizată de la distanță a unei conexiuni CLI, printr-o interfață virtuală, peste rețea. Spre deosebire de console, necesită servicii de rețea active pe device, inclusiv o interfață activă configurată cu adresă. Majoritatea versiunilor de Cisco IOS includ server SSH și client SSH.|
|**Telnet**|Metodă **in-band**, nesigură, de stabilire la distanță a unei sesiuni CLI, printr-o interfață virtuală, peste rețea. Spre deosebire de SSH, nu oferă conexiune securizată/criptată — ar trebui folosit doar în lab. Autentificare, parole și comenzi sunt trimise în plaintext peste rețea. Best practice = SSH în loc de Telnet. Cisco IOS include atât server cât și client Telnet.|

**Notă:** unele device-uri (ex: routere) pot suporta un port **auxiliary (AUX)** legacy, folosit pentru sesiune CLI de la distanță printr-o conexiune telefonică (modem). La fel ca console, AUX e out-of-band și nu necesită servicii de rețea configurate/disponibile.



### **2.1.5 Terminal Emulation Programs**

Programe de terminal emulation folosite pentru conectare la un network device, fie prin conexiune serială pe portul console, fie prin conexiune SSH/Telnet. Permit ajustarea dimensiunii ferestrei, mărimii fontului, schemelor de culori.

Exemple: **PuTTY, Tera Term, SecureCRT**.

---

## 2.2 IOS Navigation

### 2.2.1 Primary Command Modes

Cisco IOS separă accesul de management în două moduri de comandă principale (feature de securitate):

- **User EXEC Mode** – capabilități limitate, dar util pentru operații de bază. Permite doar un număr limitat de comenzi de monitorizare, **nu permite** execuția niciunei comenzi care ar putea schimba configurația device-ului. Prompt-ul se termină cu **>**. Numit adesea "view-only" mode.
- **Privileged EXEC Mode** – pentru a executa comenzi de configurare, un administrator de rețea trebuie să acceseze acest mod. Modurile de configurare mai avansate (ex: global configuration mode) pot fi accesate doar din Privileged EXEC. Prompt-ul se termină cu **#**. Permite acces la toate comenzile și feature-urile, orice comenzi de monitorizare, configurare și management.

| Mod                  | Descriere                                                   | Prompt default        |
| -------------------- | ----------------------------------------------------------- | --------------------- |
| User EXEC Mode       | acces doar la comenzi de monitorizare limitate; "view-only" | `Switch>` / `Router>` |
| Privileged EXEC Mode | acces la toate comenzile și feature-urile                   | `Switch#` / `Router#` |




### 2.2.2 Configuration Mode and Subconfiguration Modes

Pentru a configura device-ul, utilizatorul trebuie să intre în **global configuration mode** ("global config mode"). Din global config mode se fac schimbări CLI care afectează operarea device-ului ca întreg. Se identifică prin prompt care se termină cu **(config)#** după numele device-ului, ex: `Switch(config)#`.

Global config mode e accesat înaintea altor moduri de configurare specifice. Din el, utilizatorul poate intra în diverse **subconfiguration modes**, fiecare permițând configurarea unei părți/funcții specifice a device-ului IOS. Două subconfig modes comune:

- **Line Configuration Mode** – folosit pentru a configura acces console, SSH, Telnet sau AUX.
- **Interface Configuration Mode** – folosit pentru a configura un port de switch sau o interfață de rețea a router-ului.

Când e folosit CLI, modul e identificat prin prompt-ul unic acelui mod. Implicit, orice prompt începe cu numele device-ului, iar restul indică modul:

- Line config mode → `Switch(config-line)#`
- Interface config mode → `Switch(config-if)#`




### 2.2.3 Video - IOS CLI Primary Command Mode

#### Vezi video



### 2.2.4 Navigate Between IOS Modes

Diverse comenzi mută în/din prompt-urile de comandă:

- **User EXEC → Privileged EXEC**: comanda **enable**
- **Privileged EXEC → User EXEC**: comanda **disable**
- Notă: Privileged EXEC mode e uneori numit _enable mode_.
- **Privileged EXEC → Global config**: comanda **configure terminal**
- **Global config → Privileged EXEC**: comanda **exit**

Pentru subconfiguration modes: se folosește comanda **line** urmată de tipul liniei de management și numărul dorit (ex: `line console 0`). Comanda **exit** iese dintr-un subconfig mode și te întoarce în global config mode.

```
Switch(config)# line console 0
Switch(config-line)# exit
Switch(config)#
```

Din **orice** subconfiguration mode al global config mode, comanda **exit** te duce un nivel mai sus în ierarhie.

Din **orice** subconfig mode direct în **Privileged EXEC mode**: comanda **end** sau combinația **Ctrl+Z**.

```
Switch(config-line)# end
Switch#
```

Poți trece direct dintr-un subconfig mode în altul — ex, după selectarea unei interfețe, prompt-ul se schimbă din `(config-line)#` în `(config-if)#`:

```
Switch(config-line)# interface FastEthernet 0/1
Switch(config-if)#
```




### 2.2.5 Video - Navigate Between IOS Modes

## Vezi video




### 2.2.6 A Note About Syntax Checker Activities

Când înveți să modifici configurații de device, e bine să începi într-un mediu safe, non-production, înainte de a încerca pe echipament real. NetAcad oferă tool-uri de simulare pentru a construi skill-uri de configurare și troubleshooting. Fiind tool-uri de simulare, de obicei nu au toată funcționalitatea echipamentului real.

- **Syntax Checker** – primești un set de instrucțiuni pentru a introduce un set specific de comenzi. Nu poți avansa decât dacă introduci comanda exactă și completă conform specificației.
- **Packet Tracer** – tool de simulare mai avansat, permite introducerea de comenzi abreviate, la fel ca pe echipament real.

---

## 2.3 The Command Structure

### 2.3.1 Basic IOS Command Structure

![IOS](../Image/StructureIOS.png)

- Fiecare comandă IOS are un **format/sintaxă specific** și poate sa fie executată **doar în modul corect**. Structura generală: **comandă + keyword(s)/argument(s) potrivite**.

**Cele 4 componente ale unei comenzi** (din diagramă):

| Componentă                    | Rol                 | Exemplu 1 (`show ip protocols`) | Exemplu 2 (`ping 192.168.10.5`) |
| ----------------------------- | ------------------- | ------------------------------- | ------------------------------- |
| **Prompt**                    | Indică modul curent | `Switch>`                       | `Switch>`                       |
| **Command**                   | Acțiunea de bază    | `show`                          | `ping`                          |
| **Space**                     | Separator           | (spațiu)                        | (spațiu)                        |
| **Keyword(s) or Argument(s)** | Detaliile comenzii  | `ip protocols`                  | `192.168.10.5`                  |

**Explicație simplă:**
- **Keyword** = opțiune fixă, din lista "meniului" IOS-ului (ex: `ip protocols` e o opțiune predefinită pentru comanda `show`)
- **Argument** = valoare pe care **tu** o alegi/introduci (ex: o adresă IP specifică pentru `ping`)

---

### 2.3.2 IOS Command Syntax Check

- O comandă poate necesita unul sau mai multe argumente. Ca să știi ce keywords/arguments sunt necesare, te uiți la **sintaxa comenzii**  pattern-ul/formatul care trebuie respectat.

#### Convențiile de notație (esențiale, sigur apar la quiz):

| Convenție                    | Descriere                                                        |
| ---------------------------- | ---------------------------------------------------------------- |
| **boldface** (text îngroșat) | Comenzi și keywords introduse **literal, exact cum sunt scrise** |
| _italics_ (text cursiv)      | **Argumente** pentru care **tu** furnizezi valoarea              |
| `[x]` — paranteze pătrate    | Element **opțional** (keyword sau argument)                      |
| `{x}` — acolade              | Element **obligatoriu** (keyword sau argument)                   |
| `[x {y\|z}]`                 | acolade + bară verticală în paranteze pătrate                    |

**Exemple concrete de citire a sintaxei:**

1. **`ping ip-address`**
    - `ping` = comanda (boldface, literal)
    - `ip-address` = argument (italic, tu furnizezi adresa)
    - Exemplu real: `ping 10.10.10.5`
2. **`traceroute ip-address`**
    - Similar: `traceroute` = comanda, `ip-address` = argument definit de tine
    - Exemplu real: `traceroute 192.168.254.254`
3. **`description string`**
    - `description` = comandă (folosită să identifici scopul unei interfețe)
    - `string` = argument (textul tău descriptiv)
    - Exemplu: `description Connects to the main headquarter office switch`

---
### 2.3.3 IOS Help Features

- **Context-sensitive help (`?`)** = te ajută să **descoperi** ce comenzi/opțiuni există. 
- **Command syntax check** = **validează** automat ce ai scris deja, și te anunță dacă ai greșit ceva.

---

### 2.3.4 Video - Context Sensitive Help and Command Syntax Check

## Vezi video

---

### 2.3.5 Hot Keys and Shortcuts

CLI-ul IOS oferă **hot keys și shortcuts** pentru configurare/monitorizare/troubleshooting mai ușoare.

**Concept important - abrevierea comenzilor:**

- Comenzile și keywords pot fi **scurtate la minimul de caractere** care le identifică **unic**
- Exemplu: `configure` → poți scrie `conf` (funcționează, e unic)
- **Dar** `con` **NU funcționează** — pentru că mai multe comenzi încep cu "con" (ambiguu)

#### Cele mai importante shortcuts de reținut (nu memora tot tabelul, doar esențialul):

|Tastă|Ce face|
|---|---|
|**Tab**|Completează automat o comandă parțială|
|**Ctrl+C**|Iese din orice mod de configurare → revine la Privileged EXEC|
|**Ctrl+Z**|Iese din orice mod de configurare → revine la Privileged EXEC (la fel ca `end`, deja știi asta din 2.2.4)|
|**Ctrl+Shift+6**|Break sequence universal — oprește DNS lookups, traceroute, ping etc.|
|**Up Arrow / Ctrl+P**|Recheamă comanda anterioară din istoric|
|**Down Arrow / Ctrl+N**|Merge la comanda următoare din istoric|
|**Ctrl+A**|Cursor la începutul liniei|
|**Ctrl+E**|Cursor la finalul liniei|

**Notă importantă:** tasta **Delete** nu e recunoscută de structura de comenzi IOS (deși normal șterge caracterul din dreapta cursorului) — folosește **Backspace** sau **Ctrl+D** în schimb.

#### Când output-ul e prea lung - prompt `--More--`:

| Tastă                                | Efect                                         |
| ------------------------------------ | --------------------------------------------- |
| **Enter**                            | Afișează linia următoare                      |
| **Space Bar**                        | Afișează ecranul următor                      |
| **Orice altă tastă** (excepție: `y`) | Oprește afișarea, revine la promptul anterior |

---

**Idee centrală de reținut pentru quiz (cele mai probabile de testat):**

- **Tab** = auto-completare
- **Ctrl+C / Ctrl+Z** = ieșire din config mode → Privileged EXEC
- **Ctrl+Shift+6** = break/stop pentru comenzi în desfășurare (ping, traceroute, DNS lookup)
- Comenzile pot fi **abreviate**, dar trebuie să rămână **unice** (ex: `conf` merge, `con` nu merge)

---

## 2.4 Basic Device Configuration

### 2.4.1 Device Names

Prima comandă de configurare pe orice device ar trebui să fie setarea unui **hostname** unic. Default, toate device-urile au un nume din fabrică (ex: switch-ul Cisco = "Switch").

**De ce contează:** dacă toate switch-urile rămân cu numele default, nu poți identifica device-ul corect — mai ales când te conectezi remote prin SSH, hostname-ul confirmă că ești pe device-ul corect.

**Reguli de nume (naming guidelines) - de reținut:**

- Începe cu o **literă**
- **Fără spații**
- Se termină cu literă sau cifră
- Folosește doar **litere, cifre și cratime (-)**
- **Sub 64 caractere**

```Cisco CLI
Switch# configure terminal
Switch(config)# hostname Sw-Floor-1
Sw-Floor-1(config)#
```

---
### 2.4.2 Password Guidelines

**De ce contează:** parolele slabe/ghicibile = cea mai mare problemă de securitate pentru organizații.

**Reguli pentru parole puternice:**

- Peste **8 caractere**
- Combinație de **litere mari/mici, cifre, caractere speciale**
- **Nu refolosi** aceeași parolă pe toate device-urile
- Evită **cuvinte comune** (ușor de ghicit)

**Notă importantă:** în laboratoarele acestui curs se folosesc parole simple ca **`cisco`** sau **`class`** sunt slabe intenționat, doar pentru scop didactic, **niciodată** în producție reală.

---
### 2.4.3 Configure Passwords

#### Securizarea User EXEC (acces prin consolă):

```
Sw-Floor-1# configure terminal
Sw-Floor-1(config)# line console 0
Sw-Floor-1(config-line)# password cisco
Sw-Floor-1(config-line)# login
Sw-Floor-1(config-line)# end
```

- **`line console 0`** — intri în line config pentru consolă (0 = prima/singura interfață de consolă)
- **`password cisco`** — setezi parola
- **`login`** — activezi cerința de parolă la acces

#### Securizarea Privileged EXEC (cel mai important — acces complet la device):

```
Sw-Floor-1(config)# enable secret class
```

- **`enable secret`** — comanda pentru a proteja Privileged EXEC (acces total la device)

#### Securizarea VTY lines (acces remote SSH/Telnet):

```
Sw-Floor-1(config)# line vty 0 15
Sw-Floor-1(config-line)# password cisco
Sw-Floor-1(config-line)# login
```

- **VTY** (Virtual Terminal) = liniile pentru acces remote
- Multe switch-uri Cisco suportă **până la 16 linii VTY** (numerotate **0-15**)
- **`line vty 0 15`** = configurezi toate cele 16 linii simultan

**De reținut clar (3 puncte de securizat, apar sigur la quiz):**

| Ce securizezi       | Comandă mod                | Comandă parolă       |
| ------------------- | -------------------------- | -------------------- |
| User EXEC (consolă) | `line console 0`           | `password` + `login` |
| Privileged EXEC     | (direct din global config) | `enable secret`      |
| VTY (remote acces)  | `line vty 0 15`            | `password` + `login` |

---

### 2.4.4 Encrypt Passwords

**Problema:** fișierele `startup-config` și `running-config` afișează parolele **în plaintext** — risc de securitate dacă cineva are acces la ele.

**Soluția:**

```
Sw-Floor-1(config)# service password-encryption
```

- Criptează **toate parolele necriptate** din fișierul de configurare
- **Important:** criptează parolele doar **în fișierul de config**, NU parolele trimise prin rețea (asta e treaba altor protocoale, ex SSH)
- Verifici cu **`show running-config`** — vei vedea parolele ca text criptat (ex: `7 094F471A1A0A`)

---

### 2.4.5 Banner Messages

**De ce contează:** pe lângă parole, ai nevoie de un **banner** — un mesaj legal care declară că doar personalul autorizat poate accesa device-ul. Important **legal** — în unele sisteme juridice, nu poți urmări penal un intrus dacă nu exista o notificare vizibilă.

**Comanda:**

```
Sw-Floor-1(config)# banner motd #Authorized Access Only#
```

- **`banner motd`** = "message of the day"
- **`#`** = **delimiting character** — marchează începutul și sfârșitul mesajului
- Poate fi orice caracter, atât timp cât **nu apare în mesaj**
- Banner-ul apare la **toate încercările ulterioare** de acces, până e eliminat

---
## 2.5 Save Configurations

### 2.5.1 Configuration Files

Aici e conceptul cheie al secțiunii, pe care sigur îl știi deja din experiența ta cu switch-uri/routere Cisco:
- **startup-config** - stocat în **NVRAM**, se încarcă la boot, persistă la power-off
- **running-config** - stocat în **RAM**, config-ul activ, se pierde la restart

Comenzi:
- `show running-config` - vezi config-ul curent din RAM
- `show startup-config` - vezi ce s-ar încărca la următorul boot
- `copy running-config startup-config` - salvezi running → startup (altfel modificările se pierd la reboot)

---

### 2.5.2 Alter the Running Configuration

Practic, ce faci dacă strici ceva în running-config:

- Dacă **nu ai salvat** încă: `reload` te readuce la ultimul startup-config salvat (dar dă downtime scurt, pentru că device-ul repornește; la reload, IOS te întreabă dacă vrei să salvezi schimbările — răspunzi `n`/`no` ca să le arunci)
- Dacă **ai salvat deja** greșit în startup-config: `erase startup-config` (șterge din NVRAM) → confirmi cu Enter → apoi `reload` ca să încarce config-ul default din fabrică

Diferența esențială între cele două scenarii: dacă schimbarea proastă e doar în RAM, un simplu reload te scapă; dacă a ajuns și în NVRAM, trebuie s-o ștergi explicit înainte de reload.

---

### 2.5.4 Capture Configuration to a Text File

Asta e un truc practic pentru backup manual (fără TFTP server), folosind PuTTY:

1. Deschizi PuTTY, mergi la **Session → Logging**
2. Selectezi **"All session output"**, alegi un nume de fișier (ex. `MySwitchLogs`)
3. Te conectezi (SSH/Telnet/Serial) și rulezi `show running-config` sau `show startup-config` — tot ce apare în terminal se salvează în fișierul text
4. Dezactivezi logging-ul (**Session logging → None**) când ai terminat

Pentru restaurare: intri în **global config mode** pe switch și pur și simplu copy-paste textul din fișier direct în terminal — liniile sunt interpretate ca și comenzi.

---

## 2.6 Ports and Addresses

### 2.6.1 IP Addresses

Aici e recapitulare rapidă pentru tine, cu doar câteva nuanțe de reținut din formularea CCNA:

- **IPv4**: dotted decimal, 4 octeți (0-255), plus **subnet mask** (32-bit) care separă porțiunea de rețea de cea de host
- **Default gateway**: IP-ul routerului folosit pentru trafic către rețele externe (exemplul din curs: adresă 192.168.1.10, mască 255.255.255.0, gateway 192.168.1.1 — clasic /24)
- **IPv6**: 128 biți, notație hexazecimală, grupuri de 4 cifre hex separate prin `:`, case-insensitive

### 2.6.2 Interfaces and Ports

Punctul important de reținut din secțiunea asta (poate singurul lucru care merită subliniat, restul fiind cablu-uri copper/fiber/wireless pe care le știi):

- **Switch-urile Layer 2 nu au nevoie de adresă IP** ca să funcționeze — fac forwarding pe MAC address, nu pe IP
- Totuși, pentru management la distanță (SSH/Telnet), switch-ul are o **SVI (Switch Virtual Interface)** — o interfață virtuală, fără hardware fizic asociat
- SVI-ul default "din fabrică" e **VLAN1** — asta explică de ce, atunci când configurezi IP pe un switch, intri pe `interface vlan 1` și nu pe un port fizic

---

## 2.7. Configure IP Addressing

### 2.7.1 Manual IP Address Configuration for End Devices

Doar procedura Windows: Control Panel → Network Sharing Center → Change adapter settings → click dreapta pe adaptor → Properties → Local Area Connection Properties. De acolo introduci manual IP, mască, gateway. Recapitulare pură, nimic tehnic nou.

### 2.7.2 Automatic IP Address Configuration for End Devices

- **DHCP** elimină configurarea manuală pe fiecare device (IP, mască, gateway, DNS) — reduce și riscul de duplicate de adrese
- Pe Windows: bifezi **"Obtain an IP address automatically"** + **"Obtain DNS server address automatically"**
- **Notă utilă**: pentru IPv6, echivalentul e **DHCPv6** și **SLAAC** (Stateless Address Autoconfiguration) — asta e o mențiune care poate nu ai întâlnit-o explicit până acum, chiar dacă concepte similare (autoconfigurare) probabil le știi din alte contexte

### 2.7.4 Switch Virtual Interface Configuration

Aici e configurarea practică, legată direct de 2.6.2 (SVI pe VLAN1). Secvența de comenzi:

```
Sw-Floor-1# configure terminal
Sw-Floor-1(config)# interface vlan 1
Sw-Floor-1(config-if)# ip address 192.168.1.20 255.255.255.0
Sw-Floor-1(config-if)# no shutdown
Sw-Floor-1(config-if)# exit
Sw-Floor-1(config)# ip default-gateway 192.168.1.1
```

Puncte de reținut:

- `interface vlan 1` — intri în config-ul SVI-ului (nu e interfață fizică)
- `ip address ... ...` — IP + mască pe SVI
- `no shutdown` — **obligatoriu**, altfel interfața virtuală rămâne administrativ dezactivată
- `ip default-gateway` — comandă **globală** (nu sub interfață!), necesară ca switch-ul să știe pe unde trimite trafic către alte rețele

---
## 2.8 Verify Connectivity

## Vezi videouri
