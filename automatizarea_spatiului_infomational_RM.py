import asyncio
import httpx
import csv
from pypdf import PdfReader
from io import BytesIO
from playwright.async_api import async_playwright

# Linkul spre resursa cu URL-urole blocate de ASP
ASP_PDF_URL = "https://www.asp.gov.md/sites/default/files/date-deschise/jocuri-de-noroc-nu-autorizate/lista-platforme-neautorizate-jocuri-de-noroc.pdf"

# Aici se aduga manual URL-urile găsite prin Google Dorking
SUSPECT_URLS = [
    "https://pariurisportivemoldova.md/", "https://1win-bet.md/",
    "https://dontaco.md/", "https://1win-moldova.md/",
    "https://prometal.md/", "https://coalitiacub.md/",
    "https://moldovapops.md/", "https://1winapp.md/",
    "https://booin6n77p7.com", "https://capitan.vodka",
    "https://casino-playfortunai2fy1p3hx5.com", "https://drgnkk8.casino",
    "https://inception.md", "https://liceul-tretiacov.md",
    "https://money-x50.casino", "https://sailun.md",
    "https://spinbetter2z.com"
]


async def incarca_baza_date_asp():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(ASP_PDF_URL, timeout=30)
            with BytesIO(response.content) as f:
                reader = PdfReader(f)
                return "".join([p.extract_text().lower() for p in reader.pages])
    except:
        return ""


async def proceseaza(context, url, asp_data):
    domain = url.replace("https://", "").replace("http://", "").split("/")[0].lower()
    este_la_asp = domain in asp_data

    # REORDONARE: Am structurat dicționarul conform noii tale cerințe
    res = {
        "url": url,
        "tip": "-",
        "auth": "-",
        "tinta": "-",
        "social": "-",
        "legal": "ILEGAL (Prezent în lista ASP)" if este_la_asp else "Investigație..."
    }

    page = await context.new_page()
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=35000)
        await asyncio.sleep(2)
        content = (await page.content()).lower()

        # 1. TIP SERVICII
        servicii = []
        if any(x in content for x in ["casino", "slot", "păcănele"]): servicii.append("Cazinou")
        if any(x in content for x in ["bet", "pariuri"]): servicii.append("Pariuri")
        res["tip"] = ", ".join(servicii) if servicii else "Informațional"

        # 2. PUBLIC TINTA
        tinta_indici = []
        if "mdl" in content or "lei mold" in content: tinta_indici.append("MDL")
        if "+373" in content: tinta_indici.append("+373")
        if ".md" in domain or "moldova" in content: tinta_indici.append("Localizare MD")
        if "steam" in content: tinta_indici.append("Gaming/Tineri")

        res["tinta"] = "RM (" + ", ".join(tinta_indici) + ")" if tinta_indici else "General/Intl"

        # 3. SOCIAL MEDIA
        hrefs = await page.evaluate('() => Array.from(document.querySelectorAll("a")).map(a => a.href.toLowerCase())')
        retele = {"TG": "t.me", "FB": "facebook.com", "IG": "instagram.com"}
        gasite = [n for n, l in retele.items() if any(l in h for h in hrefs)]
        res["social"] = ", ".join(gasite) if gasite else "Niciuna"

        # 4. LEGALITATE (Dacă nu e deja în ASP)
        if not este_la_asp:
            indicii = []
            if "loteria națională" in content: indicii.append("Loteria Națională")  #
            if "ngm company" in content: indicii.append("NGM/PPP")  #
            res["legal"] = f"LEGAL ({', '.join(indicii)})" if indicii else "ILEGAL (Lipsă atestare)"

        # 5. AUTENTIFICARE
        btns = await page.query_selector_all("text=/Înregistrare|Registration|Sign Up/i")
        if btns:
            try:
                await btns[0].click(); await asyncio.sleep(2)
            except:
                pass

        form_text = await page.evaluate('() => document.body.innerText.toLowerCase()')
        if any(x in form_text for x in ["idnp", "cod personal"]):
            res["auth"] = "CONFORM (IDNP)"
        else:
            metode = []
            if any(x in form_text for x in ["telefon", "+373"]): metode.append("Tel")
            if "mail" in form_text: metode.append("Mail")
            if any(x in form_text for x in ["google", "facebook"]): metode.append("Social")
            res["auth"] = " | ".join(metode) if metode else "Analiză manuală"

    except Exception:
        res["auth"] = "Restricționat ASP" if este_la_asp else "Inaccesibil"
    finally:
        await page.close()
    return res


async def main():
    asp_data = await incarca_baza_date_asp()
    rezultate = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Tabel Consolă
        header_fmt = f"{'URL (RESURSĂ)':<35} | {'TIP SERVICII':<15} | {'AUTENTIFICARE':<20} | {'PUBLIC TINTA':<15} | {'REȚELE SOCIALE':<15} | {'LEGALITATE'}"
        print("\n" + "=" * 165)
        print(header_fmt)
        print("-" * 165)

        for url in SUSPECT_URLS:
            r = await proceseaza(context, url, asp_data)
            rezultate.append(r)
            print(
                f"{r['url'][:35]:<35} | {r['tip']:<15} | {r['auth']:<20} | {r['tinta']:<15} | {r['social']:<15} | {r['legal']}")

        await browser.close()

    # Salvare CSV (Excel)
    coloane = ["url", "tip", "auth", "tinta", "social", "legal"]
    with open('raport_investigatie.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=coloane)
        writer.writeheader()
        writer.writerows(rezultate)


if __name__ == "__main__":
    asyncio.run(main())