## 13.1. ICMP Messages

### 13.1.1 - ICMPv4 și ICMPv6 Messages

Ideea de bază: IP (atât v4 cât și v6) e un protocol **"best-effort"** - nu garantează livrarea. Dacă ceva merge prost, IP-ul singur nu-ți spune nimic. Aici intervine **ICMP** - trimite mesaje de eroare/informative, dar **nu face IP-ul fiabil**, doar te informează despre problemă.

**Foarte important de reținut:** ICMP nu e obligatoriu, iar în multe rețele reale e **blocat parțial din motive de securitate** (ex: firewall-uri blochează ping-uri din exterior). Nu confunda "ICMP există în teorie" cu "ICMP funcționează mereu în practică".

3 tipuri de mesaje comune atât la ICMPv4 cât și ICMPv6, discutate în acest modul:

- Host reachability
- Destination/Service Unreachable
- Time Exceeded


### 13.1.2 - Host Reachability

Mecanismul din spatele comenzii `ping`, pe care deja l-ai folosit:

1. Host-ul sursă trimite **ICMP Echo Request**
2. Dacă destinația e disponibilă, răspunde cu **ICMP Echo Reply**

Simplu, dar reține numele exact al mesajelor (Echo Request/Echo Reply) - apar des la examen ca terminologie exactă.



### 13.1.3 - Destination or Service Unreachable

Când un router/host primește un pachet pe care **nu poate să-l livreze**, trimite înapoi un mesaj **Destination Unreachable**, cu un cod care explică exact de ce.

Codurile diferă între ICMPv4 și ICMPv6 - nu le confunda:

**ICMPv4:**

- 0 - Net unreachable
- 1 - Host unreachable
- 2 - Protocol unreachable
- 3 - Port unreachable

**ICMPv6:**

- 0 - No route to destination
- 1 - Communication administratively prohibited (ex: blocat de firewall)
- 2 - Beyond scope of source address
- 3 - Address unreachable
- 4 - Port unreachable

**Nu trebuie memorate perfect toate**, dar reține conceptul: **ICMPv6 are coduri diferite și mai multe** decât ICMPv4 (5 coduri vs 4), plus codul special "administratively prohibited" care nu există explicit la v4 în lista asta - util pentru diagnosticare când ceva e blocat intenționat de un firewall, nu pentru că rețeaua chiar nu există.



### 13.1.4 - Time Exceeded

Mecanismul din spatele comenzii `traceroute`:

- **IPv4** folosește câmpul **TTL (Time to Live)** - fiecare router prin care trece pachetul scade TTL cu 1. Când TTL ajunge la 0, routerul aruncă pachetul și trimite înapoi un mesaj **Time Exceeded**.
- **IPv6** face exact același lucru, dar folosește un câmp echivalent numit **Hop Limit** în loc de TTL.

**De reținut clar pentru examen:** TTL (IPv4) și Hop Limit (IPv6) sunt **funcțional identice**, doar numele diferă între versiuni. Traceroute exploatează exact acest mecanism - trimite pachete cu TTL/Hop Limit crescător (1, 2, 3...) ca să forțeze fiecare router de pe traseu să răspundă cu Time Exceeded, developing astfel harta completă a rutei.




### 13.1.5 - ICMPv6 Messages (partea nouă, specifică IPv6)

Aici e ceva ce n-ai mai văzut concentrat - **ICMPv6 include 4 protocoale noi**, toate parte din **NDP (Neighbor Discovery Protocol)**, împărțite în 2 categorii:

**Grupul 1 - comunicare router ↔ device** (deja le cunoști!):

- **RS (Router Solicitation)** - host cere info de la router
- **RA (Router Advertisement)** - router răspunde/anunță periodic

**Grupul 2 - comunicare device ↔ device** (nou pentru tine):

- **NS (Neighbor Solicitation)** - folosit pentru 2 lucruri: **duplicate address detection** (verifici dacă adresa ta IPv6 e deja folosită de altcineva pe link) și **address resolution** (echivalentul ARP-ului la IPv4 - afli MAC-ul unui vecin pornind de la adresa lui IPv6)
- **NA (Neighbor Advertisement)** - răspunsul la NS, similar cu un ARP reply

**Legătura importantă cu ce ai învățat deja la 12.7.3:** exact NS-urile sunt trimise către adresele **solicited-node multicast** despre care am discutat - acum se leagă tot! Un device vrea să afle MAC-ul unui vecin → trimite NS către adresa solicited-node multicast a vecinului (nu broadcast la tot subnetul, ca la ARP) → vecinul răspunde cu NA.

**Bonus - Redirect message:** ICMPv6 ND include și un mesaj **Redirect**, echivalent funcțional cu Redirect-ul de la ICMPv4 - folosit când un router îi spune unui host că există o cale mai bună/scurtă către destinație, printr-un alt router de pe același subnet.


---


## 13.2. Ping and Traceroute Tests

### **13.2.1 - Ping - Test Connectivity**

- Ping e un utilitar de testare pentru IPv4 și IPv6 care folosește mesaje ICMP echo request și echo reply pentru a testa conectivitatea între hosturi.

- Pentru a testa conectivitatea către alt host, se trimite un echo request către adresa host-ului. Dacă host-ul primește request-ul, răspunde cu echo reply.

- Pe măsură ce fiecare echo reply e primit, ping oferă feedback despre timpul dintre trimiterea request-ului și primirea reply-ului. Aceasta poate fi o măsură a performanței rețelei.

- Ping are o valoare de timeout pentru reply. Dacă un reply nu e primit în intervalul de timeout, ping afișează un mesaj care indică faptul că nu s-a primit răspuns. Asta poate indica o problemă, dar poate indica și faptul că au fost activate funcții de securitate care blochează mesajele ping în rețea.

- Este obișnuit ca primul ping să dea timeout dacă trebuie efectuată rezoluția de adresă (ARP sau ND) înainte de trimiterea ICMP Echo Request-ului.

- După ce toate request-urile sunt trimise, utilitarul ping oferă un rezumat care include rata de succes și timpul mediu round-trip către destinație.


Tipurile de teste de conectivitate efectuate cu ping:
- Pinging the local loopback
- Pinging the default gateway
- Pinging the remote host



### **13.2.2 - Ping the Loopback**

- Ping poate fi folosit pentru a testa configurația internă a IPv4 sau IPv6 pe host-ul local. Pentru a efectua acest test, se face ping către adresa de loopback local - 127.0.0.1 pentru IPv4 (::1 pentru IPv6).

- Un răspuns de la 127.0.0.1 (IPv4) sau ::1 (IPv6) indică faptul că IP este instalat corect pe host. Acest răspuns vine de la network layer.

- Acest răspuns **nu** este o indicație că adresele, măștile, sau gateway-urile sunt configurate corect. Nici nu indică nimic despre statusul layer-elor inferioare din network stack.

- Acest test verifică pur și simplu IP-ul, în jos, până la network layer al IP-ului.

- Un mesaj de eroare indică faptul că TCP/IP nu este operațional pe host.



### **13.2.3 - Ping the Default Gateway**

- Ping poate fi folosit și pentru a testa abilitatea unui host de a comunica în rețeaua locală. Aceasta se face în general prin ping către adresa IP a default gateway-ului host-ului.

- Un ping reușit către default gateway indică faptul că host-ul și interfața routerului care servește ca default gateway sunt ambele operaționale pe rețeaua locală.

- Pentru acest test, adresa default gateway-ului este cel mai des folosită deoarece routerul este de obicei mereu operațional. Dacă adresa default gateway-ului nu răspunde, se poate trimite un ping către adresa IP a altui host din rețeaua locală, cunoscut ca fiind operațional.

- Dacă fie default gateway-ul, fie alt host răspunde, atunci host-ul local poate comunica cu succes în rețeaua locală. Dacă default gateway-ul nu răspunde dar alt host răspunde, aceasta ar putea indica o problemă cu interfața routerului care servește ca default gateway.

- O posibilitate este că adresa greșită de default gateway a fost configurată pe host. O altă posibilitate este că interfața routerului poate fi complet operațională dar are securitate aplicată care o împiedică să proceseze sau să răspundă la ping requests.



### **13.2.4 - Ping a Remote Host**

- Ping poate fi folosit și pentru a testa abilitatea unui host local de a comunica printr-o internetwork. Host-ul local poate face ping către un host IPv4 operațional dintr-o rețea la distanță. Routerul folosește tabela sa de rutare IP pentru a redirecționa pachetele.

- Dacă acest ping are succes, funcționarea unei părți mari din internetwork poate fi verificată. Un ping reușit peste internetwork confirmă comunicarea în rețeaua locală, funcționarea routerului care servește ca default gateway, și funcționarea tuturor celorlalte routere care ar putea fi pe traseul dintre rețeaua locală și rețeaua host-ului la distanță.

- Suplimentar, funcționalitatea host-ului la distanță poate fi verificată. Dacă host-ul la distanță nu ar putea comunica în afara rețelei sale locale, nu ar fi răspuns.

- **Notă:** Mulți administratori de rețea limitează sau interzic intrarea mesajelor ICMP în rețeaua corporativă; prin urmare, lipsa unui răspuns la ping ar putea fi din cauza restricțiilor de securitate.



### **13.2.5 - Traceroute - Test the Path**

- Ping e folosit pentru a testa conectivitatea între două hosturi dar nu oferă informații despre detaliile device-urilor dintre hosturi.

- Traceroute (tracert) este un utilitar care generează o listă de hop-uri care au fost atinse cu succes de-a lungul traseului. Această listă poate oferi informații importante de verificare și troubleshooting.

- Dacă datele ajung la destinație, atunci trace-ul listează interfața fiecărui router de pe traseul dintre hosturi. Dacă datele eșuează la un anumit hop pe parcurs, adresa ultimului router care a răspuns la trace poate oferi o indicație despre unde se află problema sau restricțiile de securitate.




#### **Round Trip Time (RTT)**

- Folosirea traceroute oferă round-trip time pentru fiecare hop de pe traseu și indică dacă un hop nu răspunde. Round-trip time este timpul pe care îl ia un pachet să ajungă la host-ul la distanță și pentru ca răspunsul de la host să se întoarcă. Un asterisc (*) este folosit pentru a indica un pachet pierdut sau la care nu s-a răspuns.

- Această informație poate fi folosită pentru a localiza un router problematic pe traseu sau poate indica faptul că routerul este configurat să nu răspundă. Dacă afișajul arată timpi de răspuns mari sau pierderi de date de la un anumit hop, aceasta este o indicație că resursele routerului sau conexiunile sale ar putea fi suprasolicitate (stressed).



#### **IPv4 TTL and IPv6 Hop Limit**

- Traceroute folosește o funcție a câmpului TTL în IPv4 și a câmpului Hop Limit în IPv6 din header-ele Layer 3, împreună cu mesajul ICMP Time Exceeded.

- Prima secvență de mesaje trimise de traceroute va avea valoarea câmpului TTL de 1. Aceasta face ca TTL-ul să expire pachetul IPv4 la primul router. Acest router răspunde apoi cu un mesaj ICMPv4 Time Exceeded. Traceroute are acum adresa primului hop.

- Traceroute apoi incrementează progresiv câmpul TTL (2, 3, 4...) pentru fiecare secvență de mesaje. Aceasta oferă trace-ului adresa fiecărui hop pe măsură ce pachetele expiră mai departe pe traseu. Câmpul TTL continuă să fie crescut până când destinația este atinsă, sau este incrementat până la un maxim predefinit.

- După ce destinația finală este atinsă, host-ul răspunde fie cu un mesaj ICMP Port Unreachable, fie cu un mesaj ICMP Echo Reply, în loc de mesajul ICMP Time Exceeded.
