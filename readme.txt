# AKJ 2.0 Sniper-Commander
## Das taktische Lagezentrum (v20.5 Elite)

---
TEIL 1: FACHLICHES DOSSIER (System-Handbuch)
---

Hier ist die detaillierte, fachliche und technische Aufschlüsselung des AKJ 2.0 Sniper-Commander v20.5. Das System wurde in v20.5 um ein dynamisches Risikomanagement, Anchored Volume Profile (AVP) und strengere Doji-/Hysterese-Filter erweitert.

### I. Das Interaktive Cockpit (Dashboard)
Das HUD wurde logisch in Blöcken gruppiert, um dir während des Tradings den perfekten Überblick über Kontext, Metriken und Exekution zu geben. 

💡 **NEU IN v20.5:** Die Werte im Cockpit besitzen interaktive Tooltips. Wenn du mit der Maus (Mouse-over) über die Parameter-Titel in TradingView fährst, liefert das System dir sofortige strategische Erklärungen. 

**Folgende Tooltips sind im Chart aktiv:**
*   **Rel. Stärke:** „Vergleicht die Performance der Aktie mit ihrem Sektor über 20 Tage. STARK bedeutet Outperformance und erhöht die Wahrscheinlichkeit für einen erfolgreichen Trade.“
*   **Weinstein-Stage:** „Strategische Marktphase nach Stan Weinstein. Stage 2 = Institutionelle Akkumulation (Long), Stage 4 = Institutionelle Distribution (Short).“
*   **Wochentrend:** „Taktische Richtung auf Wochenbasis (Sticky). Erfordert 2 Schlusskurse außerhalb der Bollinger Bänder (10/1). Bleibt aktiv, bis die Gegenseite 2 Kerzen erzwingt.“
*   **Tagestrend:** „Kurzfristiges Timing-Radar. Nutzt einen dynamischen ATR-Puffer (Hysterese v20.5), um Fehlsignale in volatilen Phasen (VIX > 25) zu filtern.“
*   **Risk-O-Meter:** „Dynamische Positionsgröße (1R). Passt das Risiko basierend auf der Marktangst (VIX) und der Aktien-Volatilität (ATR) automatisch an. Basis: 150€.“
*   **Anchor-Info:** „Startpunkt des Anchored Volume Profile (AVP). Misst das Volumen exakt ab dem letzten Weinstein-Phasenwechsel oder Pivot-Punkt.“
*   **Vacuum Quality:** „Prüft die Liquiditätsdichte (RLD). High Quality bedeutet, dass der Preis kaum auf Widerstand stoßen wird (Vakuum).“
*   **Kerzenregel:** „Prüft die Preis-Aktion (Scharf-Kerze) inkl. ATR-basiertem Doji-Filter. OK bedeutet: Die Käufer/Verkäufer haben die Kontrolle übernommen.“
*   **Stopversicherung:** „Die Volumen-Mauer (🛡️) an deinem Stopp-Level. Gemessen ab dem Ankerpunkt (v20.5). Zielwert: >10% zur Absicherung der Position.“
*   **TP Widerstand:** „Das Volumen-Hindernis (🚧) bis zum Ziel. Gemessen per RLD-Verfahren (v20.5). Zielwert: <8% für einen freien Lauf (Vakuum) zum Take-Profit.“

> ⚠️ **NUTZER-HINWEIS:** Dieses Cockpit dient als Navigationshilfe zur Skalierung eines 50k Depots. Handeln Sie nur, wenn die Signal-Validierung grün leuchtet.

---
### II. v20.5 Innovationen (Das Kern-Upgrade)
Neben den sichtbaren Tooltips schlägt unter der Haube ein neues mathematisches Herz. Die v20.5 Code-Architektur löst die größten Probleme klassischer Trading-Indikatoren:

1.  **Die AVP/RLD-Synergie (Der Gamechanger):** Klassische Profiler messen einfach stumpf feste Tage (z.B. "Volumen der letzten 100 Tage"). Die **v20.5 Anker-Logik** startet den Volumen-Zähler erst zu dem exakten Zeitpunkt, an dem das "Smart Money" die Weinstein-Phase gedreht hat. Verbunden mit dem **RLD-Check** (Relative Liquidity Density) scannen wir nun nicht nach *irgendeinem* TP-Widerstand, sondern wir validieren echtes "High-Speed-Vakuum". Diese Synergie aus Anker und relativer Dichte steigert die Qualität des Setups massiv gegenüber der Vorversion.
2.  **Repaint Protection:** Absicherung des Multi-Timeframe (MTF) 4H Volumens auf dem Tageschart via `request.security_lower_tf()` und `barstate.isconfirmed`. Alarme triggern streng ohne Intrabar-Verzerrungen.
3.  **Sticky Trend Hysterese:** Um Rauschen an den Bändern auszufiltern, muss ein Trendausbruch nun 0.2 ATR über/unter das Band hinausschießen.

---
### III. Das Alarmsystem (Risk-Recycling & Phase-Shift)
*   **1. 📡 RADAR:** "AVP Anchor validiert. Lauer-Modus!" (Vor-Alarm).
*   **2. 🎯 SNIPER:** "Risk-Recycling bereit! Feuer frei!" (Alle Preis-Action Regeln + ATR-Doji-Filter + Sticky bestanden).
*   **3. 🏆 GOLDEN SETUP:** "Phase-Shift erkannt!" (Volumenprofil passt, RLD-Vakuum bestätigt).

---
### IV. TECHNISCHE DOKUMENTATION FÜR ENTWICKLER (Pine Script v6)

**Architektur und Ausführungslogik:**
Das Pine Script ist strikt modular aufgebaut. UI ist in 22-Tabellen-Zeilen gekapselt. Alarme überprüfen zwingend `if barstate.isrealtime and barstate.isconfirmed`. Die Zell-Definitionen in `table.cell()` nutzen das `tooltip` Argument.

**Dynamisches Risiko & ATR Hysterese:**
*   `atr_buffer = atr_val * 0.2` verhindert Fakeouts an den Bollinger Bändern.
*   `use_dyn_risk` schaltet den VIX-Quotienten ein: `risk_per_trade * (20.0 / vix_c)`.

**Lower Timeframe Repaint-Schutz (RLD):**
*   `request.security_lower_tf(syminfo.tickerid, "240", volume)`. Die RLD rechnet: `(current_bar_lower_vol / avg_anchor_vol) * 100`. Ein Volumen-Vakuum wird freigegeben, wenn der Pct-Wert unter `rld_limit` (20.0%) liegt.
