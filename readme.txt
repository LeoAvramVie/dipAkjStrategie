================================================================================
  AKJ 2.0 Sniper-Commander v20.7 — TECHNISCHE REFERENZ-DOKUMENTATION
  PineScript v6 | TradingView | Stand: April 2026
================================================================================

Dieses Dokument beschreibt JEDE Berechnungsformel, JEDEN Schwellenwert und JEDE
Alarmbedingung exakt so wie sie im Code implementiert ist. Kein Interpretationsspielraum.

================================================================================
  ABSCHNITT 1: PARAMETER & STANDARDWERTE
================================================================================

RISIKOMANAGEMENT (einstellbar):
  risk_per_trade    = 100.0 €    (Basis-Risiko pro Trade)
  limit_offset_pct  = 0.2 %      (Abstand LP vom SP für Gap-Schutz)
  atr_stop_mult     = 1.0        (ATR-Multiplikator für Stop-Loss)
  use_dyn_risk      = true       (asymmetrisches Risiko ein/aus)

STRATEGIE-PARAMETER:
  bb_len   = 10    (Bollinger Band Länge, Perioden)
  bb_mult  = 1.0   (Bollinger Band Multiplikator, Standardabweichungen)
  wpr_len  = 4     (Williams %R Periode)
  atr_len  = 14    (ATR Länge)

VOLUMEN-FILTER (4H Timeframe):
  min_stop_density    = 1.5 %    (Minimale Stop-Versicherung für FEUER FREI)
  max_tp_density      = 15.0 %   (Maximaler TP-Widerstand für FEUER FREI)
  golden_stop_density = 3.0 %    (Minimale Stop-Versicherung für GOLDEN SETUP)
  golden_tp_density   = 8.0 %    (Maximaler TP-Widerstand für GOLDEN SETUP)

================================================================================
  ABSCHNITT 2: RISIKO-REGIME (VIX-basiert)
================================================================================

Datenbasis: CBOE:VIX, Tages-Schlusskurs (lookahead=off)

BERECHNUNG risk_mult_l (Long-Risiko-Faktor):
  VIX < 25.0  → risk_mult_l = 1.0   (100% Risiko)
  VIX 25-35   → risk_mult_l = 0.25  (25% Risiko)
  VIX > 35    → risk_mult_l = 0.0   (0% Risiko = gesperrt)

BERECHNUNG risk_mult_s (Short-Risiko-Faktor):
  VIX < 25.0  → risk_mult_s = 1.0   (100% Risiko)
  VIX 25-35   → risk_mult_s = 1.0   (100% Risiko — Short-Bias!)
  VIX > 35    → risk_mult_s = 0.0   (0% Risiko = gesperrt)

AKTIVES RISIKO:
  active_risk_l = risk_per_trade × risk_mult_l   (falls use_dyn_risk=true)
  active_risk_s = risk_per_trade × risk_mult_s

ANZEIGE im Cockpit:
  VIX < 25.0  → "ALPHA (Full)"
  VIX 25-35   → "DELTA (Short-Bias)"
  VIX > 35    → "OMEGA (Lock)"

================================================================================
  ABSCHNITT 3: WOCHENTREND (w_trend)
================================================================================

Datenbasis: Weekly-Timeframe (lookahead=off), letzte 2 bestätigte Wochenkerzen

BOLLINGER BAND WÖCHENTLICH:
  basis_w  = SMA(close, 10) auf Wochenbasis
  dev_w    = STDEV(close, 10) × 1.0 auf Wochenbasis
  w_up     = basis_w + dev_w    (oberes Wochenband)
  w_lo     = basis_w - dev_w    (unteres Wochenband)
  w_basis_1 = SMA(close, 10)[1] auf Wochenbasis (letzte abgeschlossene Woche)

VERWENDETE WERTE:
  w_cl_1 = Wochenclose der vorletzten Woche (close[1] auf W-Chart)
  w_cl_2 = Wochenclose der vorvorletzten Woche (close[2] auf W-Chart)
  w_up_1 = Oberes Band der vorletzten Woche
  w_lo_1 = Unteres Band der vorletzten Woche
  w_up_2, w_lo_2 = Bänder 2 Wochen zurück

ZUSTANDSMASCHINE (sticky, nur Update bei Bedingungserfüllung):
  → BULLISCH (w_trend = 1):
      Bedingung: w_cl_1 > w_up_1 UND w_cl_2 > w_up_2
      (Beide letzten Wochenkerzen schlossen ÜBER dem oberen Wochenband)

  → BÄRISCH (w_trend = -1):
      Bedingung: w_cl_1 < w_lo_1 UND w_cl_2 < w_lo_2
      (Beide letzten Wochenkerzen schlossen UNTER dem unteren Wochenband)

  → NEUTRAL (w_trend = 0) — Fix v20.6:
      Wenn vorher BULLISCH: Bedingung: w_cl_1 < w_basis_1
      (Letzte Wochenkerze schloss unter der Wochenmittellinie SMA10)
      Wenn vorher BÄRISCH: Bedingung: w_cl_1 > w_basis_1
      (Letzte Wochenkerze schloss über der Wochenmittellinie SMA10)

  Hinweis: Bleibt auf aktuellem Stand wenn keine Bedingung erfüllt (sticky).
  Initialwert = 0 (NEUTRAL).

================================================================================
  ABSCHNITT 4: WEINSTEIN STAGE
================================================================================

Datenbasis: Weekly-Timeframe, letzte 2 bestätigte Wochenkerzen
  w_sma30_1 = SMA(close, 30)[1] auf Wochenbasis
  w_sma30_2 = SMA(close, 30)[2] auf Wochenbasis

BERECHNUNG:
  Stage 2 (Long): w_cl_1 > w_sma30_1 UND w_sma30_1 > w_sma30_2
    → Kurs über der SMA30 UND SMA30 steigt (institutionelle Akkumulation)

  Stage 4 (Short): w_cl_1 < w_sma30_1 UND w_sma30_1 < w_sma30_2
    → Kurs unter der SMA30 UND SMA30 fällt (institutionelle Distribution)

  Sonst: SEITWÄRTS (weinstein_stage = 0)

ANCHOR-BARS (Startpunkt der Volumenanalyse):
  anchor_bars = bar_index - stage_change_bar
  (Anzahl Tagesbars seit letztem Weinstein Stage-Wechsel, max. 300)

================================================================================
  ABSCHNITT 5: TAGESTREND / SCHARF-MODUS (setup_strict)
================================================================================

BOLLINGER BAND TÄGLICH:
  d_basis = SMA(close, 10)
  d_up    = d_basis + STDEV(close, 10) × 1.0
  d_lo    = d_basis - STDEV(close, 10) × 1.0
  atr_buffer = ATR(14) × 0.2  (Hysteresepuffer)

SCHARF-MODUS AKTIVIERUNG (setup_strict_long = true):
  Bedingung: close[1] > d_up[1] + atr_buffer UND close[2] > d_up[2] + atr_buffer
  (Gestern UND vorgestern schloss die Aktie mind. 0.2×ATR über dem oberen Tagesband)
  → Bedeutet: Stock "läuft an den Bändern entlang" (Walking the Bands)

SCHARF-MODUS DEAKTIVIERUNG (setup_strict_long = false):
  Bedingung: close[1] < d_lo[1] UND close[2] < d_lo[2]
  (Gestern UND vorgestern schloss die Aktie unter dem unteren Tagesband)
  → Strategie 80% Dip-Käufer: Modus bleibt bis zum unteren Band aktiv!
  → Das erlaubt WPR-Signale an der Mittellinie (bester Einstiegspunkt)

DOJI-FILTER:
  is_doji = |close - open| < ATR(14) × 0.1
  (Kerzenkörper kleiner als 10% des ATR → wird als Doji gewertet, kein Signal)

================================================================================
  ABSCHNITT 6: PREISBERECHNUNG (Order-Matrix)
================================================================================

LONG:
  sp_long  = high (Stoppkauf-Trigger: Hoch der aktuellen Kerze)
  sl_long  = low - (ATR(14) × atr_stop_mult)  [Standard: low - 1.0×ATR]
  tp_long  = sp_long + (sp_long - sl_long)      [1:1 CRV]
  r_l      = max(|sp_long - sl_long| × pointvalue, mintick)
  shares_l = floor(active_risk_l / r_l)
  lp_long  = sp_long × (1 + 0.002)             [Gap-Schutz +0.2%]

SHORT:
  sp_short = low (Stoppverkauf-Trigger: Tief der aktuellen Kerze)
  sl_short = high + (ATR(14) × atr_stop_mult)
  tp_short = sp_short - (sl_short - sp_short)
  r_s      = max(|sp_short - sl_short| × pointvalue, mintick)
  shares_s = floor(active_risk_s / r_s)
  lp_short = sp_short × (1 - 0.002)            [Gap-Schutz -0.2%]

RICHTUNGSAUSWAHL (basierend auf w_trend):
  w_trend == -1  → Short-Werte aktiv
  sonst          → Long-Werte aktiv (inkl. NEUTRAL!)

================================================================================
  ABSCHNITT 7: VOLUMENANALYSE (Anchored Volume Profile, 4H)
================================================================================

METHODE: Für jeden 4H-Bar innerhalb von anchor_bars (max 300):
  zone_vol_stop += bar_volume × (Überschneidung Stop-Zone / Bar-Range)
  zone_vol_tp   += bar_volume × (Überschneidung TP-Zone / Bar-Range)

STOP-VERSICHERUNG (stop_density):
  = (zone_vol_stop / total_volume) × 100 [%]
  Stop-Zone: Preisbereich zwischen Entry (SP) und Stop-Loss (SL)

TP-WIDERSTAND (tp_density):
  = (zone_vol_tp / total_volume) × 100 [%]
  TP-Zone: Preisbereich zwischen Entry (SP) und Take-Profit (TP)

VACUUM QUALITY:
  vacuum_ok = tp_density <= max_tp_density (Standard: <= 15%)
  → "High (TP X.X%)" wenn Weg frei
  → "Low (TP X.X%)"  wenn zu viel Widerstand

PERFORMANCE-GATE: Volumenberechnung läuft nur auf dem letzten Bar oder
  innerhalb der letzten 1000 Bars (Lazy Loading für Screeningperformance).

================================================================================
  ABSCHNITT 8: BOLLINGER ZONE CHECK (12-Zonen-System)
================================================================================

BERECHNUNG:
  bc_basis = SMA(close, 10) [aktueller Tagesclose, Intrabar-Wert]
  bc_dev   = STDEV(close, 10) × 1.0
  bc_ub    = bc_basis + bc_dev    (oberes Band)
  bc_lb    = bc_basis - bc_dev    (unteres Band)
  bc_unit  = (bc_ub - bc_lb) / 12  (1/12 der Band-Breite)

ZONENEINTEILUNG:
  close > bc_ub                         → "SHORT (EXTREME)"   [über Band]
  close >= bc_lb + (8 × bc_unit)        → "SHORT ZONE"        [obere 1/3]
  close >= bc_lb + (4 × bc_unit)        → "NEUTRAL"           [mittlere 1/3]
  close >= bc_lb                        → "LONG ZONE"         [untere 1/3]
  close < bc_lb                         → "LONG (EXTREME)"    [unter Band]

ZONE-FREIGABE FÜR SIGNALE:
  is_correct_zone_l = (bc_txt == "LONG ZONE" OR "LONG (EXTREME)") OR setup_strict_long
  is_correct_zone_s = (bc_txt == "SHORT ZONE" OR "SHORT (EXTREME)") OR setup_strict_short

  → Im Scharf-Modus (setup_strict_long=true) wird die Zone automatisch übergangen!
    Das erlaubt Walking-the-Bands Signale auch wenn Kurs im oberen Bereich ist.

================================================================================
  ABSCHNITT 9: SIGNAL-IDENTIFIKATION (vollständige Bedingungskette)
================================================================================

SCHRITT 1: RADAR-ZUSTAND

  is_radar_l = high >= d_up + (ATR(14) × 0.2)
  (Hoch der aktuellen Kerze mind. 0.2×ATR über dem oberen Tagesband)

  radar_state_l = (weinstein_stage == 2) UND (is_radar_l OR setup_strict_long)
  (Weinstein Stage 2 UND: entweder aktuell über Band ODER Scharf-Modus aktiv)

  radar_state_s = (weinstein_stage == 4) UND (is_radar_s OR setup_strict_short)
  is_radar_s = low <= d_lo - (ATR(14) × 0.2)

SCHRITT 2: RAW-TRIGGER (Kerzenregel + WPR)

  long_trigger  = WPR(4) >= 80 UND close < open UND NOT is_doji UND close > d_lo
  short_trigger = WPR(4) <= 20 UND close > open UND NOT is_doji UND close < d_up

  WPR(4): abs(ta.wpr(4))  → Werte 0-100, 80+ = tief überverkauft = DIP
  Kerzenregel Long:  Bearische Kerze (close < open), kein Doji, nicht unter unterem Band
  Kerzenregel Short: Bullische Kerze (close > open), kein Doji, nicht über oberem Band

  raw_feuer_l = weinstein_stage == 2 UND long_trigger
  raw_feuer_s = weinstein_stage == 4 UND short_trigger

SCHRITT 3: VOLUMEN-VALIDIERUNG

  vol_feuer_l  = stop_density >= 1.5% UND tp_density <= 15.0%
  vol_feuer_s  = stop_density >= 1.5% UND tp_density <= 15.0%
  vol_golden_l = stop_density >= 3.0% UND tp_density <= 8.0%
  vol_golden_s = stop_density >= 3.0% UND tp_density <= 8.0%

SCHRITT 4: FINALE TRIGGER-BOOLEANS

  trigger_lauern_l = radar_state_l UND WPR(4) < 80
  trigger_lauern_s = radar_state_s UND WPR(4) > 20

  trigger_feuer_l  = raw_feuer_l
  trigger_feuer_s  = raw_feuer_s

  trigger_golden_l = raw_feuer_l UND vol_golden_l
  trigger_golden_s = raw_feuer_s UND vol_golden_s

AKJ ELITE SIGNAL (eigene Logik, unabhängig von Volumen):
  isAKJSignal_l = weinstein_stage==2 UND setup_strict_long UND WPR(4)>=80
                  UND low > d_lo UND close < open UND NOT is_doji
  isAKJSignal_s = weinstein_stage==4 UND setup_strict_short UND WPR(4)<=20
                  UND high < d_up UND close > open UND NOT is_doji

  Besonderheit: KEIN Volumenfilter! AKJ Elite prüft nur Trend + Scharf + WPR + Preiposition.
  Besonderheit: low > d_lo (Kurs über unterem Band) statt close > d_lo beim Feuer-Trigger.

================================================================================
  ABSCHNITT 10: SIGNAL-PRIORISIERUNG (Status-Hierarchie)
================================================================================

Die Statustexte werden in dieser Reihenfolge geprüft (höchste Priorität zuerst):

  1. isAKJSignal_l  → "AKJ_ELITE_LONG"
  2. isAKJSignal_s  → "AKJ_ELITE_SHORT"
  3. trigger_golden_l → "GOLDEN_LONG"
  4. trigger_golden_s → "GOLDEN_SHORT"
  5. trigger_feuer_l  → "FEUER_LONG"
  6. trigger_feuer_s  → "FEUER_SHORT"
  7. trigger_lauern_l → "LAUERN_LONG"
  8. trigger_lauern_s → "LAUERN_SHORT"
  9. (sonst)          → "STATUS: NO SIGNAL"

  → Es kann jeweils nur EIN Status aktiv sein (else-if-Kette).
  → AKJ ELITE hat immer Vorrang vor GOLDEN, GOLDEN vor FEUER, etc.

================================================================================
  ABSCHNITT 11: COCKPIT STATUSANZEIGE (Logik vs. Screener)
================================================================================

Das Cockpit prüft von oben nach unten, welcher Status erreicht ist. Jede Ebene durchläuft exakte mathematische Checks für Long- und Short-Signale:

  1. 💎 AKJ ELITE ➔ Sonder-Signal! Extremes Momentum (Scharf-Modus).
     Technisch LONG: weinstein_stage == 2 UND setup_strict_long UND wpr >= 80 UND low > d_lo UND close < open UND NOT is_doji.
     Technisch SHORT: weinstein_stage == 4 UND setup_strict_short UND wpr <= 20 UND high < d_up UND close > open UND NOT is_doji.
     Fachlich: Wir befinden uns in einem massiven Trend, dass wir jeden minimalen Rücksetzer sofort blind traden. Komplett ohne Volumencheck!

  2. 🌟 GOLDEN ➔ Das Premium-Setup! Ein FEUER-Signal plus einer massiven Volumen-Mauer.
     Technisch LONG: raw_feuer_l UND vol_golden_l (Stop-Dichte >= 3% & TP-Dichte <= 8%) UND rs_ok_for_premium.
     Technisch SHORT: raw_feuer_s UND vol_golden_s (Stop-Dichte >= 3% & TP-Dichte <= 8%) UND rs_ok_for_premium.
     Fachlich: Perfektes Timing, und das Volume Profile zeigt massive Institutionelle Orders direkt hinter dem Entry als Schutz an. Kein Zonen-Check nötig!

  3. 🟢 FEUER FREI ➔ Basis-Signal! Reines Chart- & Timing-Setup.
     Technisch LONG: raw_feuer_l (weinstein == 2 UND wpr >= 80 UND rote Kerze UND NOT doji).
     Technisch SHORT: raw_feuer_s (weinstein == 4 UND wpr <= 20 UND grüne Kerze UND NOT doji).
     Fachlich: Klasisches Pullback Setup ("Reversion to Mean"). Kein Volumenzwang, kein Bollinger-Hysterese Zwang, kein Zonen-Check! Lediglich Weinstein Stage muss stimmen.

  4. 📡 LAUERN ➔ Frühwarn-Radar. 
     Technisch LONG:  weinstein_stage == 2 UND d_wpr >= 70 UND d_wpr < 80.
     Technisch SHORT: weinstein_stage == 4 UND d_wpr <= 30 UND d_wpr > 20.
     Fachlich: Macht uns darauf aufmerksam, dass das Momentum sich bald überladen könnte. Vorwarn-Phase!

  5. STATUS: NO SIGNAL ➔ Nichts erfüllt.

ZUSÄTZE IM COCKPIT-HEADER:
  1. Cooldown-Sperre: [Wait: Xs]
     Sperrt das Signal-System für 3 Minuten nach einem Auslöser als Anti-Spam Filter.

TAGESTREND-ZEILE IM COCKPIT (Angezeigte Modi):
  • LONG / SHORT (Scharf) 
    = Der "Scharf-Modus" (starker, anhaltender Trend) ist aktiv.
      Bedingung (Long): close[1] > d_up[1] + (ATR*0.2) UND close[2] > d_up[2] + (ATR*0.2)
  • LONG / SHORT (Radar)
    = Aktie hat das äußere Bollinger Band berührt, aber der Trend ist noch nicht "Scharf" genug.
      Bedingung (Long): close[1] > d_up[1]
  • NEUTRAL
    = Weder Scharf noch Radar aktiv (Kurs bewegt sich innerhalb der Bollinger Bänder).

WARUM KOMMT ES ZU ABWEICHUNGEN (Screener +4, Cockpit LAUERN)?
  - Screener = "Snapshot" (z.B. alle paar Minuten oder auf Kerzenschluss).
  - Cockpit = "Echtzeit-Tick"
  Wenn der WPR z.B. von 80 (Snapshot / +4) auf 79.8 (Tick / LAUERN) fällt, siehst du live 
  was unter der Haube flackert. Der Alarm schützt durch sein 30s Cooldown vor diesem Flackern!

================================================================================
  ABSCHNITT 11: ALARMSYSTEM — EXAKTE BEDINGUNGEN
================================================================================

WANN KANN EIN ALARM FEUERN? (can_alert)
  can_alert = barstate.isrealtime           ← NUR bei Live-Echtzeitdaten
              UND cooldown_over             ← 3-Minuten-Sperre abgelaufen
              UND is_action_status          ← Status ist FEUER/GOLDEN/ELITE (nicht LAUERN!)
              UND status_is_new             ← Status hat sich seit letztem Alarm geändert

  cooldown_over: timenow - last_fired_time > 180.000 ms (3 Minuten)
  is_action_status: tac_txt ∈ {AKJ_ELITE_LONG/SHORT, FEUER_LONG/SHORT, GOLDEN_LONG/SHORT}
  status_is_new: tac_txt != last_fired_status

  !!! WICHTIG: LAUERN feuert KEINEN Alarm (nur Cockpit-Anzeige)
  !!! WICHTIG: Kein Alarm auf historischen Bars (nur barstate.isrealtime)
  !!! WICHTIG: Kein Alarm wenn gleicher Status wie letzter Alarm (Anti-Doppel-Alarm)

WELCHE ALARM-FREQUENZ PRO SIGNAL-TYP:
  AKJ_ELITE_LONG / AKJ_ELITE_SHORT → alert.freq_once_per_bar_close
    (Alarm NUR beim Kerzenschluss, nicht intrabar)
  GOLDEN_LONG / GOLDEN_SHORT       → alert.freq_once_per_bar
    (Alarm einmal pro Bar, kann intrabar kommen)
  FEUER_LONG / FEUER_SHORT         → alert.freq_once_per_bar

RE-ARMING (Zurücksetzen des Anti-Doppel-Schutzes):
  Wenn Status auf NO SIGNAL zurückgeht → last_fired_status = ""
  → Nächster Alarm kann wieder für den gleichen Alarmtyp feuern

STAR-TICKER PREFIX im Alarm:
  Wenn historischer Erwartungswert (Ø R × risk) > 0:
  → Alarm-Nachricht bekommt "🔥 [STAR-TICKER] " als Präfix

================================================================================
  ABSCHNITT 12: ALARMNACHRICHT — INHALT
================================================================================

Jeder Alarm enthält folgende strukturierte Nachricht:

  GRUND: [automatisch erklärter Trigger-Grund]
  --- COCKPIT DATEN ---
  ZEITPUNKT: yyyy-MM-dd HH:mm:ss (UTC)
  TICKER: [Symbol]
  [Signal-Status]
  --- MARKT-KONTEXT ---
  Sektor: [ETF] [(Ticker)]
  Rel. Stärke: STARK/MITTEL/SCHWACH
  Weinstein Stage: STAGE 2/4/SEITWÄRTS
  --- TREND-ANALYSE ---
  Wochentrend: BULLISCH/NEUTRAL/BÄRISCH (Sticky)
  Tagestrend:  LONG/SHORT (Radar/Scharf) / NEUTRAL
  --- SNIPER METRIKEN ---
  Risk-O-Meter: [€]
  Risk-Mode: ALPHA/DELTA/OMEGA
  Anchor-Info: [X] Bars ago
  Vacuum Quality: High/Low (TP X.X%)
  Momentum (WPR): [Wert 0-100]
  Kerzenregel: OK / WAIT
  Stopversicherung: X.X%
  TP Widerstand: X.X%
  --- ORDER-MATRIX ---
  Stoppreis (SP): [Preis]
  Limitpreis (LP): [SP × 1.002 (Long) / SP × 0.998 (Short)]
  Anzahl (Stk): [Shares]
  TP (Teilverkauf): [Preis]
  Stopp-Loss (SL): [Preis]
  Runner-Target: EMA 21: [Wert]
  --- ZUSATZ-INFO ---
  Bollinger Check: [Zone]

================================================================================
  ABSCHNITT 13: ZUSAMMENFASSUNG ALARM-TRIGGER-TABELLE
================================================================================

Signal          | weinstein | scharf  | WPR       | Kerze | Vol.Stop | Vol.TP | Zone   | Alarm?
----------------|-----------|---------|-----------|-------|----------|--------|--------|-------
LAUERN LONG     | Stage 2   | -       | 70 - 79   | -     | KEIN     | KEIN   | -      | JA
LAUERN SHORT    | Stage 4   | -       | 21 - 30   | -     | KEIN     | KEIN   | -      | JA
FEUER LONG      | Stage 2   | -       | >= 80     | Bear  | KEIN     | KEIN   | -      | JA
FEUER SHORT     | Stage 4   | -       | <= 20     | Bull  | KEIN     | KEIN   | -      | JA
GOLDEN LONG     | Stage 2   | -       | >= 80     | Bear  | >= 3.0%  | <= 8%  | -      | JA
GOLDEN SHORT    | Stage 4   | -       | <= 20     | Bull  | >= 3.0%  | <= 8%  | -      | JA
AKJ ELITE LONG  | Stage 2   | MUSS!   | >= 80     | Bear  | KEIN     | KEIN   | -      | JA
AKJ ELITE SHORT | Stage 4   | MUSS!   | <= 20     | Bull  | KEIN     | KEIN   | -      | JA


  "oder" bedeutet: radar_state ODER setup_strict genügen für die Radar-Bedingung
  "korrekt" bedeutet: Zone passt ODER Scharf-Modus aktiv (Zone wird dann übergangen)

ZUSÄTZLICHE SPERRUNG durch Cooldown:
  Kein Alarm wenn < 3 Minuten seit letztem Alarm vergangen sind.

================================================================================
  ABSCHNITT 14: PINE SCREENER CODE
================================================================================

Export-Variable "Sniper Status" (Werte -4 bis +4):
  +4 = AKJ_ELITE_LONG    -4 = AKJ_ELITE_SHORT
  +3 = GOLDEN_LONG        -3 = GOLDEN_SHORT
  +2 = FEUER_LONG         -2 = FEUER_SHORT
  +1 = LAUERN_LONG        -1 = LAUERN_SHORT
   0 = NO SIGNAL

================================================================================
