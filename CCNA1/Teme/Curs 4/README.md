
# Ghid de Configurare: Topologie Interconectare 4 LAN-uri

### Descrierea Proiectului

Acest document detaliază pașii necesari pentru configurarea unei topologii de rețea formate din 4 rețele locale (LAN-uri) interconectate printr-un router central. Configurația de nivel 2 se realizează exclusiv pe VLAN-ul implicit (VLAN 1).

---

## Tabel de Adresare IP 

| **Dispozitiv**  | **Interfață / VLAN** | **Adresă IP** | **Subnet Mask** | **Default Gateway** |
| --------------- | -------------------- | ------------- | --------------- | ------------------- |
| **Router**      | Gig0/0 (LAN1)        | 172.16.1.1    | 255.255.255.0   | N/A                 |
| **Router**      | Gig3/0 (LAN2)        | 172.16.2.1    | 255.255.255.0   | N/A                 |
| **Router**      | Gig2/0 (LAN3)        | 172.16.3.1    | 255.255.255.0   | N/A                 |
| **Router**      | Gig1/0 (LAN4)        | 172.16.4.1    | 255.255.255.0   | N/A                 |
| **SW0**         | VLAN 1               | 172.16.1.2    | 255.255.255.0   | 172.16.1.1          |
| **SW1**         | VLAN 1               | 172.16.2.2    | 255.255.255.0   | 172.16.2.1          |
| **SW3**         | VLAN 1               | 172.16.3.2    | 255.255.255.0   | 172.16.3.1          |
| **SW4**         | VLAN 1               | 172.16.4.2    | 255.255.255.0   | 172.16.4.1          |
| **PC0**         | FastEthernet0        | 172.16.1.3    | 255.255.255.0   | 172.16.1.1          |
| **PC2**         | FastEthernet0        | 172.16.2.3    | 255.255.255.0   | 172.16.2.1          |
| **PC1**         | FastEthernet0        | 172.16.3.3    | 255.255.255.0   | 172.16.3.1          |
| **Laptop**      | FastEthernet0        | 172.16.3.10   | 255.255.255.0   | 172.16.3.1          |
| **PC (LAN4)**   | FastEthernet0        | 172.16.4.3    | 255.255.255.0   | 172.16.4.1          |
| **Server TFTP** | FastEthernet0        | 172.16.4.4    | 255.255.255.0   | 172.16.4.1          |

---

# Pasul 1: Configurarea Dispozitivelor Finale (End Devices)

În această etapă, alocăm adresele IP statice pentru toate calculatoarele și pentru serverul TFTP.

- Accesați tab-ul **Desktop -> IP Configuration** pentru fiecare echipament.
- Introduceți Adresa IP, Subnet Mask-ul și Default Gateway-ul conform tabelului de adresare de mai sus.


---

# Pasul 2: Configurarea Switch-urilor (LAN cu LAN)

În această etapă, configurăm fiecare switch cu adresa IP de management (pe VLAN 1), gateway-ul implicit pentru a putea comunica în afara rețelei locale și setările de securitate obligatorii.

## 2.1 Configurarea LAN 1 (Switch0 / SW0)

Deschideți CLI-ul pe **Switch0** (situat în LAN1, partea stângă) și introduceți următoarele comenzi.

```Cisco CLI
enable
```

```Cisco CLI
configure terminal
```

### 1. Setare numelui

```Cisco CLI
hostname SW0
```

### 2. Configurarea parolei de mod privilegiat

```Cisco CLI
enable secret ccna
```

### 3. Configurarea adresei IP de management (VLAN 1)

```Cisco CLI
interface vlan 1 
ip address 172.16.1.2 255.255.255.0 
no shutdown 
exit
```

### 4. Setarea Default Gateway-ului (IP-ul viitor al interfeței Routerului pentru LAN 1)

```Cisco CLI
ip default-gateway 172.16.1.1
```

### 5. Securizarea accesului pe consola

```Cisco CLI
line console 0 
password user 
login 
exit
```

### 6. Securizarea accesului de la distanță (Telnet)

```Cisco CLI
line vty 0 15 
password cisco 
login 
transport input telnet 
exit
```

### 7. Criptarea parolelor și setarea mesajului de avertizare (Banner)

```Cisco CLI
service password-encryption 
banner motd $Authorization #2 Required$
```

### 8. Ieșire și salvarea configurației local

```Cisco CLI 
end 
write memory
```

