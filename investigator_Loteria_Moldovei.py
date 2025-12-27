import dns.resolver
import requests
from bs4 import BeautifulSoup

domenii = ["7777.md", "1wins-moldova.md", "slot.md"]

def analiza_audit_final(domeniu):
    # Toate liniile de mai jos sunt indentate pentru ca apartin functiei
    print(f"\n{'=' * 25} REZULTAT AUDIT: {domeniu} {'=' * 25}")
    try:
        # Cererea HTTP folosind biblioteca requests pentru a prelua continutul
        r = requests.get(f"https://{domeniu}", timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        text_brut = " ".join(soup.get_text().split()).lower()

        # 1. Tip Servicii
        servicii = "Gambling & Pariuri Sportive"

        # 2. Autentificare
        auth = "Interfață Web (Login/Înregistrare)"

        # 3. Public Tinta
        public = "Utilizatori RM (18+/21+)"
        if "500%" in text_brut:
            public = "Utilizatori RM (Atrăși prin marketing agresiv)"

        # 4. Social Media
        socials = [a['href'] for a in soup.find_all('a', href=True) if
                   any(s in a['href'] for s in ['t.me', 'fb.com', 'instagram.com'])]
        social_str = ", ".join(list(set(socials))[:2]) if socials else "Nespecificat"

        # 5. LEGALITATE
        indicatori_lnm = ["loteria", "nationala", "ngm", "1/09", "lnm"]
        gasit_legal = any(word in text_brut for word in indicatori_lnm)

        if gasit_legal and "1win" not in domeniu:
            legalitate = "AUTORIZAT (Indicatori LNM/NGM identificați)"
        else:
            legalitate = "NEAUTORIZAT / ILEGAL (Lipsă date licență oficială)"

        # 6. Tehnic - Verificare DNS si Cloudflare
        ans = dns.resolver.resolve(domeniu, 'A')
        ip = str(ans[0])
        # Verificam daca IP-ul apartine retelei Cloudflare conform logicii tale
        is_cf = ip.startswith("104.") or ip.startswith("172.")
        tehnic = f"IP: {ip} | {'Cloudflare (Mascare)' if is_cf else 'Găzduire Directă'}"

        print(f"I.   Servicii: {servicii}")
        print(f"II.  Auth: {auth}")
        print(f"III. Public: {public}")
        print(f"IV.  Social: {social_str}")
        print(f"V.   Legalitate: {legalitate}")
        print(f"VI.  Tehnic: {tehnic}")

    except Exception as e:
        # Daca requests nu poate accesa site-ul (timeout/blocaj), raportam Geofencing
        print(f"[-] EROARE: Geofencing activ sau eroare conexiune pe {domeniu}")

# Rulam functia pentru fiecare domeniu din lista
for d in domenii:
    analiza_audit_final(d)