import yfinance as yf
import pandas as pd

class FinancialCollector:
    def get_coffee_prices(self):
        """
        Busca o preço futuro do café na bolsa.
        Usaremos um placeholder, pois o ticker exato de "Conilon" pode variar.
        """
        # Exemplo com um ticker de café genérico
        ticker = "JO=F"  # Ticker de futuros de café em YFinance
        data = yf.download(ticker, period="1mo")
        return data['Close']
