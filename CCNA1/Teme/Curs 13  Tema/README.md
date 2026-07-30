# Test Practic - Evaluare Finală Modulul 1 (CCNA ITN)

Configurare de bază + adresare IPv6 (Static, EUI-64, SLAAC) pe o topologie cu router și două multilayer switch-uri, în Cisco Packet Tracer.

## Topologie

```
PC0 --- Switch0 (3560-24PS) --- Router0 (1941) --- Switch1 (3560-24PS) --- PC1
         N1: 2001:db8:cafe::/64          N2: 2001:db8:cafe:1::/64
```

- **N1** (Gig0/0): `2001:db8:cafe::/64` — adresă statică pe router
- **N2** (Gig0/1): `2001:db8:cafe:1::/64` — adresă generată prin EUI-64 pe router
- Link-local pe ambele interfețe ale routerului: `FE80::1`

## Partea 1: Configurări de bază (Router0, Switch0, Switch1)

Aceleași comenzi pe toate cele trei echipamente (se schimbă doar `hostname`):

```
enable
configure terminal
hostname Switch0
enable secret cisco12345
line console 0
 password ciscocon
 login
 exit
line vty 0 15
 password ciscovty
 login
 exit
service password-encryption
banner motd #Acces neautorizat interzis!#
end
write memory
```

> Se repetă identic pe Switch1 și Router0.

## Partea 2: Adresare IPv6 pe Router0

```
configure terminal
ipv6 unicast-routing

interface GigabitEthernet0/0
 ipv6 address 2001:db8:cafe::1/64
 ipv6 address FE80::1 link-local
 no shutdown
 exit

interface GigabitEthernet0/1
 ipv6 address 2001:db8:cafe:1::/64 eui-64
 ipv6 address FE80::1 link-local
 no shutdown
 exit

end
write memory
```

**Atenție:** pe Gig0/1 se dă o singură dată comanda cu `eui-64` la final. Dacă o dai și fără `eui-64` înainte, rămâne o adresă extra greșită (`::` ca host) — verifici cu `show ipv6 interface brief` și o ștergi cu `no ipv6 address <adresa greșită>` dacă apare.

## Partea 3: Configurare PC0 și PC1 (SLAAC)

Pe fiecare PC: **Desktop → IP Configuration → IPv6 Configuration → Automatic**

Asta activează SLAAC — PC-ul primește automat adresa globală (generată din MAC) și gateway-ul implicit (link-local-ul routerului), pe baza Router Advertisement-urilor trimise de router (posibil doar cu `ipv6 unicast-routing` activat).

## Partea 4: Salvare și test

Pe toate cele trei echipamente de rețea:
```
copy running-config startup-config
```

Test de conectivitate de pe PC0 (Command Prompt):
```
ping <adresa IPv6 a lui PC1>
```

Exemplu de rezultat așteptat:
```
Reply from 2001:DB8:CAFE:1:...: bytes=32 time<1ms TTL=127
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

## Verificări utile

```
show ipv6 interface brief    # adresele configurate pe interfețele routerului
show running-config          # confirmă hostname, parole criptate, banner
```

## Note

- Denumirile echipamentelor (`Switch0`, `Switch1`, `Router0`) trebuie să respecte exact topologia dacă se verifică strict cerința.
- `service password-encryption` criptează parolele din `line console`/`line vty`, dar `enable secret` e deja criptat implicit (tip 5, MD5).
