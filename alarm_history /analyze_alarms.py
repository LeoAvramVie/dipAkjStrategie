import csv
import re
import glob
import os
from collections import defaultdict
from datetime import datetime, timedelta
import io

directory = "/Users/leoavram/Desktop/indikator /dipAkjStrategie/alarm_history "
csv_files = glob.glob(os.path.join(directory, "*.csv"))

today = datetime(2026, 4, 4)
ten_days_ago = today - timedelta(days=10)

ticker_stats = defaultdict(lambda: {
    'count': 0, 'points': 0,
    'stop_sum': 0.0, 'tp_sum': 0.0, 'data_count': 0,
    'signal_types': []
})
daily_cluster = defaultdict(int)
daily_ticker_signals = defaultdict(list)

def parse_row_desc(row_text):
    """Extrahiert die Beschreibung aus einer CSV-Zeile"""
    # Beschreibung ist das 4. Feld (Index 3), eingebettet in Anführungszeichen
    # Wir nutzen csv.reader korrekt
    try:
        reader = csv.reader(io.StringIO(row_text))
        for fields in reader:
            if len(fields) >= 4:
                return fields[3]
    except:
        pass
    return None

for file in sorted(csv_files):
    try:
        with open(file, 'r', encoding='utf-8', errors='replace', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            
            for fields in reader:
                if len(fields) < 4:
                    continue
                desc = fields[3]
                
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
                
                # Volumen
                stop_match = re.search(r'Stopversicherung:\s*([\d\.]+)%', desc)
                tp_match = re.search(r'TP Widerstand:\s*([\d\.]+)%', desc)
                
                ticker_stats[ticker]['count'] += 1
                ticker_stats[ticker]['points'] += points
                ticker_stats[ticker]['signal_types'].append(signal_full)
                
                if stop_match and tp_match:
                    ticker_stats[ticker]['stop_sum'] += float(stop_match.group(1))
                    ticker_stats[ticker]['tp_sum'] += float(tp_match.group(1))
                    ticker_stats[ticker]['data_count'] += 1
                
                daily_cluster[alert_date_str] += 1
                
                if points >= 2:  # Feuer Frei und höher
                    daily_ticker_signals[alert_date_str].append((ticker, signal_full, sektor))
    
    except Exception as e:
        continue

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

print("=" * 70)
print("   📊 AKJ SNIPER-REPORT — TOP 10 AKTIEN (Letzte 10 Tage)")
print("=" * 70)
if not results:
    print("  Keine Ticker mit >= 3 Alarmen & Ø TP < 10% gefunden.")
else:
    print(f"{'#':<3} {'Ticker':<8} {'Alarme':<8} {'Score':<7} {'Ø Stop':>7} {'Ø TP':>7}  Signale")
    print("-" * 70)
    for i, res in enumerate(results[:10], 1):
        sigs = ", ".join(res['Signals'])
        print(f"{i:<3} {res['Ticker']:<8} {res['Alerts']:<8} {res['Score']:<7} {res['Avg_Stop']:>6.1f}%  {res['Avg_TP']:>6.1f}%  {sigs}")

# ============================================
# OUTPUT 2: Feuer Frei & Golden pro Tag
# ============================================
print("\n")
print("=" * 70)
print("   🔥 FEUER FREI & GOLDEN SETUPS — Pro Handelstag")
print("=" * 70)

if not daily_ticker_signals:
    print("  Keine Feuer Frei / Golden Signale im Zeitraum.")
else:
    for day in sorted(daily_ticker_signals.keys()):
        signals = daily_ticker_signals[day]
        elite  = [(t,s,k) for t,s,k in signals if "ELITE" in s]
        golden = [(t,s,k) for t,s,k in signals if "GOLDEN" in s]
        feuer  = [(t,s,k) for t,s,k in signals if "FEUER" in s]
        
        total = len(signals)
        print(f"\n📅 {day}  ──  {total} Signale gesamt  ({len(elite)} Elite | {len(golden)} Golden | {len(feuer)} Feuer Frei)")
        print("  " + "-" * 60)
        
        for ticker, signal, sektor in elite:
            print(f"  💎 {ticker:<10} {signal:<28} {sektor}")
        for ticker, signal, sektor in golden:
            print(f"  🌟 {ticker:<10} {signal:<28} {sektor}")
        for ticker, signal, sektor in feuer:
            print(f"  🟢 {ticker:<10} {signal:<28} {sektor}")

# ============================================
# OUTPUT 3: Cluster-Tage
# ============================================
print("\n")
print("=" * 70)
print("   ⚡ CLUSTER TAGE (Tage mit höchster Alarm-Dichte)")
print("=" * 70)
sorted_days = sorted(daily_cluster.items(), key=lambda x: x[1], reverse=True)
for day, count in sorted_days[:7]:
    bar = "█" * min(count // 10, 35)
    print(f"  {day}  {count:>5} Alarme  {bar}")

print("\n[Report Ende]")
