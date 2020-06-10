
import yfinance as yf
ticker_list = ["XYL", "GIB", "SAP", "HNR1.DE", "VNA.DE",
                "GIB.F", "RMS.PA", "DIM.PA", "SRT3.DE", "BBCA.JK",
                "KRX.IR", "URTH", "ACN", "CHGCY", "S6L.F", "NFPH.SG",
                "GOOG", "A0T.SG", "BRK-B", "AVGO", "EXPO", "FIS", "FISV",
                "HD", "ICE", "IUI1.F", "JPM", "MMC", "MXIM", "MPWR",
                "^IXIC", "NEE", "ORCL", "PKI", "POOL", "PGR", "ROP",
                "SC", "TFX", "TMO", "UNP", "VRSK", "V", "WM", "WEN", "ZTS"
                ]
return_dict = {}

for ticker in ticker_list:
    data = yf.Ticker(ticker)
    df = data.history(period="30d")

    df['close_diff'] = (df['Close'] - df['Close'].shift(1))/df['Close'].shift(1)*100
    df_zehn = df.iloc[-9:]
    df_zwanzig = df.iloc[-19:]
    df_dreisig = df

    df_zehn['cumsum_diff'] = df_zehn['close_diff'].cumsum()
    df_zwanzig['cumsum_diff'] = df_zwanzig['close_diff'].cumsum()
    df_dreisig['cumsum_diff'] = df_dreisig['close_diff'].cumsum()

    ticker_dict = {}
    ticker_dict['last 10 days'] = round(df_zehn['cumsum_diff'][-1], 2)
    ticker_dict['last 20 days'] = round(df_zwanzig['cumsum_diff'][-1], 2)
    ticker_dict['last month']= round(df_dreisig['cumsum_diff'][-1], 2)

    return_dict[ticker] = ticker_dict

for stock in return_dict:
    con = [True if x < 0 else False for x in  return_dict[stock].values()]
    if sum(con) > 0:
        print(str(stock) + ": " + str(return_dict[stock]))


