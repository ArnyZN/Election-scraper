"""election_scraper.py: třetí projekt do Engeto Online Python Akademie

author: Arnošt Raab

email: arnost.raab@gmail.com

discord: Arnošt (Arny) R.#6219"""




import requests
import bs4
import sys
import csv


from bs4 import BeautifulSoup
from requests import get

zahlavi = ["cislo_obce", "nazev_obce", "volici_v_seznamu", "vydane_obalky", "odevzdane_obalky", "platne_hlasy"]
#funkce na spojeni slovníků do jednoho řádku pro konečný zápis do souboru
def spojeni_slovniku(*slovniky): 
    vysledny_slovnik = {} 
    for slovnik in slovniky: 
        vysledny_slovnik.update(slovnik) 
    return vysledny_slovnik 
#3 funkce pro každý z druhu tabulek na stránkách
def vyber_bunky_tab1(tr_tag: "bs4.element.ResultSet"):
    return {zahlavi[0]: tr_tag[0].get_text(), 
            zahlavi[1]: tr_tag[1].get_text()
            }
def vyber_bunky_tab2(tr_tag: "bs4.element.ResultSet"):
    return {zahlavi[2]: tr_tag[3].get_text(),
            zahlavi[3]: tr_tag[4].get_text(),
            zahlavi[4]: tr_tag[6].get_text(),
            zahlavi[5]: tr_tag[7].get_text(),
            }
def vyber_bunky_tab3(tr_tag: "bs4.element.ResultSet"):
        return {tr_tag[1].get_text(): tr_tag[2].get_text()}
    
def zapis_data(data, jmeno_souboru):
    with open(jmeno_souboru, mode="w", encoding="utf-8", newline="") as csv_soubor:
        sloupce = data[0].keys()
        zapis = csv.DictWriter(csv_soubor, fieldnames=sloupce)
        zapis.writeheader()
        zapis.writerows(data)

if len(sys.argv) != 3:
    print("Nemáš zadané dva parametry při spuštění, nemohu skript spustit!")
    quit()

print("Spouštím program!")
urls =[sys.argv[1]]
print(f"Stahuji data z: {urls[0]} ")
#dolování a spojování adres z href tagu tak, aby je bylo možno volat a scrapovat data  
odpoved_serveru = requests.get(urls[0])
soup = BeautifulSoup(odpoved_serveru.text, 'html.parser')
tabulky = soup.find_all("table", {"class": "table"})
for table in tabulky:
    radky = table.find_all("tr")
    for tr in radky[2:]:
        if tr.find("td", {"class": "cislo"}):
           a_tag=(tr.find("a"))
           urls.append("https://volby.cz/pls/ps2017nss/"+a_tag["href"])
        else:
            continue
#asi trochu kostrbaté, ale nenapadlo mě to jinak, každou tabulku na stránkách jsem opatřil indexem
#a dle toho řídím rozdělování dat, protože co tabulka to jiný druh uložení jednotlivých hodnot
list1 = []
list2 = []
list3 = []
for link in urls:
    indx = urls.index(link)
    odpoved_serveru = requests.get(link)
    soup = BeautifulSoup(odpoved_serveru.text, 'html.parser')
    tabulky = soup.find_all("table", {"class": "table"})
    for table in tabulky:
        indx2 = tabulky.index(table)
        radky = table.find_all("tr")
        for tr in radky[2:]:
            if indx == 0:
                list1.append(vyber_bunky_tab1(tr.find_all("td")))
            elif indx > 0 and indx2 == 0:
                list2.append(vyber_bunky_tab2(tr.find_all("td")))
            else:
                list3.append(vyber_bunky_tab3(tr.find_all("td")))             
#list tři obsahoval slovníky s daty o stranách, ale každý zvlášť a bylo potřeba je spojit tak, aby
#každý slovník obsahoval ne jednu stranu, ale všechny politické strany na stránce
list4 = []
temp = {}

for item in list3:
    for key in item.keys():
        if key not in temp:
            temp.update(item)
        else:
            list4.append(temp)
            temp = {} 
            temp.update(item)
list4.append(temp)

print(f"Zpracovávám data a zapisuji do souboru: {sys.argv[2]}")
#finální list, ve kterém spojuji list1, list2 a list4 (přeskládaný list3)
final_list = []

for (a, b, c) in zip(list1, list2, list4):
   final_list.append(spojeni_slovniku(a, b, c))
#zápis dat
zapis_data(final_list, sys.argv[2])