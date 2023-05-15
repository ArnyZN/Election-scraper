# Election-scraper
# Popis
Election-scraper obsahuje kód, který po zadání požadovaných parametrů při spuštění umí z dané  webové stránky přečíst požadovaná data a uložit je do csv souboru.
# Jak to funguje?
Uživatel musí pro správné spuštění zadat do příkazové řádky krom samotného hlavního souboru .py rovněž
dva parametry:
    1. parametr - jde o odkaz na stránku, z které má daná data číst. V tomto případě jde o odkaz na webu www.volby.cz(Úvod > Poslanecká sněmovna 2017 > Výsledky hlasování – výběr územní úrovně) např. pro Benešov by to bylo zde https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101 
    2. parametr - uživatel zadá jméno souboru (např. zde vysledekscrapingu.csv).
Oba parametry je nutné uzavřít do závorek. Příklad spuštění pro územní celek Benešov: python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledekscrapingu.csv"

Nutností pro správnou funkci programu je rovněž instalace knihoven uvedených v requirements.txt (instalace: pip install -r requirements.txt z příkazového řádku)

# Ukázka výsledné struktury csv 
cislo_obce,nazev_obce,volici_v_seznamu,vydane_obalky,odevzdane_obalky,platne_hlasy.......
533173,Barchovice,185,132,132,132,8,0,0,11,0,14,11,0,0,2,1,0,27,0,0,8,37,0,2,2,0,1,0,1,7,0
533181,Bečváry,822,492,492,491,41,0,1,32,0,94,48,3,3,3,0,0,34,0,0,10,167,0,3,6,0,2,0,2,41,1
533190,Bělušice,229,123,123,123,9,0,0,12,0,16,18,0,1,0,0,0,8,0,0,0,46,0,0,1,0,0,0,0,12,0
