Audit Tehnic și Monitorizare Automatizată a Spațiului Informațional (.md)
🎯 Scopul Proiectului
Acest instrument a fost dezvoltat pentru a eficientiza procesul de identificare și clasificare a platformelor de gambling neautorizate în Republica Moldova. Proiectul trece de la analiza manuală la un sistem automatizat capabil să proceseze simultan multiple resurse, oferind dovezi tehnice clare privind legalitatea acestora.

🚀 Instalare și Rulare
Cerințe preliminare
Python 3.8+

Node.js (necesar pentru componentele Playwright)

Pașii de instalare
Clonarea depozitului:

Bash

git clone https://github.com/ValeriuBirladeanu/investigatie-gambling-rm.git
cd investigatie-gambling-rm
Instalarea dependențelor:

Bash

pip install -r requirements.txt
Configurarea browserului:

Bash

playwright install chromium
Rulare
Executați scriptul principal pentru a genera raportul:

Analiză Infrastructură (SERVER): Detectează automat dacă site-ul folosește servicii de mascare a identității (ex: Cloudflare).

Audit Servicii (TIP SERVICII): Clasifică platforma (Cazinou, Pariuri sau Informațional).

Verificare Conformitate (AUTENTIFICARE): Analizează metodele de înregistrare și prezența obligatorie a câmpului IDNP.

Verdict Legalitate: Corelează automat domeniul cu lista resurselor blocate de Agenția Servicii Publice (ASP).

Notă: Rezultatele sunt salvate și în format .csv pentru a permite importul datelor în Excel și raportarea ulterioară către autorități.
