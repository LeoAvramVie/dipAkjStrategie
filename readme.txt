# AKJ 2.0 Sniper-Commander
## Das taktische Lagezentrum (v20.4 Elite)

---
TEIL 1: FACHLICHES DOSSIER (System-Handbuch)
---

Hier ist die detaillierte, fachliche und technische Aufschlüsselung des AKJ 2.0 Sniper-Commander v20.4.

### I. Das Cockpit (Dashboard) – Zeile für Zeile
Das Cockpit ist deine einzige Quelle der Wahrheit. 
Es verarbeitet hunderte Datenpunkte in Millisekunden und spuckt nur das aus, was für die Exekution relevant ist.

| Zeile | Bezeichnung | Mögliche Werte | Technische Logik & Bedeutung |
| :--- | :--- | :--- | :--- |
| **0** | **Strategie** | `!!! GOLDEN SETUP !!!` (Grün)<br>`!!! FEUER FREI !!!` (Blau/Rot)<br>`LAUERN` (Gelb)<br>`Keine` (Schwarz) | **Elite-Alarm:** Sniper + Stopversicherung > 10% + TP Widerstand < 8% (oder Flex-Ratio).<br>**Sniper:** Alle tech. Regeln (Trend, Setup, Williams, Kerze) erfüllt.<br>**Vor-Alarm:** Trend da, Williams in Zone, aber Kerze fehlt.<br>**Warte-Status:** Aktie technisch unbrauchbar. |
| **1** | **🌍 Sektor** | Name (ETF-Ticker) | Dynamisches Mapping via `syminfo.sector`. ETF (z.B. XLE) Zuordnung. Blau = ETF > SMA 10, Rot = ETF < SMA 10. |
| **2** | **💪 Rel. Stärke** | STARK, MITTEL, SCHWACH | Vergleicht 20-Tage-Performance der Aktie mit Sektor-ETF. Blau = Outperformance. |
| **3** | **📈 Weinstein Stage** | STAGE 2 OK Long ✅<br>STAGE 4 OK Short ✅<br>SEITWÄRTS | Regimewechsel: Wochenkurs > SMA 30 + SMA steigend. Seitwärts = Todeszone. |
| **4** | **Wochentrend** | LONG, SHORT, --- | Sticky Trend: 2 Wochenschlüsse außerhalb BB (10/1). |
| **5** | **Tagstrend** | LONG, SHORT, LAUERN, --- | Taktischer Trigger: 2 Tage außerhalb BB (Scharf). 1 Tag (Radar). |
| **6** | **⚡ Williams %R** | Absolute Skala | Schnelle 4er-Periode (wpr_len=4) für harte Ausschläge. >80 = Überverkauft (Panik/Dip). |
| **7** | **🕯️ Kerzenregel** | OK ✅, WAIT ⏳ | Bestätigungs-Filter (Wir kaufen den Dip!): Close < Open (Rote Kerze) bei Long. Close > Open (Grün) bei Short. Dojis verboten! |
| **8** | **Stoppreis (SP)** | Zahlenwert | Trigger: 2 Ticks über High / unter Low der Signalkerze. |
| **9** | **LimitPreis (LP)** | Zahlenwert | Sicherheit: SP +/- Limit-Offset. Maximale Schmerzgrenze für Slippage. |
| **10**| **Anzahl** | Zahlenwert | Risiko-Kalkulator: Berechnet Stücke für exakt z.B. 150€ (1R) Risiko. |
| **11**| **TP-Teilverkauf**| Zahlenwert | Risk-Recycling: Das 1:1 Ziel. 50% Verkauf, Rest auf Break-Even. |
| **12**| **Stopp-Loss (SL)**| Zahlenwert | Feuerschutz: 2 Ticks unter Low / über High der Signalkerze. |
| **13**| **Stopversicherung**| Prozentwert (%) | Mauer-Check (4H): Volumen zwischen SP und SL. Ziel: >10%. |
| **14**| **TP Widerstand** | Prozentwert (%) | Vakuum-Check (4H): Volumen zwischen SP und TP. Ziel: <8%. |

### II. Das Alarmsystem – Die 3-Stufen-Rakete
Wir nutzen `alert.freq_once_per_bar`, um intraday informiert zu werden, ohne TradingView zu überlasten.

**1. Stufe: 📡 RADAR (Die Mobilmachung)**
* **Trigger:** Williams %R berührt die Zone >=80 (Long) oder <=20 (Short), während der Wochentrend passt.
* **Zweck:** Dieser Alarm weckt dich auf. Die Aktie fällt in das Beuteschema. Das Setup ist noch nicht fertig, aber die Vorbereitung (Volumen-Check auf 4H) beginnt jetzt.

**2. Stufe: 🎯 SNIPER (Der Marschbefehl)**
* **Trigger:** Alle technischen Regeln sind gleichzeitig erfüllt: Wochentrend passt (Sticky), Tagessetup Scharf, %R ist extrem, Kerzenfarbe bestätigt, KEIN Bollinger-Bruch (MK 4.7/5.6 Inner-Close).
* **Zweck:** Signal zur Order-Vorbereitung. TWS öffnen und Stop-Limit-Order bereitlegen.

**3. Stufe: 🏆 GOLDEN SETUP (Die Elite-Exekution)**
* **Trigger:** Alle Sniper-Bedingungen PLUS: Stopversicherung >= 10% und TP Widerstand <= 8% (oder freigegeben durch Flex-Ratio unterhalb des Brick-Wall-Caps).
* **Zweck:** Alarm mit der höchsten statistischen Signifikanz. Hier liegt die Mauer hinter deinem Stop und das Vakuum vor deinem Ziel. Vorrang vor allen anderen!

### III. Technische Besonderheiten für Anti Gravity
*   **MTF-Volumen-Synchronisation:** Die Volumen-Engine scannt im Hintergrund 400 Bars auf dem 4H-Timeframe (`request.security`), liefert die Daten aber verzögerungsfrei in das 1D-Cockpit.
*   **Proportionale Volumenberechnung:** Das Script berechnet mathematisch exakt, welcher prozentuale Anteil des Volumens einer Kerze innerhalb der Preisgrenzen von SP/SL und SP/TP liegt. Es ist keine Schätzung, es ist Physik.
*   **Visualisierung (HUD):** Linien für Einstieg, Stop und Ziel werden dynamisch ab der aktuellen Kerze gezeichnet für den sofortigen visuellen Abgleich.

*Jens’ strategische Zusammenfassung:* 
„Dieses System ist darauf getrimmt, den Zufall auszuschalten. Wir bewirtschaften Wahrscheinlichkeiten durch eine Filter-Kaskade: Strategie -> Taktik -> Struktur -> Finanzen. Nur wenn ein Ticker durch alle Filter fällt, bekommt er unser Geld.“


---
TEIL 2: TECHNISCHE DOKUMENTATION FÜR ENTWICKLER (Pine Script v6)
---

### 1. Architektur und Ausführungslogik
Das Skript ist als Overlay-Indikator konzipiert (`overlay=true`). Es berechnet komplexe diskretionäre Handelssignale durch State-Tracking, Volumendichteprofiler und MTF-Analyse (Multi-Timeframe). Das UI wird via Lazy-Evaluation (`if barstate.islast`) isoliert am Ende des Scripts gezeichnet, um Performance-Limits der TradingView-Engine zu umgehen.

### 2. Variablen & State-Tracking (Die "Sticky" Logik)
Das System nutzt `var` Deklarationen, um Zustände algorithmisch über mehrere Bars hinweg beizubehalten, bis eine saubere Gegensignatur auftritt.

#### 2.1 Trend-Identifikation (Woche & Tag)
*   **Wochentrend (`w_trend`) & Tagestrend (`d_trend`):** 
    *   **Werte:** `1` (Long), `-1` (Short), `0` (Neutral).
    *   **Berechnung:** Abgeleitet von Bollinger Band-Verschiebungen (z.B. Funktion `f_bb_d()`). Schließt eine Kerze über dem oberen Band (`close > d_up`), springt der Trend-State auf 1. Er bleibt zwingend auf 1, bis der Preis das gegenüberliegende untere Band berührt (`low < d_lo`). Das Modul fungiert als asymmetrischer Noise-Filter.

#### 2.2 Oszillator & Trigger-Logik
*   **Williams %R (`d_wpr`):** Nutzt eine schnelle Lookback-Periode von `wpr_len = 4` für harte, gnadenlose Reaktionen. Die absolute Skala wird genutzt, um Extremzonen abzugreifen (>=80 für Panik/Dip im Long, <=20 für Short). Die Standardperiode 14 wäre für dieses Edge-System viel zu träge.

#### 2.3 Die MK-Regeln (Strikte Einstiegs-Prüfung)
*   **MK 4.7 / 5.6 Bollinger-Bruch (`setup_strict_long` / `setup_strict_short`):**
    State-Machine Tracking für den Tagestrend. Ist der Preis nach 2 Kerzen immer noch intakt, wird das Setup für den Radar scharfgestellt (`true`). Ein Close auf der falschen Seite des Bandes de-eskaliert das Setup sofort (`false`). Verhindert den Einstieg in extreme Überdehnungen, weil das Signal-Buy explizit verlangt, dass die Kerze wieder in das Innere des Bandes schließt (`close > d_lo`).
*   **Kerzenregel (`long_trigger` / `short_trigger`):**
    Der finale Filter – wir kaufen in die Panik:
    *   **Long-Trigger:** `close < open` (Rote Kerze, Dip). Dojis (`close == open`) sind hart verboten.
    *   **Short-Trigger:** `close > open` (Grüne Kerze, Relief-Rallye). Dojis verboten.

### 3. Signal-Klassen (Die Pyramiden-Logik)
Die booleschen Variablen für Trading-Signale sind streng disjunkt und hierarchisch abgekapselt:
1.  **Radar (`is_lauern_long` / `short`):** Bestätigung, dass die Price-Action auf Tagesbasis scharf ist (Trend intakt, Preissetup formiert sich).
2.  **Sniper (`is_sniper_long` / `short`):** Wochentrend intakt + Tages-Setup scharf + Williams %R im Extrembereich (>= 80) + Kerzenbestätigung (Rote Kerze) + Inner-Bollinger Close (`close > d_lo`). Das pure Price-Action-Signal.
3.  **Golden (`is_golden_long` / `short`):** `is_sniper` + `vol_condition` (Quantitative Volumen-Verifizierung).

### 4. Multi-Timeframe (MTF) Support & Volumenprofiling
Die Kern-Innovation ist die dynamische Volumen-Dichteberechnung im Chart. Das Skript greift via `request.security(..., barmerge.lookahead_off)` auf höhere Timeframes zurück (Standard: `4H`), ohne Lookahead-Bias zu generieren.

*   **`f_calc_tf_vol()`:** Custom-Function, die über die letzten `vol_len` (Standard: 60) Bars im `vol_timeframe` iteriert.
    *   Sammelt das aggregierte Volumen (`volume[i]`) innerhalb der Preiszone Stop-Loss `[sp_price, sl_price]` -> `stop_volume`.
    *   Sammelt Volumen in der Gewinnzone `[sp_price, tp_price]` -> `tp_volume`.
    *   Wandelt die absoluten Werte in prozentuale Relation zum Gesamtvolumen um (`stop_density`, `tp_density`).
*   **`vol_condition` (Die Logik-Matrix):**
    Ein Golden-Setup benötigt grundlegend `stop_density >= min_stop_density` und `tp_density <= max_tp_density`.
*   **Die Flex-Ratio & Brick Wall Cap (v20.4):**
    Das System erlaubt elastische Setups: `density_ratio = stop_density / tp_density`. Ist Ratio > `min_vol_ratio` (1.5x), wird das Setup auch bei leichten Volumenschwächen genehmigt.
    **Hard Limit Exception:** Ein harter Cap (`brick_wall_cap = max_tp_density * 1.5`) blockiert das Setup jedoch kompromisslos, falls der absolute TP-Widerstand überdimensioniert ist (z.B. > 15%).

### 5. Diskretionäre Variablen (HUD Analyse)
Das Skript berechnet parallel institutionelle Kontext-Daten, die die Bool-Signale und Alarme logisch **niemals** beeinflussen:

*   **Dynamisches Sektor-Mapping (`f_get_auto_sector()`):** Nutzt native Variablen `syminfo.sector` & `syminfo.industry`. Mappt diese über Switch-Cases in US-Benchmarkt-Ticker um (z.B. Sektor "Semiconductors" mapped auf `SMH`).
*   **Relative Stärke (`perf_diff`):** Holt von dem identifizierten Ticker via `request.security` die Schlusskurse der letzten 20 Bars und berechnet die Performance-Differenz zur aktuellen Basis-Aktie. Zuweisung: `> 2.0` = STARK, `< -2.0` = SCHWACH.
*   **Stan Weinstein Stage:** Analysiert über MTF den wöchentlichen SMA 30.
    *   `Stage 2`: Weekly Close > SMA 30 **und** (SMA 30 steigt).
    *   `Stage 4`: Weekly Close < SMA 30 **und** (SMA 30 fällt).

### 6. Order-Preiskalkulation
Zentrale Variablen für Limit-Preise für die UI-Ausgabe (und optionale spätere API-Anbindung):
*   `sp_price` (Trigger / Stop-Preis für Entry): `high + puffer` (bei Long).
*   `sl_price` (Initial Stop-Loss): `low - puffer` (bei Long).
*   `tp_price` (Teilverkauf / T1): Ein berechneter Zielpreis (`(sp_price - sl_price) * 1.0` -> 1R) für Teilverkäufe.
*   `shares`: Kalkulierte Stückzahl basierend auf `risk_per_trade / (sp_price - sl_price)`.

### 7. Alarmsystem (`alert` calls)
Die Skript-Ausführung `alert()` triggert bei Erfüllung der logischen Baumstruktur mit dem Parameter `alert.freq_once_per_bar`. Dadurch reagiert der Indikator live auf Intrabar-Schwankungen (z.B. %R springt über Schwelle), um Diskretions-Trader frühzeitig "auf den Ping" zu holen, noch bevor die Kerze endgültig schließt.
