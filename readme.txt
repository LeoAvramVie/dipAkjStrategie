# AKJ 2.0 Sniper-Commander
## Das taktische Lagezentrum (v20.5 Elite)

---
TEIL 1: FACHLICHES DOSSIER (System-Handbuch)
---

Hier ist die detaillierte, fachliche und technische Aufschlüsselung des AKJ 2.0 Sniper-Commander v20.5. Das System wurde in v20.5 Elite um ein adaptives (asymmetrisches) Risikomanagement, Anchored Volume Profile (AVP) und strengere Doji-/Hysterese-Filter erweitert.

### I. Das Interaktive Cockpit (Dashboard)
Das HUD wurde logisch in Blöcken gruppiert, um dir während des Tradings den perfekten Überblick über Kontext, Metriken und Exekution zu geben. 

💡 **NEU IN v20.5:** Die Werte im Cockpit besitzen interaktive Tooltips. Wenn du mit der Maus (Mouse-over) über die Parameter-Titel in TradingView fährst, liefert das System dir sofortige strategische Erklärungen. 

**Folgende Tooltips sind im Chart aktiv:**
*   **Sektor:** „Der maßgebliche Sektor-ETF der Aktie. Dient zur Bestimmung des Marktumfelds und der relativen Stärke.“
*   **Rel. Stärke:** „Vergleicht die Performance der Aktie mit ihrem Sektor über 20 Tage. STARK bedeutet Outperformance und erhöht die Wahrscheinlichkeit für einen erfolgreichen Trade.“
*   **Weinstein-Stage:** „Strategische Marktphase nach Stan Weinstein. Stage 2 = Institutionelle Akkumulation (Long), Stage 4 = Institutionelle Distribution (Short).“
*   **Wochentrend:** „Taktische Richtung auf Wochenbasis (Sticky). Erfordert 2 Schlusskurse außerhalb der Bollinger Bänder (10/1). Bleibt aktiv, bis die Gegenseite 2 Kerzen erzwingt.“
*   **Tagestrend:** „Kurzfristiges Timing-Radar. Nutzt einen dynamischen ATR-Puffer (Hysterese v20.5), um Fehlsignale in volatilen Phasen (VIX > 25) zu filtern.“
*   **Risk-O-Meter:** „Dynamische Positionsgröße (1R). Passt das Risiko basierend auf der Marktangst (VIX) und der Aktien-Volatilität automatisch an.“
*   **Risk-Mode (Adaptiv):** „ALPHA: Volles Risiko. DELTA: Longs gebremst (25% R), Shorts aktiv (100% R). OMEGA: Handelsstopp wegen Extrem-Volatilität.“
*   **Anchor-Info:** „Startpunkt des Anchored Volume Profile (AVP). Misst das Volumen exakt ab dem letzten Weinstein-Phasenwechsel oder Pivot-Punkt.“
*   **Vacuum Quality:** „Prüft den historischen Ziel-Widerstand (TP < 8%). Der RLD-Current-Volumen Check blockiert Trades nicht mehr fälschlicherweise bei Breakouts.“
*   **Kerzenregel:** „Prüft die Preis-Aktion (Scharf-Kerze) inkl. ATR-basiertem Doji-Filter. OK bedeutet: Die Käufer/Verkäufer haben die Kontrolle übernommen.“
*   **Stopversicherung:** „Die Volumen-Mauer (🛡️) an deinem Stopp-Level. Gemessen ab dem Ankerpunkt (v20.5). Zielwert: >3% zur Absicherung der Position.“
*   **TP Widerstand:** „Das Volumen-Hindernis (🚧) bis zum Ziel. Gemessen per RLD-Verfahren (v20.5). Zielwert: <8% für einen freien Lauf (Vakuum) zum Take-Profit.“

**ORDER-MATRIX TOOLTIPS:**
*   **Stoppreis (SP):** „Dein Einstiegs-Preis (Trigger). Platziere hier deine Stop-Buy (Long) oder Stop-Sell (Short) Limit-Order.“
*   **LimitPreis (LP):** „Gap-Schutz für deine Einstiegsorder. Vermeidet Slippage, wenn der Markt extem wild über deinen Preis springt.“
*   **Anzahl (Stk):** „Die Anzahl an Aktien, mit denen du EXAKT dein gewünschtes asymmetrisches (€) 1R Risiko triffst.“
*   **TP (Teilverkauf):** „Das 1:1 CRV Ziel. Verkaufe hier exakt 50% deiner Position (Risk-Recycling) und ziehe den restlichen Stop auf Break-Even.“
*   **Stopp-Loss (SL):** „Initialer institutioneller ATR-Stop (1.5 * ATR14). Schützt dich vor massiven Ausbrüchen entgegen deiner Richtung.“
*   **Runner-Target:** „Dein Trailing-Radar für den 50% Runner. Wenn der heutige Tages-Schlusskurs diese EMA 21 Linie bricht, schließt du den gesamten Rest.“

> ⚠️ **NUTZER-HINWEIS:** Dieses Cockpit dient als Navigationshilfe zur Skalierung eines 50k Depots. Handeln Sie nur, wenn die Signal-Validierung grün leuchtet.

---
### II. Asymmetrisches Risiko: Die „Atmende Firewall“
In v20.5 Elite wurde das einfache "VIX an/aus" Flag (Firewall) durch ein hoch-intelligentes 3-Stufen-Modell ersetzt, um in fallenden Märkten Short-Gewinne zu extrahieren, anstatt einfach das Trading komplett einzustellen.
*   **1. Regime ALPHA (VIX < 25):** Der Markt ist geordnet. Longs und Shorts werden mit 100% Risiko (Basis 150€) gehandelt.
*   **2. Regime DELTA (VIX 25 - 35):** Es herrscht Unruhe und Abwärtsdruck. Hier wird die Strategie zu einem absoluten "Short-Spezialisten", um die Gewinnwahrscheinlichkeiten bei hoher Markt-Angst zu optimieren. Bei Long-Trades wird das Risiko zum reinen Kapitalschutz geviertelt (25% R). Short-Trades bleiben auf **100% Risiko**, um Panikverkäufe als Gewinnbeschleuniger zu nutzen.
*   **3. Regime OMEGA (VIX > 35):** Massive Volatilität / Schwarze Schwäne. Der Markt ist dysfunktional, Gaps und Slippage zerstören CRVs. Beide Seiten werden gnadenlos mit 0% Risiko blockiert.

> **Mathematische Risiko-Kontrolle (Shares):** Die Berechnung der Stückzahl ist zu 100% wasserdicht an den ATR-Stop gekoppelt (`shares = floor(dyn_risk / abs(Entry - SL))`). Das bedeutet: Unabhängig von der individuellen Volatilität der Aktie und der Weite des 1.5x ATR-Stops, verbrennt das System bei einem Stop-Out punktgenau maximal 150 € (oder den aktuellen DELTA-Betrag). Das Kapital ist absolut geschützt.
---
### III. v20.5 Innovationen (Filter-Kalibrierung & Vakuum-Definition)
Neben der asymmetrischen Risk-Logik schlägt unter der Haube ein neues mathematisches Herz, welches die größten Probleme klassischer MTF-Indikatoren löst:

1.  **Filter-Kalibrierung auf 3% (Die AVP-Synergie):** Die **v20.5 Anker-Logik** startet den Volumen-Zähler exakt zu dem Zeitpunkt, an dem das "Smart Money" die Weinstein-Phase historisch gedreht hat. Da dies ein absolutes Qualitäts-Volumen ist, reicht bereits eine Schwellenwert-Kalibrierung von **3% Stopversicherung** als starker institutioneller Schutzwall aus!
2.  **Vakuum-Definition (Entkopplung):** Das Vakuum basiert nun rein auf der historischen Preis-Volumen-Struktur bis zum Target. Es bewertet, ob der Weg historisch "frei" ist. Zuvor hat der RLD-Check hohes Live-Volumen der Breakout-Kerze fälschlicherweise bestraft – dies ist behoben! RLD dient nun rein als informatives Element.
3.  **Sticky Trend Hysterese:** Um Rauschen an den Bändern auszufiltern, muss ein Trendausbruch nun 0.2 ATR über/unter das Band hinausschießen.

### IV. Das Kaskaden-Alarmsystem (v20.6 Sensitivity)
Das Alarmsystem wurde in v20.6 komplett überarbeitet und als 3-stufiger Funnel aufgebaut. Dies löst das Problem, dass zu restriktive Filter am Anfang die besten Trades komplett verschluckt haben.
Das Alarmsystem ist als Kaskade aufgebaut, bei der der Williams %R (4) Momentum-Oszillator als Kern-Trigger dient. Die Signale sind in Stufen unterteilt, um frühzeitig zu warnen und dann präzise abzufeuern. Wir nutzen die 70/30-Zonen für die frühestmögliche Beobachtung (um keine Zeit bei der Limit-Planung zu verlieren), während wir für die tatsächliche Exekution auf das finale 80/20 Extrem warten.

1. **📡 LAUERN (Radar & 70er WPR Trigger):**
   - Das Setup erfüllt die Trend-Kriterien (Phase 2/4) und hat die Bollinger-Band-Hysterese berührt.
   - Der erste Alarm wird ausgelöst, wenn das WPR-Momentum den **70er Bereich (Long)** oder **30er Bereich (Short)** erreicht. Du weißt nun: "Achtung, das Setup baut sich auf!"

2. **🎯 FEUER FREI (Sniper & 80er WPR Trigger):**
   - Sobald die Kauf-Kerzenregel zuschlägt und das WPR-Momentum das tiefe Extrem von **80 (Long)** oder **20 (Short)** erreicht, erfolgt der finale Exekutions-Trigger.
   - Hat die Aktie hierbei min. 1.5% Stopversicherung, erscheint der blaue FEUER FREI Status.

3. **🌟 GOLDEN SETUP (Premium):** Der absolute High-Grade Trade. Nur Setups, die neben dem Trigger auch noch eine exzellente Volumen-Struktur (>3% Stop-Mauer, <8% Vakuum-Widerstand) ins Orderbuch legen, erreichen diesen Status.

4. **🔒 ANTI-SPAM SCHUTZ (v20.6.8):** v20.6.8 verfügt über ein Hard-Limit Alarmsystem. Pro Ticker werden maximal 14 Alarme innerhalb von 3 Minuten zugelassen, um die TradingView-Sperre zu umgehen. Der Zähler resettet sich alle 3 Minuten automatisch.

Risk-Recycling: **Sobald das feste CRV (Risiko) 1:1 erreicht ist, werden 50% der Position aus dem Markt genommen und der Stop-Loss läuft sofort auf Break-Even nach.**
### V. Backtest-Anleitung (IBKR Abgleich)
Es liegt ein separates `akj_sniper_backtest_v20_5.pine` Script bei. Dieses simuliert ein exaktes 50.000€ Depot, zieht 2.00€ Kommission ab und rechnet 1 Tick Slippage pro Trade.
*   Lade das Script im Pine Editor.
*   Nutze den **Tab "Strategietester"** in TradingView, um den "Simulated Net Profit" zu prüfen.
*   Wenn du auf Ticker wie LHA, TEAM, CSCO oder PYPL im Chart gehst, zeigt dir die eingebaute "IBKR Reality Check Note" unten rechts tabellarisch an, warum deine echten Depot-Ausführungen im IBKR-Statement historisch von der harten Indikator-Logik abweichen (z.B. wegen fehlendem VIX Filter bei CSCO).

---
### V. Die statistische Kante (Edge Audit & Ticker-Stars)
Die Backtest-Engine trackt historisch den gesamten Ticker über das Kaskaden-Radar. Sobald die 1:1 TP1 Winrate für ein Setup über 50% liegt, zeichnet das System die Setup-Stufe mit dem Sternchen-Label "⭐ STAR-TICKER" aus!
Zusätzlich zeigt dir das Cockpit jetzt direkt den potenziellen Geldwert (Erwartungswert in €) eines Tickers, multipliziert mit deinem Basis-Risiko. Jede Aktie mit einem **grünen Euro-Erwartungswert** im Audit ist ein statistischer Favorit.

*   **LAUERN:** Wie oft das Asset in Position lief (Stage + Scharf 1).
*   **FEUER FREI:** Wie oft der reine Trigger bei Mindestvolumen (>1.5%) zuschlug.
*   **GOLDEN:** Wie oft zudem das exzellente Momentum-Volumen (Premium-Mauer) stimmte.

Wenn bei einem Typen die Win-Rate (Kurs erreicht 1R Ziel, bevor der Initial-Stop-Loss platzt) im **grünen Bereich (>50%)** liegt, hast du in diesem Asset einen systematischen, bewiesenen Edge! Der Ø Profit inkludiert zudem das Risk-Recycling (sichere +0.5R bei Gewinn, -1.0R bei Verlust).

> **Handlungsanweisung:** „Das Audit zeigt nun die echte historische Trefferquote basierend auf Signal-Ereignissen. Ein Wert über 50% bei 'GOLDEN SETUP' signalisiert einen statistischen Edge.“

---
### VII. Professional Swing-Trading (ATR-Stops & Runner-Logik)
v20.5 nutzt nun institutionelle ATR-Stops und eine Runner-Logik am EMA 21, um Gewinne in starken Trends (Stage 2/4) zu maximieren und unnötige Ausstopper zu vermeiden.

**Das 50/50 Risk-Recycling:**
*   **TP1 (1:1 CRV):** Sobald die Distanz des ATR-Stops als Gewinn erreicht ist, werden 50% der Position verkauft. Der Stop für den Rest wandert auf Break-Even.
*   **TP2 (Der Runner):** Die verbleibenden 50% reiten den Trend so lange, bis der Tages-Schlusskurs den EMA 21 in die entgegengesetzte Richtung kreuzt oder sich die Weinstein-Phase ändert.
