### 6.1-6.2 - Man Pages

**Comanda de bază:** `man command` — afișează pagina de manual.

**Navigare:**

- săgeți sus/jos pentru scroll
- `Q` pentru a ieși
- `/termen` + Enter pentru căutare în pagină
- `n` = următoarea potrivire, `Shift+N` = potrivirea anterioară
- `H` = afișează help-ul de navigare

⚠️ **Capcană tipică de examen:** `man` folosește un _pager_ pentru afișare — de obicei `less`, dar pe unele distribuții poate fi `more`. Reține exact cuvântul **pager** ca termen generic.

**Secțiunile unei pagini de man** (ordinea contează, poate apărea la examen):

1. **NAME** — numele comenzii + descriere scurtă
2. **SYNOPSIS** — sintaxa de utilizare
3. **DESCRIPTION** — descriere detaliată
4. **OPTIONS** — lista opțiunilor (uneori inclusă în DESCRIPTION)
5. **FILES** — fișiere asociate comenzii
6. **AUTHOR** — cine a scris pagina
7. **REPORTING BUGS**
8. **COPYRIGHT**
9. **SEE ALSO** — referințe către alte comenzi

⚠️ **Capcană la SYNOPSIS:**

- `[ ]` = opțional (nu e obligatoriu)
- `...` (ellipsis) = elementul dinainte poate fi folosit de mai multe ori
- `[-u|--utc|--universal]` — bara `|` = „sau" (opțiunile fac cam același lucru, dar de obicei nu pot fi combinate)

### 6.2.4 — Cele 9 secțiuni de man pages

Foarte important pentru examen — reține ordinea:

|#|Secțiune|
|---|---|
|1|General Commands|
|2|System Calls|
|3|Library Calls|
|4|Special Files|
|5|File Formats and Conventions|
|6|Games|
|7|Miscellaneous|
|8|System Administration Commands|
|9|Kernel Routines|

⚠️ **Capcană clasică:** `man` caută secțiunile **în ordine**, de la 1 la 9, și se oprește la **prima potrivire**. Exemplu clasic dat de curs: `passwd` există ca:

- comandă (secțiunea 1) → `man passwd` arată automat asta
- fișier de configurare (secțiunea 5) → trebuie explicit `man 5 passwd`

**Comenzi conexe importante:**

- `man -f nume` sau `whatis nume` → arată în ce secțiune e comanda + descriere scurtă
- `man -k cuvant_cheie` sau `apropos cuvant_cheie` → caută cuvântul cheie în numele **și** descrierile paginilor de man (util când nu știi numele exact al comenzii)

---
### 6.3 - Localizarea comenzilor

- **`whatis`** = ce secțiune de man are comanda (poate arăta rezultate „ciudate" dacă există 2 comenzi cu același nume din variante diferite de UNIX — de asta pot exista `ls (1)` și `ls (1p)`)
- **`whereis nume`** → arată unde e localizat binarul + man page-urile asociate (ex: `/bin/ls`, `/usr/share/man/man1/ls.1.gz`)
- **`locate nume`** → caută în toată baza de date a sistemului (fișiere + directoare), nu doar comenzi

⚠️ **Capcane importante la `locate`:**

- Baza de date se actualizează de obicei **nightly** (automat, printr-un job programat) — fișierele create azi **nu apar** până la următoarea actualizare
- Actualizare manuală: `updatedb` (necesită root)
- Ca user obișnuit, `locate` **nu arată** fișiere la care nu ai acces (măsură de securitate)
- `locate -c termen` → doar **numărul** de rezultate, nu lista
- `locate -b termen` → caută doar în **basename** (numele fișierului, fără calea directorului)
- `locate -b "\termen"` → backslash-ul limitează la potrivire **exactă** a numelui de fișier

---
### 6.4 - Info Documentation

Diferența cheie față de man pages (posibilă întrebare de examen):

|Man pages|Info docs|
|---|---|
|Documente independente|Un singur "book" cu toate documentele legate între ele|
|Resursă de **referință**|Ghid de **învățare**|
|Structură plată|Structură organizată pe noduri (nodes), ca un cuprins|

**Comandă:** `info command`

**Navigare (diferă de man!):**

- `Shift+H` → afișează comenzile de navigare
- `Q` → închide info complet
- `L` → înapoi la ultimul nod vizitat
- `U` → un nivel mai sus
- `[` / `]` → nodul anterior/următor în document
- `P` / `N` → nodul anterior/următor pe același nivel
- `TAB` → sari la următorul hyperlink
- `RET` (Enter) → urmează hyperlink-ul de sub cursor

⚠️ **Capcană:** `info` (fără argumente) → te duce la **top level** al arborelui de documentație (nodul "Directory node"), util pentru explorare generală.

---
### 6.5 - Alte surse de ajutor

- **`command --help`** → afișare rapidă tip SYNOPSIS, direct din linia de comandă
- **README files** → documentație suplimentară de la vendori terți, localizată de obicei în `/usr/share/doc` sau `/usr/doc`