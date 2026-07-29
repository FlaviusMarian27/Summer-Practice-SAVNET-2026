# Configurare Rețea IPv6 Cap-la-Cap în Cisco Packet Tracer

Acest ghid detaliază pașii necesari pentru configurarea unei rețele IPv6 complet funcționale în Cisco Packet Tracer, incluzând alocare dinamică (SLAAC), adresare statică, rutare statică între routere și configurarea switch-urilor de Layer 2 pentru management de la distanță.

## Topologia Rețelei

Rețeaua este formată din două LAN-uri conectate printr-o legătură Point-to-Point (WAN) între două routere:

| Segment | Prefix |
|---|---|
| LAN Stânga (SLAAC) | `2001:cafe:db8:1::/64` |
| LAN Dreapta (Manual/Static) | `2001:cafe:db8:2::/64` |
| Legătură WAN (Router 0 - Router 1) | `2001:cafe:db8:3::/64` |

## Pasul 1: Configurarea Routerelor

Ambele routere trebuie să aibă rutarea IPv6 activată și rute statice configurate pentru a „vedea” rețeaua cealaltă.

> **Notă:** Înlocuiți `[Interfața LAN]` și `[Interfața WAN]` cu interfețele reale din Packet Tracer, de ex: `g0/0`, `g0/1`.

### Router 0 (LAN Stânga)

```
enable
configure terminal
! Activare rutare IPv6
ipv6 unicast-routing

! Configurare interfață LAN
interface [Interfața LAN]
 ipv6 address 2001:cafe:db8:1::1/64
 no shutdown
 exit

! Configurare interfață WAN (către Router 1)
interface [Interfața WAN]
 ipv6 address 2001:cafe:db8:3::1/64
 no shutdown
 exit

! Rută statică spre LAN-ul din dreapta
ipv6 route 2001:cafe:db8:2::/64 2001:cafe:db8:3::2
```

### Router 1 (LAN Dreapta)

```
enable
configure terminal
! Activare rutare IPv6
ipv6 unicast-routing

! Configurare interfață LAN
interface [Interfața LAN]
 ipv6 address 2001:cafe:db8:2::1/64
 no shutdown
 exit

! Configurare interfață WAN (către Router 0)
interface [Interfața WAN]
 ipv6 address 2001:cafe:db8:3::2/64
 no shutdown
 exit

! Rută statică spre LAN-ul din stânga
ipv6 route 2001:cafe:db8:1::/64 2001:cafe:db8:3::1
```

## Pasul 2: Configurarea Switch-urilor (Management IPv6)

Pentru ca switch-urile (ex: Cisco 2960) să suporte IPv6, trebuie modificată alocarea memoriei SDM. De asemenea, pentru a răspunde la ping-uri din alte rețele, necesită o rută implicită.

### Switch 0 (LAN Stânga)

```
enable
configure terminal
! Activare suport IPv6 pe Switch
sdm prefer dual-ipv4-and-ipv6 default
end
! Necesită repornire pentru aplicarea setărilor SDM
reload

! DUPĂ REPORNIRE:
enable
configure terminal
interface vlan 1
 ! O adresă aleatoare din rețeaua locală pentru management
 ipv6 address 2001:cafe:db8:1::2/64
 no shutdown
 exit

! Rută implicită către Router 0 (Gateway)
ipv6 route ::/0 2001:cafe:db8:1::1
```

### Switch 1 (LAN Dreapta)

```
enable
configure terminal
sdm prefer dual-ipv4-and-ipv6 default
end
reload

! DUPĂ REPORNIRE:
enable
configure terminal
interface vlan 1
 ipv6 address 2001:cafe:db8:2::2/64
 no shutdown
 exit

! Rută implicită către Router 1 (Gateway)
ipv6 route ::/0 2001:cafe:db8:2::1
```

## Pasul 3: Configurarea Dispozitivelor Finale (End Devices)

### Dispozitive din LAN Stânga (SLAAC)

Pentru calculatoarele din stânga, adresa este generată automat pe baza prefixului oferit de router.

1. Deschideți PC-ul/Laptopul → tab-ul **Desktop** → **IP Configuration**.
2. La secțiunea **IPv6 Configuration**, bifați opțiunea **Automatic**.
3. Dispozitivul va primi automat o adresă din clasa `2001:cafe:db8:1::/64` și gateway-ul corect.

### Dispozitive din LAN Dreapta (Static)

Pentru calculatoarele din dreapta, adresele se introduc manual.
Mergeți la **Desktop → IP Configuration** → bifați **Static** și introduceți:

| Dispozitiv | IPv6 Address | Prefix | IPv6 Gateway |
|---|---|---|---|
| Laptop0 | `2001:cafe:db8:2::10` | 64 | `2001:cafe:db8:2::1` |
| Laptop1 | `2001:cafe:db8:2::11` | 64 | `2001:cafe:db8:2::1` |
| PC2 | `2001:cafe:db8:2::12` | 64 | `2001:cafe:db8:2::1` |

## Pasul 4: Verificare și Testare

Pentru a verifica funcționalitatea end-to-end (Cap-la-Cap), se deschide Command Prompt de pe un calculator din LAN Stânga și se rulează:

**Ping către un dispozitiv din rețeaua opusă:**
```
ping 2001:cafe:db8:2::10
```

**Ping către gateway-ul din rețeaua opusă:**
```
ping 2001:cafe:db8:2::1
```

**Ping către Switch 1** (pentru verificarea rutei implicite a switch-ului, presupunând că i s-a alocat `::2` pe interfața VLAN 1):
```
ping 2001:cafe:db8:2::2
```

> **Notă:** Este normal ca primele 1-2 pachete ICMP să eșueze („Request timed out”) în timpul procesului de **Neighbor Discovery (NDP)**. Dacă se repetă comanda, rata de succes va fi de 100%.
