# Topologie IPv6 — PC0 ↔ R0 ↔ R1 ↔ PC1

Configurare IPv6 static/SLAAC/EUI-64 pentru o topologie cu 2 routere, 2 switch-uri și 2 PC-uri.

## Schema rețelei

```
PC0 --- SW0 --- R0 --- R1 --- SW1 --- PC1
       (LAN A) Gi0/0  Gi0/1  Gi0/0  Gi0/1 (LAN B)
```

| Rețea | Prefix | Note |
|---|---|---|
| LAN A (PC0) | `2025:abcd:db8:a::/64` | R0 Gi0/0 configurat cu **eui-64** |
| Link R0–R1 | `2025:abcd:db8:1::/64` | R0 Gi0/1 = `::1`, R1 Gi0/0 = `::2` (manual) |
| LAN B (PC1) | `2025:abcd:db8:b::/64` | R1 Gi0/1 configurat cu **eui-64** |

IP-ul primit de la ISP (`2025:abcd:db8::/48`) e doar informativ — de acolo au fost derivate cele 3 subrețele `/64`.

## R0

```
enable
configure terminal
hostname R0
ipv6 unicast-routing

interface gig0/0
 ipv6 address 2025:abcd:db8:a::/64 eui-64
 no shutdown
 exit

interface gig0/1
 ipv6 address 2025:abcd:db8:1::1/64
 no shutdown
 exit

ipv6 route 2025:abcd:db8:b::/64 2025:abcd:db8:1::2

end
write memory
```

## R1

```
enable
configure terminal
hostname R1
ipv6 unicast-routing

interface gig0/0
 ipv6 address 2025:abcd:db8:1::2/64
 no shutdown
 exit

interface gig0/1
 ipv6 address 2025:abcd:db8:b::/64 eui-64
 no shutdown
 exit

ipv6 route 2025:abcd:db8:a::/64 2025:abcd:db8:1::1

end
write memory
```

## PC0 — Auto Config (SLAAC)

Desktop → IP Configuration → IPv6 → **Automatic**

PC-ul primește singur adresa + gateway din Router Advertisement-urile trimise de R0. Nu se completează nimic manual.

## PC1 — Static

Desktop → IP Configuration → IPv6 → **Static**

| Câmp | Valoare |
|---|---|
| IPv6 Address | `2025:abcd:db8:b::2` |
| Prefix Length | `64` |
| Default Gateway | adresa **eui-64** generată pe R1 Gi0/1 (vezi mai jos) |

## Switch0 / Switch1

Nu necesită nicio configurare — sunt switch-uri L2 pure, funcționează by-default.

## Cum aflu adresa eui-64 a unei interfețe

Pe router, în modul privilegiat (nu în config mode — dacă ești în `(config)#` pune `do` în față):

```
show ipv6 interface brief
```

Adresa lungă afișată sub prefixul `/64` (nu cea link-local `FE80::...`) e cea generată automat — aceea e gateway-ul pe care îl pui pe PC1.

⚠️ **Atenție:** cu eui-64, gateway-ul NU e `::1` — e adresa completă generată din MAC-ul interfeței. `::1` funcționează doar dacă interfața a fost configurată manual cu acea adresă.

## Verificare — teste de ping

```
PC0 > ping 2025:abcd:db8:1::1     (R0 Gi0/1)
PC0 > ping 2025:abcd:db8:1::2     (R1 Gi0/0)
PC0 > ping [adresa lui PC1]
PC1 > ping [adresa lui PC0]
```

Dacă un ping dă fail:
1. Verifică `show ipv6 interface brief` pe ambele routere — toate interfețele trebuie `up/up`.
2. Verifică gateway-ul PC-urilor — mai ales pe interfețele cu eui-64.
3. Verifică rutele statice cu `show ipv6 route` — fiecare router trebuie să aibă o rută spre subrețeaua opusă.
