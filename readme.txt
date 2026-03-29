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
*   **Vacuum Quality:** „Prüft den historischen Ziel-Widerstand (TP < 8%). Der RLD-Current-Volumen Check blockiert Trades nicht mehr fälschlicherweise bei Breakouts.“
*   **Kerzenregel:** „Prüft die Preis-Aktion (Scharf-Kerze) inkl. ATR-basiertem Doji-Filter. OK bedeutet: Die Käufer/Verkäufer haben die Kontrolle übernommen.“
*   **Stopversicherung:** „Die Volumen-Mauer (🛡️) an deinem Stopp-Level. Gemessen ab dem Ankerpunkt (v20.5). Zielwert: >3% zur Absicherung der Position.“
*   **TP Widerstand:** „Das Volumen-Hindernis (🚧) bis zum Ziel. Gemessen per RLD-Verfahren (v20.5). Zielwert: <8% für einen freien Lauf (Vakuum) zum Take-Profit.“

> ⚠️ **NUTZER-HINWEIS:** Dieses Cockpit dient als Navigationshilfe zur Skalierung eines 50k Depots. Handeln Sie nur, wenn die Signal-Validierung grün leuchtet.

---
### II. Asymmetrisches Risiko: Die „Atmende Firewall“
In v20.5 Elite wurde das einfache "VIX an/aus" Flag (Firewall) durch ein hoch-intelligentes 3-Stufen-Modell ersetzt, um in fallenden Märkten Short-Gewinne zu extrahieren, anstatt einfach das Trading komplett einzustellen.
*   **1. Regime ALPHA (VIX < 25):** Der Markt ist geordnet. Longs und Shorts werden mit 100% Risiko (Basis 150€) gehandelt.
*   **2. Regime DELTA (VIX 25 - 35):** Es herrscht Unruhe und Abwärtsdruck. Hier wird die Strategie zu einem absoluten "Short-Spezialisten", um die Gewinnwahrscheinlichkeiten bei hoher Markt-Angst zu optimieren. Bei Long-Trades wird das Risiko zum reinen Kapitalschutz geviertelt (25% R). Short-Trades bleiben auf **100% Risiko**, um Panikverkäufe als Gewinnbeschleuniger zu nutzen.
*   **3. Regime OMEGA (VIX > 35):** Massive Volatilität / Schwarze Schwäne. Der Markt ist dysfunktional, Gaps und Slippage zerstören CRVs. Beide Seiten werden gnadenlos mit 0% Risiko blockiert.

---
### III. v20.5 Innovationen (Filter-Kalibrierung & Vakuum-Definition)
Neben der asymmetrischen Risk-Logik schlägt unter der Haube ein neues mathematisches Herz, welches die größten Probleme klassischer MTF-Indikatoren löst:

1.  **Filter-Kalibrierung auf 3% (Die AVP-Synergie):** Die **v20.5 Anker-Logik** startet den Volumen-Zähler exakt zu dem Zeitpunkt, an dem das "Smart Money" die Weinstein-Phase historisch gedreht hat. Da dies ein absolutes Qualitäts-Volumen ist, reicht bereits eine Schwellenwert-Kalibrierung von **3% Stopversicherung** als starker institutioneller Schutzwall aus!
2.  **Vakuum-Definition (Entkopplung):** Das Vakuum basiert nun rein auf der historischen Preis-Volumen-Struktur bis zum Target. Es bewertet, ob der Weg historisch "frei" ist. Zuvor hat der RLD-Check hohes Live-Volumen der Breakout-Kerze fälschlicherweise bestraft – dies ist behoben! RLD dient nun rein als informatives Element.
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

---
### VI. Die statistische Kante (Edge)
Die Backtest-Engine wurde von klassischer Exekution auf ein umfassendes **Funnel- & Status-Audit-System** umgestellt. Auf dem Chart erscheint nun direkt das "State-Audit Cockpit". 
Dieses trackt die gesamte Historie des Tickers (alle Signale und Phasen), ohne von Pine-Script Constraints blockiert zu werden.

**Wie wird die Trefferquote gelesen?**
* **LAUERN:** Wie oft das Asset in Position lief (Phase 2/4 + Trend + Hysterese).
* **FEUER FREI:** Wie oft eine Scharf-Kerze den Trigger in der Lauer-Position zog.
* **GOLDEN SETUP:** Wie oft zudem das gesamte Volumen-Setup (Schutz-Wall & Vakuum) stimmte.

Wenn bei einem Typen die Win-Rate (Kurs erreicht 1R Ziel, bevor der Initial-Stop-Loss platzt) im **grünen Bereich (>50%)** liegt, hast du in diesem Asset einen systematischen, bewiesenen Edge! Der Ø Profit inkludiert zudem das Risk-Recycling (sichere +0.5R bei Gewinn, -1.0R bei Verlust).

> **Handlungsanweisung:** „Das Audit zeigt nun die echte historische Trefferquote basierend auf Signal-Ereignissen. Ein Wert über 50% bei 'GOLDEN SETUP' signalisiert einen statistischen Edge.“
