# AKJ 2.0 Sniper-Commander
## Das taktische Lagezentrum (v20.6 Elite)

---
TEIL 1: FACHLICHES DOSSIER (System-Handbuch)
---

Detaillierte, technische Aufschlüsselung des AKJ 2.0 Sniper-Commander v20.6.
Das System wurde in v20.6 um drei kritische Logik-Fixes erweitert:
(1) Wochentrend-Midline-Reset, (2) Tagesscharf-Midline-Reset, (3) Zonen-Check im Signal-Flow.

---
### I. Das Interaktive Cockpit (Dashboard)
Das HUD ist logisch in Blöcken gruppiert, um dir während des Tradings den perfekten
Überblick über Kontext, Metriken und Exekution zu geben.

💡 Die Werte im Cockpit besitzen interaktive Tooltips. Wenn du mit der Maus (Mouse-over)
   über die Parameter-Titel in TradingView fährst, liefert das System dir sofortige
   strategische Erklärungen.

COCKPIT BLÖCKE:
---------------
1. STATUS-ZEILE
   - Zeigt den aktuellen Signalzustand: 💎 AKJ ELITE / 🌟 GOLDEN / 🟢 FEUER FREI / 📡 LAUERN / NO SIGNAL
   - Zeigt außerdem das aktive Risiko-Regime (ALPHA / DELTA / OMEGA) und einen Cooldown-Timer.

2. MARKT-KONTEXT
   - 🌍 Sektor:        Automatisch erkannter Sektor-ETF (z.B. SMH für Halbleiter, XLE für Energie).
   - 💪 Rel. Stärke:   Vergleich der Aktie mit dem Sektor über 20 Tage. STARK = Outperformance.
   - 📈 Weinstein:     Stage 2 = institutionelle Akkumulation (Long). Stage 4 = Distribution (Short).

3. TREND-ANALYSE (v20.6 Fix)
   - 📅 Wochentrend:   BULLISCH / NEUTRAL / BÄRISCH.
     → [v20.6 FIX] Wird jetzt sofort auf NEUTRAL gesetzt, wenn der Wochenschlusskurs
       unter die Wochi-Mittellinie (SMA 10, Wochenbasis) fällt – nicht erst am unteren Band!
   - ☀️ Tagestrend:    LONG (Radar/Scharf) / SHORT (Radar/Scharf) / NEUTRAL.
     → [v20.6 FIX] Scharf-Modus endet sofort, wenn der Tagesschlusskurs die Tages-Mittellinie
       (SMA 10, Tagesbasis) kreuzt – nicht erst am unteren Band!

4. SNIPER METRIKEN
   - 📊 Risk-O-Meter:  Dynamische Positionsgröße in €. Passt sich VIX und ATR an.
   - 🛡️ Risk-Mode:    ALPHA (VIX < 25) / DELTA (VIX 25-35) / OMEGA (VIX > 35)
   - ⚓ Anchor-Info:   Startpunkt der Anchored-Volume-Analyse (ab letztem Weinstein-Wechsel).
   - 📐 Vacuum Quality: Zeigt ob der Weg zum TP historisch frei ist (< max. TP-Density %).

5. SIGNAL-VALIDIERUNG
   - 🕹️ Momentum (WPR): Williams %R (Periode 4). Trigger bei 80/20 (Feuer), Radar bei 70/30.
   - 🕯️ Kerzenregel:   Prüft ob die Kerze eine echte Impulskerze ist (kein Doji, Richtung stimmt).
   - 🛡️ Stopversicherung: Volumen-Mauer am Stop-Level in %. Zielwert für FEUER: > 1.5%.
   - 🚧 TP Widerstand:  Volumen-Widerstand bis zum Ziel in %. Zielwert: < 15% (FEUER) / < 8% (GOLDEN).
   - 🔭 Bollinger Check: [v20.6 FIX] Jetzt aktiv im Signal-Flow! Bestimmt ob Preis in der richtigen
     Bollinger-Zone ist für ein FEUER oder GOLDEN Signal.
     → LONG ZONE / LONG EXTREME  = Erlaubt Long-Signale
     → SHORT ZONE / SHORT EXTREME = Erlaubt Short-Signale
     → Im Scharf-Modus (Walking the Bands) wird dieser Check automatisch überbrückt.

6. ORDER-MATRIX
   - 🎯 SP (Stoppreis):  Dein Einstiegs-Trigger-Preis. Platziere hier Stop-Buy / Stop-Sell.
   - 🤝 LP (Limitpreis): Gap-Schutz. Um 0.2% versetzt vom SP (einstellbar).
   - 🔢 Stk (Anzahl):    Exakte Stückzahl für punktgenaues 1R Risiko.
   - 💸 TP (Teilverkauf): 1:1 CRV Ziel (50% der Position schließen, Rest auf Break-Even).
   - 🏁 SL (Stop-Loss):  ATR-basierter institutioneller Stop. Standard: 1.0x ATR14.
   - 🏃 Runner-Target:   EMA 21 als Trailing-Kriterium für die 50% Runner-Position.

> ⚠️ NUTZER-HINWEIS: Handeln Sie nur, wenn die Signal-Validierung grün leuchtet.
>    Das Cockpit ist eine Navigationshilfe für ein 50k Depot.

---
### II. Asymmetrisches Risiko: Die „Atmende Firewall"
Das System nutzt ein 3-Stufen-Risiko-Regime basierend auf dem CBOE VIX.

1. REGIME ALPHA (VIX < 25) – Normalbetrieb:
   Longs und Shorts werden mit 100% Risiko gehandelt (Basis: einstellbar, Standard 100€).

2. REGIME DELTA (VIX 25 – 35) – Short-Spezialist:
   - Long-Trades: nur noch 25% des Basis-Risikos (Kapitalschutz).
   - Short-Trades: weiterhin 100% Risiko (Panikverkäufe als Beschleuniger nutzen).

3. REGIME OMEGA (VIX > 35) – Handelsstopp:
   Beide Richtungen werden auf 0% Risiko gesetzt. Dysfunktionaler Markt (Gaps, Slippage).

MATHEMATIK: shares = floor(aktives_Risiko / abs(Entry - SL))
Das bedeutet: Bei einem Stop-Out verbrennt das System punktgenau maximal dein Basis-Risiko.

---
### III. Die 4 Signalstufen (Kaskaden-System)

Das System ist als aufsteigender Funnel aufgebaut. Jede Stufe erfordert mehr Bedingungen.

1. 📡 LAUERN (Radar-Phase):
   BEDINGUNGEN: Weinstein Stage 2/4 ✓ + Bollinger Hysterese berührt ✓ + WPR ≥ 70 (Long)
               oder WPR ≤ 30 (Short) ✓
   BEDEUTUNG:   Das Setup baut sich auf. Bereite dein Limit vor!

2. 🟢 FEUER FREI (Sniper-Trigger):
   BEDINGUNGEN: Alles wie LAUERN + WPR ≥ 80 (Long) / ≤ 20 (Short) ✓
               + Kerzenregel OK ✓ + Stopversicherung ≥ 1.5% ✓ + TP Widerstand ≤ 15% ✓
               + [v20.6 FIX] Bollinger Zone passt ✓
   BEDEUTUNG:   Einstieg möglich. Platziere Stop-Buy / Stop-Sell Order.

3. 🌟 GOLDEN SETUP (Premium-Trade):
   BEDINGUNGEN: Alles wie FEUER FREI + Stopversicherung ≥ 3.0% ✓ + TP Widerstand ≤ 8.0% ✓
               + [v20.6 FIX] Bollinger Zone passt ✓
   BEDEUTUNG:   High-Grade Entry. Smart Money steht hinter dem Stop. Volle 1R einsetzen.

4. 💎 AKJ ELITE (Ultra-Präzision):
   BEDINGUNGEN: Weinstein Stage 2/4 ✓ + Scharf-Modus aktiv (2 Kerzen außerhalb) ✓
               + WPR ≥ 80 / ≤ 20 ✓ + Kerze kein Doji ✓ + Kurs noch diesseits des Bandes
   BEDEUTUNG:   Der seltenste und sauberste Signal-Typ. Nur für erfahrene Trader.

🔒 ANTI-SPAM SCHUTZ: Jeder Ticker kann nur alle 3 Minuten einen Alarm senden.
   Schützt vor automatischer TradingView-Sperrung bei hoher Marktaktivität (VIX 30+).

---
### IV. v20.6 Bug-Fixes (Technische Änderungen)

FIX 1 – Wochentrend Midline-Reset:
   PROBLEM:  w_trend blieb "BULLISCH" bis der Preis das untere Band erreichte (Wochen!).
   FIX:      w_trend wird auf NEUTRAL gesetzt, sobald der wöchentliche Schlusskurs unter
             die Wochenmittellinie (SMA 10) fällt.
   CODE:     else if w_trend == 1 and w_cl_1 < w_basis_1 → w_trend := 0

FIX 2 – Tages-Scharf Midline-Reset:
   PROBLEM:  setup_strict_long blieb aktiv bis 2 Kerzen unter dem unteren Band schlossen.
   FIX:      setup_strict_long wird sofort deaktiviert, wenn close[1] < d_basis[1].
   CODE:     if close[1] < d_basis[1] → setup_strict_long := false

FIX 3 – Zone-Check im Signal-Flow:
   PROBLEM:  is_correct_zone_l/s war zwar berechnet, wurde aber nie in den Trigger-Booleans
             verwendet (stiller toter Code).
   FIX:      is_correct_zone_l/s ist jetzt Pflichtbedingung für FEUER und GOLDEN Signale.
   CODE:     trigger_feuer_l  = raw_feuer_l and vol_feuer_l  and is_correct_zone_l
             trigger_golden_l = raw_feuer_l and vol_golden_l and is_correct_zone_l

---
### V. Backtest-Anleitung (akj_sniper_backtest_v20_6.pine)

Das beigelegte Backtest-Script simuliert ein exaktes 50.000€ Depot.
- Kommission:  2.00€ pro Order (IBKR-Standard)
- Slippage:    1 Tick
- Einstieg:    Nur GOLDEN SETUP Signale werden exekutiert.
- Exit:        50% bei TP1 (1:1 CRV), 50% Runner bis EMA 21 oder Wochentrend-Wechsel.
- Fallback:    Zeitbasierter Exit nach 5 Tagen (wenn weder TP noch SL erreicht).

ANLEITUNG:
1. Lade das Script im Pine Editor von TradingView.
2. Öffne den Tab "Strategietester".
3. Prüfe "Simulated Net Profit" und "Max Drawdown".
4. Das Audit-Cockpit (oben Mitte) zeigt die historische Winrate pro Signalstufe.

AUDIT-AUSWERTUNG:
- Win-Rate > 50% bei GOLDEN = statistischer Edge nachgewiesen 🔥 STAR-TICKER
- Erwartungswert (€) = Durchschnittlicher R-Gewinn * Basis-Risiko

---
### VI. Pine Screener Export (Massenscreening 1000+ Aktien)

Der Indikator exportiert einen "Sniper Status" Code für den TradingView Pine Screener.

  +4 = AKJ ELITE LONG      -4 = AKJ ELITE SHORT
  +3 = GOLDEN SETUP LONG   -3 = GOLDEN SETUP SHORT
  +2 = FEUER FREI LONG     -2 = FEUER FREI SHORT
  +1 = LAUERN LONG         -1 = LAUERN SHORT
   0 = Kein Signal

So kannst du mit einem einzigen Script eine Watchlist von 1000 Aktien
gleichzeitig auf aktive Signale scannen (Pine Screener → Column hinzufügen →
"Sniper Status" auswählen → nach Wert filtern).

---
### VII. Risk-Recycling Strategie (50/50 Runner-Logik)

TP1 (1:1 CRV):
  - Sobald der Preis die ATR-Stop-Distanz als Gewinn zurücklegt, werden 50% verkauft.
  - Der Stop-Loss der verbliebenen 50% wandert auf Break-Even (zero-loss-Modus).

TP2 (Runner Trailing):
  - Die 50% Runner-Position läuft so lange, bis EINER dieser Exits triggert:
    a) Tages-Schlusskurs kreuzt EMA 21 in die entgegengesetzte Richtung.
    b) Wochentrend wechselt auf die Gegenseite.
    c) 5 Handelstage vergangen ohne TP-Hit (Zeitbasierter Exit – Backtest).

---
Leitgedanke v20.6:
"Der Sniper-Commander v20.6 schließt die logische Lücke zwischen Trend-Definition
und Signal-Qualität. Er feuert nicht nur wenn das Setup da ist – er stellt sicher,
dass der Trend nicht bereits eine Leiche ist, wenn er feuert."
