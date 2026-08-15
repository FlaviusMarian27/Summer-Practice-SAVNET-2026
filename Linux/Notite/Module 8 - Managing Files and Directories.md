### 8.2 — Globbing (wildcard-uri)

⚠️ **Definiție cheie pentru examen:** glob-urile sunt o caracteristică a **shell-ului**, nu a unei comenzi anume — funcționează cu orice comandă Linux. Shell-ul "expandează" pattern-ul înainte ca acesta să ajungă la comandă.

**Cele 3 tipuri de caractere glob:**

#### `*` (asterisk)

Matches **zero sau mai multe** caractere (oricare).

- `echo *` → toate fișierele
- `echo D*` → tot ce începe cu D
- `echo *s` → tot ce se termină cu s
- `echo D*n*s` → poate apărea de mai multe ori/oriunde în pattern

#### `?` (semnul întrebării)

Matches **exact un** caracter — nici mai mult, nici mai puțin.

- `echo ??????` → fișiere de exact 6 caractere
- `echo D????????` → începe cu D + exact 8 caractere după (9 total)

⚠️ **Capcană de examen:** `*` = zero sau mai multe; `?` = exact unul. Se pot **combina**: `echo ?????*s` → minim 5 caractere + orice + termină în s.

#### `[ ]` (paranteze pătrate) — character class

Specifică ce caracter e permis pe acea poziție — un singur caracter din listă/interval.

- `echo [DP]*` → primul caracter e D **sau** P
- `echo [!DP]*` → primul caracter e **orice, în afară de** D sau P (negare cu `!`)
- `echo [D-P]*` → primul caracter e în intervalul D-P (bazat pe tabela ASCII)
- `echo [!D-P]*` → primul caracter NU e în intervalul D-P

⚠️ **Capcană subtilă:** intervalele se bazează pe **ordinea din tabela ASCII**, nu pe alfabet intuitiv. De exemplu `[1-A]` include cifre, simboluri (`:;<=>?@`) și litera A — nu doar ce ai crede logic. Comanda `ascii` afișează tabela.

### 8.3 — Copiere, mutare, redenumire

#### `cp` (copy)

```
cp sursa destinație
```

**Opțiuni esențiale:**

|Opțiune|Efect|
|---|---|
|`-v` (verbose)|arată ce se copiază: `'sursa' -> 'destinație'`|
|`-p`|**preservă** atributele fișierului (timestamp, permisiuni)|
|`-R`|copiere **recursivă** (obligatorie pentru directoare!)|

⚠️ **Capcană importantă:** fără `-p`, copia primește data/ora **curentă**, nu timestamp-ul original. Cu `-p`, timestamp-ul original e păstrat.

⚠️ **Capcană cu `.` (punct):** `cp -v /etc/hosts .` → copiază în directorul curent, folosind `.` ca prescurtare. Funcționează cu orice comandă Linux, nu doar `cp`.

⚠️ **Copierea unui director necesită `-R`:** `cp /etc/udev Myetc` **fără** `-R` ar da eroare — trebuie `cp -R /etc/udev Myetc`. Directorul destinație (`Myetc`) trebuie creat înainte cu `mkdir` dacă vrei o structură specifică, dar `cp -R` poate crea și el directorul țintă dacă nu există.

#### `rm` (remove)

|Comandă|Efect|
|---|---|
|`rm fisier`|șterge un fișier|
|`rm fisier1 fisier2`|poți șterge **mai multe** fișiere odată|
|`rm -r director`|șterge un director **recursiv**, cu tot conținutul|
|`rmdir director`|șterge director, dar **doar dacă e gol**|

⚠️ **Capcană de examen — diferența `rmdir` vs `rm -r`:** `rmdir` eșuează dacă directorul conține fișiere; `rm -r` șterge orice, inclusiv conținutul.

#### `mv` (move / rename)

```
mv sursa destinație
```

⚠️ **Concept cheie:** `mv` = „cut and paste". Nu există o comandă separată de „rename" în Linux — **mutarea și redenumirea sunt aceeași operație** (`mv fisier_vechi fisier_nou` în același director = redenumire).

#### `touch`

Creează un fișier gol (folosit des în exemple/laburi pentru a genera rapid fișiere test).

---

**Rezumat rapid al comenzilor din acest lab:**

| Comandă                        | Scop                   |
| ------------------------------ | ---------------------- |
| `mkdir nume`                   | creează director       |
| `touch nume`                   | creează fișier gol     |
| `cp [-v] [-p] [-R] sursa dest` | copiază                |
| `mv sursa dest`                | mută/redenumește       |
| `rm [-r] nume`                 | șterge fișier/director |
| `rmdir nume`                   | șterge director gol    |