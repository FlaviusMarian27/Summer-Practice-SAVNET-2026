# Lab Networking — IPv4, IPv6 & Securitate

Documentație completă pentru laboratorul cu topologia: 2x switch de acces (SW-ACCESS1, SW-ACCESS2), 2x router de graniță (Border1, Border2), 5 servere (DHCP, EMAIL, TFTP, DNS, HTTP) în LAN1, 3 PC-uri (PC1 în LAN1, PC2/PC3 în LAN2).

---

## Partea 1 — IPv4 (3.5 puncte)

### 1. Aflarea lui x optim

Se dă `172.16.0.0/x` cu cerințele: LAN1 = 63 hosturi, LAN2 = 25 hosturi, WAN = 2 hosturi.

| Rețea | Hosturi cerute | Biți host necesari | Hosturi disponibile | Mască |
|---|---|---|---|---|
| LAN1 | 63 | 7 | 126 | /25 |
| LAN2 | 25 | 5 | 30 | /27 |
| WAN | 2 | 2 | 2 | /30 |

Total adrese necesare: 128 + 32 + 4 = 164 → cel mai mic bloc putere-a-lui-2 care încape toate rețelele = **256 adrese = /24**.

**x = 24** → rețeaua de bază: `172.16.0.0/24`

### 2. Subnetting VLSM (de la cea mai mare la cea mai mică rețea)

| Rețea | Adresă subrețea | Mască | Interval uzabil | Broadcast |
|---|---|---|---|---|
| LAN1 (63 host) | 172.16.0.0 | /25 (255.255.255.128) | .1 – .126 | .127 |
| LAN2 (25 host) | 172.16.0.128 | /27 (255.255.255.224) | .129 – .158 | .159 |
| WAN (2 host) | 172.16.0.160 | /30 (255.255.255.252) | .161 – .162 | .163 |

### 3. Asignarea adreselor IPv4

**LAN1 (172.16.0.0/25):**

| Echipament | Adresă |
|---|---|
| PC1 | 172.16.0.1 |
| DHCP server | 172.16.0.2 |
| EMAIL server | 172.16.0.3 |
| TFTP server | 172.16.0.4 |
| DNS server | 172.16.0.5 |
| HTTP server | 172.16.0.6 |
| Border1 G0/0 | 172.16.0.126 |
| SW-ACCESS1 SVI | 172.16.0.125 |

**LAN2 (172.16.0.128/27):**

| Echipament | Adresă |
|---|---|
| PC2 | 172.16.0.129 |
| PC3 | 172.16.0.130 |
| Border2 G0/0 | 172.16.0.158 |
| SW-ACCESS2 SVI | 172.16.0.157 |

**WAN (172.16.0.160/30):**

| Echipament | Adresă |
|---|---|
| Border1 G0/1 | 172.16.0.161 |
| Border2 G0/1 | 172.16.0.162 |

### 4. Configurare servicii pe servere

- **DHCP**: pool cu network 172.16.0.0/255.255.255.128, gateway 172.16.0.126, DNS 172.16.0.5
- **EMAIL**: activare SMTP + POP3
- **TFTP**: activare serviciu TFTP
- **HTTP**: activare serviciu HTTP
- **DNS**: activare serviciu, apoi record A cu Name = `savnet.com`, Address = **172.16.0.6** (adresa serverului HTTP — nu a serverului DNS!) → nu uita să apeși **Add** ca recordul să fie salvat în listă, nu doar completat în formular.

### 5. Configurare switch-uri (IPv4)

**SW-ACCESS1:**
```
enable
configure terminal
hostname SW-ACCESS1
interface vlan 1
 ip address 172.16.0.125 255.255.255.128
 no shutdown
exit
ip default-gateway 172.16.0.126
end
write memory
```

**SW-ACCESS2:**
```
enable
configure terminal
hostname SW-ACCESS2
interface vlan 1
 ip address 172.16.0.157 255.255.255.224
 no shutdown
exit
ip default-gateway 172.16.0.158
end
write memory
```

### 6. Configurare routere (IPv4 + rută statică)

**Border1:**
```
enable
configure terminal
hostname Border1
interface gigabitEthernet 0/0
 ip address 172.16.0.126 255.255.255.128
 no shutdown
exit
interface gigabitEthernet 0/1
 ip address 172.16.0.161 255.255.255.252
 no shutdown
exit
ip route 172.16.0.128 255.255.255.224 172.16.0.162
end
write memory
```

**Border2:**
```
enable
configure terminal
hostname Border2
interface gigabitEthernet 0/0
 ip address 172.16.0.158 255.255.255.224
 no shutdown
exit
interface gigabitEthernet 0/1
 ip address 172.16.0.162 255.255.255.252
 no shutdown
exit
ip route 172.16.0.0 255.255.255.128 172.16.0.161
end
write memory
```

> **Notă:** rutele statice folosesc masca exactă a rețelei țintă (nu o rută default), conform cerinței "folosiți cea mai specifică rută posibilă, default route-ul nu se acceptă".

### 7. Verificare conectivitate IPv4

Ping între orice echipament — de verificat în special traversarea LAN1 ↔ LAN2 prin ambele routere. Primele pachete pot da timeout din cauza rezolvării ARP, e normal; ce contează e ca replicile ulterioare să vină curat.

---

## Partea 2 — IPv6 (3.5 puncte)

### 1. Subnetare conform topologiei

Se dă `2000:ABC:DEF::/48`, subnetat pe /64 conform notațiilor din topologie:

| Rețea | Prefix |
|---|---|
| LAN1 | 2000:ABC:DEF:A::/64 |
| WAN (Border1–Border2) | 2000:ABC:DEF:1::/64 |
| LAN2 | 2000:ABC:DEF:B::/64 |

### 2. Pregătire switch-uri pentru IPv6 (SDM)

Switch-urile 3560 folosesc implicit un template SDM optimizat doar pentru IPv4. Pentru rutare/adresare IPv6 corectă e nevoie de template dual-stack, care necesită reload:

```
enable
configure terminal
sdm prefer dual-ipv4-and-ipv6 default
end
write memory
reload
```

Verificare după reload:
```
show sdm prefer
```
→ trebuie să arate `desktop IPv4 and IPv6 default` (sau echivalent).

### 3. Adresare IPv6 — SW-ACCESS1

```
enable
configure terminal
ipv6 unicast-routing
interface vlan 1
 ipv6 address 2000:ABC:DEF:A::/64 eui-64
 no shutdown
exit
end
write memory
```

Rută default (next-hop = **GUA** al lui Border1, nu link-local — sintaxa `ipv6 route ::/0 Vlan1 FE80::1` a dat "Invalid input" pe acest IOS din Packet Tracer):
```
configure terminal
ipv6 route ::/0 2000:ABC:DEF:A::1
end
write memory
```

### 4. Adresare IPv6 — SW-ACCESS2

```
enable
configure terminal
ipv6 unicast-routing
interface vlan 1
 ipv6 address FE80::2 link-local
 ipv6 address 2000:ABC:DEF:B::9/64
 no shutdown
exit
ipv6 route ::/0 2000:ABC:DEF:B::1
end
write memory
```

### 5. Adresare IPv6 — Border1

```
enable
configure terminal
ipv6 unicast-routing
interface gigabitEthernet 0/0
 ipv6 address FE80::1 link-local
 ipv6 address 2000:ABC:DEF:A::1/64
 no shutdown
exit
interface gigabitEthernet 0/1
 ipv6 address 2000:ABC:DEF:1::1/64
 no shutdown
exit
ipv6 route ::/0 2000:ABC:DEF:1::2
end
write memory
```

### 6. Adresare IPv6 — Border2

```
enable
configure terminal
ipv6 unicast-routing
interface gigabitEthernet 0/0
 ipv6 address FE80::1 link-local
 ipv6 address 2000:ABC:DEF:B::1/64
 no shutdown
exit
interface gigabitEthernet 0/1
 ipv6 address 2000:ABC:DEF:1::2/64
 no shutdown
exit
ipv6 route ::/0 2000:ABC:DEF:1::1
end
write memory
```

> **De ce FE80::1 pe ambele routere?** Fiecare LAN are propriul gateway local. Adresele link-local sunt valabile doar per-link (nu sunt globale), deci FE80::1 pe G0/0 al lui Border1 (spre LAN1) și FE80::1 pe G0/0 al lui Border2 (spre LAN2) nu se ciocnesc — sunt rețele separate.

### 7. Adresare end-devices

| Echipament | Adresă | Prefix | Gateway |
|---|---|---|---|
| PC1 | 2000:ABC:DEF:A::3 (a 3-a adresă) | /64 | FE80::1 |
| DHCP server | 2000:ABC:DEF:A::4 (a 4-a adresă) | /64 | FE80::1 |
| EMAIL server | 2000:ABC:DEF:A::5 | /64 | FE80::1 |
| TFTP server | 2000:ABC:DEF:A::6 | /64 | FE80::1 |
| DNS server | 2000:ABC:DEF:A::7 | /64 | FE80::1 |
| HTTP server | 2000:ABC:DEF:A::8 | /64 | FE80::1 |
| PC2 | **SLAAC** (Automatic) | — | primit automat prin RA |
| PC3 | 2000:ABC:DEF:B::3 | /64 | FE80::1 |

> Pentru ca SLAAC să funcționeze pe PC2, Border2 trebuie să trimită Router Advertisements — se întâmplă automat cu `ipv6 unicast-routing` activ și interfața G0/0 up.

### 8. Verificare conectivitate IPv6

Comenzi utile de debug dacă o rută statică pare să nu funcționeze:
```
show ipv6 route
show ipv6 interface brief
```

Simptom tipic al unei rute lipsă: `Reply from <adresa proprie a routerului>: Destination host unreachable` — înseamnă că routerul primește pachetul dar nu are unde să-l trimită mai departe (ruta default nu s-a salvat).

---

## Partea 3 — Securitate (1 punct)

### SW-ACCESS1 (0.3p)

```
enable
configure terminal
hostname SW-ACCESS1
service password-encryption
enable secret cisco
banner motd $Proprietate Savnet$
line vty 0 15
 password cisco
 login
 transport input telnet
exit
end
write memory
```

### Border2 (0.3p)

```
enable
configure terminal
hostname Border2
service password-encryption
enable secret cisco
banner motd $Proprietate Savnet$
ip domain-name savnet.local
crypto key generate rsa general-keys modulus 1024
username cisco password cisco
line vty 0 15
 login local
 transport input ssh
exit
login block-for 180 attempts 4 within 120
end
write memory
```

**Explicație parametri:**
- `ip domain-name` trebuie setat **înainte** de generarea cheilor RSA (prerechizit obligatoriu pentru SSH)
- `crypto key generate rsa general-keys modulus 1024` — pe unele IOS-uri din Packet Tracer, `general-keys` e obligatoriu în sintaxă (varianta scurtă `crypto key generate rsa modulus 1024` dă "Invalid input")
- `login block-for 180 attempts 4 within 120` = blochează accesul timp de **3 minute** (180s) dacă s-au încercat **4 accesări eșuate în 2 minute** (120s)

### Testare SSH

De pe un PC cu conectivitate spre Border2:
```
ssh -l cisco 172.16.0.158
```
→ va cere parola (`cisco`), va afișa banner-ul "Proprietate Savnet" și va intra în modul user (`Border2>`).

---

## Checklist final

- [ ] x optim calculat corect (/24)
- [ ] VLSM aplicat fără risipă de adrese
- [ ] Toate adresele IPv4 asignate conform cerinței
- [ ] DHCP, EMAIL, TFTP, HTTP, DNS pornite și configurate corect
- [ ] Record DNS A pentru savnet.com → 172.16.0.6, salvat cu Add
- [ ] Rute statice IPv4 (nu default) pe Border1 și Border2
- [ ] Ping IPv4 funcțional între orice echipamente
- [ ] SDM dual-stack aplicat + reload pe ambele switch-uri
- [ ] Adresare IPv6 completă (EUI-64, manual, SLAAC conform cerinței)
- [ ] Rute default IPv6 pe routere (GUA) și switch-uri
- [ ] Ping IPv6 funcțional între orice echipamente
- [ ] SW-ACCESS1: hostname, criptare, banner, telnet VTY
- [ ] Border2: hostname, criptare, banner, SSH, block-for
- [ ] Test SSH reușit către Border2
