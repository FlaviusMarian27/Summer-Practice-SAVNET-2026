# 3.1 Navigating the Linux Desktop

- un administrator de sistem trebuie să cunoască foarte bine Linux și să aibă skill-rui ICT de bază.

## 3.1.1 Getting to the Command Line

- Pe GUI există 2 metode de a ajunge la linia de comandă:
	- **GUI terminal -** un program în mediul GUI care emulează o fereastră de terminal
	- **Virtual terminal -** poate rula simultan cu GUI-ul, dar necesită login separta prin comenzi înainte de a putea executa comenzi.

---

# 3.2 Applications

- kernel-ul decide ce blocuri de memorie primește fiecare program, pornește/oprește aplicații, gestionează afișarea.
	- aplicațiile fac cereri către kernel prin API și nu trebuie să știe detalii de implementare (ex: ce stocare este SSD sau HDD).
	- **Multitasking -** kernel-ul comută rapid între task-uri, dând impresia că mai multe lucruri se întâmplă simultan.
	- **Process -** o singură sarcină încărcată și urmărită de kernel; O aplicație poate avea nevoie de mai multe procese pentru a funcționa.

## 3.2.1 Major Applications

- **Server Applications -** fără interacțiune directă cu monitor/tastatură, servesc informații către clients.
- **Desktop Applications -** browsere, editoare de text, playere audio.
- **Tools -** categorie eterogenă: configurare display-uri, shell-uri, compilers.


## 3.2.2 Server Applications

- Web Servers:
	- pagina statică - server-ul trimite fișierul așa cum e pe disk.
	- pagina dinamică - cererea merge la o aplicație care generează conținutul.
	- Apache - Apache Software Foundation.
	- NGINX - din Rusia, axat pe performanță, folosește kernel-ul UNIX mai modern.
	- peste 65% din website-uri sunt pe NGINX sau Apache.

- Private Cloud Servers:
	- **ownCloud -** lansat în 2010 de Frank Karlitscheck
	- **Nextcloud -** fork din ownCloud, lansat în 2016

- Database Servers:
	- **MariaDB =** fork community-developed al MySQL.
	- Alte baze de date: FireBird, PostgreSQL.
	- SQL - limbaj folosit pentru interogare și agregare de date.

- Email Servers:
	- MTA - Mail Transfer Agent: transferă mesajele (ex: Sendmail, Postfix).
	- MDA - Mail Delivery Agent: stochează email-urile în mailbox-ul userului
	- POP/IMAP Server: preia mail-urile de pe server.

- File Sharing:
	- **Samba -** soluția pentru file sharing centrat pe Windows.
	- **Netatalk -** echivalentul pentru Apple Macintosh
	- NFS - protocol nativ de file sharing pentru UNIX/Linux
	- DNS - convertește nume în adresă IP.
	- LDAP - sistem director, stochează obiecte în structură de arbore.
	- DHCP - alocă adresă IP automat.


## 3.2.3 Desktop Applications

- Email: Thunderbird(Mozilla), Evolution(GNOME) și KMail(KDE).
- Cretive: Blender, GIMP, Audacity.
- Productivity: LibreOffice, LibreOffice Writer.
- Web Browsers: Firefox și Chrome.


---

# 3.3 Console Tools

- un sysadmin trebuie să aibă competențe de bază în programare.

## 3.3.1 Shells

-  acceptă comenzi și le plasează kernelului Linux pentru execuție.
- Bourne Shell și C shell.
- Bash - shell implicit pe majoritatea sistemelor și tcsh.
- alte shell-uri ksh și zsh.

## 3.3.2 Text Editors

- Cele 2 editoare majore: Vi/Vim și Emacs
- Editoare simple: Pico și Nano.
- Nano a apărut din cauză că Pico nu este open source și interzice modificarea.

---

# 3.4 Package Management

## 3.4.1 Debian Package Management

- Debian și derivatele (Ubuntu, Mail) folosesc pachete cu extensia .deb.
- dpkg - tool dificil pentru începători.
- front-end prietenos apt-get.
- alte front-end-uri: aptitude, Synaptic și Software Center.

## 3.4.2 RPM Package Management

- Linux Standards Base specifică RPM ca sistem standard de package management.
- folosti de distribuții derivate din Red Hat.

---

# 3.5 Development Languages

- limbaj interpretate vs compilate:
	- compilat: tradus în cod mașină dintr-o dată.
	- interpretat: tradus pe măsură ce rulează.

- Linux e scris în C - avantajul este codul mic și eficient, care este mapat direct pe codul mașină generat.
- Extensii ale C: C++ și Object C.
- Java: compilează către o mașină ipotetică - JVM. 


---

# 3.6 Security

- cookies - mecanismul principal prin care site-urie te urmăresc.

## 3.6.1 Passwork Issues

- root = user-ul cel mai privelegiat, creat automat la instalare OS-ului e contul de administrator principal.
- password manager, 2FA

## 3.6.2 Protecting Yourself

- Parolă bună = minim 10 caractere, mixt de cifre, litere mari și mici, caracter special.
- tool ca și KeePassX
- Firewall = dispozitiv care filtrează traficul de rețea. Ubuntu - GUFW.

## 3.6.3 Privacy Tools

- Encryption = cel mai cunoscut/răspândit privacy tool.
- VPN - creează un canal criptat între 2 sisteme.
- Tor - relayează cererile prin o rețea de servere pentru a ascunde identitatea.


---

# 3.7 The Cloud

1. Public Cloud - oferită publicului larg.
2. Private Cloud - pentru companii.
3. Community Cloud - grup de organizații.
4. Hybrid Cload - private + public + community.

## 3.7.1 Linux in the Cloud

- flexibility
- accessibility
- cost-effective
- manageability
- security

## Virtualization 

- linux e un OS multi-user.
- host - conmputerul fizic.
- hypervisor
- bare metal hypervisor.

## Containers

- Docker
- Kubernetes