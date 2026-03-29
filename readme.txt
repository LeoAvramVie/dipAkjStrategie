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
*   **Rel. Stärke:** „Vergleicht die Performance der Aktie mit ihrem Sektor über 20 Tage. STARK bedeutet Outperformance und erhöht die Wahrscheinlichkeit für einen erfolgreichen Trade.“
*   **Weinstein-Stage:** „Strategische Marktphase nach Stan Weinstein. Stage 2 = Institutionelle Akkumulation (Long), Stage 4 = Institutionelle Distribution (Short).“
*   **Wochentrend:** „Taktische Richtung auf Wochenbasis (Sticky). Erfordert 2 Schlusskurse außerhalb der Bollinger Bänder (10/1). Bleibt aktiv, bis die Gegenseite 2 Kerzen erzwingt.“
*   **Tagestrend:** „Kurzfristiges Timing-Radar. Nutzt einen dynamischen ATR-Puffer (Hysterese v20.5), um Fehlsignale in volatilen Phasen (VIX > 25) zu filtern.“
*   **Risk-O-Meter:** „Dynamische Positionsgröße (1R). Passt das Risiko basierend auf der Marktangst (VIX) und der Aktien-Volatilität automatisch an.“
*   **Risk-Mode (Adaptiv):** „ALPHA: Volles Risiko. DELTA: Longs gebremst (25% R), Shorts aktiv (100% R). OMEGA: Handelsstopp wegen Extrem-Volatilität.“
*   **Anchor-Info:** „Startpunkt des Anchored Volume Profile (AVP). Misst das Volumen exakt ab dem letzten Weinstein-Phasenwechsel oder Pivot-Punkt.“
*   **Vacuum Quality:** „Prüft die Liquiditätsdichte (RLD). High Quality bedeutet, dass der Preis kaum auf Widerstand stoßen wird (Vakuum).“
*   **Kerzenregel:** „Prüft die Preis-Aktion (Scharf-Kerze) inkl. ATR-basiertem Doji-Filter. OK bedeutet: Die Käufer/Verkäufer haben die Kontrolle übernommen.“
*   **Stopversicherung:** „Die Volumen-Mauer (🛡️) an deinem Stopp-Level. Gemessen ab dem Ankerpunkt (v20.5). Zielwert: >10% zur Absicherung der Position.“
*   **TP Widerstand:** „Das Volumen-Hindernis (🚧) bis zum Ziel. Gemessen per RLD-Verfahren (v20.5). Zielwert: <8% für einen freien Lauf (Vakuum) zum Take-Profit.“

> ⚠️ **NUTZER-HINWEIS:** Dieses Cockpit dient als Navigationshilfe zur Skalierung eines 50k Depots. Handeln Sie nur, wenn die Signal-Validierung grün leuchtet.

---
### II. Asymmetrisches Risiko: Die „Atmende Firewall“
In v20.5 Elite wurde das einfache "VIX an/aus" Flag (Firewall) durch ein hoch-intelligentes 3-Stufen-Modell ersetzt, um in fallenden Märkten Short-Gewinne zu extrahieren, anstatt einfach das Trading komplett einzustellen.
*   **1. Regime ALPHA (VIX < 25):** Der Markt ist geordnet. Longs und Shorts werden mit 100% Risiko (Basis 150€) gehandelt.
*   **2. Regime DELTA (VIX 25 - 35):** Es herrscht Unruhe und Abwärtsdruck. Das System nutzt ab hier die Schwerkraft: Bei Long-Trades wird das Risiko zum Kapitalschutz geviertelt (25% R). Short-Trades bleiben auf **100% Risiko**, um Panikverkäufe für das Depot optimal als Beschleuniger zu nutzen.
*   **3. Regime OMEGA (VIX > 35):** Massive Volatilität / Schwarze Schwäne. Der Markt ist dysfunktional, Gaps und Slippage zerstören CRVs. Beide Seiten werden gnadenlos mit 0% Risiko blockiert.

---
### III. v20.5 Innovationen (Das Kern-Upgrade)
Neben der asymmetrischen Risk-Logik schlägt unter der Haube ein neues mathematisches Herz, welches die größten Probleme klassischer MTF-Indikatoren löst:

1.  **Die AVP/RLD-Synergie (Der Gamechanger):** Klassische Profiler messen einfach stumpf feste Tage. Die **v20.5 Anker-Logik** startet den Volumen-Zähler erst zu dem exakten Zeitpunkt, an dem das "Smart Money" die Weinstein-Phase historisch gedreht hat. Verbunden mit dem **RLD-Check** (Relative Liquidity Density) sichern wir unsere Stops über diese Anker-Aufschichtung ab. Diese Synergie steigert die Qualität der Trades massiv.
2.  **Repaint Protection:** Absicherung des Multi-Timeframe (MTF) 4H Volumens auf dem Tageschart via `request.security_lower_tf()` und `barstate.isconfirmed`. Alarme triggern streng ohne Intrabar-Verzerrungen.
3.  **Sticky Trend Hysterese:** Um Rauschen an den Bändern auszufiltern, muss ein Trendausbruch nun 0.2 ATR über/unter das Band hinausschießen.

---
### IV. Das Alarmsystem (Risk-Recycling & Phase-Shift)
Das Alarmsystem bindet sich nun adaptiv immer an den aktuellen Risk-Mode. Du erhältst Pings wie: "DELTA Mode - 🎯 SNIPER: Risk-Recycling bereit!".
Risk-Recycling bedeutet in der v20.5 Backtest-Strategie folgendes: **Sobald das feste CRV (Risiko) 1:1 erreicht ist, werden 50% der Position aus dem Markt genommen und der Stop-Loss läuft sofort auf Break-Even nach.**

---
### V. Backtest-Anleitung (IBKR Abgleich)
Es liegt ein separates `akj_sniper_backtest_v20_5.pine` Script bei. Dieses simuliert ein exaktes 50.000€ Depot, zieht 2.00€ Kommission ab und rechnet 1 Tick Slippage pro Trade.
*   Lade das Script im Pine Editor.
*   Nutze den **Tab "Strategietester"** in TradingView, um den "Simulated Net Profit" zu prüfen.
*   Wenn du auf Ticker wie LHA, TEAM, CSCO oder PYPL im Chart gehst, zeigt dir die eingebaute "IBKR Reality Check Note" unten rechts tabellarisch an, warum deine echten Depot-Ausführungen im IBKR-Statement historisch von der harten Indikator-Logik abweichen (z.B. wegen fehlendem VIX Filter bei CSCO).
