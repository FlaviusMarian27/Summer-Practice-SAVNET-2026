# 🌐 Configurare și Verificare Topologie Multi-LAN cu Server Web în Cisco Packet Tracer

Acest proiect reprezintă un ghid complet pentru configurarea, validarea și testarea unei rețele end-to-end. Topologia este compusă din două subrețele (LAN-uri) interconectate printr-un router, incluzând managementul switch-urilor și un Server Web funcțional pentru testarea nivelului de aplicație (Layer 7).

---

## 🏗️ Structura Topologiei

Rețeaua este împărțită în două domenii de broadcast, rutate prin echipamentul **R1**:

- **LAN 1 (Rețeaua Clienților)**
    - **Subrețea:** `192.168.1.0/25` (Subnet Mask: `255.255.255.128`)
    - **Gateway (R1 - Gi0/0):** `192.168.1.1`
    - **Switch-uri:** SW0 (`192.168.1.2`), SW1 (`192.168.1.3`)
    - **Echipamente finale:** PC-uri client (ex: terminalul `webterm`).
- **LAN 2 (Rețeaua Serverelor)**
    - **Subrețea:** `172.16.0.0/24` (Subnet Mask: `255.255.255.0`)
    - **Gateway (R1 - Gi0/1):** `172.16.0.1`
    - **Switch-uri:** SW2 (`172.16.0.2`), SW4 (`172.16.0.3`)
    - **Server Web (Server0):** `172.16.0.10`

---

## ⚙️ Pași Esențiali de Configurare

### 1. Configurarea Router-ului (R1)

Router-ul are rolul de a interconecta cele două LAN-uri. Trebuie configurate și activate interfețele care deservesc fiecare rețea.

```cisco
R1> enable
R1# configure terminal

! Configurarea interfeței pentru LAN 1
R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip address 192.168.1.1 255.255.255.128
R1(config-if)# no shutdown
R1(config-if)# exit

! Configurarea interfeței pentru LAN 2
R1(config)# interface GigabitEthernet0/1
R1(config-if)# ip address 172.16.0.1 255.255.255.0
R1(config-if)# no shutdown
R1(config-if)# end
```

### 2. Configurarea Switch-urilor (Exemplu pentru SW0)

Pentru a putea administra switch-urile de la distanță (ex: prin Telnet/SSH) sau pentru a le testa prin ping, acestea au nevoie de o adresă IP pe interfața virtuală (VLAN 1) și de o rută implicită (Default Gateway).

```cisco
SW0> enable
SW0# configure terminal

! Configurarea adresei IP de management
SW0(config)# interface vlan 1
SW0(config-if)# ip address 192.168.1.2 255.255.255.128
SW0(config-if)# no shutdown
SW0(config-if)# exit

! Configurarea gateway-ului (către router)
SW0(config)# ip default-gateway 192.168.1.1
SW0(config)# end
```

> **Notă:** Aceeași logică se aplică și pentru restul switch-urilor, adaptând adresa IP și gateway-ul în funcție de rețeaua în care se află.

### 3. Configurarea Echipamentelor Finale (PC-uri și Server)

Setările se fac din interfața grafică a dispozitivelor (tab-ul **Desktop → IP Configuration**):

- **Adresă IP:** Din plaja subrețelei respective (ex: `172.16.0.10` pentru Server0).
- **Subnet Mask:** Aferent rețelei (`255.255.255.0` pentru LAN 2).
- **Default Gateway:** Adresa interfeței de router corespunzătoare acelui LAN (ex: `172.16.0.1`).

---

## 🚀 Ghid de Verificare și Diagnoză

Validarea funcționării rețelei se face de la baza stivei OSI până la nivelul superior:

### A. Nivelul 1 și 2 (Fizic și Legătură de Date)

**Starea interfețelor:** Verifică dacă porturile au negociat corect viteza și duplexul.

```cisco
show interfaces status
```

_(Se așteaptă status `connected`, duplex `a-full`)_

**Tabela MAC:** Confirmă că switch-ul învață corect adresele fizice ale dispozitivelor.

```cisco
show mac address-table
```

### B. Nivelul 3 (Rețea - ICMP)

Testarea conectivității de bază folosind comanda `ping` din Command Prompt:

- `ping 172.16.0.1` — Testare conectivitate către Gateway
- `ping 172.16.0.10` — Testare comunicare end-to-end între un PC din LAN 1 și Serverul din LAN 2

### C. Nivelul 7 (Aplicație - HTTP)

Acesta confirmă că rutele, adresele IP și serviciile sunt complet operaționale.

1. Se deschide un PC (ex: `webterm`), se accesează **Web Browser**.
2. Se introduce adresa: `http://172.16.0.10`.
3. **Succes:** Pagina web personalizată se încarcă fără erori.

---

## 💻 Sursă Pagină Web Personalizată (HTML/CSS)

Pentru implementarea interfeței web pe Server0, s-a utilizat următorul cod. Acesta trebuie inserat în tab-ul **Services → HTTP → index.html**:

```html
<html>
<head>
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #e9ecef;
        color: #333;
        text-align: center;
        margin-top: 40px;
    }
    .container {
        background-color: #ffffff;
        border-top: 6px solid #0056b3;
        border-radius: 8px;
        padding: 30px;
        width: 75%;
        margin: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    h1 {
        color: #0056b3;
        margin-bottom: 5px;
    }
    h2 {
        color: #28a745;
        margin-top: 0;
        font-size: 22px;
    }
    p {
        font-size: 16px;
        line-height: 1.6;
    }
    hr {
        border: 0;
        height: 1px;
        background: #ddd;
        margin: 20px 0;
    }
    .links {
        text-align: left;
        display: inline-block;
        background-color: #f8f9fa;
        padding: 15px 30px;
        border-radius: 5px;
        border: 1px solid #e2e6ea;
    }
    a {
        color: #007bff;
        text-decoration: none;
        font-weight: bold;
    }
    a:hover {
        text-decoration: underline;
        color: #0056b3;
    }
</style>
</head>
<body>
    <div class="container">
        <h1>Laborator de Rețelistică</h1>
        <h2>Conexiune realizată cu succes!</h2>
        <p>Felicitări! Dacă poți citi acest mesaj de pe <b>webterm</b>, înseamnă că ai configurat corect rutele, adresele IP și gateway-urile, iar echipamentele comunică perfect între cele două LAN-uri.</p>
        <hr>
        <p><strong>Link-uri de test predefinite:</strong></p>
        <div class="links">
            <p><a href='helloworld.html'>O pagină simplă (Hello World)</a></p>
            <p>©️ <a href='copyrights.html'>Drepturi de autor (Copyrights)</a></p>
            <p><a href='image.html'>Pagină cu imagine demonstrativă</a></p>
            <p><a href='cscoptlogo177x111.jpg'>Afișează imaginea direct</a></p>
        </div>
    </div>
</body>
</html>
```

---

## 💾 Salvarea Configurațiilor

Pentru a preveni pierderea setărilor la repornirea echipamentelor, este obligatorie salvarea configurației din memoria RAM (`running-config`) în NVRAM (`startup-config`).

Executați următoarea comandă în modul privilegiat (`#`) pe toate routerele și switch-urile din rețea:

```cisco
copy running-config startup-config
```

_(Alternativ, se poate folosi comanda prescurtată: `write memory` sau `wr`)_
