"""Core Goldfolio application logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

API_URL = "https://BrsApi.ir/Api/Market/Gold_Currency.php?key=BcDh6ALgW4TfCPPVDx2zAxKFXEyFdGi3"
REQUEST_TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class Holding:
    label: str
    symbol: str
    quantity: float
    multiplier_symbol: str | None = None


DEFAULT_HOLDINGS: Tuple[Holding, ...] = (
    Holding("18K Gold (Millies)", "IR_GOLD_18K", 0.175),
    Holding("18K Gold (Physical)", "IR_GOLD_18K", 1),
    Holding("Quarter Coin", "IR_COIN_QUARTER", 4),
    Holding("Half Coin", "IR_COIN_HALF", 2),
    Holding("Bahar Azadi Coin", "IR_COIN_BAHAR", 2),
    Holding("Tether (USDT)", "USDT", 1.35, multiplier_symbol="USDT_IRT"),
    Holding("Shiba Inu", "SHIB", 8500, multiplier_symbol="USD"),
)


def fetch_market_data(url: str = API_URL) -> dict:
    """Fetch market data from the source API."""
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json, text/plain, */*"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("Unexpected API response shape")
    return payload


def build_price_map(payload: dict) -> Dict[str, float]:
    prices: Dict[str, float] = {}
    for section in ("gold", "currency", "cryptocurrency"):
        for item in payload.get(section, []) or []:
            symbol = item.get("symbol")
            price = item.get("price")
            if symbol is None or price is None:
                continue
            prices[str(symbol)] = float(price)
    return prices


def compute_portfolio(
    prices: Dict[str, float],
    holdings: Iterable[Holding] = DEFAULT_HOLDINGS,
) -> Tuple[List[Tuple[str, float]], float]:
    report: List[Tuple[str, float]] = []
    total_toman = 0.0

    for holding in holdings:
        if holding.quantity == 0:
            continue

        if holding.symbol not in prices:
            raise KeyError(f"Missing price for symbol: {holding.symbol}")

        value = holding.quantity * prices[holding.symbol]

        if holding.multiplier_symbol:
            if holding.multiplier_symbol not in prices:
                raise KeyError(f"Missing price for symbol: {holding.multiplier_symbol}")
            value *= prices[holding.multiplier_symbol]

        report.append((holding.label, value))
        total_toman += value

    return report, total_toman


def run_cli() -> int:
    try:
        payload = fetch_market_data()
        prices = build_price_map(payload)
        report, total_toman = compute_portfolio(prices)
    except HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        print(f"[HTTPError] status={status} - {e}")
        return 1
    except Timeout:
        print("⏱️ Timeout")
        return 1
    except ConnectionError:
        print("🌐 ConnectionError")
        return 1
    except RequestException as e:
        print(f"❗ RequestException: {e}")
        return 1
    except (ValueError, KeyError) as e:
        print(f"❗ DataError: {e}")
        return 1

    print("✅ Data Processed.\n")
    print("📊 Portfolio Report:")
    for name, value in report:
        print(f" - {name:<20} : {value:,.0f} Toman")

    print("\n💰 Total Portfolio Value:", f"{total_toman:,.0f}", "Toman")
    return 0
