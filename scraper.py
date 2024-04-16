import requests
import csv
import time
url = "https://scanner.tradingview.com/america/scan"

payload = "{\"columns\":[\"name\",\"description\",\"logoid\",\"update_mode\",\"type\",\"typespecs\",\"close\",\"pricescale\",\"minmov\",\"fractional\",\"minmove2\",\"currency\",\"change\",\"volume\",\"relative_volume_10d_calc\",\"market_cap_basic\",\"fundamental_currency_code\",\"price_earnings_ttm\",\"earnings_per_share_diluted_ttm\",\"earnings_per_share_diluted_yoy_growth_ttm\",\"dividends_yield_current\",\"sector.tr\",\"market\",\"sector\",\"recommendation_mark\",\"exchange\"],\"ignore_unknown_fields\":false,\"options\":{\"lang\":\"en\"},\"range\":[0,15000],\"sort\":{\"sortBy\":\"market_cap_basic\",\"sortOrder\":\"desc\"},\"symbols\":{},\"markets\":[\"america\"],\"filter2\":{\"operator\":\"and\",\"operands\":[{\"operation\":{\"operator\":\"or\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"expression\":{\"left\":\"type\",\"operation\":\"equal\",\"right\":\"stock\"}},{\"expression\":{\"left\":\"typespecs\",\"operation\":\"has\",\"right\":[\"common\"]}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"expression\":{\"left\":\"type\",\"operation\":\"equal\",\"right\":\"stock\"}},{\"expression\":{\"left\":\"typespecs\",\"operation\":\"has\",\"right\":[\"preferred\"]}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"expression\":{\"left\":\"type\",\"operation\":\"equal\",\"right\":\"dr\"}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"expression\":{\"left\":\"type\",\"operation\":\"equal\",\"right\":\"fund\"}},{\"expression\":{\"left\":\"typespecs\",\"operation\":\"has_none_of\",\"right\":[\"etf\"]}}]}}]}}]}}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.tradingview.com/",
    "Content-Type": "text/plain;charset=UTF-8",
    "Origin": "https://www.tradingview.com",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive"
}

response = requests.request("POST", url, data=payload, headers=headers)

data_json = response.json()

lists = data_json["data"]

data_list = []
for item in lists:
    name = item['d'][0]
    price = item['d'][6]
    change = item['d'][12]
    volume = item['d'][13]
    relative_volume = item['d'][14]
    market_cap = item['d'][15]
    pe = item['d'][17]
    eps_diluted = item['d'][18]
    eps_diluted_growth = item['d'][19]
    dividends_yield = item['d'][20]
    sector = item['d'][22]

    data = {
        'name': name,
        'price': price,
        'change': change,
        'volume': volume,
        'relative_volume': relative_volume,
        'market_cap': market_cap,
        'pe': pe,
        'eps_diluted': eps_diluted,
        'eps_diluted_growth': eps_diluted_growth,
        'dividends_yield': dividends_yield,
        'sector': sector
    }

    data_list.append(data)
    time.sleep(3)

# Open a CSV file for writing
with open('stocks_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'price', 'change', 'volume', 'relative_volume', 'market_cap',
                  'pe', 'eps_diluted', 'eps_diluted_growth', 'dividends_yield', 'sector']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for data in data_list:
        writer.writerow(data)
