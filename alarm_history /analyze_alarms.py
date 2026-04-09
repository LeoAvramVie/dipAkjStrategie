import csv
import re
import glob
import os
import json
from collections import defaultdict
from datetime import datetime, timedelta
import io

try:
    import yfinance as yf
    import pandas as pd
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False
    print("yfinance or pandas not found. Backtest simulation will be skipped.")

# Dynamisch den Ordner des Skripts ermitteln, um Fehler mit Leerzeichen im Pfad zu vermeiden
directory = os.path.dirname(os.path.abspath(__file__))
# Recursive search for csv
csv_files = glob.glob(os.path.join(directory, "**/*.csv"), recursive=True)

# Note: In a real system you'd use datetime.now(), but we lock the date to match the project constraints
today = datetime(2026, 4, 10) # 10th of april so we have some days for backtesting of older april alarms
ten_days_ago = today - timedelta(days=15) # Relaxed a bit to test march/april

ticker_stats = defaultdict(lambda: {
    'count': 0, 'points': 0,
    'stop_sum': 0.0, 'tp_sum': 0.0, 'data_count': 0,
    'signal_types': []
})
daily_cluster = defaultdict(int)
daily_ticker_signals = defaultdict(list)

# Collections for Backtesting
backtest_trades = []

for file in sorted(csv_files):
    try:
        with open(file, 'r', encoding='utf-8', errors='replace', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            
            for fields in reader:
                if len(fields) < 4:
                    continue
                desc = fields[3]
                
                # Check for JSON payload first
                payload = None
                json_match = re.search(r'---\s*JSON PAYLOAD\s*---\s*(\{.*\})', desc, re.DOTALL)
                if json_match:
                    try:
                        payload = json.loads(json_match.group(1))
                    except:
                        pass
                
                # Datum
                date_match = re.search(r'ZEITPUNKT:\s*(\d{4}-\d{2}-\d{2})', desc)
                if not date_match:
                    continue
                alert_date_str = date_match.group(1)
                try:
                    alert_date = datetime.strptime(alert_date_str, "%Y-%m-%d")
                except:
                    continue
                
                if alert_date < ten_days_ago:
                    continue
                
                # Ticker
                if payload and 'ticker' in payload:
                    ticker = payload['ticker']
                else:
                    ticker_match = re.search(r'TICKER:\s*([A-Za-z0-9\.\-]+)', desc)
                    if not ticker_match:
                        continue
                    ticker = ticker_match.group(1).strip()
                
                # Signal Typ (aus erstem Teil der Beschreibung)
                first_line = desc.split('\n')[0]
                signal_type = ""
                points = 0
                if "ELITE" in first_line or "AKJ ELITE" in first_line:
                    signal_type = "💎 ELITE"
                    points = 4
                elif "GOLDEN" in first_line:
                    signal_type = "🌟 GOLDEN"
                    points = 3
                elif "FEUER FREI" in first_line:
                    signal_type = "🟢 FEUER FREI"
                    points = 2
                elif "LAUERN" in first_line:
                    signal_type = "📡 LAUERN"
                    points = 1
                
                if points == 0:
                    continue
                
                direction = "SHORT" if "SHORT" in first_line else "LONG"
                signal_full = f"{signal_type} {direction}"
                
                # Sektor
                sektor_match = re.search(r'Sektor:\s*(.+?)(?:\n|\r|$)', desc)
                sektor = sektor_match.group(1).strip() if sektor_match else "?"
                
                # Parse Stats & Setup for Backtesting
                stop_str = None
                tp_str = None
                
                if payload:
                    stop_str = payload.get('stop_wall')
                    tp_str = payload.get('tp_resistance')
                    sp = payload.get('sp')
                    sl = payload.get('sl')
                    tp = payload.get('tp')
                    signal_id = payload.get('signal')
                    
                    if sp and sl and tp and points >= 3:
                        backtest_trades.append({
                            'date': alert_date,
                            'ticker': ticker,
                            'direction': direction,
                            'signal': signal_type,
                            'sp': float(sp),
                            'sl': float(sl),
                            'tp': float(tp)
                        })
                else:
                    stop_m = re.search(r'Stopversicherung:\s*([\d\.]+)%', desc)
                    tp_m = re.search(r'TP Widerstand:\s*([\d\.]+)%', desc)
                    if stop_m and tp_m:
                        stop_str = stop_m.group(1)
                        tp_str = tp_m.group(1)
                        
                ticker_stats[ticker]['count'] += 1
                ticker_stats[ticker]['points'] += points
                ticker_stats[ticker]['signal_types'].append(signal_full)
                
                if stop_str is not None and tp_str is not None:
                    ticker_stats[ticker]['stop_sum'] += float(stop_str)
                    ticker_stats[ticker]['tp_sum'] += float(tp_str)
                    ticker_stats[ticker]['data_count'] += 1
                
                daily_cluster[alert_date_str] += 1
                
                if points >= 2:  # Feuer Frei und höher
                    daily_ticker_signals[alert_date_str].append((ticker, signal_full, sektor))
    
    except Exception as e:
        continue

# ============================================
# BACKTESTING ENGINE
# ============================================
bt_results = {'elite_win': 0, 'elite_loss': 0, 'golden_win': 0, 'golden_loss': 0, 'unfilled': 0, 'expired': 0}
total_r = 0.0

if YF_AVAILABLE and backtest_trades:
    unique_tickers = list(set([t['ticker'] for t in backtest_trades]))
    # Download data from 15 days ago to now to cover dates
    start_date = (today - timedelta(days=20)).strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=1)).strftime("%Y-%m-%d") # Until current to ensure latest info
    
    print(f"\n[Backtest] Lade historische Daten für {len(unique_tickers)} Ticker...")
    try:
        data = yf.download(unique_tickers, start=start_date, end=end_date, progress=False)
        hist_data = {}
        
        # Depending on multi-index structure:
        if len(unique_tickers) == 1:
            hist_data[unique_tickers[0]] = data
        else:
            for t in unique_tickers:
                # yfinance returns multi-index when multiple tickers
                hist_data[t] = data.xs(t, axis=1, level=1) if isinstance(data.columns, pd.MultiIndex) else data
                
        for t in backtest_trades:
            ticker = t['ticker']
            alert_d = t['date']
            df = hist_data.get(ticker)
            if df is None or df.empty:
                t['outcome'] = 'NO_DATA'
                continue
                
            # Filter days after alert date
            df_future = df[df.index > pd.Timestamp(alert_d)]
            if df_future.empty:
                t['outcome'] = 'NO_DATA'
                continue
            
            # Limit to 5 trading days
            df_sim = df_future.head(5)
            
            entry_filled = False
            outcome = 'EXPIRED' # default if filled but neither stop nor tp hit 
            r_gained = 0.0
            
            sp, sl, tp, dir_ = t['sp'], t['sl'], t['tp'], t['direction']
            
            for index, row in df_sim.iterrows():
                h, l = row['High'], row['Low']
                c = row['Close']
                
                # Check Entry
                if not entry_filled:
                    if dir_ == 'LONG' and h >= sp:
                        entry_filled = True
                    elif dir_ == 'SHORT' and l <= sp:
                        entry_filled = True
                        
                if entry_filled:
                    # Check SL/TP on the SAME day of entry (worst case scenario: both hit -> assume SL!)
                    hit_sl = False
                    hit_tp = False
                    if dir_ == 'LONG':
                        if l <= sl: hit_sl = True
                        if h >= tp: hit_tp = True
                    else:
                        if h >= sl: hit_sl = True
                        if l <= tp: hit_tp = True
                    
                    if hit_sl:
                        outcome = 'LOSS'
                        r_gained = -1.0
                        break
                    elif hit_tp:
                        outcome = 'WIN'
                        r_gained = 1.0 # Standard 1R win
                        break
            
            if not entry_filled:
                outcome = 'UNFILLED'
                bt_results['unfilled'] += 1
            elif outcome == 'EXPIRED':
                # Time exit on close of day 5
                last_c = df_sim.iloc[-1]['Close']
                if dir_ == 'LONG':
                    r_gained = (last_c - sp) / (tp - sp) if (tp - sp) != 0 else 0
                else:
                    r_gained = (sp - last_c) / (sp - tp) if (sp - tp) != 0 else 0
                
                if r_gained > 0:
                    outcome = 'WIN'
                else:
                    outcome = 'LOSS'
                bt_results['expired'] += 1
                
            t['outcome'] = outcome
            t['r_gained'] = r_gained
            
            if outcome == 'WIN':
                if "ELITE" in t['signal']: bt_results['elite_win'] += 1
                else: bt_results['golden_win'] += 1
                total_r += r_gained
            elif outcome == 'LOSS':
                if "ELITE" in t['signal']: bt_results['elite_loss'] += 1
                else: bt_results['golden_loss'] += 1
                total_r += r_gained

    except Exception as e:
        print(f"[ERROR] Fehler beim YF Download: {e}")

# ============================================
# OUTPUT 1: TOP 10 Ticker (Ranking)
# ============================================
results = []
for ticker, data in ticker_stats.items():
    if data['count'] >= 3:
        avg_stop = (data['stop_sum'] / data['data_count']) if data['data_count'] > 0 else 0
        avg_tp = (data['tp_sum'] / data['data_count']) if data['data_count'] > 0 else 0
        if avg_tp < 10.0:
            results.append({
                'Ticker': ticker,
                'Score': data['points'],
                'Alerts': data['count'],
                'Avg_Stop': avg_stop,
                'Avg_TP': avg_tp,
                'Signals': sorted(set(data['signal_types']))
            })

results.sort(key=lambda x: (x['Alerts'], x['Score']), reverse=True)

with open(f"{directory}/sniper_report.txt", "w") as f:
    
    def log(msg):
        print(msg)
        f.write(msg + "\n")

    log("=" * 70)
    log("   📊 AKJ SNIPER-REPORT — TOP 10 AKTIEN (Letzte 15 Tage)")
    log("=" * 70)
    if not results:
        log("  Keine Ticker mit >= 3 Alarmen & Ø TP < 10% gefunden.")
    else:
        log(f"{'#':<3} {'Ticker':<8} {'Alarme':<8} {'Score':<7} {'Ø Stop':>7} {'Ø TP':>7}  Signale")
        log("-" * 70)
        for i, res in enumerate(results[:10], 1):
            sigs = ", ".join(res['Signals'])
            log(f"{i:<3} {res['Ticker']:<8} {res['Alerts']:<8} {res['Score']:<7} {res['Avg_Stop']:>6.1f}%  {res['Avg_TP']:>6.1f}%  {sigs}")

    # ============================================
    # OUTPUT 2: Feuer Frei & Golden pro Tag
    # ============================================
    log("\n")
    log("=" * 70)
    log("   🔥 FEUER FREI & GOLDEN SETUPS — Pro Handelstag")
    log("=" * 70)

    if not daily_ticker_signals:
        log("  Keine Feuer Frei / Golden Signale im Zeitraum.")
    else:
        for day in sorted(daily_ticker_signals.keys(), reverse=True):
            signals = daily_ticker_signals[day]
            elite  = [(t,s,k) for t,s,k in signals if "ELITE" in s]
            golden = [(t,s,k) for t,s,k in signals if "GOLDEN" in s]
            feuer  = [(t,s,k) for t,s,k in signals if "FEUER" in s]
            
            total = len(signals)
            log(f"\n📅 {day}  ──  {total} Signale gesamt  ({len(elite)} Elite | {len(golden)} Golden | {len(feuer)} Feuer Frei)")
            log("  " + "-" * 60)
            
            for ticker, signal, sektor in elite:
                log(f"  💎 {ticker:<10} {signal:<28} {sektor}")
            for ticker, signal, sektor in golden:
                log(f"  🌟 {ticker:<10} {signal:<28} {sektor}")
            for ticker, signal, sektor in feuer:
                log(f"  🟢 {ticker:<10} {signal:<28} {sektor}")

    # ============================================
    # OUTPUT 3: Cluster-Tage
    # ============================================
    log("\n")
    log("=" * 70)
    log("   ⚡ CLUSTER TAGE (Tage mit höchster Alarm-Dichte)")
    log("=" * 70)
    sorted_days = sorted(daily_cluster.items(), key=lambda x: x[1], reverse=True)
    for day, count in sorted_days[:7]:
        bar = "█" * min(count // 10, 35)
        log(f"  {day}  {count:>5} Alarme  {bar}")

    # ============================================
    # OUTPUT 4: Backtest Performance
    # ============================================
    log("\n")
    log("=" * 70)
    log("   📈 STRATEGY BACKTEST (ELITE & GOLDEN SETUPS)")
    log("=" * 70)
    
    if YF_AVAILABLE and backtest_trades:
        e_win = bt_results['elite_win']
        e_loss = bt_results['elite_loss']
        e_tot = e_win + e_loss
        g_win = bt_results['golden_win']
        g_loss = bt_results['golden_loss']
        g_tot = g_win + g_loss
        
        tot_trades = e_tot + g_tot
        win_rate = ((e_win + g_win) / tot_trades * 100) if tot_trades > 0 else 0
        e_win_rate = (e_win / e_tot * 100) if e_tot > 0 else 0
        g_win_rate = (g_win / g_tot * 100) if g_tot > 0 else 0
        
        log(f"  Trades insgesamt analysiert: {len(backtest_trades)}")
        log(f"  Davon abgelaufen (Kein Entry-Trigger): {bt_results['unfilled']}")
        log(f"  Time-Exits (nach 5 Tagen weder TP noch SL): {bt_results['expired']}\n")
        
        log("  --- GEWINNRATEN ---")
        log(f"  🏆 Gesamt-Winrate:  {win_rate:>5.1f}%   ({e_win + g_win} Gewinne, {e_loss + g_loss} Verluste)")
        log(f"  💎 Elite Setups:    {e_win_rate:>5.1f}%   ({e_win} Gewinne, {e_loss} Verluste)")
        log(f"  🌟 Golden Setups:   {g_win_rate:>5.1f}%   ({g_win} Gewinne, {g_loss} Verluste)")
        log("\n  --- KAPITAL-ENTWICKLUNG ---")
        log(f"  Erwirtschaftete R (Risk-Unit): {total_r:>7.2f} R")
        log(f"  (Bei 100€ Risk pro Trade entspräche das ca. {total_r * 100:.2f} €)")
    else:
        log("  Backtest übersprungen (Zu wenig Daten oder yfinance/pandas fehlt).")
    
    log("\n[Report Ende]")
