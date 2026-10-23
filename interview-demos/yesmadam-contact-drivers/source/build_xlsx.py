"""Build the contact-driver teardown workbook. Every count is a COUNTIFS on the Reviews tab."""
import datetime as dt
import json
import sys

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import FormulaRule, ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

D = json.load(open(sys.argv[1]))
FULL = json.load(open(sys.argv[2]))
OUT = sys.argv[3]
S, M = D["story"], D["meta"]
DRV, SUB = D["drivers"], D["subtags"]

FONT = "Arial"
F = lambda **k: Font(name=FONT, size=k.pop("size", 10), **k)
INK, MUTED, WHITE = "1F2937", "6B7280", "FFFFFF"
HEAD = PatternFill("solid", fgColor="1F2937")
BLOCK = PatternFill("solid", fgColor="EEF0F3")
INPUT = PatternFill("solid", fgColor="FFF2CC")
HL = PatternFill("solid", fgColor="E8F1FC")
GREEN = PatternFill("solid", fgColor="D9F2DC")
AMBER = PatternFill("solid", fgColor="FFE9B3")
RED = PatternFill("solid", fgColor="F8D3D3")
HAIR = Side(style="thin", color="D9D9D6")
BOT = Border(bottom=HAIR)
INPUT_FONT = F(color="0000FF", bold=True)
LINK = F(color="008000")
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center")
PCT1, PCT0, INT = "0.0%", "0%", "#,##0"
RS = '"₹"#,##0'
RSL = '"₹"#,##0.0," L"'

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


def put(ws, ref, v, font=None, fmt=None, fill=None, align=None, border=None):
    c = ws[ref]
    c.value = v
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


def header(ws, row, col0, labels):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=col0 + i, value=lab)
        c.font = F(bold=True, color=WHITE)
        c.fill = HEAD
        c.alignment = Alignment(horizontal="left" if i == 0 else "center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 30


def title(ws, t, sub=None):
    put(ws, "B1", t, F(size=16, bold=True, color=INK))
    if sub:
        put(ws, "B2", sub, F(italic=True, color=MUTED))
    ws.column_dimensions["A"].width = 2
    ws.row_dimensions[1].height = 26


def widths(ws, spec):
    for k, v in spec.items():
        ws.column_dimensions[k].width = v


NOTE = "Real public App Store reviews (India), tagged twice with one codebook (AI-assisted), disagreements settled. Names and order IDs removed. Prepared by Chethan."

ws_cover = sheet("Cover", tab="1F2937")
ws_par = sheet("Pareto", tab="2A78D6")
ws_top = sheet("Top Drivers", tab="2A78D6")
ws_why = sheet("Five Whys", tab="2A78D6")
ws_imp = sheet("Impact Model", tab="2A78D6")
ws_fix = sheet("Fixes", tab="2A78D6")
ws_read = sheet("Readout", tab="2A78D6")
ws_ben = sheet("Benchmark", tab="EB6834")
ws_tr = sheet("Trends", tab="EB6834")
ws_rel = sheet("Reliability", tab="EB6834")
ws_code = sheet("Codebook", tab="FAB219")
ws_jd = sheet("JD Map", tab="FAB219")
ws_rv = sheet("Reviews", grid=True, tab="9CA3AF")
ws_uc = sheet("UC Reviews", grid=True, tab="9CA3AF")
ws_lists = sheet("Lists", grid=True)

# ---------------------------------------------------------------- Reviews (all 500, tagged)
reviews = FULL["reviews"]
RCOLS = [("#", "n", 6), ("Date", "date", 11), ("Month", None, 9), ("Stars", "rating", 6), ("App version", "version", 9),
         ("Title", "title", 26), ("Review (names and IDs removed)", "text", 70), ("Primary driver", "primary", 20),
         ("Subtag", "subtag", 22), ("Also mentions", "secondary", 22), ("Contacted support", "contacted", 10),
         ("Support failed", "failed", 9), ("Severity", "severity", 9), ("Says they'll leave", "churn", 9),
         ("Service", "service", 13), ("City", "city", 11), ("Amount ₹", "amount", 9), ("Evidence quote", "quote", 40),
         ("Tagger A", "tagA", 18), ("Tagger B", "tagB", 18), ("Tie-break note", "adjudicated", 40)]
header(ws_rv, 1, 1, [c[0] for c in RCOLS])
for i, r in enumerate(reviews, start=2):
    for j, (h, k, w) in enumerate(RCOLS, start=1):
        if k is None:
            v = f'=TEXT(B{i},"yyyy-mm")'
        elif k == "date":
            v = dt.datetime.fromisoformat(r["date"])
        elif k == "secondary":
            v = ", ".join(r["secondary"])
        elif k == "churn":
            v = "yes" if r["churn"] else "no"
        else:
            v = r.get(k, "")
        c = ws_rv.cell(row=i, column=j, value=v)
        c.font = F()
        if k == "date":
            c.number_format = "d mmm yyyy"
        if k in ("text", "quote", "adjudicated", "title"):
            c.alignment = Alignment(wrap_text=False, vertical="top")
LR = len(reviews) + 1
for j, (h, k, w) in enumerate(RCOLS, start=1):
    col = ws_rv.cell(row=1, column=j).column_letter
    ws_rv.column_dimensions[col].width = w
for nm, col in (("r_n", "A"), ("r_date", "B"), ("r_month", "C"), ("r_star", "D"), ("r_ver", "E"), ("r_primary", "H"), ("r_sub", "I"),
                ("r_sec", "J"), ("r_contact", "K"), ("r_failed", "L"), ("r_sev", "M"), ("r_churn", "N"), ("r_service", "O"),
                ("r_tagA", "S"), ("r_tagB", "T")):
    name(nm, f"Reviews!${col}$2:${col}${LR}")
ws_rv.freeze_panes = "H2"
ws_rv.auto_filter.ref = f"A1:U{LR}"

# ---------------------------------------------------------------- UC Reviews (tags only)
uc_tags = {x["n"]: x for x in FULL["uc_tags"]}
UCOLS = ["#", "Date", "Stars", "Primary driver", "Subtag", "Contacted support", "Severity", "Says they'll leave"]
header(ws_uc, 1, 1, UCOLS)
ucr = [r for r in FULL["uc_rows"] if r["n"] in uc_tags]
for i, r in enumerate(ucr, start=2):
    t = uc_tags[r["n"]]
    vals = [r["n"], dt.datetime.fromisoformat(r["date"]), r["rating"], t["primary"], t["subtag"], t["contacted_support"], t["severity"],
            "yes" if t["churn_signal"] else "no"]
    for j, v in enumerate(vals, start=1):
        c = ws_uc.cell(row=i, column=j, value=v)
        c.font = F()
        if j == 2:
            c.number_format = "d mmm yyyy"
LU = len(ucr) + 1
for nm, col in (("u_primary", "D"), ("u_contact", "F"), ("u_sev", "G"), ("u_churn", "H"), ("u_star", "C")):
    name(nm, f"'UC Reviews'!${col}$2:${col}${LU}")
widths(ws_uc, {"A": 6, "B": 12, "C": 6, "D": 22, "E": 24, "F": 10, "G": 10, "H": 10})
put(ws_uc, f"A{LU + 2}", "Urban Company review text is not included: only the tags, for the benchmark.", F(italic=True, color=MUTED))
ws_uc.freeze_panes = "A2"

# ---------------------------------------------------------------- Lists
ORDER = S["order"]
for i, k in enumerate(ORDER + ["praise"], start=2):
    ws_lists.cell(row=i, column=1, value=k)
ws_lists.sheet_state = "hidden"

# ---------------------------------------------------------------- Pareto
ws = ws_par
title(ws, "Pareto of complaint drivers", "One primary driver per review. Counts are COUNTIFS on the Reviews tab; change a tag there and this recalculates.")
put(ws, "B4", "Reviews read", F(bold=True)); put(ws, "D4", "=COUNTA(r_n)", F(bold=True), INT)
put(ws, "B5", "Complaints (not praise)", F(bold=True)); put(ws, "D5", '=COUNTA(r_n)-COUNTIF(r_primary,"praise")', F(bold=True), INT)
put(ws, "B6", "1-star reviews", F(bold=True)); put(ws, "D6", "=COUNTIF(r_star,1)", F(bold=True), INT)
put(ws, "E6", "=D6/D4", F(), PCT0)
put(ws, "F6", f"of written reviews are 1★, while the store average is {M['store_avg']:.2f}★ across {M['store_ratings']:,} ratings. Reviews are a complaint channel.", F(color=MUTED))
name("n_reviews", "Pareto!$D$4"); name("n_comp", "Pareto!$D$5")
header(ws, 8, 2, ["Driver key", "Driver", "Reviews", "Share of complaints", "Running share", "Mentioned anywhere", "% of driver: contacted support", "% of driver: high severity", "% of driver: say they'll leave", "Top 3?", "Share of all who contacted support"])
ws.row_dimensions[8].height = 46
P0 = 9
for i, k in enumerate(ORDER):
    r = P0 + i
    put(ws, f"B{r}", k, F(color=MUTED), border=BOT)
    put(ws, f"C{r}", DRV[k]["label"], F(bold=k in S["top3"]), border=BOT)
    put(ws, f"D{r}", f"=COUNTIF(r_primary,B{r})", F(bold=True), INT, border=BOT)
    put(ws, f"E{r}", f"=D{r}/n_comp", F(), PCT1, border=BOT)
    put(ws, f"F{r}", f"=SUM($D${P0}:D{r})/n_comp", F(color=MUTED), PCT0, border=BOT)
    put(ws, f"G{r}", f'=SUMPRODUCT(--(((r_primary=B{r})+ISNUMBER(SEARCH(B{r},r_sec)))>0))', F(), INT, border=BOT)
    put(ws, f"H{r}", f'=IFERROR(COUNTIFS(r_primary,B{r},r_contact,"yes")/D{r},0)', F(), PCT0, border=BOT)
    put(ws, f"I{r}", f'=IFERROR(COUNTIFS(r_primary,B{r},r_sev,"high")/D{r},0)', F(), PCT0, border=BOT)
    put(ws, f"J{r}", f'=IFERROR(COUNTIFS(r_primary,B{r},r_churn,"yes")/D{r},0)', F(), PCT0, border=BOT)
    put(ws, f"K{r}", "Yes" if k in S["top3"] else "", F(bold=True, color="2A78D6"), align=CENTER, border=BOT)
    put(ws, f"L{r}", f'=IFERROR(COUNTIFS(r_primary,B{r},r_contact,"yes")/COUNTIFS(r_primary,"<>praise",r_contact,"yes"),0)', F(), PCT0, border=BOT)
PL = P0 + len(ORDER) - 1
put(ws, f"C{PL + 1}", "All complaints", F(bold=True))
put(ws, f"D{PL + 1}", f"=SUM(D{P0}:D{PL})", F(bold=True), INT)
put(ws, f"E{PL + 1}", f"=SUM(E{P0}:E{PL})", F(bold=True), PCT0)
put(ws, f"F{PL + 1}", f'=IF(D{PL + 1}=n_comp,"Ties to complaint count","Does not tie: check tags")', F(color=MUTED))
put(ws, f"C{PL + 3}", "Top 3 drivers' share of complaints", F(bold=True))
put(ws, f"E{PL + 3}", f'=SUMIFS(D{P0}:D{PL},K{P0}:K{PL},"Yes")/n_comp', F(bold=True, color="2A78D6"), PCT0)
name("top3_share", f"Pareto!$E${PL + 3}")
put(ws, f"C{PL + 4}", "Top 3 drivers' share of those who contacted support", F(bold=True))
put(ws, f"E{PL + 4}", f'=SUMIFS(L{P0}:L{PL},K{P0}:K{PL},"Yes")', F(bold=True, color="2A78D6"), PCT0)
put(ws, f"F{PL + 4}", "Weighted by reviews that say they already contacted support: the better proxy for contacts, on a smaller sample", F(color=MUTED))
for r in range(P0, PL + 1):
    pass
ws.conditional_formatting.add(f"B{P0}:L{PL}", FormulaRule(formula=[f'$K{P0}="Yes"'], fill=HL))
ch = BarChart(); ch.type = "bar"; ch.title = "Complaints by primary driver"; ch.height, ch.width = 8, 15
ch.add_data(Reference(ws, min_col=4, min_row=8, max_row=PL), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=3, min_row=P0, max_row=PL))
ch.x_axis.scaling.orientation = "maxMin"; ch.legend = None; ch.y_axis.majorGridlines = None
ch.series[0].graphicalProperties.solidFill = "2A78D6"
ws.add_chart(ch, f"N8")
widths(ws, {"B": 22, "C": 28, "D": 10, "E": 12, "F": 11, "G": 12, "H": 14, "I": 14, "J": 14, "K": 8, "L": 14})
ws.freeze_panes = "B9"

# ---------------------------------------------------------------- Top drivers
ws = ws_top
title(ws, "The top three drivers", "Subtags, contact and severity for each, plus the quotes used on slide 2.")
r = 4
for idx, k in enumerate(S["top3"], start=1):
    put(ws, f"B{r}", f"#{idx} {DRV[k]['label']}", F(size=12, bold=True, color="2A78D6"))
    put(ws, f"F{r}", f'=COUNTIF(r_primary,"{k}")', F(bold=True), INT)
    put(ws, f"G{r}", f"=F{r}/n_comp", F(bold=True), PCT0)
    put(ws, f"H{r}", "of complaints", F(color=MUTED))
    r += 1
    header(ws, r, 2, ["Subtag", "Label", "Reviews", "Share of driver"])
    r += 1
    subs = sorted({x["subtag"] for x in reviews if x["primary"] == k}, key=lambda s: -sum(1 for x in reviews if x["primary"] == k and x["subtag"] == s))
    r0 = r
    for s in subs:
        put(ws, f"B{r}", s, F(color=MUTED), border=BOT)
        put(ws, f"C{r}", SUB.get(s, s), F(), border=BOT)
        put(ws, f"D{r}", f'=COUNTIFS(r_primary,"{k}",r_sub,B{r})', F(bold=True), INT, border=BOT)
        put(ws, f"E{r}", f'=D{r}/COUNTIF(r_primary,"{k}")', F(), PCT0, border=BOT)
        r += 1
    put(ws, f"C{r}", "Contacted support", F()); put(ws, f"E{r}", f'=COUNTIFS(r_primary,"{k}",r_contact,"yes")/COUNTIF(r_primary,"{k}")', F(bold=True), PCT0); r += 1
    put(ws, f"C{r}", "High severity", F()); put(ws, f"E{r}", f'=COUNTIFS(r_primary,"{k}",r_sev,"high")/COUNTIF(r_primary,"{k}")', F(bold=True), PCT0); r += 1
    put(ws, f"C{r}", "Say they'll leave", F()); put(ws, f"E{r}", f'=COUNTIFS(r_primary,"{k}",r_churn,"yes")/COUNTIF(r_primary,"{k}")', F(bold=True), PCT0); r += 1
    put(ws, f"C{r}", "Quotes", F(bold=True)); r += 1
    for q in S["quotes"].get(k, [])[:3]:
        put(ws, f"C{r}", f'"{q["text"]}"', F(italic=True), align=WRAP)
        ws.merge_cells(f"C{r}:H{r}")
        put(ws, f"I{r}", f'{q["rating"]}★ · {q["date"]}', F(color=MUTED))
        ws.row_dimensions[r].height = 30
        r += 1
    r += 2
widths(ws, {"B": 26, "C": 30, "D": 10, "E": 12, "F": 10, "G": 10, "H": 14, "I": 16})

# ---------------------------------------------------------------- Five whys
ws = ws_why
title(ws, "Root causes: five whys on the top three drivers", '"In reviews" = customers say it. "To verify" = my hypothesis, to check against ticket and ops data.')
r = 4
for w in S["whys"]:
    put(ws, f"B{r}", DRV[w["driver"]]["label"], F(size=12, bold=True, color="2A78D6")); r += 1
    put(ws, f"B{r}", "Problem", F(bold=True)); put(ws, f"C{r}", w["problem"], F(), align=WRAP); ws.merge_cells(f"C{r}:F{r}"); r += 1
    header(ws, r, 2, ["Why", "Answer", "", "", "Evidence"]); r += 1
    for i, c in enumerate(w["chain"], start=1):
        put(ws, f"B{r}", f"Why {i}", F(color=MUTED), border=BOT)
        put(ws, f"C{r}", c["text"], F(), align=WRAP, border=BOT); ws.merge_cells(f"C{r}:E{r}")
        put(ws, f"F{r}", "In reviews" if c["ev"] == "E" else "To verify", F(bold=True, color="006100" if c["ev"] == "E" else "7A5000"), border=BOT)
        ws.row_dimensions[r].height = 30
        r += 1
    put(ws, f"B{r}", "Root cause", F(bold=True)); put(ws, f"C{r}", w["root"], F(bold=True), align=WRAP); ws.merge_cells(f"C{r}:F{r}"); ws.row_dimensions[r].height = 30; r += 1
    put(ws, f"B{r}", "Would prove me wrong", F(bold=True, color=MUTED)); put(ws, f"C{r}", w["test"], F(color=MUTED), align=WRAP); ws.merge_cells(f"C{r}:F{r}"); ws.row_dimensions[r].height = 30; r += 3
widths(ws, {"B": 20, "C": 40, "D": 30, "E": 30, "F": 12})

# ---------------------------------------------------------------- Impact model
ws = ws_imp
title(ws, "Impact in contacts and rupees", "Yellow cells are assumptions. Change them and everything below updates. Driver mix comes from the Pareto tab.")
dfl = D["impact"]["defaults"]
INPUTS = [("Bookings a month", dfl["bookings"], INT, "inp_bookings", "Public figure: about 3.5 lakh bookings a month"),
          ("Contacts per 100 bookings", dfl["contactRate"], "0", "inp_rate", "Assumption. Typical for at-home services: 8–15. Replace with the real number"),
          ("Cost per contact (₹)", dfl["costPerContact"], RS, "inp_cost", "Assumption: blended chat and voice"),
          ("Cut in top-3 contacts from the fixes", dfl["reduction"] / 100, PCT0, "inp_cut", "Target for the three fixes"),
          ("Customers lost per top-3 contact", dfl["lostShare"] / 100, PCT0, "inp_lost", f"Reviews say {D['impact']['churnTop3']:.0%}; the real rate is lower, so this is cautious"),
          ("Yearly value of a customer (₹)", dfl["annualValue"], RS, "inp_value", "Assumption: about ₹1,350 a visit, 4 visits a year")]
header(ws, 4, 2, ["Assumption", "Value", "Note"])
for i, (lab, v, fmt, nm, note) in enumerate(INPUTS, start=5):
    put(ws, f"B{i}", lab, F(bold=True), border=BOT)
    put(ws, f"C{i}", v, INPUT_FONT, fmt, INPUT, border=BOT)
    put(ws, f"D{i}", note, F(color=MUTED), border=BOT)
    name(nm, f"'Impact Model'!$C${i}")
r = 13
header(ws, r, 2, ["Result", "Value", "How"])
RES = [("Contacts a month", "=inp_bookings*inp_rate/100", INT, "bookings × contacts per 100"),
       ("Support cost a month", "=C14*inp_cost", RS, "contacts × cost per contact"),
       ("Contacts from the top 3 drivers", "=C14*top3_share", INT, "contacts × top-3 share of complaints"),
       ("Contacts removed a month", "=C16*inp_cut", INT, "top-3 contacts × cut"),
       ("Support cost saved a year", "=C17*inp_cost*12", RS, "removed contacts × cost × 12"),
       ("Customers kept a month", "=C17*inp_lost", INT, "removed contacts × customers lost per contact"),
       ("Revenue kept a year (up to)", "=C19*12*inp_value", RS, "customers kept × 12 × yearly value")]
for i, (lab, f, fmt, how) in enumerate(RES, start=14):
    put(ws, f"B{i}", lab, F(bold=True), border=BOT)
    put(ws, f"C{i}", f, F(bold=True, color="2A78D6"), fmt, border=BOT)
    put(ws, f"D{i}", how, F(color=MUTED), border=BOT)
r = 23
put(ws, f"B{r}", "By driver, per month", F(size=12, bold=True)); r += 1
header(ws, r, 2, ["Driver", "Share", "Contacts", "Cost", "After fixes"]); r += 1
for i, k in enumerate(ORDER):
    pr = P0 + i
    put(ws, f"B{r}", DRV[k]["label"], F(bold=k in S["top3"]), border=BOT)
    put(ws, f"C{r}", f"=Pareto!E{pr}", LINK, PCT1, border=BOT)
    put(ws, f"D{r}", f"=$C$14*C{r}", F(), INT, border=BOT)
    put(ws, f"E{r}", f"=D{r}*inp_cost", F(), RS, border=BOT)
    put(ws, f"F{r}", f'=IF(Pareto!K{pr}="Yes",D{r}*(1-inp_cut),D{r})', F(), INT, border=BOT)
    r += 1
put(ws, f"B{r}", "Total", F(bold=True))
for col, fmt in (("C", PCT0), ("D", INT), ("E", RS), ("F", INT)):
    put(ws, f"{col}{r}", f"=SUM({col}{r - len(ORDER)}:{col}{r - 1})", F(bold=True), fmt)
put(ws, f"B{r + 2}", "Caveat: the driver mix comes from reviews, which over-weight severe problems. Real ticket data would replace it in week 1.", F(italic=True, color=MUTED))
widths(ws, {"B": 34, "C": 14, "D": 52, "E": 14, "F": 14})

# ---------------------------------------------------------------- Fixes
ws = ws_fix
title(ws, "First three fixes, and how I'd measure them", "One fix per top driver. Each has an owner, one metric, a target and a test.")
header(ws, 4, 2, ["Fix", "Driver", "Owner", "What changes", "Metric", "Target", "How I'd measure it"])
for i, f in enumerate(S["fixes"], start=5):
    for j, v in enumerate([f["name"], DRV[f["driver"]]["label"], f["owner"], f["what"], f["metric"], f["target"], f["measure"]], start=2):
        c = ws.cell(row=i, column=j, value=v); c.font = F(bold=j == 2); c.alignment = WRAP; c.border = BOT
    ws.row_dimensions[i].height = 75
r = 5 + len(S["fixes"]) + 1
put(ws, f"B{r}", "First 30 days", F(size=12, bold=True)); r += 1
for x in S["plan30"]:
    put(ws, f"B{r}", "•", F(color=MUTED)); put(ws, f"C{r}", x, F(), align=WRAP); ws.merge_cells(f"C{r}:H{r}"); r += 1
widths(ws, {"B": 26, "C": 22, "D": 16, "E": 40, "F": 22, "G": 22, "H": 44})

# ---------------------------------------------------------------- Readout
ws = ws_read
title(ws, "One-page readout", S["tR"])
r = 4
for head_, key in (("Problem", "problem"), ("Root cause", "root"), ("Impact", "impact"), ("Action", "action")):
    put(ws, f"B{r}", head_, F(size=12, bold=True, color="2A78D6")); r += 1
    for x in S["readout"][key]:
        put(ws, f"B{r}", "•", F(color=MUTED)); put(ws, f"C{r}", x, F(), align=WRAP); ws.merge_cells(f"C{r}:J{r}")
        ws.row_dimensions[r].height = 30; r += 1
    r += 1
put(ws, f"B{r}", S["readout"]["caveat"], F(italic=True, color=MUTED), align=WRAP); ws.merge_cells(f"B{r}:J{r}"); ws.row_dimensions[r].height = 30
widths(ws, {"B": 4, "C": 14, "D": 14, "E": 14, "F": 14, "G": 14, "H": 14, "I": 14, "J": 14})
ws.page_setup.orientation = "portrait"; ws.page_setup.fitToWidth = 1; ws.sheet_properties.pageSetUpPr.fitToPage = True

# ---------------------------------------------------------------- Benchmark
ws = ws_ben
title(ws, "Benchmark: Urban Company", f"Same codebook on Urban Company's {D['uc']['n']} most recent App Store reviews. Urban Company covers all home services.")
put(ws, "B4", "Urban Company complaints", F(bold=True)); put(ws, "D4", '=COUNTA(u_primary)-COUNTIF(u_primary,"praise")', F(bold=True), INT)
name("u_comp", "Benchmark!$D$4")
header(ws, 6, 2, ["Driver key", "Driver", "Yes Madam", "Urban Company", "Gap (pts)"])
for i, k in enumerate(ORDER, start=7):
    put(ws, f"B{i}", k, F(color=MUTED), border=BOT)
    put(ws, f"C{i}", DRV[k]["label"], F(bold=k in S["top3"]), border=BOT)
    put(ws, f"D{i}", f"=COUNTIF(r_primary,B{i})/n_comp", F(), PCT1, border=BOT)
    put(ws, f"E{i}", f"=COUNTIF(u_primary,B{i})/u_comp", F(), PCT1, border=BOT)
    put(ws, f"F{i}", f"=(D{i}-E{i})*100", F(bold=True), '+0.0;-0.0;0.0', border=BOT)
BL = 6 + len(ORDER)
ws.conditional_formatting.add(f"F7:F{BL}", ColorScaleRule(start_type="num", start_value=-10, start_color="6DA7EC", mid_type="num", mid_value=0, mid_color="FFFFFF", end_type="num", end_value=10, end_color="E66A63"))
put(ws, f"B{BL + 2}", "Contacted support (share of complaints)", F()); put(ws, f"D{BL + 2}", '=COUNTIF(r_contact,"yes")/n_comp', F(), PCT0); put(ws, f"E{BL + 2}", '=COUNTIF(u_contact,"yes")/u_comp', F(), PCT0)
put(ws, f"B{BL + 3}", "High severity", F()); put(ws, f"D{BL + 3}", '=COUNTIF(r_sev,"high")/n_comp', F(), PCT0); put(ws, f"E{BL + 3}", '=COUNTIF(u_sev,"high")/u_comp', F(), PCT0)
put(ws, f"B{BL + 4}", "Say they'll leave", F()); put(ws, f"D{BL + 4}", '=COUNTIF(r_churn,"yes")/n_comp', F(), PCT0); put(ws, f"E{BL + 4}", '=COUNTIF(u_churn,"yes")/u_comp', F(), PCT0)
bc = BarChart(); bc.type = "bar"; bc.title = "Share of complaints by driver"; bc.height, bc.width = 9, 15
bc.add_data(Reference(ws, min_col=4, max_col=5, min_row=6, max_row=BL), titles_from_data=True)
bc.set_categories(Reference(ws, min_col=3, min_row=7, max_row=BL)); bc.x_axis.scaling.orientation = "maxMin"; bc.y_axis.majorGridlines = None
bc.series[0].graphicalProperties.solidFill = "2A78D6"; bc.series[1].graphicalProperties.solidFill = "EB6834"; bc.legend.position = "b"
ws.add_chart(bc, "H6")
widths(ws, {"B": 22, "C": 28, "D": 12, "E": 14, "F": 10})

# ---------------------------------------------------------------- Trends
ws = ws_tr
title(ws, "Trends", "Complaint reviews by month and driver, and app complaints by app version.")
months = sorted({x["date"][:7] for x in reviews})
header(ws, 4, 2, ["Driver"] + months + ["Total"])
for i, k in enumerate(ORDER, start=5):
    put(ws, f"B{i}", DRV[k]["label"], F(bold=k in S["top3"]), border=BOT)
    for j, m in enumerate(months):
        c = ws.cell(row=i, column=3 + j, value=f'=COUNTIFS(r_primary,"{k}",r_month,"{m}")'); c.font = F(); c.border = BOT; c.alignment = CENTER
    tc = ws.cell(row=i, column=3 + len(months), value=f"=SUM({ws.cell(row=i, column=3).coordinate}:{ws.cell(row=i, column=2 + len(months)).coordinate})")
    tc.font = F(bold=True); tc.alignment = CENTER
TL = 4 + len(ORDER)
put(ws, f"B{TL + 1}", "All complaints", F(bold=True))
for j in range(len(months) + 1):
    col = ws.cell(row=5, column=3 + j).column_letter
    c = ws.cell(row=TL + 1, column=3 + j, value=f"=SUM({col}5:{col}{TL})"); c.font = F(bold=True); c.alignment = CENTER
put(ws, f"B{TL + 2}", "All reviews", F(color=MUTED))
for j, m in enumerate(months):
    c = ws.cell(row=TL + 2, column=3 + j, value=f'=COUNTIF(r_month,"{m}")'); c.font = F(color=MUTED); c.alignment = CENTER
ws.conditional_formatting.add(f"C5:{ws.cell(row=TL, column=2 + len(months)).coordinate}", ColorScaleRule(start_type="num", start_value=0, start_color="FFFFFF", end_type="max", end_color="6DA7EC"))
put(ws, f"B{TL + 3}", f"{months[0]} starts on {M['from']}; {months[-1]} runs to {M['to']}. Both are part months.", F(italic=True, color=MUTED))
v0 = TL + 6
put(ws, f"B{v0 - 1}", "App complaints by app version", F(size=12, bold=True))
header(ws, v0, 2, ["Version", "Reviews", "App complaints", "Share"])
vers = sorted({x["version"] for x in reviews}, key=lambda v: [int(p) if p.isdigit() else 0 for p in v.split(".")], reverse=True)
for i, v in enumerate(vers, start=v0 + 1):
    put(ws, f"B{i}", v, F(bold=True), border=BOT)
    put(ws, f"C{i}", f'=COUNTIF(r_ver,B{i})', F(), INT, border=BOT)
    put(ws, f"D{i}", f'=COUNTIFS(r_ver,B{i},r_primary,"app")', F(), INT, border=BOT)
    put(ws, f"E{i}", f"=IFERROR(D{i}/C{i},0)", F(), PCT0, border=BOT)
widths(ws, {"B": 28, **{ws.cell(row=4, column=3 + j).column_letter: 11 for j in range(len(months) + 1)}})

# ---------------------------------------------------------------- Reliability
ws = ws_rel
title(ws, "Tagging reliability", "Every review was tagged in two independent passes with the same codebook. Agreement and Cohen's kappa are computed live from the Reviews tab.")
put(ws, "B4", "Reviews double-tagged", F(bold=True)); put(ws, "E4", '=SUMPRODUCT(--(r_tagA<>""),--(r_tagB<>""))', F(bold=True), INT)
put(ws, "B5", "Same primary driver", F(bold=True)); put(ws, "E5", "=SUMPRODUCT(--(r_tagA=r_tagB),--(r_tagA<>\"\"))", F(bold=True), INT)
put(ws, "B6", "Observed agreement (po)", F(bold=True)); put(ws, "E6", "=E5/E4", F(bold=True, color="2A78D6"), PCT1)
header(ws, 8, 2, ["Driver", "Tagger A count", "Tagger B count", "Chance agreement"])
for i, k in enumerate(ORDER + ["praise"], start=9):
    put(ws, f"B{i}", k, F(), border=BOT)
    put(ws, f"C{i}", f'=COUNTIF(r_tagA,B{i})', F(), INT, border=BOT)
    put(ws, f"D{i}", f'=COUNTIF(r_tagB,B{i})', F(), INT, border=BOT)
    put(ws, f"E{i}", f"=(C{i}/$E$4)*(D{i}/$E$4)", F(), "0.0000", border=BOT)
RL = 8 + len(ORDER) + 1
put(ws, f"B{RL + 1}", "Chance agreement (pe)", F(bold=True)); put(ws, f"E{RL + 1}", f"=SUM(E9:E{RL})", F(bold=True), "0.000")
put(ws, f"B{RL + 2}", "Cohen's kappa = (po − pe) ÷ (1 − pe)", F(bold=True)); put(ws, f"E{RL + 2}", f"=(E6-E{RL + 1})/(1-E{RL + 1})", F(bold=True, color="2A78D6"), "0.00")
put(ws, f"B{RL + 3}", "Reading: above 0.6 is substantial agreement, above 0.8 near-perfect. Disagreements were settled by a third read against the codebook (Tie-break note column on Reviews).", F(italic=True, color=MUTED))
put(ws, f"B{RL + 4}", "Disagreements settled", F(bold=True)); put(ws, f"E{RL + 4}", "=E4-E5", F(bold=True), INT)
widths(ws, {"B": 30, "C": 14, "D": 14, "E": 16})

# ---------------------------------------------------------------- Codebook
ws = ws_code
title(ws, "Codebook", "One primary driver per review: the reason that customer would contact support.")
header(ws, 4, 2, ["Key", "Driver", "What counts", "Subtags"])
for i, (k, v) in enumerate(DRV.items(), start=5):
    subs = sorted({x["subtag"] for x in reviews if x["primary"] == k})
    for j, val in enumerate([k, v["label"], v["desc"], ", ".join(SUB.get(s, s) for s in subs)], start=2):
        c = ws.cell(row=i, column=j, value=val); c.font = F(bold=j == 3); c.alignment = WRAP; c.border = BOT
    ws.row_dimensions[i].height = 32
r = 6 + len(DRV)
for t in ["Rule 1: support is the driver only when support itself is the whole complaint; otherwise the underlying problem is the driver and support is secondary.",
          "Rule 2: a burn or rash blamed on technique is Service quality; blamed on the product is Products used.",
          "Rule 3: vanishing offers, unusable coupons and fake promo notifications are Price & offer clarity.",
          "Rule 4: a mixed review counts its complaint. A vague 'worst app' with no detail is Other."]:
    put(ws, f"B{r}", t, F(), align=WRAP); ws.merge_cells(f"B{r}:E{r}"); ws.row_dimensions[r].height = 28; r += 1
widths(ws, {"B": 22, "C": 26, "D": 60, "E": 60})

# ---------------------------------------------------------------- JD map
ws = ws_jd
title(ws, "Built for this role", "Each JD line, where it is in this teardown, and where I've done it before.")
header(ws, 4, 2, ["The JD asks for", "In this teardown", "Where I've done it before"])
for i, row in enumerate(S["jd"], start=5):
    for j, v in enumerate(row, start=2):
        c = ws.cell(row=i, column=j, value=v); c.font = F(bold=j == 2); c.alignment = WRAP; c.border = BOT
    ws.row_dimensions[i].height = 44
widths(ws, {"B": 30, "C": 60, "D": 60})

# ---------------------------------------------------------------- Cover
ws = ws_cover
put(ws, "B2", "Contact-driver teardown · Yes Madam", F(size=22, bold=True, color=INK))
put(ws, "B3", f"{M['n']} real App Store reviews ({M['from']} to {M['to']}), tagged into contact drivers", F(size=12, color=MUTED))
put(ws, "B4", NOTE, F(bold=True, color="006100"), fill=GREEN)
for col in "CDE":
    ws[f"{col}4"].fill = GREEN
put(ws, "B6", "Top 3 drivers' share of complaints", F(bold=True, color=MUTED))
put(ws, "B7", "=top3_share", F(size=26, bold=True, color="2A78D6"), PCT0)
put(ws, "C7", " / ".join(DRV[k]["label"] for k in S["top3"]), F(size=11))
put(ws, "B9", "How to use", F(size=12, bold=True))
for i, t in enumerate(["1. Reviews is the source: every row is one real review with its tags. Change a tag and every tab recalculates.",
                       "2. Pareto and Top Drivers count the tags with COUNTIFS. Impact Model turns them into contacts and rupees: change the yellow assumptions.",
                       "3. Reliability shows two independent taggers' agreement and Cohen's kappa, computed live."], start=10):
    put(ws, f"B{i}", t, F())
put(ws, "B14", "Tabs", F(size=12, bold=True))
TABS = [("Pareto", "Complaint drivers, share and running share"), ("Top Drivers", "Subtags, severity and quotes for the top 3"),
        ("Five Whys", "Root-cause chains, evidence vs hypothesis"), ("Impact Model", "Contacts and rupees, with editable assumptions"),
        ("Fixes", "First three fixes, owner, metric, target, test"), ("Readout", "One page: problem, root cause, impact, action"),
        ("Benchmark", "Same method on Urban Company"), ("Trends", "By month and by app version"), ("Reliability", "Agreement and kappa"),
        ("Codebook", "Driver definitions and rules"), ("JD Map", "JD × this teardown × my track record"),
        ("Reviews", "All 500 reviews with tags (names and IDs removed)"), ("UC Reviews", "Urban Company tags for the benchmark")]
for i, (t, d) in enumerate(TABS, start=15):
    c = put(ws, f"B{i}", t, F(color="2A78D6", underline="single")); c.hyperlink = f"#'{t}'!A1"
    put(ws, f"C{i}", d, F(color=MUTED))
put(ws, f"B{16 + len(TABS)}", "Bias: reviews skew negative, iOS-only, and are not ticket data. Use them for the mix of problems, not their rate.", F(italic=True, color=MUTED))
widths(ws, {"A": 3, "B": 30, "C": 90})

for w in wb.worksheets:
    w.page_setup.orientation = w.page_setup.orientation or "landscape"
    w.page_setup.fitToWidth = 1
    w.page_setup.fitToHeight = 0
    w.sheet_properties.pageSetUpPr.fitToPage = True
wb.active = 0
wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print("saved", OUT)
