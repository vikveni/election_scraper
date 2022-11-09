"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Viktor Veniger
email: viktorveniger@gmail.com
discord: VikVeni#8755
"""

import requests
from bs4 import BeautifulSoup
import sys
import csv

header = ["Kód obce",
          "Název obce",
          "Voliči v seznamu",
          "Vydané obálky",
          "Platné hlasy"]


def main():
    url = sys.argv[1]
    file_name = sys.argv[2]
    codes = code_of_city(url)
    names = names_of_cities(url)
    data = scraping(url)
    links = link_for_datas(url)
    if valid_link(url, file_name) is True:
        print("Downloading data from: ", str(sys.argv[1]),
              "Storing data into: ", str(sys.argv[2]))
        csv_header(file_name)
        output = []
        votes = []
        for link in links:
            pv = pparties_votes(link)
            votes.append(pv)
        for i in range(len(link_for_datas(url))):
            output.append([codes.pop(0), names.pop(0)] + data.pop(0) + votes.pop(0))
        csv_write(file_name, output)
        print(f"Data are stored in {file_name}...")


def valid_link(input_link, input_file):
    if "https://volby.cz/pls/ps2017nss/" not in input_link and input_file.endswith(".csv") and len(sys.argv) == 3:
        return True
    else:
        print("WRONG INPUT")
        quit()


def url_respond(url):
    respond = requests.get(url).text
    return BeautifulSoup(respond, "html.parser")


def link_for_datas(url):
    links = []
    soup = url_respond(url)
    for link in soup.select("td.cislo a"):
        links.append("https://volby.cz/pls/ps2017nss/" + link["href"])
    return links


def code_of_city(url):
    data = url_respond(url)
    codes = []
    for code in data.find_all('td', {'class': 'cislo'}):
        all_codes = code.text.replace('\xa0', '')
        codes.append(all_codes)
    return codes


def names_of_cities(url):
    data = url_respond(url)
    towns = []
    for town in data.find_all('td', {'class': 'overflow_name'}):
        all_towns = town.text.replace("\xa0", "")
        towns.append(all_towns)
    return towns


def scraping(url):
    data = []
    links = link_for_datas(url)
    for link in links:
        souped_url = url_respond(link)
        datas = [souped_url.find("td", headers="sa2").text.replace("\xa0", ""),
                 souped_url.find("td", headers="sa3").text.replace("\xa0", ""),
                 souped_url.find("td", headers="sa6").text.replace("\xa0", "")]
        data.append(datas)
    return data


def names_of_pparties():
    names = []
    souped = url_respond("https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=506761&xvyber=7103")
    for name in souped.find_all("td", {"class": "overflow_name"}):
        names.append(name.get_text(""))
    return names


def pparties_votes(url):
    votes = []
    soup = url_respond(url)
    for td in soup.find_all('td', {'class': 'cislo', 'headers': 't1sa2 t1sb3'}):
        v = td.text.replace('\xa0', '')
        votes.append(v)
    for td in soup.find_all('td', {'class': 'cislo', 'headers': 't2sa2 t2sb3'}):
        v = td.text.replace('\xa0', '')
        votes.append(v)
    return votes


def csv_header(file_name):
    header.extend(names_of_pparties())
    with open(f"{file_name}", "w", newline='') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(header)


def csv_write(file_name, data):
    with open(file_name, "a+", newline="") as file_csv:
        write = csv.writer(file_csv)
        write.writerows(data)


if __name__ == "__main__":
    main()
