import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException

GOLD_18K_MILLIES = 0.175
GOLD_18K_PHYSICAL = 1
COIN_QUARTER = 4
COIN_HALF = 2
COIN_BAHAR = 2
CRYPTO_USDT = 1.35
CRYPTO_SHIB = 8500

url = "https://BrsApi.ir/Api/Market/Gold_Currency.php?key=BcDh6ALgW4TfCPPVDx2zAxKFXEyFdGi3"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
except HTTPError as e:
    status = e.response.status_code if e.response else None
    print(f"[HTTPError] status={status} - {e}")
except Timeout:
    print("⏱️ Timeout")
except ConnectionError:
    print("🌐 ConnectionError")
except RequestException as e:
    print(f"❗ RequestException: {e}")
else:
    print("✅ Data Processed.\n")

    prices = {}
    for section in ("gold", "currency", "cryptocurrency"):
        for item in data.get(section, []):
            prices[item["symbol"]] = item["price"]

    report = []
    total_toman = 0

    if GOLD_18K_MILLIES:
        value = GOLD_18K_MILLIES * prices["IR_GOLD_18K"]
        report.append(("18K Gold (Millies)", value))
        total_toman += value

    if GOLD_18K_PHYSICAL:
        value = GOLD_18K_PHYSICAL * prices["IR_GOLD_18K"]
        report.append(("18K Gold (Physical)", value))
        total_toman += value

    if COIN_QUARTER:
        value = COIN_QUARTER * prices["IR_COIN_QUARTER"]
        report.append(("Quarter Coin", value))
        total_toman += value

    if COIN_HALF:
        value = COIN_HALF * prices["IR_COIN_HALF"]
        report.append(("Half Coin", value))
        total_toman += value

    if COIN_BAHAR:
        value = COIN_BAHAR * prices["IR_COIN_BAHAR"]
        report.append(("Bahar Azadi Coin", value))
        total_toman += value

    if CRYPTO_USDT:
        value = CRYPTO_USDT * float(prices["USDT"]) * prices["USDT_IRT"]
        report.append(("Tether (USDT)", value))
        total_toman += value

    if CRYPTO_SHIB:
        value = CRYPTO_SHIB * float(prices["SHIB"]) * prices["USD"]
        report.append(("Shiba Inu", value))
        total_toman += value

    # Print CLI report
    print("📊 Portfolio Report:")
    for name, value in report:
        print(f" - {name:<20} : {value:,.0f} Toman")

    print("\n💰 Total Portfolio Value:", f"{total_toman:,.0f}", "Toman")
