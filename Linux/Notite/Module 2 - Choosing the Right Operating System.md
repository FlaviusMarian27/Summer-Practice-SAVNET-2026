
# 2.1 Operating Systems

- ***Operanting Systems:*** software care rulează pe un dispozitiv și gestionează comportamentul hardware, cât și software ale sistemului. Sistemele moderne pot face mult-tasking și oferă servicii standard pentru utilizator (ex: print-ul).

## 2.1.1 Decision Points

- **Role -** prima decizie va fi desktop sau server.

- **Function -** software-ul specific + numărul de mașinii care rulează în paralele.

- **Life Cycle:**
	- release cycle = ritmul periodic în care apar update-uri de OS/software.
	- maintenance cycle / life cycle = perioada în care vendorul oferă update-rui pentru  versiune mai veche.
	- în entreprise, upgrade-urile sunt costisitoare -> soluție modernă: virtualization.
	- cloud provideres - AWS, Rackspace, MIcrosoft Azure.
	
- **Stability:** software-ul poate să fie beta sau stable (testat deja).

- **Compatibility:** backward compatibility = abilitatea versiunilor noi de OS, de a rula software-ul făcut pentru versiuni mai vechi.

- **Cost:** depinde de hardware, skill-urile echipei și costul de achiziție/mentenanță.

- **Interface:** 

	 switch/plugboard -> punch cards -> terminal text-based (CLI) -> GUI (dezvoltat de Xerox PARC în 1970, popularizat de Apple în anii 1980).


# 2.2 Microsoft Windows

- la Windows apar mereu versiuni noi la fiecare câțiva ani.
- au existat 16 versiuni de Windows din 1985.
- Windows Server curent: versiunea 2019.
- Microsoft a făcut progrese mari pe partea de CLI prin PowerShell și WSL.


# 2.3 Apple macOS

- macOS e pațial bazat pe software din proiectul FreeBSD și a trecut prin certificare UNIX.
- favorizat de școli, small businesses și industrii pentru integrării stabile hardware + software.


# 2.4 Linux

- **Role:** acoperă o gamă largă - server, desktop, firewall, supercomputere, sisteme embedded, POS.

- **Function:** guvernele / enterprise-urile mari preferă  adesea distribuții cu suport comercial.

- **Life Cycle:** 
	- distribuții enthusiast - update rapid, fără suport enterprise
	- enterprise - LTS

- **Stability:** unele distribuții oferă release-uri stable, testing, unstable.

- **Cost:** distribuția poate fi gratuită, dar suport se poate plăti

- **Interface:** GUI vs CLI - la fel ca la orice OS


### Mecanica CLI:
- **Terminal -** aplicația care oferă interfața CLI, acceptă ce trasează userul.
- **Shell -** interpretează comenzile tastate în terminal și le execută.
- **Login CLI -** user + parolă.
- **MOTD -** text afișat la login
- Terminalul trebuie să mențină istoricul comenzilor.