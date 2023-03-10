import requests
from datetime import date
from pathlib import Path
import json
import datetime


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
    
    timestamp = datetime.datetime.now().isoformat()
    date = data[0].split()[0]
    return {"timestamp": timestamp,"date": date, "rates": exchange_rate_list}


def save_data_into_file(data, filename):
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    with open(filename, mode="w", encoding="utf-8") as file:
        file.write(json_data)


def get_data_from_file(filename):
    with open(filename, mode="r", encoding="utf-8") as file:
        data = file.read()
    
    return json.loads(data)


def get_today_date_as_string():
    return date.today().strftime("%d.%m.%Y")


def rates_update_needed(FILENAME):
    today = get_today_date_as_string()
    if not Path(FILENAME).is_file():
        return True
    data = get_data_from_file(FILENAME)
    if data["date"] != today:
        timestamp_from_file = datetime.datetime.fromisoformat(data["timestamp"])
        now = datetime.datetime.now()
        diff_minutes = (now - timestamp_from_file).total_seconds() // 60
        if diff_minutes > 120:
            return True
    return False


def get_rates():
    FILENAME = "exchange_rates.txt"
    NEED_NEW_DATA = rates_update_needed(FILENAME)
    today = get_today_date_as_string()

    if NEED_NEW_DATA:
        url = f"https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date={today}"

        response = requests.get(url)
        
        if response.status_code == 200:
            exchange_rate_list = create_exchange_rate_list(response)
            save_data_into_file(exchange_rate_list, FILENAME)
        else:
            # TODO response code not 200
            raise NotImplementedError("Response code not 200")
    else:
        exchange_rate_list = get_data_from_file(FILENAME)

    return exchange_rate_list
