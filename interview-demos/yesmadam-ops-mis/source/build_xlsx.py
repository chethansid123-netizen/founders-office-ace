"""Build the VP Ops weekly MIS workbook from data.json. Every KPI is a live formula."""
import datetime as dt
import json
import random
import sys

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.comments import Comment
from openpyxl.formatting.rule import ColorScaleRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

D = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
CUR, PREV = D["meta"]["cur"], D["meta"]["prev"]
WEEKS = D["meta"]["weeks"]
CITIES = D["cities"]

# ------------------------------------------------------------------ styles
FONT = "Arial"
F = lambda **k: Font(name=FONT, size=k.pop("size", 10), **k)
INK, MUTED, WHITE = "1F2937", "6B7280", "FFFFFF"
HEAD_FILL = PatternFill("solid", fgColor="1F2937")
BLOCK_FILL = PatternFill("solid", fgColor="EEF0F3")
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
NOTE_FILL = PatternFill("solid", fgColor="F7F7F4")
GREEN_FILL = PatternFill("solid", fgColor="D9F2DC")
AMBER_FILL = PatternFill("solid", fgColor="FFE9B3")
RED_FILL = PatternFill("solid", fgColor="F8D3D3")
GRAY_FILL = PatternFill("solid", fgColor="E7E7E4")
HAIR = Side(style="thin", color="D9D9D6")
BOTTOM = Border(bottom=HAIR)
INPUT_FONT = F(color="0000FF", bold=True)
LINK_FONT = F(color="008000")
CENTER = Alignment(horizontal="center", vertical="center")
WRAP = Alignment(wrap_text=True, vertical="top")

PCT1, PCT0, INT, D1, D2 = "0.0%", "0%", "#,##0", "0.0", "0.00"
PTS = '+0.0" pts";-0.0" pts";0.0" pts"'
CHG = "+0.0%;-0.0%;0.0%"
CD1, CD2 = "+0.0;-0.0;0.0", "+0.00;-0.00;0.00"
LAKH = '"₹"#,##0.0" L"'

wb = Workbook()
wb.remove(wb.active)


def sheet(name, grid=False, tab=None):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = grid
    if tab:
        ws.sheet_properties.tabColor = tab
    return ws


def name(n, ref):
    wb.defined_names[n] = DefinedName(n, attr_text=ref)


def put(ws, ref, value, font=None, fmt=None, fill=None, align=None, border=None):
    c = ws[ref]
    c.value = value
    c.font = font or F()
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if align:
        c.alignment = align
    if border:
        c.border = border
    return c


def header_row(ws, row, col0, labels, widths=None):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=col0 + i, value=lab)
        c.font = F(bold=True, color=WHITE)
        c.fill = HEAD_FILL
        c.alignment = Alignment(horizontal="center" if i else "left", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 30


def title(ws, text, sub=None):
    put(ws, "B1", text, F(size=16, bold=True, color=INK))
    if sub:
        put(ws, "B2", sub, F(size=10, italic=True, color=MUTED))
    ws.row_dimensions[1].height = 26
    ws.column_dimensions["A"].width = 2


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


def rag_rules(ws, rng):
    first = rng.split(":")[0]
    for txt, fill, color in (("Green", GREEN_FILL, "006100"), ("Amber", AMBER_FILL, "7A5000"),
                             ("Red", RED_FILL, "9C0006"), ("Info", GRAY_FILL, "52514E")):
        ws.conditional_formatting.add(rng, FormulaRule(formula=[f'{first}="{txt}"'], fill=fill,
                                                       font=Font(name=FONT, bold=True, color=color)))


MOCK = "Mock data for an interview demo. Not actual company figures. Prepared by Chethan."

# ------------------------------------------------------------------ sheets (order = tab order)
ws_cover = sheet("Cover", tab="1F2937")
ws_mis = sheet("Weekly MIS", tab="2A78D6")
ws_ns = sheet("North Star", tab="2A78D6")
ws_mon = sheet("Monthly", tab="2A78D6")
ws_city = sheet("City View", tab="2A78D6")
ws_sup = sheet("Supply", tab="2A78D6")
ws_q = sheet("Quality & Kits", tab="2A78D6")
ws_act = sheet("Action Tracker", tab="EB6834")
ws_chk = sheet("Data Checks", tab="EB6834")
ws_tgt = sheet("Targets", tab="FAB219")
ws_dict = sheet("Metric Dictionary", tab="FAB219")
ws_jd = sheet("JD Map", tab="FAB219")
ws_data = sheet("Data", grid=True, tab="9CA3AF")
ws_raw = sheet("Raw Bookings", grid=True, tab="9CA3AF")
ws_lists = sheet("Lists", grid=True)

# ------------------------------------------------------------------ Data (fact table)
DCOLS = [  # header, json key, defined name, format
    ("Week", "week", "d_week", "0"), ("Week starting", "week_start", "d_start", "d mmm yyyy"),
    ("Month (ISO)", "month", "d_month", None), ("City", "city", "d_city", None),
    ("Booking requests", "req", "d_req", INT), ("Partner assigned", "asg", "d_asg", INT),
    ("Cancelled, customer", "cc", "d_cc", INT), ("Cancelled, partner", "pc", "d_pc", INT),
    ("Jobs completed", "comp", "d_comp", INT), ("Started on time", "ot", "d_ot", INT),
    ("Perfect bookings", "perfect", "d_perf", INT), ("Complaints", "cpl", "d_cpl", INT),
    ("Redo / refunds", "redo", "d_redo", INT), ("Ratings given", "rc", "d_rc", INT),
    ("Sum of stars", "rs", "d_rs", INT), ("Ratings below 4★", "low", "d_low", INT),
    ("Active partners", "act", "d_act", INT), ("New partners certified", "cert", "d_cert", INT),
    ("Partners with kit stock-out", "stock", "d_stock", INT), ("Cohort size (joined 13 wks ago)", "coh", "d_coh", INT),
    ("Cohort still active", "coh_a", "d_coha", INT), ("GMV (₹)", "gmv", "d_gmv", INT),
]
ws_data["A1"].value = None
header_row(ws_data, 1, 1, [c[0] for c in DCOLS])
rows = sorted(D["rows"], key=lambda r: (r["week"], CITIES.index(r["city"])))
NROW = len(rows)
LAST = NROW + 1
for i, r in enumerate(rows, start=2):
    for j, (h, k, n, fmt) in enumerate(DCOLS, start=1):
        v = r[k]
        if k == "week_start":
            v = dt.datetime.fromisoformat(v)
        c = ws_data.cell(row=i, column=j, value=v)
        c.font = F()
        if fmt:
            c.number_format = fmt
for j, (h, k, n, fmt) in enumerate(DCOLS, start=1):
    col = ws_data.cell(row=1, column=j).column_letter
    name(n, f"Data!${col}$2:${col}${LAST}")
    ws_data.column_dimensions[col].width = 13 if j > 4 else (16 if j == 4 else 11)
ws_data.column_dimensions["D"].width = 18
ws_data.freeze_panes = "E2"
ws_data.auto_filter.ref = f"A1:{ws_data.cell(row=1, column=len(DCOLS)).column_letter}{LAST}"
note = ws_data.cell(row=LAST + 2, column=1, value="Source: ops app weekly extract by city (mock). One row per city per week. "
                    "Every KPI in this workbook is built from these counts with SUMIFS, then divided. Rates are never averaged.")
note.font = F(italic=True, color=MUTED)

# ------------------------------------------------------------------ Lists (validation sources)
ws_lists["A1"], ws_lists["B1"], ws_lists["C1"], ws_lists["D1"] = "Weeks", "Scope", "Owners", "Statuses"
for i, w in enumerate(range(32, CUR + 1), start=2):
    ws_lists.cell(row=i, column=1, value=w)
for i, c in enumerate(["All India"] + CITIES, start=2):
    ws_lists.cell(row=i, column=2, value=c)
OWNERS = ["City Ops", "Supply", "Training & QA", "CX", "Inventory", "Founder's Office"]
for i, c in enumerate(OWNERS, start=2):
    ws_lists.cell(row=i, column=3, value=c)
STATUSES = ["Not started", "In progress", "Blocked", "Done"]
for i, c in enumerate(STATUSES, start=2):
    ws_lists.cell(row=i, column=4, value=c)
ws_lists.sheet_state = "hidden"

# ------------------------------------------------------------------ Targets
KPIS = [  # key, block, metric, unit, direction, target, owner, good-when, national-only, fmt
    ("nsm", "North Star", "Perfect booking rate", "rate", "Higher", 0.77, "All five", "Up", "No", PCT1),
    ("req", "Demand & fulfilment", "Booking requests", "count", "Info", None, "City Ops", "Up", "No", INT),
    ("fill", None, "Fill rate", "rate", "Higher", 0.95, "City Ops", "Up", "No", PCT1),
    ("comp", None, "Jobs completed", "count", "Info", None, "City Ops", "Up", "No", INT),
    ("ot", None, "On-time arrival", "rate", "Higher", 0.92, "City Ops", "Up", "No", PCT1),
    ("cc", None, "Cancellations, customer side", "rate", "Lower", 0.03, "CX", "Down", "No", PCT1),
    ("pc", None, "Cancellations, partner side", "rate", "Lower", 0.015, "Supply", "Down", "No", PCT1),
    ("act", "Partner supply", "Active partners (1+ job)", "count", "Higher", 7600, "Supply", "Up", "Yes", INT),
    ("cert", None, "New partners certified", "count", "Higher", 200, "Training & QA", "Up", "Yes", INT),
    ("ret", None, "90-day retention (cohort)", "rate", "Higher", 0.70, "Supply", "Up", "No", PCT0),
    ("jppd", "Productivity", "Jobs per active partner per day", "decimal", "Higher", 1.65, "City Ops", "Up", "No", D2),
    ("rating", "Quality", "Average rating", "decimal", "Higher", 4.70, "Training & QA", "Up", "No", D2),
    ("cpk", None, "Complaints per 1,000 jobs", "decimal", "Lower", 8.0, "CX", "Down", "No", D1),
    ("redo", None, "Redo / refund rate", "rate", "Lower", 0.012, "CX", "Down", "No", PCT1),
    ("kit", "Kits", "Partners with a kit stock-out", "rate", "Lower", 0.02, "Inventory", "Down", "No", PCT1),
]
title(ws_tgt, "Targets and status rule", "Change a target here and every status in the workbook updates. Yellow cells are inputs.")
put(ws_tgt, "B4", "Amber band", F(bold=True))
put(ws_tgt, "C4", 0.05, INPUT_FONT, PCT0, INPUT_FILL)
put(ws_tgt, "D4", "Green meets target. Amber is within this % of target. Red is further off.", F(color=MUTED))
name("amber_band", "Targets!$C$4")
header_row(ws_tgt, 6, 2, ["Key", "Metric", "Unit", "Direction", "Target", "Owner", "Good when", "National target only", "Notes"])
NOTES = {
    "nsm": "North Star. Perfect bookings ÷ booking requests",
    "act": "National target. Shows as Info when a single city is selected",
    "cert": "National target. Shows as Info when a single city is selected",
    "ret": "Cohort that joined 13 weeks ago",
    "jppd": "Assumes 6 working days a week",
    "ot": "On time = started within 15 min of slot. To agree with the VP",
}
TROW = {}
for i, k in enumerate(KPIS, start=7):
    key, block, metric, unit, dirn, tgt, owner, good, nat, fmt = k
    TROW[key] = i
    vals = [key, metric, unit, dirn, tgt, owner, good, nat, NOTES.get(key, "")]
    for j, v in enumerate(vals, start=2):
        c = ws_tgt.cell(row=i, column=j, value=v)
        c.font = F()
        c.border = BOTTOM
    tc = ws_tgt.cell(row=i, column=6)
    if tgt is not None:
        tc.font, tc.fill, tc.number_format = INPUT_FONT, INPUT_FILL, fmt
        name(f"t_{key}", f"Targets!$F${i}")
    else:
        tc.value = "–"
        tc.alignment = CENTER
T0, T1 = 7, 6 + len(KPIS)
for n, col in (("tg_key", "B"), ("tg_metric", "C"), ("tg_dir", "E"), ("tg_target", "F"), ("tg_owner", "G"),
               ("tg_good", "H"), ("tg_nat", "I")):
    name(n, f"Targets!${col}${T0}:${col}${T1}")
widths(ws_tgt, {"B": 9, "C": 32, "D": 9, "E": 11, "F": 10, "G": 15, "H": 11, "I": 12, "J": 58})
ws_tgt.freeze_panes = "B7"

# ------------------------------------------------------------------ KPI formula builder
FIELD = {"req": "req", "asg": "asg", "cc": "cc", "pc": "pc", "comp": "comp", "ot": "ot", "perf": "perf",
         "cpl": "cpl", "redo": "redo", "rc": "rc", "rs": "rs", "low": "low", "act": "act", "cert": "cert",
         "stock": "stock", "coh": "coh", "coha": "coha", "gmv": "gmv"}


def kpi_expr(key, S, n="1"):
    """S(field) returns an expression for the summed count; n is the number of weeks summed."""
    return {
        "nsm": f"{S('perf')}/{S('req')}",
        "req": f"{S('req')}/{n}",
        "fill": f"{S('asg')}/{S('req')}",
        "comp": f"{S('comp')}/{n}",
        "ot": f"{S('ot')}/{S('comp')}",
        "cc": f"{S('cc')}/{S('asg')}",
        "pc": f"{S('pc')}/{S('asg')}",
        "act": f"{S('act')}/{n}",
        "cert": f"{S('cert')}/{n}",
        "ret": f"{S('coha')}/{S('coh')}",
        "jppd": f"{S('comp')}/({S('act')}*6)",
        "rating": f"{S('rs')}/{S('rc')}",
        "cpk": f"{S('cpl')}/{S('comp')}*1000",
        "redo": f"{S('redo')}/{S('comp')}",
        "kit": f"{S('stock')}/{S('act')}",
    }[key]


def lookup(col_name, row_key_ref):
    return f"INDEX({col_name},MATCH({row_key_ref},tg_key,0))"


def status_formula(key_ref, val_ref, tgt_ref):
    d = lookup("tg_dir", key_ref)
    return (f'=IF(OR({d}="Info",{tgt_ref}="–"),"Info",IF({d}="Higher",'
            f'IF({val_ref}>={tgt_ref},"Green",IF({val_ref}>={tgt_ref}*(1-amber_band),"Amber","Red")),'
            f'IF({val_ref}<={tgt_ref},"Green",IF({val_ref}<={tgt_ref}*(1+amber_band),"Amber","Red"))))')


def change_fmt(unit, fmt):
    if unit == "rate":
        return PTS
    if unit == "count":
        return CHG
    return CD1 if fmt == D1 else CD2


def change_formula(unit, cur, prev):
    if unit == "rate":
        return f"=({cur}-{prev})*100"
    if unit == "count":
        return f"={cur}/{prev}-1"
    return f"={cur}-{prev}"


# ------------------------------------------------------------------ Weekly MIS
ws = ws_mis
title(ws, "VP Operations · Weekly MIS", MOCK)
put(ws, "B4", "Week", F(bold=True))
put(ws, "C4", CUR, INPUT_FONT, '"W"0', INPUT_FILL, CENTER)
put(ws, "D4", '="W"&C4&"  ·  "&TEXT(INDEX(d_start,MATCH(C4,d_week,0)),"d mmm")&" – "&TEXT(INDEX(d_start,MATCH(C4,d_week,0))+6,"d mmm yyyy")',
    F(color=MUTED))
put(ws, "B5", "Scope", F(bold=True))
put(ws, "C5", "All India", INPUT_FONT, None, INPUT_FILL, CENTER)
put(ws, "B6", "Compared with", F(bold=True))
put(ws, "C6", "=C4-1", F(), '"W"0', None, CENTER)
put(ws, "G4", "How to use", F(bold=True))
put(ws, "G5", "Pick a week (W32–W42) and a scope in the yellow cells. Every number below recalculates.", F(color=MUTED))
put(ws, "G6", "Status: Green meets target · Amber within 5% of it · Red further off · Info has no target.", F(color=MUTED))
ws.merge_cells("C4:C4")
dv_w = DataValidation(type="list", formula1="=Lists!$A$2:$A$12", allow_blank=False, showDropDown=False)
dv_w.error, dv_w.errorTitle = "Pick a week between 32 and 42", "Week"
dv_s = DataValidation(type="list", formula1="=Lists!$B$2:$B$10", allow_blank=False)
ws.add_data_validation(dv_w)
ws.add_data_validation(dv_s)
dv_w.add("C4")
dv_s.add("C5")
for ref in ("C4", "C5"):
    ws[ref].protection = Protection(locked=False)
name("sel_week", "'Weekly MIS'!$C$4")
name("sel_scope", "'Weekly MIS'!$C$5")

# Calculation block: summed counts for this week, last week and last 4 weeks
CB = 13  # column M
put(ws, "M7", "Calculation block: summed counts (formulas, do not edit)", F(bold=True, color=MUTED))
header_row(ws, 8, CB, ["Count", "This week", "Last week", "Last 4 weeks"])
CALC_FIELDS = ["req", "asg", "cc", "pc", "comp", "ot", "perf", "cpl", "redo", "rc", "rs", "low", "act", "cert",
               "stock", "coh", "coha", "gmv"]
for i, f in enumerate(CALC_FIELDS, start=9):
    lab = [c[0] for c in DCOLS if c[2] == "d_" + f][0]
    put(ws, f"M{i}", lab, F(color=MUTED), border=BOTTOM)
    base = f"d_{f}"
    tw = f'=IF(sel_scope="All India",SUMIFS({base},d_week,sel_week),SUMIFS({base},d_week,sel_week,d_city,sel_scope))'
    lw = f'=IF(sel_scope="All India",SUMIFS({base},d_week,sel_week-1),SUMIFS({base},d_week,sel_week-1,d_city,sel_scope))'
    l4 = (f'=IF(sel_scope="All India",SUMIFS({base},d_week,">="&(sel_week-3),d_week,"<="&sel_week),'
          f'SUMIFS({base},d_week,">="&(sel_week-3),d_week,"<="&sel_week,d_city,sel_scope))')
    for col, fml, pre in (("N", tw, "tw_"), ("O", lw, "lw_"), ("P", l4, "l4_")):
        put(ws, f"{col}{i}", fml, F(color=MUTED), INT, border=BOTTOM)
        name(pre + f, f"'Weekly MIS'!${col}${i}")

header_row(ws, 8, 2, ["Metric", "This wk", "Last wk", "Change", "Last 4 wks", "Target", "Status", "Owner"])
ws["A8"].value = None
r = 9
MIS_ROW = {}
for k in KPIS:
    key, block, metric, unit, dirn, tgt, owner, good, nat, fmt = k
    if block:
        for col in "BCDEFGHI":
            ws[f"{col}{r}"].fill = BLOCK_FILL
        put(ws, f"B{r}", block, F(bold=True, color="52514E"), fill=BLOCK_FILL)
        r += 1
    MIS_ROW[key] = r
    put(ws, f"A{r}", key, F(color="FFFFFF", size=8))
    put(ws, f"B{r}", metric, F(bold=key == "nsm"), border=BOTTOM)
    put(ws, f"C{r}", "=" + kpi_expr(key, lambda f: "tw_" + f), F(bold=True), fmt, border=BOTTOM)
    put(ws, f"D{r}", "=" + kpi_expr(key, lambda f: "lw_" + f), F(), fmt, border=BOTTOM)
    put(ws, f"E{r}", change_formula(unit, f"C{r}", f"D{r}"), F(), change_fmt(unit, fmt), border=BOTTOM)
    put(ws, f"F{r}", "=" + kpi_expr(key, lambda f: "l4_" + f, "4"), F(), fmt, border=BOTTOM)
    put(ws, f"G{r}", f'=IF({lookup("tg_dir", f"$A{r}")}="Info","–",IF(AND(sel_scope<>"All India",{lookup("tg_nat", f"$A{r}")}="Yes"),"–",{lookup("tg_target", f"$A{r}")}))',
        LINK_FONT, fmt, border=BOTTOM, align=Alignment(horizontal="right"))
    put(ws, f"H{r}", status_formula(f"$A{r}", f"C{r}", f"G{r}"), F(bold=True), None, border=BOTTOM, align=CENTER)
    put(ws, f"I{r}", "=" + lookup("tg_owner", f"$A{r}"), LINK_FONT, border=BOTTOM)
    put(ws, f"K{r}", "=" + lookup("tg_good", f"$A{r}"), F(color="FFFFFF", size=8))
    r += 1
MIS_LAST = r - 1
rag_rules(ws, f"H9:H{MIS_LAST}")
ws.conditional_formatting.add(f"E9:E{MIS_LAST}", FormulaRule(
    formula=[f'OR(AND($K9="Up",E9>0),AND($K9="Down",E9<0))'], font=Font(name=FONT, color="006100", bold=True)))
ws.conditional_formatting.add(f"E9:E{MIS_LAST}", FormulaRule(
    formula=[f'OR(AND($K9="Up",E9<0),AND($K9="Down",E9>0))'], font=Font(name=FONT, color="B02A2A", bold=True)))

# Status summary and W42 commentary
r = MIS_LAST + 2
put(ws, f"B{r}", "Status count (excluding the North Star)", F(bold=True))
for i, s in enumerate(["Green", "Amber", "Red", "Info"]):
    put(ws, f"{'CDEF'[i]}{r}", s, F(bold=True), align=CENTER)
    put(ws, f"{'CDEF'[i]}{r + 1}", f'=COUNTIF($H${MIS_ROW["req"]}:$H${MIS_LAST},"{s}")', F(size=12, bold=True), align=CENTER)
rag_rules(ws, f"C{r}:F{r}")
r += 3
put(ws, f"B{r}", "Commentary, Week 42 (written for W42; the numbers above recalculate for any week)", F(bold=True, color=INK))
r += 1
COMMENT = [
    ("Top 3 issues", [
        "1. Complaints rose to 9.8 per 1,000. Mostly waxing, in GGN-2 and GGN-4. Retrain 41 flagged partners and QC the wax batch. CX with Training & QA, due Thu 22 Oct.",
        "2. Partner cancellations rose to 1.6%, in step with kit stock-outs (3.2%). Refill the top 5 items at hubs. Inventory, was due 16 Oct, now 3 days late.",
        "3. Fill rate fell to 91.6%, weakest on weekend evenings in Mumbai and Bengaluru. Weekend shift incentive in 3 hubs. City Ops, due Fri 23 Oct.",
    ]),
    ("Wins", [
        "210 partners certified, above the 200 target. Best week in 12.",
        "Average rating held at 4.72, above 4.70, despite the complaint spike.",
        "Customer cancellations stayed under 3% with 1.9% more requests.",
    ]),
    ("Decisions needed from the VP", [
        "1. Approve the weekend-evening incentive pilot in MUM-2, MUM-4 and BLR-1 for 2 weekends.",
        "2. Approve 5 days of buffer kit stock per hub, so reorders trigger automatically.",
        "3. Sign off the metric dictionary, so all 5 teams report one fill rate.",
    ]),
]
for head, lines in COMMENT:
    put(ws, f"B{r}", head, F(bold=True), fill=NOTE_FILL)
    for col in "CDEFGHI":
        ws[f"{col}{r}"].fill = NOTE_FILL
    r += 1
    for ln in lines:
        put(ws, f"B{r}", ln, F())
        r += 1
    r += 1
widths(ws, {"A": 2, "B": 34, "C": 11, "D": 11, "E": 11, "F": 11, "G": 10, "H": 10, "I": 15, "J": 3, "K": 4, "L": 3,
            "M": 30, "N": 12, "O": 12, "P": 12})
ws.freeze_panes = "C9"
ws.protection.sheet = True
ws.protection.formatCells = False
ws.protection.formatColumns = False
ws.protection.formatRows = False
ws.protection.selectLockedCells = False
ws.protection.selectUnlockedCells = False
ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1
ws.sheet_properties.pageSetUpPr.fitToPage = True

# ------------------------------------------------------------------ North Star
ws = ws_ns
title(ws, "North Star · Perfect bookings", "Perfect booking = completed, started within 15 min of the slot, no complaint, no redo or refund, rated 4★+ or not rated.")
header_row(ws, 4, 1, ["Week", "Label", "Requests", "Assigned", "Completed", "Started on time", "Perfect bookings",
                      "Perfect rate", "Target", "Status", "Fill rate", "Completion", "On-time", "Quality pass", "Check: product = rate"])
ws["A4"].alignment = CENTER
for i, w in enumerate(WEEKS, start=5):
    S = lambda f, i=i: f"SUMIFS(d_{f},d_week,$A{i})"
    put(ws, f"A{i}", w, F(), "0", align=CENTER)
    put(ws, f"B{i}", f'="W"&A{i}', F(), align=CENTER)
    for col, f in zip("CDEFG", ["req", "asg", "comp", "ot", "perf"]):
        put(ws, f"{col}{i}", "=" + S(f), F(), INT)
    put(ws, f"H{i}", f"=G{i}/C{i}", F(bold=True), PCT1)
    put(ws, f"I{i}", "=t_nsm", LINK_FONT, PCT0)
    put(ws, f"J{i}", f'=IF(H{i}>=I{i},"Green",IF(H{i}>=I{i}*(1-amber_band),"Amber","Red"))', F(bold=True), align=CENTER)
    put(ws, f"K{i}", f"=D{i}/C{i}", F(), PCT1)
    put(ws, f"L{i}", f"=E{i}/D{i}", F(), PCT1)
    put(ws, f"M{i}", f"=F{i}/E{i}", F(), PCT1)
    put(ws, f"N{i}", f"=G{i}/F{i}", F(), PCT1)
    put(ws, f"O{i}", f"=ROUND(K{i}*L{i}*M{i}*N{i}-H{i},9)=0", F(color=MUTED), align=CENTER)
NS_LAST = 4 + len(WEEKS)
rag_rules(ws, f"J5:J{NS_LAST}")
put(ws, f"A{NS_LAST + 1}", "Perfect rate = Fill × Completion × On-time × Quality pass. Every manager owns one term, so a drop always has an owner.",
    F(italic=True, color=MUTED))

# Leak split for the selected week
r0 = NS_LAST + 3
put(ws, f"A{r0}", "Where the week leaked", F(size=12, bold=True))
put(ws, f"D{r0}", "Week", F(bold=True))
put(ws, f"E{r0}", "=sel_week", LINK_FONT, '"W"0')
put(ws, f"F{r0}", "(set on the Weekly MIS tab)", F(color=MUTED))
header_row(ws, r0 + 1, 1, ["Term", "", "This week", "Last week", "Change", "Perfect bookings this term moved"])
terms = [("Booking requests", "C", INT), ("Fill rate", "K", PCT1), ("Completion", "L", PCT1), ("On-time", "M", PCT1),
         ("Quality pass", "N", PCT1)]
for j, (lab, col, fmt) in enumerate(terms):
    rr = r0 + 2 + j
    put(ws, f"A{rr}", lab, F(bold=True), border=BOTTOM)
    put(ws, f"C{rr}", f"=INDEX({col}$5:{col}${NS_LAST},MATCH(sel_week,$A$5:$A${NS_LAST},0))", F(), fmt, border=BOTTOM)
    put(ws, f"D{rr}", f"=INDEX({col}$5:{col}${NS_LAST},MATCH(sel_week-1,$A$5:$A${NS_LAST},0))", F(), fmt, border=BOTTOM)
    put(ws, f"E{rr}", f"=C{rr}/D{rr}-1" if fmt == INT else f"=(C{rr}-D{rr})*100", F(), CHG if fmt == INT else PTS, border=BOTTOM)
pr = r0 + 7
put(ws, f"A{pr}", "Perfect bookings", F(bold=True), border=BOTTOM)
put(ws, f"C{pr}", f"=INDEX(G$5:G${NS_LAST},MATCH(sel_week,$A$5:$A${NS_LAST},0))", F(bold=True), INT, border=BOTTOM)
put(ws, f"D{pr}", f"=INDEX(G$5:G${NS_LAST},MATCH(sel_week-1,$A$5:$A${NS_LAST},0))", F(), INT, border=BOTTOM)
put(ws, f"E{pr}", f"=C{pr}-D{pr}", F(bold=True), '+#,##0;-#,##0;0', border=BOTTOM)
for j in range(5):
    rr = r0 + 2 + j
    put(ws, f"F{rr}", f"=$E${pr}*LN(C{rr}/D{rr})/LN($C${pr}/$D${pr})", F(bold=True), '+#,##0;-#,##0;0', border=BOTTOM)
put(ws, f"F{pr}", f"=SUM(F{r0 + 2}:F{r0 + 6})", F(bold=True), '+#,##0;-#,##0;0', border=BOTTOM)
ws.conditional_formatting.add(f"F{r0 + 2}:F{pr}", FormulaRule(formula=[f"F{r0 + 2}<0"], font=Font(name=FONT, color="B02A2A", bold=True)))
ws.conditional_formatting.add(f"F{r0 + 2}:F{pr}", FormulaRule(formula=[f"F{r0 + 2}>0"], font=Font(name=FONT, color="006100", bold=True)))
put(ws, f"A{pr + 1}", "Log split: each term's share of the change in ln(perfect bookings). The five terms add up to the total change.",
    F(italic=True, color=MUTED))

ch = LineChart()
ch.title = "Perfect booking rate vs target"
ch.height, ch.width = 7.5, 17
ch.y_axis.number_format = "0%"
ch.y_axis.scaling.min, ch.y_axis.scaling.max = 0.72, 0.82
ch.y_axis.majorGridlines = None
ch.add_data(Reference(ws, min_col=8, max_col=9, min_row=4, max_row=NS_LAST), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=2, min_row=5, max_row=NS_LAST))
ch.series[0].graphicalProperties.line.solidFill = "2A78D6"
ch.series[0].graphicalProperties.line.width = 28000
ch.series[1].graphicalProperties.line.solidFill = "9CA3AF"
ch.series[1].graphicalProperties.line.dashStyle = "dash"
ch.legend.position = "b"
ws.add_chart(ch, f"H{r0}")
widths(ws, {"A": 18, "B": 7, "C": 11, "D": 11, "E": 11, "F": 14, "G": 13, "H": 11, "I": 9, "J": 9, "K": 9, "L": 11,
            "M": 9, "N": 11, "O": 12})
ws.freeze_panes = "C5"

# ------------------------------------------------------------------ Monthly
ws = ws_mon
title(ws, "Monthly review", "Weeks roll up to the month their Thursday falls in (ISO rule). Counts are weekly averages so months compare fairly.")
MONTHS = ["Aug", "Sep", "Oct"]
header_row(ws, 4, 2, ["Metric", "Aug", "Sep", "Oct (to date)", "Sep → Oct", "Target", "Oct status", "Owner"])
put(ws, "B5", "Month key", F(color=MUTED))
put(ws, "B6", "Weeks in month", F(color=MUTED))
for j, m in enumerate(MONTHS):
    col = "CDE"[j]
    put(ws, f"{col}5", m, F(color=MUTED), align=CENTER)
    put(ws, f"{col}6", f'=COUNTIFS(d_month,{col}$5,d_city,"Delhi")', F(color=MUTED), "0", align=CENTER)
r = 7
for k in KPIS:
    key, block, metric, unit, dirn, tgt, owner, good, nat, fmt = k
    if block:
        for col in "BCDEFGHI":
            ws[f"{col}{r}"].fill = BLOCK_FILL
        put(ws, f"B{r}", block, F(bold=True, color="52514E"), fill=BLOCK_FILL)
        r += 1
    put(ws, f"A{r}", key, F(color="FFFFFF", size=8))
    put(ws, f"B{r}", metric, F(bold=key == "nsm"), border=BOTTOM)
    for j in range(3):
        col = "CDE"[j]
        S = lambda f, col=col: f"SUMIFS(d_{f},d_month,{col}$5)"
        put(ws, f"{col}{r}", "=" + kpi_expr(key, S, f"{col}$6"), F(bold=j == 2), fmt, border=BOTTOM)
    put(ws, f"F{r}", change_formula(unit, f"E{r}", f"D{r}"), F(), change_fmt(unit, fmt), border=BOTTOM)
    put(ws, f"G{r}", f'=IF({lookup("tg_dir", f"$A{r}")}="Info","–",{lookup("tg_target", f"$A{r}")})', LINK_FONT, fmt,
        border=BOTTOM, align=Alignment(horizontal="right"))
    put(ws, f"H{r}", status_formula(f"$A{r}", f"E{r}", f"G{r}"), F(bold=True), border=BOTTOM, align=CENTER)
    put(ws, f"I{r}", "=" + lookup("tg_owner", f"$A{r}"), LINK_FONT, border=BOTTOM)
    r += 1
rag_rules(ws, f"H8:H{r - 1}")
put(ws, f"B{r + 1}", "Oct is 3 weeks to date (W40–W42). Jul has only W31 in this extract, so it is left out.", F(italic=True, color=MUTED))
widths(ws, {"A": 2, "B": 34, "C": 11, "D": 11, "E": 13, "F": 11, "G": 10, "H": 11, "I": 15})
ws.freeze_panes = "C5"

# ------------------------------------------------------------------ City View
ws = ws_city
title(ws, "City view", "Same formulas as the Weekly MIS, split by city. Week follows the Weekly MIS tab.")
put(ws, "B4", "Week", F(bold=True))
put(ws, "C4", "=sel_week", LINK_FONT, '"W"0', align=CENTER)
CV_COLS = [("Requests", None, INT), ("Requests last wk", None, INT), ("vs last wk", None, CHG), ("Fill rate", "fill", PCT1),
           ("On-time arrival", "ot", PCT1), ("Cust. cancel", "cc", PCT1), ("Partner cancel", "pc", PCT1),
           ("Jobs / partner / day", "jppd", D2), ("Complaints / 1,000", "cpk", D1), ("Kit stock-out", "kit", PCT1),
           ("Perfect rate", "nsm", PCT1), ("Unfilled requests", None, INT), ("GMV (₹ lakh)", None, LAKH)]
header_row(ws, 6, 2, ["City"] + [c[0] for c in CV_COLS])
city_rows = CITIES + ["All India"]
for i, c in enumerate(city_rows, start=7):
    allin = c == "All India"
    put(ws, f"B{i}", c, F(bold=allin), border=BOTTOM)

    def S(f, wk="$C$4", allin=allin, i=i):
        return f"SUMIFS(d_{f},d_week,{wk})" if allin else f"SUMIFS(d_{f},d_week,{wk},d_city,$B{i})"
    put(ws, f"C{i}", "=" + S("req"), F(bold=allin), INT, border=BOTTOM)
    put(ws, f"D{i}", "=" + S("req", "$C$4-1"), F(bold=allin), INT, border=BOTTOM)
    put(ws, f"E{i}", f"=C{i}/D{i}-1", F(bold=allin), CHG, border=BOTTOM)
    for j, (lab, key, fmt) in enumerate(CV_COLS[3:11], start=6):
        col = ws.cell(row=i, column=j).column_letter
        put(ws, f"{col}{i}", "=" + kpi_expr(key, S), F(bold=allin), fmt, border=BOTTOM)
    put(ws, f"N{i}", f"={S('req')}-{S('asg')}", F(bold=allin), INT, border=BOTTOM)
    put(ws, f"O{i}", f"={S('gmv')}/100000", F(bold=allin), LAKH, border=BOTTOM)
CV_LAST = 6 + len(city_rows)
for col, key in zip("FGHIJKLM", ["fill", "ot", "cc", "pc", "jppd", "cpk", "kit", "nsm"]):
    rng = f"{col}7:{col}{CV_LAST}"
    t = f"t_{key}"
    up = [k for k in KPIS if k[0] == key][0][4] == "Higher"
    g = f"{col}7>={t}" if up else f"{col}7<={t}"
    a = f"{col}7>={t}*(1-amber_band)" if up else f"{col}7<={t}*(1+amber_band)"
    ws.conditional_formatting.add(rng, FormulaRule(formula=[g], fill=GREEN_FILL, stopIfTrue=True))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[a], fill=AMBER_FILL, stopIfTrue=True))
    ws.conditional_formatting.add(rng, FormulaRule(formula=["TRUE"], fill=RED_FILL))
put(ws, f"B{CV_LAST + 1}", "Cell colour = status against the Targets tab. All India sums the city counts first, then divides.",
    F(italic=True, color=MUTED))

bc = BarChart()
bc.type = "bar"
bc.title = "Fill rate by city"
bc.height, bc.width = 7.5, 13
bc.add_data(Reference(ws, min_col=6, min_row=6, max_row=6 + len(CITIES)), titles_from_data=True)
bc.set_categories(Reference(ws, min_col=2, min_row=7, max_row=6 + len(CITIES)))
bc.x_axis.scaling.orientation = "maxMin"
bc.y_axis.number_format = "0%"
bc.y_axis.scaling.min, bc.y_axis.scaling.max = 0.85, 0.97
bc.y_axis.majorGridlines = None
bc.legend = None
bc.series[0].graphicalProperties.solidFill = "2A78D6"
ws.add_chart(bc, f"Q6")

# Day x slot grid (W42) and the averaging trap
g0 = CV_LAST + 4
G = D["grid"]
put(ws, f"B{g0}", "Week 42 by day and slot: requests, partner assigned and fill rate", F(size=12, bold=True))
header_row(ws, g0 + 1, 2, ["Requests"] + G["slots"])
header_row(ws, g0 + 1, 9, ["Assigned"] + G["slots"])
header_row(ws, g0 + 10, 2, ["Fill rate"] + G["slots"])
for d, day in enumerate(G["days"]):
    ra, rf = g0 + 2 + d, g0 + 11 + d
    put(ws, f"B{ra}", day, F(bold=True))
    put(ws, f"I{ra}", day, F(bold=True))
    put(ws, f"B{rf}", day, F(bold=True))
    for s in range(5):
        cell = G["cells"][d][s]
        c1 = ws.cell(row=ra, column=3 + s, value=cell["req"])
        c2 = ws.cell(row=ra, column=10 + s, value=cell["asg"])
        c1.font = c2.font = F()
        c1.number_format = c2.number_format = INT
        rq, asn = c1.coordinate, c2.coordinate
        c3 = ws.cell(row=rf, column=3 + s, value=f"={asn}/{rq}")
        c3.font, c3.number_format, c3.alignment = F(bold=True), PCT1, CENTER
grid_rng = f"C{g0 + 11}:G{g0 + 17}"
ws.conditional_formatting.add(grid_rng, ColorScaleRule(start_type="num", start_value=0.80, start_color="E66A63",
                                                       mid_type="num", mid_value=0.95, mid_color="F0EFEC",
                                                       end_type="num", end_value=0.98, end_color="6DA7EC"))
tr = g0 + 19
put(ws, f"B{tr}", "The averaging trap", F(size=12, bold=True))
put(ws, f"B{tr + 1}", "Average of the 35 slot fill rates", F())
put(ws, f"F{tr + 1}", f"=AVERAGE({grid_rng})", F(bold=True, color="B02A2A"), PCT1)
put(ws, f"G{tr + 1}", "Wrong: a quiet Monday slot counts as much as a packed Sunday evening", F(color=MUTED))
put(ws, f"B{tr + 2}", "Total assigned ÷ total requests", F())
put(ws, f"F{tr + 2}", f"=SUM(J{g0 + 2}:N{g0 + 8})/SUM(C{g0 + 2}:G{g0 + 8})", F(bold=True, color="006100"), PCT1)
put(ws, f"G{tr + 2}", "Right: add the counts first, then divide", F(color=MUTED))
put(ws, f"B{tr + 3}", "Weekend evenings (Sat–Sun, 17–22): share of requests", F())
put(ws, f"F{tr + 3}", f"=SUM(F{g0 + 7}:G{g0 + 8})/SUM(C{g0 + 2}:G{g0 + 8})", F(bold=True), PCT1)
put(ws, f"B{tr + 4}", "Weekend evenings: share of unfilled requests", F())
put(ws, f"F{tr + 4}", f"=(SUM(F{g0 + 7}:G{g0 + 8})-SUM(M{g0 + 7}:N{g0 + 8}))/(SUM(C{g0 + 2}:G{g0 + 8})-SUM(J{g0 + 2}:N{g0 + 8}))",
    F(bold=True), PCT1)
name("trap_simple", f"'City View'!$F${tr + 1}")
name("trap_right", f"'City View'!$F${tr + 2}")
widths(ws, {"A": 2, "B": 20, "C": 11, "D": 11, "E": 10, "F": 10, "G": 10, "H": 10, "I": 11, "J": 11, "K": 11, "L": 11,
            "M": 10, "N": 11, "O": 11})
ws.freeze_panes = "C7"

# ------------------------------------------------------------------ Supply
ws = ws_sup
title(ws, "Partner supply & productivity", "Onboarding funnel by week, cohort retention and utilisation. Owners: Supply, Training & QA.")
header_row(ws, 4, 2, ["Week", "Leads sourced", "Started training", "Certified", "Kit issued", "First job in 7 days",
                      "In training now", "Sourced → started", "Started → certified", "Certified → kit", "Kit → first job",
                      "Active partners", "Target"])
for i, s in enumerate(D["supply"], start=5):
    put(ws, f"B{i}", s["week"], F(), '"W"0', align=CENTER)
    for col, k in zip("CDEFGH", ["sourced", "started", "cert", "kit", "first_job", "in_training"]):
        put(ws, f"{col}{i}", s[k], F(color="0000FF"), INT)
    put(ws, f"E{i}", f"=SUMIFS(d_cert,d_week,B{i})", F(), INT)
    put(ws, f"I{i}", f"=D{i}/C{i}", F(), PCT0)
    put(ws, f"J{i}", f"=E{i}/D{i}", F(), PCT0)
    put(ws, f"K{i}", f"=F{i}/E{i}", F(), PCT0)
    put(ws, f"L{i}", f"=G{i}/F{i}", F(), PCT0)
    put(ws, f"M{i}", f"=SUMIFS(d_act,d_week,B{i})", F(bold=True), INT)
    put(ws, f"N{i}", "=t_act", LINK_FONT, INT)
SUP_LAST = 4 + len(D["supply"])
put(ws, f"B{SUP_LAST + 1}", "Blue numbers are pipeline counts from the onboarding tracker (mock). Certified and active partners come from the Data tab. "
    "Conversions compare this week's counts, so they are an approximation of a 15–45 day pipeline.", F(italic=True, color=MUTED))
put(ws, f"B{SUP_LAST + 2}", "Certified partners still waiting for a kit (this week)", F(bold=True))
put(ws, f"H{SUP_LAST + 2}", f"=E{SUP_LAST}-F{SUP_LAST}", F(bold=True), INT)

c0 = SUP_LAST + 4
put(ws, f"B{c0}", "Retention by joining cohort: % still active, by week since joining", F(size=12, bold=True))
header_row(ws, c0 + 1, 2, ["Cohort", "Joined", "Week 1", "Week 2", "Week 4", "Week 8", "Week 13", "Lost in weeks 2–4"])
for i, ch_ in enumerate(D["cohorts"], start=c0 + 2):
    put(ws, f"B{i}", ch_["cohort"], F(bold=True))
    put(ws, f"C{i}", ch_["size"], F(color="0000FF"), INT)
    for j, v in enumerate(ch_["ret"]):
        cell = ws.cell(row=i, column=4 + j, value=(v / 100 if v is not None else "–"))
        cell.font, cell.number_format, cell.alignment = F(color="0000FF"), PCT0, CENTER
    put(ws, f"I{i}", f"=(E{i}-F{i})*100", F(bold=True), '0.0" pts"')
coh_last = c0 + 1 + len(D["cohorts"])
ws.conditional_formatting.add(f"D{c0 + 2}:H{coh_last}", ColorScaleRule(start_type="num", start_value=0.6, start_color="CDE2FB",
                                                                       end_type="num", end_value=0.95, end_color="1C5CAB"))
u0 = coh_last + 3
put(ws, f"B{u0}", "Partners by average jobs per working day, Week 42", F(size=12, bold=True))
header_row(ws, u0 + 1, 2, ["Band", "Partners", "Share"])
for i, (band, n) in enumerate(D["util_bands"], start=u0 + 2):
    put(ws, f"B{i}", band, F(), align=CENTER)
    put(ws, f"C{i}", n, F(color="0000FF"), INT)
    put(ws, f"D{i}", f"=C{i}/SUM($C${u0 + 2}:$C${u0 + 7})", F(), PCT0)
ub = u0 + 8
put(ws, f"B{ub}", "Total", F(bold=True))
put(ws, f"C{ub}", f"=SUM(C{u0 + 2}:C{u0 + 7})", F(bold=True), INT)
put(ws, f"E{ub}", f'=IF(C{ub}=SUMIFS(d_act,d_week,{CUR}),"Ties to active partners","Does not tie: check")', F(color=MUTED))
put(ws, f"B{ub + 1}", "Under 1 job a day", F(bold=True))
put(ws, f"C{ub + 1}", f"=C{u0 + 2}+C{u0 + 3}", F(bold=True), INT)
put(ws, f"D{ub + 1}", f"=C{ub + 1}/C{ub}", F(bold=True), PCT0)
put(ws, f"B{ub + 3}", "Utilisation lever: extra jobs a week if jobs per partner per day hit target", F(bold=True))
put(ws, f"H{ub + 3}", f"=SUMIFS(d_act,d_week,{CUR})*6*(t_jppd-SUMIFS(d_comp,d_week,{CUR})/(SUMIFS(d_act,d_week,{CUR})*6))",
    F(bold=True, color="006100"), INT)

lc = LineChart()
lc.title = "Active partners vs target"
lc.height, lc.width = 7, 15
lc.add_data(Reference(ws, min_col=13, max_col=14, min_row=4, max_row=SUP_LAST), titles_from_data=True)
lc.set_categories(Reference(ws, min_col=2, min_row=5, max_row=SUP_LAST))
lc.y_axis.scaling.min, lc.y_axis.scaling.max = 6800, 7800
lc.y_axis.majorGridlines = None
lc.series[0].graphicalProperties.line.solidFill = "2A78D6"
lc.series[0].graphicalProperties.line.width = 28000
lc.series[1].graphicalProperties.line.solidFill = "9CA3AF"
lc.series[1].graphicalProperties.line.dashStyle = "dash"
lc.legend.position = "b"
ws.add_chart(lc, f"K{c0}")
widths(ws, {"A": 2, "B": 14, "C": 12, "D": 12, "E": 11, "F": 11, "G": 13, "H": 12, "I": 13, "J": 13, "K": 12, "L": 12,
            "M": 12, "N": 10})
ws.freeze_panes = "C5"

# ------------------------------------------------------------------ Quality & Kits
ws = ws_q
title(ws, "Quality, CX & kits", "Complaints by service and hub, kit items reported missing. Owners: Training & QA, CX, Inventory.")
header_row(ws, 4, 2, ["Service", "Jobs W41", "Complaints W41", "Jobs W42", "Complaints W42", "Per 1,000 W41",
                      "Per 1,000 W42", "Change", "Share of the rise"])
q0 = 5
for i, c in enumerate(D["cats"], start=q0):
    put(ws, f"B{i}", c["cat"], F(bold=c["cat"] == "Waxing"), border=BOTTOM)
    for col, k in zip("CDEF", ["jobs41", "cpl41", "jobs42", "cpl42"]):
        put(ws, f"{col}{i}", c[k], F(color="0000FF"), INT, border=BOTTOM)
    put(ws, f"G{i}", f"=D{i}/C{i}*1000", F(), D1, border=BOTTOM)
    put(ws, f"H{i}", f"=F{i}/E{i}*1000", F(bold=True), D1, border=BOTTOM)
    put(ws, f"I{i}", f"=H{i}-G{i}", F(), CD1, border=BOTTOM)
qn = q0 + len(D["cats"])
for i in range(q0, qn):
    put(ws, f"J{i}", f"=(F{i}-D{i})/(F${qn}-D${qn})", F(), PCT0, border=BOTTOM)
put(ws, f"B{qn}", "All services", F(bold=True))
for col in "CDEF":
    put(ws, f"{col}{qn}", f"=SUM({col}{q0}:{col}{qn - 1})", F(bold=True), INT)
put(ws, f"G{qn}", f"=D{qn}/C{qn}*1000", F(bold=True), D1)
put(ws, f"H{qn}", f"=F{qn}/E{qn}*1000", F(bold=True), D1)
put(ws, f"I{qn}", f"=H{qn}-G{qn}", F(bold=True), CD1)
put(ws, f"K{qn}", f'=IF(AND(E{qn}=SUMIFS(d_comp,d_week,{CUR}),F{qn}=SUMIFS(d_cpl,d_week,{CUR})),"Ties to Data tab","Does not tie: check")',
    F(color=MUTED))
ws.conditional_formatting.add(f"I{q0}:I{qn - 1}", ColorScaleRule(start_type="num", start_value=0, start_color="FFFFFF",
                                                                 end_type="max", end_color="E66A63"))

h0 = qn + 3
put(ws, f"B{h0 - 1}", "Hubs, Week 42 (12 of about 140)", F(size=12, bold=True))
header_row(ws, h0, 2, ["Hub", "City", "Partners", "Jobs", "Complaints", "Kit stock-out partners", "Partner cancels",
                       "Assigned", "Complaints / 1,000", "Kit stock-out", "Partner cancel"])
for i, h in enumerate(D["hubs"], start=h0 + 1):
    put(ws, f"B{i}", h["hub"], F(bold=True), border=BOTTOM)
    put(ws, f"C{i}", h["city"], F(), border=BOTTOM)
    for col, k in zip("DEFGHI", ["partners", "jobs", "cpl", "stock", "pc", "asg"]):
        put(ws, f"{col}{i}", h[k], F(color="0000FF"), INT, border=BOTTOM)
    put(ws, f"J{i}", f"=F{i}/E{i}*1000", F(bold=True), D1, border=BOTTOM)
    put(ws, f"K{i}", f"=G{i}/D{i}", F(), PCT1, border=BOTTOM)
    put(ws, f"L{i}", f"=H{i}/I{i}", F(), PCT1, border=BOTTOM)
hl = h0 + len(D["hubs"])
for col, key in (("J", "cpk"), ("K", "kit"), ("L", "pc")):
    ws.conditional_formatting.add(f"{col}{h0 + 1}:{col}{hl}", FormulaRule(formula=[f"{col}{h0 + 1}<=t_{key}"], fill=GREEN_FILL, stopIfTrue=True))
    ws.conditional_formatting.add(f"{col}{h0 + 1}:{col}{hl}", FormulaRule(formula=[f"{col}{h0 + 1}<=t_{key}*(1+amber_band)"], fill=AMBER_FILL, stopIfTrue=True))
    ws.conditional_formatting.add(f"{col}{h0 + 1}:{col}{hl}", FormulaRule(formula=["TRUE"], fill=RED_FILL))
put(ws, f"B{hl + 1}", "Correlation, hub kit stock-out vs partner cancel", F(bold=True))
put(ws, f"G{hl + 1}", f"=CORREL(K{h0 + 1}:K{hl},L{h0 + 1}:L{hl})", F(bold=True), "0.00")
put(ws, f"H{hl + 1}", "Hubs short on kits cancel more. Fix kits upstream.", F(color=MUTED))

s0 = hl + 4
put(ws, f"B{s0 - 1}", "Kit items reported missing (partners reporting each item)", F(size=12, bold=True))
header_row(ws, s0, 2, ["Item", "W41", "W42", "Change", "Share of W42 reports", "Top 5?"])
for i, s in enumerate(D["skus"], start=s0 + 1):
    put(ws, f"B{i}", s["sku"], F(), border=BOTTOM)
    put(ws, f"C{i}", s["w41"], F(color="0000FF"), INT, border=BOTTOM)
    put(ws, f"D{i}", s["w42"], F(color="0000FF"), INT, border=BOTTOM)
    put(ws, f"E{i}", f"=D{i}/C{i}-1", F(), CHG, border=BOTTOM)
    put(ws, f"F{i}", f"=D{i}/SUM($D${s0 + 1}:$D${s0 + len(D['skus'])})", F(), PCT0, border=BOTTOM)
    put(ws, f"G{i}", f'=IF(RANK(D{i},$D${s0 + 1}:$D${s0 + len(D["skus"])})<=5,"Yes","")', F(), border=BOTTOM, align=CENTER)
sl = s0 + len(D["skus"])
put(ws, f"B{sl + 1}", "Top 5 items' share of reports", F(bold=True))
put(ws, f"F{sl + 1}", f'=SUMIFS(F{s0 + 1}:F{sl},G{s0 + 1}:G{sl},"Yes")', F(bold=True), PCT0)

w0 = sl + 4
put(ws, f"B{w0 - 1}", "Complaints by reason, Week 42", F(size=12, bold=True))
header_row(ws, w0, 2, ["Reason", "Complaints", "Share"])
for i, (k, v) in enumerate(D["reasons"], start=w0 + 1):
    put(ws, f"B{i}", k, F(), border=BOTTOM)
    put(ws, f"C{i}", v, F(color="0000FF"), INT, border=BOTTOM)
    put(ws, f"D{i}", f"=C{i}/SUM($C${w0 + 1}:$C${w0 + len(D['reasons'])})", F(), PCT0, border=BOTTOM)

cb = BarChart()
cb.type = "bar"
cb.title = "Complaints per 1,000 jobs, by service"
cb.height, cb.width = 8, 14
cb.add_data(Reference(ws, min_col=7, max_col=8, min_row=4, max_row=qn - 1), titles_from_data=True)
cb.set_categories(Reference(ws, min_col=2, min_row=q0, max_row=qn - 1))
cb.x_axis.scaling.orientation = "maxMin"
cb.y_axis.majorGridlines = None
cb.series[0].graphicalProperties.solidFill = "9EC5F4"
cb.series[1].graphicalProperties.solidFill = "2A78D6"
cb.legend.position = "b"
ws.add_chart(cb, "M4")
widths(ws, {"A": 2, "B": 26, "C": 18, "D": 11, "E": 11, "F": 13, "G": 13, "H": 13, "I": 11, "J": 14, "K": 13, "L": 13})
ws.freeze_panes = "C5"

# ------------------------------------------------------------------ Action Tracker
ws = ws_act
title(ws, "Action tracker · five managers", "One owner and one date per action. Days late and flags are formulas. Yellow cells are inputs.")
put(ws, "B3", "Report date", F(bold=True))
put(ws, "C3", dt.datetime(2026, 10, 19), INPUT_FONT, "d mmm yyyy", INPUT_FILL, CENTER)
name("report_date", "'Action Tracker'!$C$3")
A_HEAD = ["ID", "Action", "Owner", "Linked KPI", "Raised", "Due", "Status", "Closed on", "Days late", "Flag",
          "Last update", "Next step"]
header_row(ws, 5, 2, A_HEAD)
a0 = 6
for i, a in enumerate(D["actions"], start=a0):
    vals = [a["id"], a["action"], a["owner"], a["kpi"], dt.datetime.fromisoformat(a["raised"]),
            dt.datetime.fromisoformat(a["due"]), a["status"],
            dt.datetime.fromisoformat(a["closed"]) if a["closed"] else None, None, None, a["update"], a["next"]]
    for j, v in enumerate(vals, start=2):
        c = ws.cell(row=i, column=j, value=v)
        c.font = F(color="0000FF") if j in (4, 7, 8, 9, 12, 13) else F()
        c.border = BOTTOM
        if j in (6, 7, 9):
            c.number_format = "d mmm"
    put(ws, f"J{i}", f'=IF(H{i}="Done",MAX(0,I{i}-G{i}),MAX(0,report_date-G{i}))', F(bold=True), "0", border=BOTTOM, align=CENTER)
    put(ws, f"K{i}", f'=IF(H{i}="Done",IF(I{i}<=G{i},"Done on time","Done late"),IF(report_date>G{i},"Overdue",'
        f'IF(ISNUMBER(SEARCH("VP",L{i})),"Needs VP decision",IF(G{i}-report_date<=2,"Due soon","On track"))))',
        F(bold=True), border=BOTTOM, align=CENTER)
al = a0 + len(D["actions"]) - 1
for txt, fill, color in (("Overdue", RED_FILL, "9C0006"), ("Due soon", AMBER_FILL, "7A5000"), ("Needs VP decision", AMBER_FILL, "7A5000"),
                         ("On track", GREEN_FILL, "006100"), ("Done on time", GRAY_FILL, "52514E"), ("Done late", GRAY_FILL, "9C0006")):
    ws.conditional_formatting.add(f"K{a0}:K{al}", FormulaRule(formula=[f'K{a0}="{txt}"'], fill=fill, font=Font(name=FONT, bold=True, color=color)))
dv_o = DataValidation(type="list", formula1="=Lists!$C$2:$C$7")
dv_st = DataValidation(type="list", formula1="=Lists!$D$2:$D$5")
ws.add_data_validation(dv_o)
ws.add_data_validation(dv_st)
dv_o.add(f"D{a0}:D{al + 20}")
dv_st.add(f"H{a0}:H{al + 20}")
for i in range(a0, al + 1):
    ws.row_dimensions[i].height = 28
    for col in "CLM":
        ws[f"{col}{i}"].alignment = Alignment(wrap_text=True, vertical="center")
m0 = al + 3
put(ws, f"B{m0}", "Manager summary", F(size=12, bold=True))
header_row(ws, m0 + 1, 2, ["", "Owner", "Open", "Overdue", "Needs VP", "Closed this week", "Closed on time, last 4 wks",
                           "Closed, last 4 wks", "On-time closure"])
CLOSURE = D["closure"]
for i, o in enumerate(OWNERS, start=m0 + 2):
    put(ws, f"C{i}", o, F(bold=True), border=BOTTOM)
    put(ws, f"D{i}", f'=COUNTIFS($D${a0}:$D${al},C{i},$H${a0}:$H${al},"<>Done")', F(), "0", border=BOTTOM, align=CENTER)
    put(ws, f"E{i}", f'=COUNTIFS($D${a0}:$D${al},C{i},$K${a0}:$K${al},"Overdue")', F(bold=True), "0", border=BOTTOM, align=CENTER)
    put(ws, f"F{i}", f'=COUNTIFS($D${a0}:$D${al},C{i},$K${a0}:$K${al},"Needs VP decision")', F(), "0", border=BOTTOM, align=CENTER)
    put(ws, f"G{i}", f'=COUNTIFS($D${a0}:$D${al},C{i},$I${a0}:$I${al},">="&(report_date-7))', F(), "0", border=BOTTOM, align=CENTER)
    ok, tot = CLOSURE[o]
    put(ws, f"H{i}", ok, F(color="0000FF"), "0", border=BOTTOM, align=CENTER)
    put(ws, f"I{i}", tot, F(color="0000FF"), "0", border=BOTTOM, align=CENTER)
    put(ws, f"J{i}", f"=H{i}/I{i}", F(bold=True), PCT0, border=BOTTOM, align=CENTER)
ml = m0 + 1 + len(OWNERS)
ws.conditional_formatting.add(f"E{m0 + 2}:E{ml}", FormulaRule(formula=[f"E{m0 + 2}>0"], fill=RED_FILL, font=Font(name=FONT, bold=True, color="9C0006")))
put(ws, f"C{ml + 1}", "Total", F(bold=True))
for col in "DEFG":
    put(ws, f"{col}{ml + 1}", f"=SUM({col}{m0 + 2}:{col}{ml})", F(bold=True), "0", align=CENTER)
put(ws, f"B{ml + 3}", "Escalation ladder: Day 1 private nudge → Day 2–3 offer help, clear the blocker → Day 5 raise in the weekly review with data → VP decision. "
    "The manager hears it before the VP does.", F(italic=True, color=MUTED))
widths(ws, {"A": 2, "B": 8, "C": 46, "D": 16, "E": 22, "F": 10, "G": 10, "H": 12, "I": 11, "J": 9, "K": 18, "L": 40, "M": 34})
ws.freeze_panes = "D6"

# ------------------------------------------------------------------ Raw Bookings (sample)
ws = ws_raw
rnd = random.Random(7)
RAW_HEAD = ["Booking ID", "Service date", "City", "Hub", "Partner ID", "Service", "Slot", "Status", "On time",
            "Rating", "Complaint", "Note"]
header_row(ws, 1, 1, RAW_HEAD)
HUBS_BY_CITY = {"Delhi": ["DEL-1", "DEL-2", "DEL-3"], "Gurugram": ["GGN-1", "GGN-2", "GGN-4"],
                "Noida & Ghaziabad": ["NOI-1", "NOI-3", "GZB-1"], "Mumbai": ["MUM-2", "MUM-4", "MUM-5"],
                "Bengaluru": ["BLR-1", "BLR-3"], "Hyderabad": ["HYD-2", "HYD-1"], "Pune": ["PUN-1"],
                "Rest of India": ["JAI-1", "LKO-1", "CHD-1", "AHM-2"]}
CATS = [c["cat"] for c in D["cats"]]
raw = []
for n in range(300):
    city = rnd.choices(CITIES, weights=[17, 12, 11, 14, 12, 8, 6, 20])[0]
    day = dt.datetime(2026, 10, 12) + dt.timedelta(days=rnd.choices(range(7), weights=[12, 11.6, 11.8, 12.1, 13.5, 19.4, 19.6])[0])
    slot = rnd.choices(D["grid"]["slots"], weights=[20, 24, 21, 23, 12])[0]
    status = rnd.choices(["Completed", "Unassigned", "Cancelled – customer", "Cancelled – partner"],
                         weights=[87.5, 8.4, 2.7, 1.5])[0]
    done = status == "Completed"
    rated = done and rnd.random() < 0.62
    rating = rnd.choices([5, 4, 3, 2, 1], weights=[78, 18, 2.4, 1, 0.6])[0] if rated else None
    raw.append([f"YM{2610120000 + rnd.randint(1000, 99999)}", day, city, rnd.choice(HUBS_BY_CITY[city]),
                f"P-{rnd.randint(10000, 29999)}" if status != "Unassigned" else None,
                rnd.choices(CATS, weights=[24, 20, 9, 13, 12, 11, 6, 5])[0], slot, status,
                ("Y" if rnd.random() < 0.884 else "N") if done else None, rating,
                ("Y" if rnd.random() < 0.012 else "N") if done else None, None])
for src, dst in ((12, 40), (88, 141), (203, 262)):  # three reschedules logged twice under the same ID
    raw[dst] = list(raw[src])
    raw[dst][1] = raw[src][1] + dt.timedelta(days=1)
    raw[dst][11] = "Rescheduled"
    raw[src][11] = "Rescheduled"
for i, row in enumerate(raw, start=2):
    for j, v in enumerate(row, start=1):
        c = ws.cell(row=i, column=j, value=v)
        c.font = F()
        if j == 2:
            c.number_format = "d mmm yyyy"
RAW_LAST = len(raw) + 1
name("raw_id", f"'Raw Bookings'!$A$2:$A${RAW_LAST}")
widths(ws, {"A": 15, "B": 13, "C": 18, "D": 8, "E": 10, "F": 18, "G": 8, "H": 20, "I": 8, "J": 7, "K": 10, "L": 12,
            "M": 3, "N": 18, "O": 10, "P": 11, "Q": 12, "R": 11, "S": 11})
ws.freeze_panes = "B2"
ws.auto_filter.ref = f"A1:L{RAW_LAST}"
put(ws, "N1", "Sample summary (COUNTIFS / AVERAGEIFS)", F(bold=True))
header_row(ws, 2, 14, ["City", "Bookings", "Completed", "Completion", "Avg rating", "Complaints"])
for i, c in enumerate(CITIES, start=3):
    put(ws, f"N{i}", c, F())
    put(ws, f"O{i}", f'=COUNTIFS($C$2:$C${RAW_LAST},N{i})', F(), "0")
    put(ws, f"P{i}", f'=COUNTIFS($C$2:$C${RAW_LAST},N{i},$H$2:$H${RAW_LAST},"Completed")', F(), "0")
    put(ws, f"Q{i}", f'=IFERROR(P{i}/O{i},0)', F(), PCT0)
    put(ws, f"R{i}", f'=IFERROR(AVERAGEIFS($J$2:$J${RAW_LAST},$C$2:$C${RAW_LAST},N{i}),0)', F(), D2)
    put(ws, f"S{i}", f'=COUNTIFS($C$2:$C${RAW_LAST},N{i},$K$2:$K${RAW_LAST},"Y")', F(), "0")
rt = 3 + len(CITIES)
put(ws, f"N{rt}", "Total", F(bold=True))
for col in "OPS":
    put(ws, f"{col}{rt}", f"=SUM({col}3:{col}{rt - 1})", F(bold=True), "0")
put(ws, f"Q{rt}", f"=P{rt}/O{rt}", F(bold=True), PCT0)
put(ws, f"R{rt}", f"=AVERAGE($J$2:$J${RAW_LAST})", F(bold=True), D2)
put(ws, f"N{rt + 2}", "A 300-row extract to practise on: one row per booking. Three rescheduled bookings appear twice "
    "with the same ID. The Data Checks tab catches them.", F(italic=True, color=MUTED))
ws.conditional_formatting.add(f"A2:A{RAW_LAST}", FormulaRule(formula=[f"COUNTIF(raw_id,A2)>1"], fill=AMBER_FILL))

# ------------------------------------------------------------------ Data Checks
ws = ws_chk
title(ws, "Data checks · run before the MIS goes out", "Each check is a live formula on the Data and Raw Bookings tabs. Two problems were caught and fixed this week.")
header_row(ws, 4, 2, ["#", "Check", "What it tests", "Result", "Detail"])
SYS = {w: sum(r["req"] for r in D["rows"] if r["week"] == w) for w in WEEKS}
SYSC = {w: sum(r["comp"] for r in D["rows"] if r["week"] == w) for w in WEEKS}
CHECKS = [
    ("Funnel order holds", "Requests ≥ assigned ≥ completed on every row",
     '=IF(SUMPRODUCT(--(d_asg>d_req))+SUMPRODUCT(--(d_comp>d_asg))=0,"PASS","FAIL")',
     f'=SUMPRODUCT(--(d_asg>d_req))+SUMPRODUCT(--(d_comp>d_asg))&" rows break the order, of "&ROWS(d_req)'),
    ("Cancellations reconcile", "Completed = assigned − customer cancels − partner cancels",
     '=IF(SUMPRODUCT(--(d_comp<>d_asg-d_cc-d_pc))=0,"PASS","FAIL")',
     '=SUMPRODUCT(--(d_comp<>d_asg-d_cc-d_pc))&" rows do not reconcile"'),
    ("No impossible counts", "On time ≤ completed, perfect ≤ on time, stock-outs ≤ active partners",
     '=IF(SUMPRODUCT(--(d_ot>d_comp))+SUMPRODUCT(--(d_perf>d_ot))+SUMPRODUCT(--(d_stock>d_act))=0,"PASS","FAIL")',
     '="0 = clean"'),
    ("Cities add up to the ops-app total", "City rows summed vs the national totals the ops app reports (table below)",
     None, None),
    ("No blanks or negatives", "Every count in the Data tab is filled in and ≥ 0",
     f'=IF(AND(COUNTBLANK(Data!A2:V{LAST})=0,COUNTIF(Data!E2:V{LAST},"<0")=0),"PASS","FAIL")',
     f'=COUNTBLANK(Data!A2:V{LAST})&" blanks, "&COUNTIF(Data!E2:V{LAST},"<0")&" negatives"'),
    ("Duplicate booking IDs", "Reschedules logged twice would inflate requests",
     '=IF(SUMPRODUCT(--(COUNTIF(raw_id,raw_id)>1))=0,"PASS","FIXED")',
     '=SUMPRODUCT(--(COUNTIF(raw_id,raw_id)>1))&" rows share an ID in the raw sample. Counted once, by booking ID"'),
    ("One fill-rate definition", "City Ops left out requests cancelled by customers within 5 minutes",
     '="FIXED"', None),
    ("Rates are never averaged", "Average of slot rates vs sum ÷ sum, from the City View tab",
     '="NOTE"', '="Simple average "&TEXT(trap_simple,"0.0%")&" vs right answer "&TEXT(trap_right,"0.0%")'),
]
rec0 = 4 + len(CHECKS) + 4
for i, (lab, what, res, det) in enumerate(CHECKS, start=5):
    put(ws, f"B{i}", i - 4, F(), "0", border=BOTTOM, align=CENTER)
    put(ws, f"C{i}", lab, F(bold=True), border=BOTTOM)
    put(ws, f"D{i}", what, F(color=MUTED), border=BOTTOM)
    if lab.startswith("Cities add up"):
        res = f'=IF(SUMPRODUCT(ABS(E{rec0 + 1}:E{rec0 + len(WEEKS)}))+SUMPRODUCT(ABS(H{rec0 + 1}:H{rec0 + len(WEEKS)}))=0,"PASS","FAIL")'
        det = f'="Difference over 12 weeks: "&SUMPRODUCT(ABS(E{rec0 + 1}:E{rec0 + len(WEEKS)}))'
    if lab.startswith("One fill-rate"):
        det = f'="City Ops said "&TEXT(SUMIFS(d_asg,d_week,{CUR})/(SUMIFS(d_req,d_week,{CUR})-1620),"0.0%")&", MIS said "&TEXT(SUMIFS(d_asg,d_week,{CUR})/SUMIFS(d_req,d_week,{CUR}),"0.0%")&". Fixed with the metric dictionary (A-113)"'
    put(ws, f"E{i}", res, F(bold=True), border=BOTTOM, align=CENTER)
    put(ws, f"F{i}", det, F(), border=BOTTOM)
CL = 4 + len(CHECKS)
for txt, fill, color in (("PASS", GREEN_FILL, "006100"), ("FIXED", AMBER_FILL, "7A5000"), ("NOTE", GRAY_FILL, "52514E"), ("FAIL", RED_FILL, "9C0006")):
    ws.conditional_formatting.add(f"E5:E{CL}", FormulaRule(formula=[f'E5="{txt}"'], fill=fill, font=Font(name=FONT, bold=True, color=color)))
put(ws, f"B{rec0 - 1}", "Reconciliation: ops-app national totals vs the city rows in the Data tab", F(size=12, bold=True))
header_row(ws, rec0, 2, ["Week", "Ops app: requests", "Data tab: requests", "Difference", "Ops app: completed",
                         "Data tab: completed", "Difference"])
for i, w in enumerate(WEEKS, start=rec0 + 1):
    put(ws, f"B{i}", w, F(), '"W"0', align=CENTER)
    put(ws, f"C{i}", SYS[w], F(color="0000FF"), INT)
    put(ws, f"D{i}", f"=SUMIFS(d_req,d_week,B{i})", F(), INT)
    put(ws, f"E{i}", f"=D{i}-C{i}", F(bold=True), '#,##0;-#,##0;"–"')
    put(ws, f"F{i}", SYSC[w], F(color="0000FF"), INT)
    put(ws, f"G{i}", f"=SUMIFS(d_comp,d_week,B{i})", F(), INT)
    put(ws, f"H{i}", f"=G{i}-F{i}", F(bold=True), '#,##0;-#,##0;"–"')
widths(ws, {"A": 2, "B": 7, "C": 30, "D": 52, "E": 10, "F": 70, "G": 14, "H": 12})
for i in range(5, CL + 1):
    ws.row_dimensions[i].height = 20

# ------------------------------------------------------------------ Metric Dictionary
ws = ws_dict
title(ws, "Metric dictionary, v1", "One definition per number. Most 'data mismatches' between managers are definition mismatches.")
header_row(ws, 4, 2, ["Metric", "Definition", "Formula in this workbook", "Owner"])
DICT = [
    ("Perfect booking (North Star)", "Completed, started within 15 min of the slot, no complaint, no redo or refund, rated 4★+ or not rated. Rate = ÷ booking requests", "perfect ÷ requests", "All five"),
    ("Booking requests", "Unique booking IDs with a service date in the week. A reschedule counts once", "SUMIFS(requests)", "City Ops"),
    ("Fill rate", "Requests assigned a partner ÷ booking requests", "assigned ÷ requests", "City Ops"),
    ("Jobs completed", "Assigned − customer cancels − partner cancels", "assigned − cancels", "City Ops"),
    ("On-time arrival", "Jobs started within 15 min of slot ÷ jobs completed (15 min to agree with the VP)", "on time ÷ completed", "City Ops"),
    ("Cancellation rate", "Cancelled after assignment ÷ assigned. Split customer side and partner side", "cancels ÷ assigned", "CX / Supply"),
    ("Active partner", "Did 1 or more jobs in the week", "SUMIFS(active partners)", "Supply"),
    ("New partners certified", "Passed the final assessment this week", "SUMIFS(certified)", "Training & QA"),
    ("90-day retention", "Partners from the cohort that joined 13 weeks ago, still active this week ÷ cohort size", "cohort active ÷ cohort size", "Supply"),
    ("Jobs per partner per day", "Jobs completed ÷ (active partners × 6 working days)", "completed ÷ (active × 6)", "City Ops"),
    ("Average rating", "Sum of stars ÷ number of ratings", "stars ÷ ratings", "Training & QA"),
    ("Complaints per 1,000", "Complaints ÷ jobs completed × 1,000", "complaints ÷ completed × 1,000", "CX"),
    ("Redo / refund rate", "Jobs redone or refunded ÷ jobs completed", "redo ÷ completed", "CX"),
    ("Kit stock-out", "Partners reporting 1 or more missing kit items ÷ active partners", "stock-out partners ÷ active", "Inventory"),
    ("Week", "Service date, Monday to Sunday, IST. ISO week number", "—", "Founder's Office"),
]
for i, row in enumerate(DICT, start=5):
    for j, v in enumerate(row, start=2):
        c = ws.cell(row=i, column=j, value=v)
        c.font = F(bold=j == 2)
        c.alignment = WRAP
        c.border = BOTTOM
    ws.row_dimensions[i].height = 30
widths(ws, {"A": 2, "B": 28, "C": 70, "D": 30, "E": 16})
ws.freeze_panes = "B5"

# ------------------------------------------------------------------ JD Map
ws = ws_jd
title(ws, "Built for this role", "Each line of the job description, where it shows up in this pack, and where I've done it before.")
header_row(ws, 4, 2, ["The JD asks for", "Where it is in this pack", "Where I've done it before"])
JD = [
    ("MIS reporting and dashboards", "Dashboard slides 1–5. This workbook: one Data tab feeds every number", "LVX: automated dashboards in Google Sheets and Power BI tracking ₹7 Cr+ of pipeline. Reporting accuracy up 30%"),
    ("Turn data into insights", "North Star leak split; ₹ impact; kits → cancellations → fill rate link (CORREL on Quality & Kits)", "LVX: funnel analysis across ₹3.5 Cr, ₹7 Cr and ₹9 Cr+ launches. Conversion up 20%"),
    ("Weekly and monthly reports, review decks", "Weekly MIS tab (one page) and Monthly tab. The dashboard is the review deck", "Techvaraha: weekly and monthly reviews across 4 departments. 15+ executive presentations"),
    ("Spot discrepancies, gaps and bottlenecks", "Data Checks tab: 8 live checks, reconciliation to the ops-app totals, duplicate IDs", "LVX: reporting SOPs and data workflows. Manual errors down 35%"),
    ("Track managers' priorities, deliverables and timelines", "Action Tracker: one owner and one date per action, days late and flags by formula", "Techvaraha: kept 15–20 people across our team and client CXOs moving together. Project delays down 25%"),
    ("Follow up and close on time", "Manager summary, on-time closure %, escalation ladder", "Techvaraha: escalation turnaround down 40%. Zero missed deliverables for 3 quarters"),
    ("Monitor metrics against targets", "Targets tab drives every status. One red-amber-green rule for all 14 KPIs", "Techvaraha: 4 SOPs, QA workflows and KRAs. On-time delivery from 65% to 90%"),
    ("Confidentiality and integrity", "Mock data only. Weekly MIS is protected; only the yellow input cells can be edited", "LVX: owned investor consent and compliance workflows for the Dubai corridor"),
    ("Strong Excel and Google Sheets", "SUMIFS, COUNTIFS, INDEX-MATCH, named ranges, data validation, conditional formatting, CORREL", "Advanced Excel. Automated Google Sheets dashboards at LVX"),
    ("Partner supply and ops", "Supply tab: onboarding funnel, cohort retention, utilisation lever", "Built a network of 1,400+ healthcare practitioners and 15+ hospital tie-ups. Ran sourcing, inventory and QC at Gomedha"),
    ("A fast leadership office", "Built over one weekend, from public information", "Two Founder's Office roles. Best Execution Award 2025"),
]
for i, row in enumerate(JD, start=5):
    for j, v in enumerate(row, start=2):
        c = ws.cell(row=i, column=j, value=v)
        c.font = F(bold=j == 2)
        c.alignment = WRAP
        c.border = BOTTOM
    ws.row_dimensions[i].height = 42
r = 5 + len(JD) + 1
put(ws, f"B{r}", "My first 90 days", F(size=12, bold=True))
for j, (h, t) in enumerate([("Days 1–30", "Learn each manager's area. Audit today's MIS. Write the metric dictionary."),
                            ("Days 31–60", "Launch one weekly MIS and one action tracker. Run the weekly review."),
                            ("Days 61–90", "Automate the manual parts. Own one bottleneck fix end to end, picked with the VP.")], start=r + 1):
    put(ws, f"B{j}", h, F(bold=True, color="2A78D6"))
    put(ws, f"C{j}", t, F())
r += 5
put(ws, f"B{r}", "Public facts this mock is scaled to", F(size=12, bold=True))
for j, (k, v) in enumerate([("Bookings a month", "about 3.5 lakh"), ("Partners onboarded", "12,000+"),
                            ("Active partners", "about 7,500"), ("Cities", "55–60")], start=r + 1):
    put(ws, f"B{j}", k, F())
    put(ws, f"C{j}", v, F(bold=True))
put(ws, f"B{r + 5}", "From company statements and press (YourStory, Apr 2026). Everything else in this workbook is mock.", F(italic=True, color=MUTED))
widths(ws, {"A": 2, "B": 34, "C": 62, "D": 70})

# ------------------------------------------------------------------ Cover
ws = ws_cover
put(ws, "B2", "VP Operations · Weekly MIS", F(size=22, bold=True, color=INK))
put(ws, "B3", "Week 42 · 12–18 Oct 2026 · a working demo for the Founder's Office – Operations role", F(size=12, color=MUTED))
put(ws, "B4", MOCK, F(size=10, bold=True, color="7A5000"), fill=AMBER_FILL)
for col in "CDE":
    ws[f"{col}4"].fill = AMBER_FILL
put(ws, "B6", "North Star this week", F(bold=True, color=MUTED))
put(ws, "B7", f"=SUMIFS(d_perf,d_week,{CUR})", F(size=26, bold=True, color="2A78D6"), INT)
put(ws, "C7", f'="perfect bookings · "&TEXT(SUMIFS(d_perf,d_week,{CUR})/SUMIFS(d_req,d_week,{CUR}),"0.0%")&" of requests · target "&TEXT(t_nsm,"0%")',
    F(size=11, color=INK))
put(ws, "B9", "How to use", F(size=12, bold=True))
for i, t in enumerate([
    "1. Open Weekly MIS. Pick a week and a city in the yellow cells. Every number recalculates.",
    "2. Change a target on the Targets tab. Every status, in every tab, follows.",
    "3. All KPIs are built from the Data tab with SUMIFS: counts are summed first, then divided. Rates are never averaged.",
], start=10):
    put(ws, f"B{i}", t, F())
put(ws, "B14", "Tabs", F(size=12, bold=True))
TABS = [
    ("Weekly MIS", "One-page MIS: 15 KPIs, this week vs last week vs target, with status and owner"),
    ("North Star", "Perfect bookings over 12 weeks, and which funnel term moved it"),
    ("Monthly", "Aug, Sep and Oct to date, for the monthly review"),
    ("City View", "Every KPI by city, plus fill rate by day and slot"),
    ("Supply", "Onboarding funnel, cohort retention, utilisation"),
    ("Quality & Kits", "Complaints by service and hub, kit items missing, CORREL"),
    ("Action Tracker", "Five managers' actions, flags by formula, manager summary"),
    ("Data Checks", "8 checks that run before the MIS goes out"),
    ("Targets", "Targets, direction and owners. Drives every status"),
    ("Metric Dictionary", "One definition per number"),
    ("JD Map", "Job description × this pack × my track record"),
    ("Data", "Fact table: 12 weeks × 8 cities of counts"),
    ("Raw Bookings", "A 300-row booking log to practise on"),
]
for i, (tab, desc) in enumerate(TABS, start=15):
    c = put(ws, f"B{i}", tab, F(color="2A78D6", underline="single"))
    c.hyperlink = f"#'{tab}'!A1"
    put(ws, f"C{i}", desc, F(color=MUTED))
r = 15 + len(TABS) + 1
put(ws, f"B{r}", "Cell colours", F(size=12, bold=True))
put(ws, f"B{r + 1}", "Input", INPUT_FONT, fill=INPUT_FILL)
put(ws, f"C{r + 1}", "Yellow fill, blue text: change these", F(color=MUTED))
put(ws, f"B{r + 2}", "Formula", F())
put(ws, f"C{r + 2}", "Black text: calculated, don't type over", F(color=MUTED))
put(ws, f"B{r + 3}", "Link", LINK_FONT)
put(ws, f"C{r + 3}", "Green text: pulled from another tab", F(color=MUTED))
put(ws, f"B{r + 4}", "Raw input", F(color="0000FF"))
put(ws, f"C{r + 4}", "Blue text: source data typed in or pasted from a system", F(color=MUTED))
put(ws, f"B{r + 6}", "Status rule", F(size=12, bold=True))
for j, (s, t, fill) in enumerate([("Green", "Meets target", GREEN_FILL), ("Amber", "Within 5% of target", AMBER_FILL),
                                   ("Red", "Further off than 5%", RED_FILL), ("Info", "Tracked, no target", GRAY_FILL)], start=r + 7):
    put(ws, f"B{j}", s, F(bold=True), fill=fill, align=CENTER)
    put(ws, f"C{j}", t, F(color=MUTED))
put(ws, f"B{r + 12}", "Prepared by Chethan for the interview on Mon 19 Oct 2026.", F(italic=True, color=MUTED))
widths(ws, {"A": 3, "B": 22, "C": 90})

for w in wb.worksheets:
    w.page_setup.orientation = "landscape"
    w.page_setup.fitToWidth = 1
    w.page_setup.fitToHeight = 0
    w.sheet_properties.pageSetUpPr.fitToPage = True
wb.active = wb.sheetnames.index("Cover")
wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print("saved", OUT)
