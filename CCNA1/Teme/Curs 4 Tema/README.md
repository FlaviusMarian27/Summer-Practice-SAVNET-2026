
# 1. End Devices (Dispozitivele finale)

Acestea se configurează din interfața grafică (GUI) în Packet Tracer, la tab-ul **Desktop -> IP Configuration**:

- **PC1 (LAN 1):**
    - IP Address: `192.168.1.3`
    - Subnet Mask: `255.255.255.0`
    - Default Gateway: `192.168.1.1` (Interfața routerului)
        
- **Server-PT SV1 (LAN 2):**
    - IP Address: `192.168.2.3`
    - Subnet Mask: `255.255.255.0`
    - Default Gateway: `192.168.2.1` (Interfața routerului)

---
# 2. Configurare switch-ul

## 2. Configurarea Switch-ului 1 (SW1)

Deschide CLI-ul pe **SW1** și introdu următoarele comenzi. Acestea rezolvă IP-ul de management, gateway-ul și absolut toate cerințele de securitate de la punctul 3 (a, b, c, d, e, f).

```Cisco CLI
enable
configure terminal

! 3.a Hostname
hostname SW1

! 3.b Parola de trecere din user in privilegiat
enable secret ccna

! 3.c Parola pe linia de consola
line console 0
password user
login
exit

! 3.f Telnet
line vty 0 4
password cisco
login
transport input telnet
exit

! 3.d Criptarea parolelor si 3.e Banner
service password-encryption
banner motd $Acces restrictionat!$

! Cerința 1: IP pe device (Management)
interface vlan 1
ip address 192.168.1.2 255.255.255.0
no shutdown
exit

! Setare Default Gateway pentru ca switch-ul sa poata raspunde la ping din alta retea
ip default-gateway 192.168.1.1

end
write memory
```

## 3. Configurarea Switch-ului 2 (SW2)

Procedura este identică, doar adresele și numele diferă:

```Cisco CLI
enable
configure terminal
hostname SW2
enable secret ccna
line console 0
password user
login
exit
line vty 0 4
password cisco
login
transport input telnet
exit
service password-encryption
banner motd $Acces restrictionat!$

interface vlan 1
ip address 192.168.2.2 255.255.255.0
no shutdown
exit
ip default-gateway 192.168.2.1

end
write memory
```


# 4. Configurarea Routerului (R1)

Pentru router bifăm din nou cerințele de securitate și configurăm cele două interfețe GigabitEthernet (Gig0/0 spre LAN 1 și Gig0/1 spre LAN 2).

```Cisco CLI
enable
configure terminal
hostname R1
enable secret ccna
line console 0
password user
login
exit
line vty 0 4
password cisco
login
transport input telnet
exit
service password-encryption
banner motd $Acces restrictionat!$

! Configurare interfață spre LAN 1
interface GigabitEthernet0/0
ip address 192.168.1.1 255.255.255.0
no shutdown
exit

! Configurare interfață spre LAN 2
interface GigabitEthernet0/1
ip address 192.168.2.1 255.255.255.0
no shutdown
exit

end
write memory
```


# Cerința Bonus (Pentru Olimpici): Salvare config pe server prin TFTP

Deoarece ai setat corect _Default Gateway-ul_ pe toate echipamentele și routerul face _Inter-VLAN Routing_, echipamentele din LAN 1 pot acum comunica cu serverul din LAN 2 (`192.168.2.3`).

Pentru a lua punctajul maxim, du-te în modul privilegiat (pe R1, SW1 și SW2) și rulează comanda de backup:

```Cisco CLI
copy running-config tftp
```

Când ești întrebat:

1. **Address or name of remote host []?** -> Introdu `192.168.2.3` (IP-ul Serverului)
2. **Destination filename [...]?** -> Apasă **Enter** pentru a confirma numele implicit.