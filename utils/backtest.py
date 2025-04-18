import pandas as pd

def backtest_strategy(df, signals, sl_pct, tp_pct):
    equity = 10000
    balance = equity
    results = []

    for signal in signals.itertuples():
        entry_price = signal.Price
        is_buy = signal.Signal == 'Buy'

        sl_price = entry_price * (1 - sl_pct / 100) if is_buy else entry_price * (1 + sl_pct / 100)
        tp_price = entry_price * (1 + tp_pct / 100) if is_buy else entry_price * (1 - tp_pct / 100)

        for i in range(df.index.get_loc(signal.Datetime), len(df)):
            high = df['High'].iloc[i]
            low = df['Low'].iloc[i]

            if is_buy:
                if low <= sl_price:
                    pnl = -sl_pct
                    break
                elif high >= tp_price:
                    pnl = tp_pct
                    break
            else:
                if high >= sl_price:
                    pnl = -sl_pct
                    break
                elif low <= tp_price:
                    pnl = tp_pct
                    break
        balance *= (1 + pnl / 100)
        results.append(balance)

    return pd.DataFrame({"Equity": results}), results