### 12.2 Motherboard (placa de bază)

Componenta centrală prin care se conectează CPU, RAM și celelalte componente. Unele device-uri (CPU, RAM) se atașează direct pe placă, altele (plăci de extensie) prin **bus**.

### 12.3 Procesoare (CPU)

- **Multiprocessor** = sistem cu mai mult de un procesor fizic
- **Multi-core** = mai multe nuclee într-un singur chip
- Doar 2 arhitecturi principale pe Linux: **x86** (32-bit) și **x86_64** (64-bit, compatibil retroactiv cu 32-bit)

Comenzi cheie:

```
arch          → afișează arhitectura (ex: x86_64)
lscpu         → informații detaliate despre CPU
```

⚠️ **Capcană:** `arch` = x86_64 înseamnă CPU-ul rulează **în mod** 64-bit, dar `lscpu` arată `CPU op-mode(s): 32-bit, 64-bit` → adică CPU-ul e capabil de ambele moduri.

### 12.4 RAM (Random Access Memory)

- Sisteme **32-bit** → maxim **4 GB RAM** adresabil
- Sisteme **64-bit** → mult mai mult
- Când RAM-ul se termină, se folosește **swap space** (spațiu pe disk care simulează RAM)

Comandă cheie:

```
free -m       # afișează în MB
free -g       # afișează în GB
```

Coloane: `total`, `used`, `free`, `shared`, `buffers`, `cached`, plus rândul `Swap`.

### 12.5 Buses & Peripheral Devices

- **Bus** = conexiune high-speed pentru comunicare între componente (ex: **PCI**, **USB**)
- **Peripheral devices** = componente conectate pentru input/output/storage (tastatură, mouse, monitor, HDD)

Comenzi:

```
lspci   → listează device-urile conectate prin bus-ul PCI (VGA, SCSI, Ethernet etc.)
lsusb   → listează device-urile conectate prin USB
```

⚠️ **Capcană importantă:**

- Device-uri **interne** = **cold-plug** (trebuie oprit sistemul ca să le conectezi/deconectezi)
- Device-uri **USB** = **hot-plug** (poți conecta/deconecta în timp ce sistemul rulează) — dar tot trebuie **unmount**-ate corect înainte, altfel risc de pierdere/coruperea datelor.

### 12.6 Hard Drives

Tipuri de **partitioning**:

- **MBR** (Master Boot Record) — vechi, tool-uri: `fdisk`, `cfdisk`, `sfdisk`
- **GPT** (GUID Partitioning Table) — din anul 2000, permite mai multe partiții și partiții >2TB, tool-uri: `gdisk`, `cgdisk`, `sgdisk`
- **parted** + **gparted** (grafic) — suportă ambele tipuri

**Convenția de nume de device (foarte testată la examen!):**

- Prefix după tip: `hd` = IDE, `sd` = SATA/SCSI/USB
- Literă după prefix = ordinea device-ului: `/dev/hda`, `/dev/hdb`...
- Cifră la final = numărul partiției: `/dev/sda1`, `/dev/sda2`

Exemplu clasic de examen:

```
/dev/sda, /dev/sda1, /dev/sda2   → primul disc, 2 partiții
/dev/sdb, /dev/sdb1              → al doilea disc, 1 partiție
/dev/sdc                         → al treilea disc, fără partiții create
```

Comandă utilă (necesită root):

```
fdisk -l /dev/sda
```

### 12.7 Solid State Disks (SSD)

⚠️ **Capcană tipică:** diferența față de HDD clasic:

- HDD = discuri rotative, cap de citire, date scrise secvențial
- SSD = fără piese mobile, controller citește direct din memorie → **mai rapid**

Avantaje SSD: consum mai mic, boot mai rapid, mai puțină căldură/vibrație.  
Dezavantaje: preț mai mare, capacitate mai mică la același preț, dacă e lipit pe placă → nu poate fi upgradat.

### 12.8 Optical Drives

- Discuri optice (CD/DVD/Blu-Ray) = **removable storage media**
- Se montează de obicei în:
    - `/media` — distribuții moderne
    - `/mnt` — distribuții mai vechi

Comandă pentru demontare: `umount`

⚠️ Capcană: e `umount`, **NU** `unmount` (fără "n" în mijloc)!

### 12.9 Managing Devices

- Hardware-ul are nevoie de **drivere** pentru a comunica cu OS-ul
- Driverul poate fi: compilat în kernel, încărcat ca **modul** al kernelului, sau încărcat de o aplicație user-space
- Suportul vendorilor e de obicei mai bun pentru Windows; pentru Linux există mult suport **community-driven**
- Recomandare practică: verifică certificarea hardware-ului pe site-ul distribuției (ex: Red Hat, SUSE au liste oficiale de hardware certificat)

### 12.10 Video Display Devices

**4 tipuri de cabluri video** (foarte testat la examen, cu numărul de pini!):

|Cablu|Pini|Notă|
|---|---|---|
|VGA|15-pin|analog, cel mai vechi|
|DVI|29-pin|digital|
|HDMI|19 sau 29-pin|suportă până la 4K/Ultra HD|
|DisplayPort (DP)|20-pin|cel mai nou; Mini DisplayPort = variantă mai mică, folosită de Apple|

### 12.11 Power Supplies

- Convertesc curent alternativ (**AC**, 120v/240v) în curent continuu (**DC**, 3.3v/5v/12v)
- Nu sunt programabile, dar calitatea lor contează enorm — o sursă defectă poate distruge tot sistemul
- Sistemele desktop/server/rack sunt **mai vulnerabile** la fluctuațiile de tensiune decât laptopurile (care au baterie ca buffer)