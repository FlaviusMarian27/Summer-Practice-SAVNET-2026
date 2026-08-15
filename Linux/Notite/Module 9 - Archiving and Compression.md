### 9.1-9.2 — Concepte de bază

**Archiving** vs **Compression** — diferența e testată des:

- **Archiving** = combină mai multe fișiere într-unul singur (elimină overhead-ul fișierelor individuale, ușurează transferul)
- **Compression** = micșorează fișierele prin eliminarea informației redundante

**Lossless vs Lossy:**

|Tip|Descriere|Exemple|
|---|---|---|
|**Lossless**|Nicio informație nu se pierde; decompresia = originalul exact|GIF, PNG, `gzip`|
|**Lossy**|Informație se pierde; rezultatul e ușor diferit de original|JPEG|

⚠️ **Capcană de examen:** comprimarea unui fișier deja comprimat **nu îl mai micșorează** — irelevant pentru lossless, dar la algoritmi lossy, comprimarea repetată degradează fișierul progresiv până devine "unrecognizable".

### 9.2 — `gzip` / `gunzip`

```
gzip fisier          → creează fisier.gz, fisierul original dispare
gunzip fisier.gz      → decomprimă, restaurează fisierul original
gzip -d fisier.gz      → echivalent cu gunzip
gzip -l fisier.gz      → arată statistici de compresie (ratio)
```

⚠️ **Notă din curs:** `gunzip` e de fapt doar un script care apelează `gzip` cu parametrii corecți.

**Comenzi similare, cu algoritmi diferiți:**

|Comandă|Algoritm|Extensie|
|---|---|---|
|`gzip`/`gunzip`|Lempel-Ziv|`.gz`|
|`bzip2`/`bunzip2`|Burrows-Wheeler|`.bz` / `.bz2`|
|`xz`/`unxz`|Lempel-Ziv-Markov (LZMA)|`.xz`|

⚠️ **Capcană de examen (trade-off-uri):**

- `bzip2` → comprimă **mai bine** decât `gzip`, dar consumă **mai mult CPU**
- `xz` → timp de decompresie similar cu `gzip`, dar rată de compresie mai bună (apropiată de `bzip2`)

### 9.3 — `tar` (Tape Archive)

**Cele 3 moduri esențiale** — memorează-le, apar garantat la examen:

|Mod|Opțiune|Funcție|
|---|---|---|
|**Create**|`-c`|creează un archive nou|
|**Extract**|`-x`|extrage fișiere din archive|
|**List**|`-t`|arată conținutul fără extragere|

#### Create Mode

```
tar -c [-f ARCHIVE] [OPTIONS] [FILE...]
```

- `-c` = create
- `-f ARCHIVE` = numele fișierului rezultat (obligatoriu de specificat explicit)
- Poți folosi wildcard-uri: `tar -cf alpha_files.tar alpha*`

**Compresie combinată cu tar:**

|Opțiune|Compresie|
|---|---|
|`-z`|gzip → `.tar.gz` / `.tgz`|
|`-j`|bzip2 → `.tar.bz2` / `.tbz` / `.tbz2`|

Exemplu: `tar -czf alpha_files.tar.gz alpha*`

⚠️ **Important:** extensiile fișierelor (`.tar`, `.tar.gz`) sunt doar **convenție** — nu influențează efectiv cum se comportă fișierul, dar e bine să le respecți.

#### List Mode

```
tar -t [-f ARCHIVE] [OPTIONS]
```

Exemplu: `tar -tjf folders.tbz` (`-t` list + `-j` bzip2 + `-f` fișier)

⚠️ **Notă:** `tar` intră automat recursiv în subdirectoare la creare/listare, păstrând calea completă în arhivă.

#### Extract Mode

```
tar -x [-f ARCHIVE] [OPTIONS]
```

Exemplu: `tar -xjf folders.tbz`

**Opțiuni utile:**

- `-v` (verbose) → arată fișierele procesate
- Pentru a extrage **doar anumite fișiere**, adaugă numele lor la finalul comenzii (trebuie să corespundă exact numelui din arhivă, sau pattern)

⚠️ **CAPCANĂ MAJORĂ DE EXAMEN — ordinea opțiunilor:** `-f` trebuie să fie **ultima** flag înainte de numele fișierului, pentru că `tar` presupune că tot ce urmează după `-f` e numele arhivei.

Exemplu greșit din curs: `tar -xjfv folders.tbz` → **eșuează**, pentru că `tar` crede că `v` e numele fișierului:

```
tar (child): v: Cannot open: No such file or directory
```

Varianta corectă: `tar -xjvf folders.tbz` (cu `-f` ultimul).

### 9.4 — ZIP Files

⚠️ **Diferență majoră față de tar+gzip:** `zip`/`unzip` **nu** sunt interschimbabile cu `tar`/`gzip` la nivel de opțiuni — au comportament propriu.

```
zip [OPTIONS] zipfile [file...]
```

**Comportamente cheie de reținut:**

- Modul implicit al `zip` = adaugă fișiere **și** le comprimă simultan (nu separat, ca la tar)
- `zip` **nu** necesită `-f` pentru a specifica numele fișierului (spre deosebire de `tar`)
- ⚠️ **Capcană importantă:** `zip` **nu intră recursiv** în subdirectoare by default! Dacă adaugi doar un director, se adaugă directorul gol, fără conținut. Pentru recursivitate (comportament similar cu `tar`), trebuie folosită opțiunea **`-r`**

```
zip -r School.zip School
```

**Comenzi utile:**

|Comandă|Efect|
|---|---|
|`unzip -l fisier.zip`|listează conținutul, fără extragere|
|`unzip fisier.zip`|extrage tot (întreabă dacă suprascrie fișiere existente)|
|`unzip fisier.zip nume_fisier`|extrage un fișier specific (trebuie calea exactă din arhivă)|
|`unzip fisier.zip "folder/*t"`|extrage cu pattern, similar cu tar|

⚠️ **Notă practică:** dacă dai calea greșită (fără directorul părinte), primești `caution: filename not matched`.

---

**Tabel recapitulativ rapid — comenzile din capitol:**

|Comandă|Ce face|
|---|---|
|`gzip fisier`|comprimă (lossless), șterge originalul|
|`gunzip` / `gzip -d`|decomprimă|
|`gzip -l`|statistici compresie|
|`tar -c -f arhiva.tar fisiere`|creează arhivă|
|`tar -x -f arhiva.tar`|extrage arhivă|
|`tar -t -f arhiva.tar`|listează conținut|
|`tar ... -z`|+ compresie gzip|
|`tar ... -j`|+ compresie bzip2|
|`zip -r arhiva.zip director`|arhivează + comprimă (recursiv)|
|`unzip -l arhiva.zip`|listează|
|`unzip arhiva.zip`|extrage|