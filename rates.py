import requests
from datetime import date
from pathlib import Path
import json


def create_exchange_rate_list(response):
    exchange_rate_list = []
    data = response.text.strip().split("\n")
    for row in data[2:]:
        country, currency, amount, code, rate = row.split("|")
        rate = float(rate.replace(",", "."))
        exchange_rate_data = {"country": country,
                "currency": currency,
                "amount": int(amount),
                "code": code,
                "rate": rate}
        exchange_rate_list.append(exchange_rate_data)

    return {"date": data[0].split()[0], "rates": exchange_rate_list}


def save_data_into_file(data, filename):
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    with open(filename, mode="w", encoding="utf-8") as file:
        file.write(json_data)
        print(f"Data written into '{filename}'!")


def get_data_from_file(filename):
    with open(filename, mode="r", encoding="utf-8") as file:
        data = file.read()
    
    return json.loads(data)

# Dnešní datum v textové podobě a správném formátu
today = date.today().strftime("%d.%m.%Y")
print(f"Today is {today}")

# POZOR - Data pro aktuální pracovní den jsou k dispozici po 14:30
# https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu

# Nejdříve se podívám, jestli už soubor s daty mám - mohou nastat tyto situace
#      1. soubor existuje a obsahuje dnešní data
#      2. soubor existuje a obsahuje neaktuální data -> musím stáhnout nová data
#      3. soubor neexistuje -> musím stáhnout nová data

FILENAME = "exchange_rates.txt"
NEED_NEW_DATA = False

# Zjistím, zda soubor existuje
path = Path(FILENAME)
if path.is_file():
    # soubor existuje = zjistím, zda obsahuje aktuální data
    # pokud ne, tak potřebuji nová data
    data = get_data_from_file(FILENAME)
    if data["date"] != today:
        NEED_NEW_DATA = True
else:
    # soubor neexistuje
    NEED_NEW_DATA = True

if NEED_NEW_DATA:
    url = f"https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date={today}"

    response = requests.get(url)
    
    if response.status_code == 200:
        exchange_rate_list = create_exchange_rate_list(response)
        save_data_into_file(exchange_rate_list, FILENAME)
    else:
        # TODO
        print("this should be implemented")
else:
    exchange_rate_list = get_data_from_file(FILENAME)

# na více míst by se muselo dát kontrola na výjimky, ale to můžeme probrat pak

# když pak chci udělat tu konverzi, tak tady je trocha matematiky pro cenu 1000 Kč
price = 1000

print(f"{price} Kč je:")
for item in exchange_rate_list["rates"]:
    code = item["code"]
    amount = item["amount"]
    rate = item["rate"]
    converted_price = round((amount * price) / rate, 2)
    print(f"  {code} {converted_price}")
