# CCNARSM1 - Ghid Partea 1 (IPv4) și Partea 2 (IPv6)

## Topologie
```
LAN1 (stânga): PC1, TFTP, DHCP, DNS, HTTP, EMAIL — toate pe Switch1 (SW1)
SW1 --- Gi0/0 --- Router1 --- Gi0/1 --- SW2 --- PC2 (LAN2)
```

---

# PARTEA 1 (IPv4)

## 1. Calcul x optim

Se dă: `137.45.0.0/x`
- LAN1 = 120 hosturi → nevoie 126 hosturi utilizabile → **/25**
- LAN2 = 259 hosturi → nevoie 510 hosturi utilizabile → **/23**

Suma blocurilor: 512 + 128 = 640 → rotunjit la puterea lui 2 imediat superioară = 1024

**x optim = /22**

## 2. VLSM

| Rețea | Cerință | Prefix | Subnet | Interval utilizabil | Broadcast | Mască |
|---|---|---|---|---|---|---|
| LAN2 | 259 h | /23 | 137.45.0.0/23 | 137.45.0.1 – 137.45.1.254 | 137.45.1.255 | 255.255.254.0 |
| LAN1 | 120 h | /25 | 137.45.2.0/25 | 137.45.2.1 – 137.45.2.126 | 137.45.2.127 | 255.255.255.128 |

## 3. Alocare adrese IPv4

### LAN1 (137.45.2.0/25)
| Echipament | IP | Mască | Gateway |
|---|---|---|---|
| PC1 | 137.45.2.1 | 255.255.255.128 | 137.45.2.126 |
| TFTP | 137.45.2.2 | 255.255.255.128 | 137.45.2.126 |
| DHCP | 137.45.2.3 | 255.255.255.128 | 137.45.2.126 |
| DNS | 137.45.2.4 | 255.255.255.128 | 137.45.2.126 |
| HTTP | 137.45.2.5 | 255.255.255.128 | 137.45.2.126 |
| EMAIL | 137.45.2.6 | 255.255.255.128 | 137.45.2.126 |
| SVI SW1 | 137.45.2.125 | 255.255.255.128 | - |
| R1 Gi0/0 (DGW) | 137.45.2.126 | 255.255.255.128 | - |

### LAN2 (137.45.0.0/23)
| Echipament | IP | Mască | Gateway |
|---|---|---|---|
| PC2 | 137.45.0.1 | 255.255.254.0 | 137.45.1.254 |
| SVI SW2 | 137.45.1.253 | 255.255.254.0 | - |
| R1 Gi0/1 (DGW) | 137.45.1.254 | 255.255.254.0 | - |

## 4. Comenzi Router R1

```
enable
configure terminal
interface GigabitEthernet0/0
 ip address 137.45.2.126 255.255.255.128
 no shutdown
 description LAN1
exit
interface GigabitEthernet0/1
 ip address 137.45.1.254 255.255.254.0
 no shutdown
 description LAN2
exit
end
write memory
```

## 5. Comenzi Switch1 (SVI LAN1)

```
enable
configure terminal
interface vlan 1
 ip address 137.45.2.125 255.255.255.128
 no shutdown
exit
ip default-gateway 137.45.2.126
end
write memory
```

## 6. Comenzi Switch2 (SVI LAN2)

```
enable
configure terminal
interface vlan 1
 ip address 137.45.1.253 255.255.254.0
 no shutdown
exit
ip default-gateway 137.45.1.254
end
write memory
```

## 7. Configurare PC-uri (Desktop > IP Configuration)

- **PC1**: IP 137.45.2.1 / 255.255.255.128 / GW 137.45.2.126 (DNS 137.45.2.4 opțional)
- **PC2**: IP 137.45.0.1 / 255.255.254.0 / GW 137.45.1.254

## 8. Verificare conectivitate

```
show ip interface brief
show ip route
ping 137.45.2.1
ping 137.45.0.1
```

## 9. Tabel ping PC1 → PC2 (de completat manual)

Reguli:
- **Src/Dest IPv4** rămân **neschimbate** pe tot traseul: 137.45.2.1 → 137.45.0.1
- **Src/Dest MAC** se schimbă la fiecare salt Layer 3 (router face MAC rewrite pe fiecare interfață)
- Pe switch-uri, MAC-urile sunt identice cu echipamentele conectate (switch nu modifică nimic)

Comenzi utile pentru completare:
```
! pe PC1
arp -a
! pe switch
show mac address-table
! pe router
show interfaces gigabitEthernet 0/0
show interfaces gigabitEthernet 0/1
```

---

# PARTEA 2 (IPv6)

## 1. Subnetting

Se dă: `2001:db2:abcd::/48` → subnete /64 per LAN

| Rețea | Subnet |
|---|---|
| LAN1 | 2001:db2:abcd:1::/64 |
| LAN2 | 2001:db2:abcd:2::/64 |

## 2. Alocare adrese IPv6

| Echipament | Global-unicast | Link-local |
|---|---|---|
| SVI SW1 | eui-64 (auto, pe 2001:db2:abcd:1::/64) | auto |
| R1 Gi0/0 | eui-64 (auto, pe 2001:db2:abcd:1::/64) | auto |
| PC1 | 2001:db2:abcd:1::3/64 (**manual**) | auto |
| Servere LAN1 | la alegere (ex. ::10, ::11...) | auto |
| SVI SW2 | 2001:db2:abcd:2::2/64 (**manual**) | FE80::2 (**manual**) |
| R1 Gi0/1 | 2001:db2:abcd:2::1/64 (**manual**) | FE80::1 (**manual**) |
| PC2 | SLAAC (Automatic) | auto |

⚠️ **Important**: acolo unde cerința zice "eui-64" → pui doar prefixul + eui-64.
Acolo unde zice "prima/a doua/a treia adresă de gazdă" → calculezi și scrii manual adresa completă.

## 3. IMPORTANT — pași obligatorii înainte de configurare

### a) Pe Router — activează rutarea IPv6 (o singură dată, global)
```
enable
configure terminal
ipv6 unicast-routing
end
write memory
```
Fără această comandă, router-ul **nu rutează deloc** trafic IPv6 între interfețe, chiar dacă adresele sunt corect configurate!

### b) Pe fiecare Switch — schimbă șablonul SDM la dual-stack (o singură dată)
```
enable
configure terminal
sdm prefer dual-ipv4-and-ipv6 default
end
write memory
reload
```
- Fă `write memory` **înainte** de reload ca să nu pierzi configurația IPv4 deja făcută (Partea 1)!
- Confirmă reload-ul când te întreabă switch-ul
- Verifică după reload cu: `show sdm prefer`

## 4. Comenzi Router R1 (interfețe)

```
enable
configure terminal
interface GigabitEthernet0/0
 ipv6 address 2001:db2:abcd:1::/64 eui-64
exit
interface GigabitEthernet0/1
 ipv6 address 2001:db2:abcd:2::1/64
 ipv6 address FE80::1 link-local
exit
end
write memory
```

## 5. Comenzi Switch1 (SVI LAN1)

```
enable
configure terminal
interface vlan 1
 ipv6 address 2001:db2:abcd:1::/64 eui-64
 no shutdown
exit
end
write memory
```

## 6. Comenzi Switch2 (SVI LAN2)

```
enable
configure terminal
interface vlan 1
 ipv6 address 2001:db2:abcd:2::2/64
 ipv6 address FE80::2 link-local
 no shutdown
exit
end
write memory
```

## 7. Aflarea adresei eui-64 a router-ului (necesară ca gateway pe PC1 și servere LAN1)

```
show ipv6 interface brief
```
Notează adresa globală de pe Gi0/0 (ceva de forma `2001:DB2:ABCD:1:XXXX:XXXX:XXXX:XXXX`).

## 8. Configurare PC1 (Desktop > IP Configuration > IPv6 Static)

- **IPv6 Address**: `2001:db2:abcd:1::3` / prefix `64`
- **Default Gateway**: adresa eui-64 a lui R1 Gi0/0 (obținută la pasul 7)

⚠️ **Cea mai frecventă greșeală**: dacă lași câmpul Default Gateway gol (`::`), pingurile către alte rețele/echipamente vor da mereu "Request timed out", chiar dacă adresa IPv6 e corectă! Completează-l mereu manual.

## 9. Configurare PC2 (Desktop > IP Configuration)

- Bifează **Automatic** la IPv6 Configuration (SLAAC)
- Necesită ca `ipv6 unicast-routing` să fie deja activ pe router (pasul 3a) ca să primească Router Advertisements

## 10. Configurare servere LAN1 (la alegere conform cerinței g)

Ex. TFTP → `2001:db2:abcd:1::10/64`, Gateway = adresa eui-64 a R1 Gi0/0 (pasul 7)
La fel pentru DHCP, DNS, HTTP, EMAIL — schimbi doar ultimul octet (::11, ::12...)

Pot fi și pe Automatic, dar verifică mereu cu `ipconfig` dacă Default Gateway IPv6 s-a completat — Packet Tracer are un bug cunoscut unde uneori rămâne gol chiar și pe Automatic.

## 11. Verificare conectivitate

```
! pe R1
show ipv6 interface brief
show ipv6 route
ping 2001:db2:abcd:1::3      ! spre PC1
ping 2001:db2:abcd:2::2      ! spre SVI SW2
ping 2001:db2:abcd:2::1      ! spre propriul Gi0/1 (sanity check)
```

```
! pe PC1 sau PC2
ping 2001:db2:abcd:1::3
ping 2001:db2:abcd:2::2
ping <adresa completă SLAAC a celuilalt PC, obținută din ipconfig>
```

## 12. Afișare adrese / tabelă rutare / config interfețe (cerința c)

```
show ipv6 interface brief
show ipv6 route
show running-config interface GigabitEthernet0/0
show running-config interface GigabitEthernet0/1
```

---

# Checklist rapid de depanare IPv6

| Simptom | Cauză probabilă | Soluție |
|---|---|---|
| Ping între LAN1↔LAN2 pică complet, dar în LAN e ok | Lipsește `ipv6 unicast-routing` pe router | Adaugă comanda global pe R1 |
| `ipv6 address` nu se aplică pe SVI switch | SDM nu e pe dual-stack | `sdm prefer dual-ipv4-and-ipv6 default` + `write memory` + `reload` |
| Ping de la un PC către alte rețele dă mereu timeout, dar PC-ul are IPv6 corect | Default Gateway IPv6 gol (`::`) | Completează manual gateway-ul (adresa eui-64/link-local a router-ului) |
| SLAAC nu generează adresă pe PC2/servere | `ipv6 unicast-routing` lipsă pe router, sau interfața router spre acea rețea nu are IPv6 configurat | Verifică pasul 3a și pasul 4 |