# AKJ 2.0 Sniper-Commander
## Das taktische Lagezentrum (v20.5 Elite)

---
TEIL 1: FACHLICHES DOSSIER (System-Handbuch)
---

Hier ist die detaillierte, fachliche und technische Aufschlüsselung des AKJ 2.0 Sniper-Commander v20.5. Das System wurde in v20.5 um ein dynamisches Risikomanagement, Anchored Volume Profile (AVP) und strengere Doji-/Hysterese-Filter erweitert.

### I. Das Cockpit (Dashboard) – Die neue v20.5 Architektur
Das HUD wurde logisch gruppiert, um dir während des Tradings den perfekten Überblick über Kontext, Metriken und Exekution zu geben.

**1. STATUS-ZEILE**
*   `!! GOLDEN !!` / `! FEUER FREI !` / `LAUERN` / `STAY`: Gibt den finalen Exekutions-Status vor.

**2. MARKT-KONTEXT**
*   **🌍 Sektor:** Dynamisches Mapping via `syminfo.sector`. ETF (z.B. SMH) Zuordnung.
*   **💪 Rel. Stärke:** Vergleicht die 20-Tage-Performance der Aktie mit dem Sektor-ETF (STARK, MITTEL, SCHWACH).
*   **📈 Weinstein Stage:** Regimewechsel via Wochen-SMA 30 (STAGE 2 Long / STAGE 4 Short / SEITWÄRTS).

**3. SNIPER-METRIKEN (Die v20.5 Engine)**
*   **📊 Risk-O-Meter (1R):** Dynamisches 1R basierend auf dem VIX. An volatilen Tagen wird das Basis-Risiko von z.B. 150€ automatisch reduziert (VIX/ATR-Ratio).
*   **⚓ Anchor-Info:** Zeigt an, vor wie vielen Bars das Anchored Volume Profile (AVP) gestartet wurde (Start beim letzten Weinstein-Stage Wechsel, max 300 Bars).
*   **📐 Vacuum Quality:** Relative Liquidity Density (RLD). Ein TP-Widerstand ist nur "High Quality" und valide, wenn die Dichte < 20% des Durchschnittsvolumens im Anker-Zeitraum liegt.

**4. MK-VALIDIERUNG**
*   **🕯️ Kerzenregel:** Wir kaufen den Dip! OK ✅ erfordert einen roten/grünen Körper gegen den Trend. NEU in v20.5: Ein ATR-Doji-Filter (Körper > 10% der ATR) verhindert falsche Signale.
*   **🛡️ Stopversicherung:** Volumen zwischen SP und SL. Ziel: > 10%.
*   **🚧 TP Widerstand:** Volumen zwischen SP und TP. Ziel: < 8% UND bestandener RLD-Check.

**5. ORDER-MATRIX**
*   **SP (Stoppreis):** Trigger für Einstieg.
*   **LP (LimitPreis):** Maximale Schmerzgrenze für Slippage.
*   **Stk (Anzahl):** Automatisch berechnete Stückzahl basierend auf dem Risk-O-Meter!
*   **TP (Teilverkauf):** Das kalkulierte 1:1 Risiko-Ertrags-Ziel (Risk-Recycling).
*   **SL (Stopp-Loss):** Feuerschutz unter der Signalkerze.

### II. Das Alarmsystem (Risk-Recycling & Phase-Shift)
*   **1. 📡 RADAR:** "AVP Anchor validiert. Lauer-Modus!" (Vor-Alarm).
*   **2. 🎯 SNIPER:** "Risk-Recycling bereit! Feuer frei!" (Alle Preis-Action Regeln + ATR-Doji-Filter + Sticky-Hysterese bestanden).
*   **3. 🏆 GOLDEN SETUP:** "Phase-Shift erkannt!" (Volumenprofil passt, RLD-Vakuum bestätigt).

### III. v20.5 Core Logik-Upgrades
1.  **Repaint Protection:** Absicherung des Multi-Timeframe (MTF) 4H Volumens auf dem Tageschart via `request.security_lower_tf()` und `barstate.isconfirmed`. Kein Vormogeln mehr unfertiger Kerzen!
2.  **Anchored Volume Profile (AVP):** Das System scannt nicht mehr stumpf 100 Tage zurück, sondern verankert den Beginn der Volumenmessung am Punkt des letzten signifikanten Regimewechsels (Weinstein Stage-Shift).
3.  **Sticky Trend Hysterese:** Um Rauschen an den Bollinger Bändern auszufiltern, muss ein Trendausbruch nun 0.2 ATR über/unter das Band hinausschießen, um den Setup-Zustand auszulösen.

---
TEIL 2: TECHNISCHE DOKUMENTATION FÜR ENTWICKLER (Pine Script v6)
---

### 1. Architektur und Ausführungslogik
Das Pine Script ist strikt modular aufgebaut. UI ist in Tabellen gekapselt und Alarme reagieren `freq_once_per_bar` bei echten Bestätigungen. 

### 2. Dynamisches Risiko & ATR Hysterese
*   `atr_buffer = atr_val * 0.2` verhindert Fakeouts an den Bollinger Bändern.
*   `use_dyn_risk` schaltet den VIX-Quotienten ein: `risk_per_trade * (20.0 / vix_c)`. Das schützt in Panikphasen das Kapital durch Positionsverkleinerung.

### 3. Lower Timeframe Repaint-Schutz (RLD)
Anstatt nur `request.security` zu nutzen, fragt v20.5 `request.security_lower_tf(syminfo.tickerid, "240", volume)` ab.
*   Die Relative Liquidity Density (RLD) rechnet: `(current_bar_lower_vol / avg_anchor_vol) * 100`.
*   Ein Volumen-Vakuum bis zum TP (Take Profit) wird nur freigegeben (`rld_valid = true`), wenn der Pct-Wert unter `rld_limit` (20.0%) liegt.

### 4. Anchored Iterator
Die eigene Volumen-Funktion `f_calc_tf_vol_anchored` bekommt einen dynamischen Lookback in `anchor_bars` übergeben. Dadurch wird die Density-Ratio nicht durch irrelevante alte Historie der Aktie vor dem letzten Trendbruch verzerrt.

### Fazit
Der Sniper-Commander v20.5 schließt die mathematische Brücke zwischen Volatilität und Volumen. Er handelt nicht nur, wenn das Setup "da ist", sondern wenn die Volumen-Textur im Markt den Trade auch *zulässt*.
