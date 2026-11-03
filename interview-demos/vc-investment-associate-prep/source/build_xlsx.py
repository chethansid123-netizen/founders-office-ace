#!/usr/bin/env python3
"""Build the VC Investment Associate interview-prep workbook.

Usage:  python3 build_xlsx.py ../VC-Investment-Associate-Prep.xlsx
Then recalculate (Excel does it on open; for LibreOffice use the xlsx skill's recalc.py).
"""
import math
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from content_glossary import GLOSSARY
from content_interview import (CASE_FRAMEWORK, CASES, CHEAT_SHEET, DD_CHECKLIST, DEAL_PROCESS, DONT_DO, EXITS,
                               FIRM_RESEARCH, FOUNDER_SIGNALS, FOUNDER_TYPES, FUND_LIFECYCLE, IC_MEMO, INTERVIEW_FLOW,
                               MONEY_FLOW, PLAYERS, QA, QUESTIONS_TO_ASK, REFERENCE_QS, SCORECARD, STAGES, STUDY_PLAN,
                               TERM_SHEET, USE_OF_FUNDS)
from content_sectors import (CONSUMER_LENS, DEEPTECH_LENS, HEALTH_LENS, HEALTH_SEGMENTS, INDIA_LANDSCAPE, SECTORS,
                             THEMES, TRL)

# ------------------------------------------------------------------ styles
FONT = "Arial"
NAVY = "1F3864"
BLUE_IN = "0000FF"
GREEN_LINK = "008000"
GREY = "404040"


def font(bold=False, color="000000", size=10, italic=False, underline=None):
    return Font(name=FONT, size=size, bold=bold, color=color, italic=italic, underline=underline)


def fill(c):
    return PatternFill("solid", fgColor=c)


HDR = fill("1F3864")
SECF = fill("D6E4F0")
ALT = fill("F5F8FC")
INP = fill("FFFF00")
KEY = fill("E2EFDA")
NOTEF = fill("FFF8E1")
thin = Side(style="thin", color="C9D3E0")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
TOPWRAP = Alignment(wrap_text=True, vertical="top")

INR = '"₹"#,##0;("₹"#,##0);"-"'
INR2 = '"₹"#,##0.00;("₹"#,##0.00);"-"'
LAKH = '"₹"#,##0.00" L";("₹"#,##0.00" L");"-"'
CR = '"₹"#,##0.00" cr";("₹"#,##0.00" cr");"-"'
CR0 = '"₹"#,##0" cr";("₹"#,##0" cr");"-"'
USDM = '"$"#,##0.0"M";("$"#,##0.0"M");"-"'
PCT = '0.0%;(0.0%);"-"'
MULT = '0.00"x";(0.00"x");"-"'
MULT1 = '0.0"x";(0.0"x");"-"'
NUM = '#,##0;(#,##0);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
NUM2 = '#,##0.00;(#,##0.00);"-"'
MONTHS = '0.0" months";(0.0" months");"-"'
DAYS = '0" days";(0" days");"-"'
YEARS = '0" years"'
GEN = "General"

# ------------------------------------------------------------------ helpers
REG = {}  # key -> (sheet title, coordinate)


def ref(key, sheet):
    sh, coord = REG[key]
    m = re.match(r"([A-Z]+)(\d+)$", coord)
    a = f"${m.group(1)}${m.group(2)}"
    return a if sh == sheet else f"'{sh}'!{a}"


def fx(s, sheet):
    return re.sub(r"\{(\w+)\}", lambda m: ref(m.group(1), sheet), s)


def width(ws, c):
    return ws.column_dimensions[get_column_letter(c)].width or 8.43


def nlines(text, w):
    cpl = max(1.0, w * 1.18)
    return sum(max(1, math.ceil(len(p) / cpl)) for p in str(text).split("\n"))


def fit(ws, r, c1, c2, minh=15.0):
    lines = 1
    for c in range(c1, c2 + 1):
        v = ws.cell(r, c).value
        if v is None or (isinstance(v, str) and v.startswith("=")):
            continue
        lines = max(lines, nlines(v, width(ws, c)))
    ws.row_dimensions[r].height = max(minh, 12.8 * lines + 3)


def safe(v):
    if isinstance(v, str) and v.startswith("="):
        return "Excel: " + v[1:]
    return v


def new_sheet(wb, name, title, subtitle, widths, tab=None):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.cell(1, 2, title).font = font(True, NAVY, 15)
    ws.row_dimensions[1].height = 24
    ws.cell(2, 2, subtitle).font = font(False, "595959", 10, True)
    if name != "00 Start Here":
        b = ws.cell(3, 2, "◀ Back to contents")
        b.hyperlink = "#'00 Start Here'!A1"
        b.font = font(False, "0563C1", 9, underline="single")
    if tab:
        ws.sheet_properties.tabColor = tab
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return ws


def sec(ws, r, text, c1=2, c2=6):
    for c in range(c1, c2 + 1):
        ws.cell(r, c).fill = SECF
    ws.cell(r, c1, text).font = font(True, NAVY, 12)
    ws.row_dimensions[r].height = 20
    return r + 1


def note(ws, r, text, c1=2, c2=6, f=NOTEF, bold=False, color="000000", italic=False):
    if c2 > c1:
        ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
    c = ws.cell(r, c1, text)
    c.font = font(bold, color, italic=italic)
    c.alignment = TOPWRAP
    if f is not None:
        c.fill = f
    w = sum(width(ws, k) for k in range(c1, c2 + 1))
    ws.row_dimensions[r].height = max(15, 12.8 * nlines(text, w) + 4)
    return r + 1


def header(ws, r, labels, c1=2):
    for j, h in enumerate(labels):
        c = ws.cell(r, c1 + j, h)
        c.font = font(True, "FFFFFF")
        c.fill = HDR
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = BOX
    fit(ws, r, c1, c1 + len(labels) - 1, minh=18)
    return r + 1


def table(ws, r, headers, rows, c1=2, bold_first=True, input_cols=(), zebra=True):
    hdr_row = r
    r = header(ws, r, headers, c1)
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = ws.cell(r, c1 + j, safe(v))
            c.font = font(bold_first and j == 0)
            c.alignment = TOPWRAP
            c.border = BOX
            if zebra and i % 2 == 1:
                c.fill = ALT
            if j in input_cols:
                c.fill = INP
                c.font = font(False, BLUE_IN)
        fit(ws, r, c1, c1 + len(headers) - 1)
        r += 1
    return r, hdr_row


def setv(ws, r, c, val, fmt=None, key=None, inp=False, result=False, align=None):
    cell = ws.cell(r, c)
    is_formula = isinstance(val, str) and val.startswith("=")
    if is_formula:
        f = fx(val, ws.title)
        cell.value = f
        cell.font = font(result, GREEN_LINK if "!" in f else "000000")
    else:
        cell.value = val
        cell.font = font(False, BLUE_IN) if inp else font(result)
        if inp:
            cell.fill = INP
    if result:
        cell.fill = KEY
    if fmt:
        cell.number_format = fmt
    cell.border = BOX
    if align is None:
        align = "left" if (isinstance(val, str) and not is_formula) else "right"
    cell.alignment = Alignment(horizontal=align, vertical="top", wrap_text=(align == "left"))
    if key:
        REG[key] = (ws.title, f"{get_column_letter(c)}{r}")
    return cell


def crow(ws, r, key, label, val, fmt, how="", note_="", inp=False, result=False, wide=None, align=None):
    """One calculator row: label (B), value (C), then either how (D) + meaning (E), or one merged note D..wide."""
    lab = ws.cell(r, 2, label)
    lab.font = font(result)
    lab.alignment = TOPWRAP
    lab.border = BOX
    if result:
        lab.fill = KEY
    setv(ws, r, 3, val, fmt, key, inp, result, align)
    if fmt == GEN and isinstance(val, str) and val.startswith("="):
        # text verdict: give it the full row width so it is never clipped
        end = wide or 4
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=end)
        ws.cell(r, 3).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        ws.cell(r, 3).font = font(True)
        if not wide:
            x = ws.cell(r, 5, (how + (" — " if how and note_ else "") + note_) if (how or note_) else "")
            x.font = font(False, GREY)
            x.alignment = TOPWRAP
            x.border = BOX
        ws.row_dimensions[r].height = max(15, 12.8 * nlines(label, width(ws, 2)) + 3)
        return r + 1
    if wide:
        text = how if not note_ else (how + (" — " if how else "") + note_)
        if wide > 4:
            ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=wide)
        c = ws.cell(r, 4, text)
        c.font = font(False, GREY)
        c.alignment = TOPWRAP
        w = sum(width(ws, k) for k in range(4, wide + 1))
        lines = max(nlines(text, w) if text else 1, nlines(label, width(ws, 2)))
        ws.row_dimensions[r].height = max(15, 12.8 * lines + 3)
    else:
        for c, t in ((4, how), (5, note_)):
            x = ws.cell(r, c, t)
            x.font = font(False, GREY)
            x.alignment = TOPWRAP
            x.border = BOX
        fit(ws, r, 2, 5)
    return r + 1


def block(ws, r, title, rows, wide=None, c2=None):
    """rows: (key, label, value, fmt, how, note, is_input[, is_result])"""
    r = sec(ws, r, title, 2, c2 or (wide or 5))
    if not wide:
        r = header(ws, r, ["Item", "Value", "Formula / how it is calculated", "What it means / source"])
    for row in rows:
        key, label, val, fmt, how, nt = row[:6]
        inp = row[6] if len(row) > 6 else False
        res = row[7] if len(row) > 7 else False
        r = crow(ws, r, key, label, val, fmt, how, nt, inp, res, wide)
    return r + 1


ILL = "Illustrative assumption — change it"

# ------------------------------------------------------------------ sheets
CONTENTS = [
    ("00 Start Here", "How to use this file, the likely interview flow, tonight's study plan, night-before cheat sheet", "Read first"),
    ("01 How VC Works", "LPs, GPs, fund structure, stages & round sizes in India, fund life, exits, corporate VC vs independent VC", "Foundation"),
    ("02 Glossary", f"{len(GLOSSARY)} terms: ARR, MRR, ROI, CAC, LTV, NRR, burn, IRR, TVPI, CCPS, TRL, rNPV … each with formula, example, benchmark and why VCs care", "Learn every term"),
    ("03 Formula Lab", "Live calculator for every key formula — change the yellow cells and watch results move", "Practise numbers"),
    ("04 Consumer", "Consumer / D2C worked example: per-order CM1-CM2-CM3, channel economics, cohorts, LTV:CAC, P&L, working capital, evaluation lens", "Consumption deep-dive"),
    ("05 Deep Tech", "Deep tech worked example (drones): TRL ladder, milestone funding & dilution, learning-curve unit economics, risk-adjusted valuation, grants, lens", "Deep tech deep-dive"),
    ("06 Healthcare", "Healthcare segment map, diagnostic-centre unit economics, medtech rNPV, regulatory pathways, clinical success rates, lens", "Healthcare deep-dive"),
    ("07 Sector Playbook", f"{len(SECTORS)} sectors — one-line how each runs, how it makes money, metrics, good vs red flags, Indian examples, how to evaluate", "Every industry in one line"),
    ("08 Founder Evaluation", "Weighted founder/startup scorecard (live), founder signals, founder types incl. manufacturing founders, reference-check questions", "Judging founders"),
    ("09 Manufacturing", "5-year plant model: utilisation, EBITDA, ROCE, break-even, payback + manufacturing diligence checklist", "Manufacturing founders"),
    ("10 Valuation", "VC method, comparable companies, DCF, Scorecard, Berkus, First Chicago — all live", "How to value a startup"),
    ("11 Cap Table", "Seed + Series A cap table with option-pool shuffle, SAFE conversion, dilution chain", "Ownership & dilution"),
    ("12 Waterfall", "Liquidation preference: 1x non-participating vs participating vs capped, at 7 exit values", "Who gets paid at exit"),
    ("13 Term Sheet", "Every term-sheet clause decoded + live anti-dilution example", "Deal terms"),
    ("14 Fund Economics", "Fees, reserves, portfolio construction, power-law outcomes, carry, LP waterfall, J-curve & IRR, MOIC→IRR grid", "How the fund makes money"),
    ("15 Financial Statements", "Linked P&L, balance sheet, cash flow for a startup + how to read them + red flags", "Reading financials"),
    ("16 Deal Process", "10-step deal process with the associate's job at each step, how money flows LP → startup → exit, use of funds by sector", "What you'll do daily"),
    ("17 Market Sizing", "TAM / SAM / SOM top-down and bottom-up (live) + venture-scale check + guesstimate method", "Market sizing questions"),
    ("18 India Landscape", "Indian VC funds by focus, government programmes, data sources, 2026 themes", "Market awareness"),
    ("19 Interview Q&A", f"{len(QA)} likely questions with what's being tested, how to structure and sample answers", "Practise out loud"),
    ("20 Mini Cases", "6-step case framework + 5 worked cases (consumer, deep tech, healthcare, SaaS, manufacturing)", "Case questions"),
    ("21 IC Memo", "Investment committee memo template with a worked example column and a blank column for you", "Written thinking"),
    ("22 DD Checklist", "Due-diligence checklist with status dropdowns", "Diligence"),
    ("23 Firm & Questions", "Fill-in research sheet for the firm and Chandru + smart questions to ask + what not to do", "Do tonight"),
]


def sheet_start(wb):
    ws = new_sheet(wb, "00 Start Here", "VC Investment Associate — Interview Prep Workbook",
                   "People Moves — general round with the CEO (Chandru). Everything in one file: concepts, live formulas, sector examples, cases and Q&A.",
                   [2, 26, 70, 60, 4], tab=NAVY)
    r = 4
    r = note(ws, r, "Firm: People Moves — new venture-capital arm, CEO Chandru. A web search found no public coverage of the firm "
                    "or its portfolio yet (likely new or private). Tonight, check their website, LinkedIn page and Chandru's LinkedIn, "
                    "and fill in tab 23 (Firm & Questions). If People Moves has an existing business (e.g., in people/talent), read "
                    "the 'corporate VC arm' table in tab 01 — it will shape his questions.", 2, 4,
             bold=True)
    r += 1
    r = sec(ws, r, "How to read this workbook", 2, 4)
    legend = [
        ("Blue text on yellow", "An input or assumption. Change it and every result recalculates."),
        ("Black number", "A formula. Don't type over it."),
        ("Green number", "A formula pulling a value from another tab."),
        ("Green-shaded row", "A key result to remember."),
        ("₹ L / ₹ cr", "Lakh (1,00,000) and crore (1,00,00,000). $1M ≈ ₹8.8 cr at ₹88/$ (rate is an input in tab 03)."),
        ("Examples", "Companies in worked examples are fictional and all numbers are illustrative. Benchmarks are rules of thumb that vary by stage, sector and market cycle."),
    ]
    sample = ws.cell(r, 2)
    r, _ = table(ws, r, ["Style", "Meaning"], legend, c1=2)
    ws.cell(r - 6, 2).font = font(True, BLUE_IN)
    ws.cell(r - 6, 2).fill = INP
    ws.cell(r - 4, 2).font = font(True, GREEN_LINK)
    ws.cell(r - 3, 2).fill = KEY
    del sample
    r += 1
    r = sec(ws, r, "Contents (click a tab name to jump)", 2, 4)
    r = header(ws, r, ["Tab", "What's inside", "Use it for"])
    for i, (name, what, use) in enumerate(CONTENTS):
        c = ws.cell(r, 2, name)
        c.hyperlink = f"#'{name}'!A1"
        c.font = font(True, "0563C1", underline="single")
        c.border = BOX
        c.alignment = TOPWRAP
        for j, t in enumerate((what, use), start=3):
            x = ws.cell(r, j, t)
            x.font = font()
            x.alignment = TOPWRAP
            x.border = BOX
            if i % 2:
                x.fill = ALT
        fit(ws, r, 2, 4)
        r += 1
    r += 1
    r = sec(ws, r, "What an Investment Associate does", 2, 4)
    duties = [
        ("Sourcing", "Find startups through networks, accelerators, cold outreach, events and thesis-led market maps; log them in the CRM."),
        ("Screening", "Read decks fast, check fit with the fund's thesis, stage and cheque size, flag red flags."),
        ("Analysis", "Build cohort, unit-economics and market-sizing analysis; compare with peers; model valuation and returns."),
        ("Diligence", "Run customer calls, reference checks, data-room review; coordinate lawyers and auditors."),
        ("IC memos", "Write the investment memo and defend it with the partners / investment committee."),
        ("Portfolio support", "Track monthly MIS, prepare board material, help with hiring, customers and the next round."),
        ("Fund building (new arm)", "Help shape the thesis, set up processes, templates and dashboards, and build the brand in the ecosystem."),
    ]
    r, _ = table(ws, r, ["Area", "What you do"], duties, c1=2)
    r += 1
    r = sec(ws, r, "How tomorrow's general round will probably run (about 45–60 minutes)", 2, 4)
    r, _ = table(ws, r, ["Time", "What he'll cover", "What he's testing / how to prepare"],
                 [(a, b, f"{c} {d}") for a, b, c, d in INTERVIEW_FLOW], c1=2)
    r += 1
    r = sec(ws, r, "Tonight's study plan (about 6 hours)", 2, 4)
    r, _ = table(ws, r, ["When", "Tabs", "How"], STUDY_PLAN, c1=2)
    r += 1
    r = sec(ws, r, "Night-before cheat sheet (read this in the morning)", 2, 4)
    for i, line in enumerate(CHEAT_SHEET, start=1):
        r = note(ws, r, f"{i}. {line}", 2, 4, f=None)
    r += 1
    r = sec(ws, r, "Avoid these", 2, 4)
    for line in DONT_DO:
        r = note(ws, r, "✗ " + line, 2, 4, f=None)
    ws.freeze_panes = "A4"


def sheet_vc(wb):
    ws = new_sheet(wb, "01 How VC Works", "How venture capital works", "Who's who, where the money comes from, stages, fund life and exits.",
                   [2, 30, 44, 34, 40, 40, 36], tab="2E75B6")
    r = 5
    r = sec(ws, r, "The players", 2, 5)
    r, _ = table(ws, r, ["Player", "Role", "Who they are", "What they want"], PLAYERS)
    r += 1
    r = sec(ws, r, "How money flows: LP → fund → startup → exit → back to LPs", 2, 4)
    r, _ = table(ws, r, ["Step", "What happens", "Detail"], MONEY_FLOW)
    r = note(ws, r, "Fund economics in one line: the GP charges ~2% a year as management fee (pays salaries and costs) and keeps "
                    "~20% of profits as carried interest, usually only after LPs get their capital back plus a hurdle (often 8%). "
                    "See tab 14 for the live model.", 2, 5)
    r += 1
    r = sec(ws, r, "Startup stages in India (approximate, rule-of-thumb ranges; they move with the market)", 2, 7)
    r, _ = table(ws, r, ["Stage", "What the company has", "Typical round size", "Typical post-money", "What investors look for", "Who invests"], STAGES)
    r += 1
    r = sec(ws, r, "Fund life (typical 10-year closed-end fund)", 2, 4)
    r, _ = table(ws, r, ["Years", "Phase", "What happens"], FUND_LIFECYCLE)
    r += 1
    r = sec(ws, r, "Exit routes — how a VC finally makes money", 2, 4)
    r, _ = table(ws, r, ["Exit", "How it works", "Indian examples"], EXITS)
    r += 1
    r = sec(ws, r, "Independent VC vs corporate / family-office VC arm (relevant if this is a 'new arm')", 2, 4)
    cvc = [
        ("Objective", "Financial returns only (3x+ net to LPs)", "Financial returns + strategic value (new tech, partnerships, market insight)"),
        ("Money source", "Outside LPs; raised every 3–4 years", "Parent company / family balance sheet (evergreen) or a fund with the parent as anchor LP"),
        ("Decision-making", "Partners + investment committee", "Investment committee often includes parent-company executives"),
        ("Value-add to founders", "Network, hiring, next-round support", "Distribution, customers, supply chain, brand of the parent"),
        ("Risks", "Fundraising pressure, fund cycle", "Conflicts of interest, slower decisions, strategy changes at the parent, founder worries about data sharing"),
        ("Time horizon", "10-year fund life", "Can be longer (evergreen) — useful for deep tech and healthcare"),
        ("What makes a good associate here", "Deal flow + analysis", "All of that + the ability to link startups to the parent's business units"),
    ]
    r, _ = table(ws, r, ["Dimension", "Independent VC fund", "Corporate / family-office VC arm"], cvc)
    r += 1
    r = sec(ws, r, "Key India regulations for a VC fund", 2, 4)
    regs = [
        ("SEBI (AIF) Regulations, 2012", "VC funds register as Category I (VC funds, angel funds) or Category II (PE, others) AIFs", "Minimum investor commitment ₹1 cr; minimum corpus ₹20 cr per scheme; manager/sponsor commitment 2.5% of corpus or ₹5 cr, whichever is lower"),
        ("FEMA / FDI rules", "Govern foreign money into Indian startups", "Issue price to non-residents ≥ fair value; sector caps; FC-GPR filing with RBI within 30 days"),
        ("Companies Act, 2013", "Private placement and share-issue rules", "Valuation reports, board/shareholder approvals, ROC filings (PAS-3)"),
        ("Income Tax Act", "Angel tax (Sec 56(2)(viib)) abolished from FY 2025-26", "Rule 11UA valuation still used; capital-gains rules on exit"),
        ("Sector regulators", "RBI (fintech), IRDAI (insurance), CDSCO (health), FSSAI (food), DGCA (drones), IN-SPACe (space)", "Licences can make or break a startup — always diligence them"),
    ]
    r, _ = table(ws, r, ["Rule", "What it covers", "Key points"], regs)


def sheet_glossary(wb):
    ws = new_sheet(wb, "02 Glossary", f"Glossary — {len(GLOSSARY)} terms you must know",
                   "Use the filter on the header row to study one category at a time. Examples are illustrative.",
                   [2, 6, 20, 24, 22, 40, 36, 32, 32, 34], tab="2E75B6")
    rows = [(i, *g[:1], *g[1:]) for i, g in enumerate(GLOSSARY, start=1)]
    rows = [(i, cat, term, full, mean, form, ex, bench, why) for (i, cat, term, full, mean, form, ex, bench, why) in rows]
    r, hdr = table(ws, 5, ["#", "Category", "Term", "Full form", "Simple meaning", "Formula", "Worked example", "Benchmark / rule of thumb", "Why a VC cares"],
                   rows, bold_first=False)
    for rr in range(hdr + 1, r):
        ws.cell(rr, 4).font = font(True)
    ws.freeze_panes = ws.cell(hdr + 1, 5)
    ws.auto_filter.ref = f"B{hdr}:J{r - 1}"


def sheet_lab(wb):
    ws = new_sheet(wb, "03 Formula Lab", "Formula Lab — every key formula, live",
                   "Change the yellow cells. Each result shows the formula in words and what it tells an investor.",
                   [2, 44, 18, 48, 58], tab="548235")
    r = 5
    r = block(ws, r, "A. Recurring revenue (SaaS)", [
        ("fl_cust", "Paying customers", 200, NUM, "Input", ILL, True),
        ("fl_fee", "Average monthly fee per customer (₹)", 25000, INR, "Input", ILL, True),
        ("fl_mrr", "MRR (₹ lakh)", "={fl_cust}*{fl_fee}/100000", LAKH, "Customers × monthly fee ÷ 1,00,000", "Predictable revenue every month", False, True),
        ("fl_arr", "ARR (₹ crore)", "={fl_mrr}*12/100", CR, "MRR × 12 (÷100 converts lakh to crore)", "Main valuation base for SaaS", False, True),
        ("fl_acv", "ACV — annual value per customer (₹ lakh)", "={fl_arr}*100/{fl_cust}", LAKH, "ARR ÷ customers", "Decides sales motion: self-serve vs inside vs field sales"),
    ])
    r = block(ws, r, "B. Retention — last 12 months, customers who were active a year ago", [
        ("fl_sarr", "Starting ARR from these customers (₹ cr)", 6.0, CR, "Input", ILL, True),
        ("fl_exp", "Expansion (upsell, more seats) (₹ cr)", 1.5, CR, "Input", ILL, True),
        ("fl_con", "Contraction (downgrades) (₹ cr)", 0.2, CR, "Input", ILL, True),
        ("fl_chm", "Churned (cancelled) (₹ cr)", 0.4, CR, "Input", ILL, True),
        ("fl_grr", "GRR — gross revenue retention", "=({fl_sarr}-{fl_con}-{fl_chm})/{fl_sarr}", PCT, "(Start − contraction − churn) ÷ Start", "Pure stickiness; max 100%. SMB 80–85%, enterprise 90%+", False, True),
        ("fl_nrr", "NRR — net revenue retention", "=({fl_sarr}+{fl_exp}-{fl_con}-{fl_chm})/{fl_sarr}", PCT, "(Start + expansion − contraction − churn) ÷ Start", ">100% = base grows by itself; >120% elite", False, True),
        ("fl_c0", "Customers at start of the month", 200, NUM, "Input", ILL, True),
        ("fl_lost", "Customers lost during the month", 6, NUM, "Input", ILL, True),
        ("fl_churn", "Monthly logo churn", "={fl_lost}/{fl_c0}", PCT, "Lost ÷ customers at start", "SMB SaaS 2–5%/month is common", False, True),
        ("fl_life", "Average customer lifetime (months)", "=1/{fl_churn}", MONTHS, "1 ÷ monthly churn", "3% churn ≈ 33 months"),
    ])
    r = block(ws, r, "C. CAC, LTV and payback", [
        ("fl_sm", "Sales & marketing spend this month (₹ lakh)", 60, LAKH, "Input", ILL, True),
        ("fl_new", "New customers won this month", 40, NUM, "Input", ILL, True),
        ("fl_cac", "CAC (₹)", "={fl_sm}*100000/{fl_new}", INR, "S&M spend ÷ new customers", "Cost to win one customer", False, True),
        ("fl_gm", "Gross margin %", 0.75, PCT, "Input", "SaaS usually 70–85%", True),
        ("fl_ltv", "LTV (₹)", "={fl_fee}*{fl_gm}/{fl_churn}", INR, "Monthly fee × gross margin ÷ monthly churn", "Gross profit over the customer's life", False, True),
        ("fl_ltvcac", "LTV : CAC", "={fl_ltv}/{fl_cac}", MULT1, "LTV ÷ CAC", ">3x healthy; <1x destroys value", False, True),
        ("fl_pay", "CAC payback (months)", "={fl_cac}/({fl_fee}*{fl_gm})", MONTHS, "CAC ÷ (monthly fee × gross margin)", "<12–18 months is good for SaaS", False, True),
        ("fl_v1", "Verdict", '=IF({fl_ltvcac}>=3,"Healthy (3x or more)",IF({fl_ltvcac}>=1,"Weak (1–3x)","Value-destroying (<1x)"))', GEN, "Rule of thumb", ""),
    ])
    r = block(ws, r, "D. Burn, runway and burn multiple", [
        ("fl_cash", "Cash in bank (₹ cr)", 16, CR, "Input", ILL, True),
        ("fl_out", "Monthly cash out (₹ cr)", 1.5, CR, "Input", ILL, True),
        ("fl_in", "Monthly cash in (₹ cr)", 0.7, CR, "Input", ILL, True),
        ("fl_burn", "Net burn per month (₹ cr)", "={fl_out}-{fl_in}", CR, "Cash out − cash in", "Gross burn = cash out only", False, True),
        ("fl_run", "Runway (months)", "={fl_cash}/{fl_burn}", MONTHS, "Cash ÷ net burn", "Raise with 18–24 months left; <6 months is danger", False, True),
        ("fl_nnarr", "Net new ARR added in last 12 months (₹ cr)", 8, CR, "Input", ILL, True),
        ("fl_bm", "Burn multiple", "={fl_burn}*12/{fl_nnarr}", MULT, "Annual net burn ÷ net new ARR", "<1x amazing, 1–1.5x good, >2x suspect", False, True),
        ("fl_v2", "Verdict", '=IF({fl_bm}<1,"Amazing",IF({fl_bm}<=1.5,"Good",IF({fl_bm}<=2,"OK","Suspect / bad")))', GEN, "Rule of thumb (David Sacks' scale)", ""),
    ])
    r = block(ws, r, "E. Rule of 40 and magic number (SaaS efficiency)", [
        ("fl_g", "Revenue growth YoY", 0.60, PCT, "Input", ILL, True),
        ("fl_m", "EBITDA (or FCF) margin", -0.15, PCT, "Input", ILL, True),
        ("fl_r40", "Rule of 40 score", "=({fl_g}+{fl_m})*100", NUM1, "(Growth % + margin %) × 100", "40 or more is healthy", False, True),
        ("fl_v3", "Verdict", '=IF({fl_r40}>=40,"Passes Rule of 40","Fails Rule of 40")', GEN, "", ""),
        ("fl_q1", "Revenue this quarter (₹ cr)", 3.0, CR, "Input", ILL, True),
        ("fl_q0", "Revenue last quarter (₹ cr)", 2.5, CR, "Input", ILL, True),
        ("fl_sm0", "Sales & marketing spend last quarter (₹ cr)", 2.0, CR, "Input", ILL, True),
        ("fl_magic", "Magic number", "=({fl_q1}-{fl_q0})*4/{fl_sm0}", MULT, "(Δ quarterly revenue × 4) ÷ last quarter's S&M", ">0.75 → spend more on sales; <0.5 → fix GTM", False, True),
        ("fl_v4", "Verdict", '=IF({fl_magic}>0.75,"Efficient — invest more in S&M",IF({fl_magic}>=0.5,"Okay — optimise","Fix go-to-market first"))', GEN, "", ""),
    ])
    r = block(ws, r, "F. Growth rates", [
        ("fl_s", "Revenue at start (₹ cr)", 10, CR, "Input", ILL, True),
        ("fl_e", "Revenue at end (₹ cr)", 40, CR, "Input", ILL, True),
        ("fl_y", "Number of years", 3, YEARS, "Input", ILL, True),
        ("fl_cagr", "CAGR", "=({fl_e}/{fl_s})^(1/{fl_y})-1", PCT, "(End ÷ Start)^(1 ÷ years) − 1", "Smoothed yearly growth", False, True),
        ("fl_lm", "Revenue last month (₹ lakh)", 50, LAKH, "Input", ILL, True),
        ("fl_tm", "Revenue this month (₹ lakh)", 55, LAKH, "Input", ILL, True),
        ("fl_mom", "Month-on-month growth", "=({fl_tm}-{fl_lm})/{fl_lm}", PCT, "(This − last) ÷ last", "10–20% MoM is strong at seed", False, True),
        ("fl_dbl", "Months to double at this MoM rate", "=LN(2)/LN(1+{fl_mom})", MONTHS, "ln(2) ÷ ln(1 + MoM)", "Rule of 72: 72 ÷ 10 ≈ 7 months"),
    ])
    r = block(ws, r, "G. ROI, MOIC and IRR (single investment)", [
        ("fl_inv", "Amount invested (₹ cr)", 10, CR, "Input", ILL, True),
        ("fl_exitv", "Value received at exit (₹ cr)", 50, CR, "Input", ILL, True),
        ("fl_yrs", "Years held", 6, YEARS, "Input", ILL, True),
        ("fl_roi", "ROI", "=({fl_exitv}-{fl_inv})/{fl_inv}", PCT, "(Value − investment) ÷ investment", "Ignores time", False, True),
        ("fl_moic", "MOIC", "={fl_exitv}/{fl_inv}", MULT1, "Value ÷ investment", "How many times the money came back", False, True),
        ("fl_irr", "IRR (one cash-in, one cash-out)", "={fl_moic}^(1/{fl_yrs})-1", PCT, "MOIC^(1 ÷ years) − 1", "Adds time; see tab 14 for IRR on a full cash-flow series", False, True),
    ])
    r = block(ws, r, "H. Marketplace: GMV, take rate, NMV", [
        ("fl_gmv", "GMV (₹ cr)", 100, CR, "Input", ILL, True),
        ("fl_take", "Take rate", 0.12, PCT, "Input", ILL, True),
        ("fl_ret", "Returns & cancellations (% of GMV)", 0.08, PCT, "Input", ILL, True),
        ("fl_mrev", "Platform revenue (₹ cr)", "={fl_gmv}*{fl_take}", CR, "GMV × take rate", "This is the real revenue, not GMV", False, True),
        ("fl_nmv", "NMV (₹ cr)", "={fl_gmv}*(1-{fl_ret})", CR, "GMV × (1 − returns %)", "Demand that was kept"),
    ])
    r = block(ws, r, "I. Working capital and cash conversion cycle", [
        ("fl_rev", "Annual revenue (₹ cr)", 40, CR, "Input", ILL, True),
        ("fl_cogs", "Annual COGS (₹ cr)", 18, CR, "Input", ILL, True),
        ("fl_invt", "Inventory (₹ cr)", 3, CR, "Input", ILL, True),
        ("fl_rec", "Receivables (₹ cr)", 4, CR, "Input", ILL, True),
        ("fl_pay2", "Payables (₹ cr)", 2, CR, "Input", ILL, True),
        ("fl_dio", "DIO — inventory days", "={fl_invt}/{fl_cogs}*365", DAYS, "Inventory ÷ COGS × 365", "Days stock sits"),
        ("fl_dso", "DSO — receivable days", "={fl_rec}/{fl_rev}*365", DAYS, "Receivables ÷ revenue × 365", "Days to collect cash"),
        ("fl_dpo", "DPO — payable days", "={fl_pay2}/{fl_cogs}*365", DAYS, "Payables ÷ COGS × 365", "Days to pay suppliers (MSMEs: 45-day legal limit)"),
        ("fl_ccc", "Cash conversion cycle", "={fl_dio}+{fl_dso}-{fl_dpo}", DAYS, "DIO + DSO − DPO", "Days cash is locked up; lower is better", False, True),
        ("fl_nwc", "Net working capital (₹ cr)", "={fl_invt}+{fl_rec}-{fl_pay2}", CR, "Inventory + receivables − payables", "Cash needed to run operations"),
    ])
    r = block(ws, r, "J. Break-even", [
        ("fl_fixed", "Fixed costs per month (₹ lakh)", 30, LAKH, "Input", ILL, True),
        ("fl_price", "Net price per unit (₹)", 381, INR, "Input", ILL, True),
        ("fl_var", "Variable cost per unit (₹)", 281, INR, "Input", ILL, True),
        ("fl_cpu", "Contribution per unit (₹)", "={fl_price}-{fl_var}", INR, "Price − variable cost", ""),
        ("fl_be", "Break-even units per month", "={fl_fixed}*100000/{fl_cpu}", NUM, "Fixed costs ÷ contribution per unit", "Volume needed to stop losing money", False, True),
    ])
    r = block(ws, r, "K. Advertising efficiency", [
        ("fl_ad", "Ad spend (₹ lakh)", 10, LAKH, "Input", ILL, True),
        ("fl_adrev", "Revenue attributed to ads (₹ lakh)", 30, LAKH, "Input", ILL, True),
        ("fl_cm2p", "CM2 % (contribution before marketing)", 0.40, PCT, "Input", "From tab 04 logic", True),
        ("fl_roas", "ROAS", "={fl_adrev}/{fl_ad}", MULT, "Ad revenue ÷ ad spend", "", False, True),
        ("fl_beroas", "Break-even ROAS", "=1/{fl_cm2p}", MULT, "1 ÷ CM2 %", "ROAS below this loses money on each ad-driven sale", False, True),
        ("fl_v5", "Verdict", '=IF({fl_roas}>={fl_beroas},"Profitable on contribution","Losing money on each ad-driven sale")', GEN, "", ""),
    ])
    r = block(ws, r, "L. Pre-money, post-money, ownership, dilution", [
        ("fl_pre", "Pre-money valuation (₹ cr)", 40, CR, "Input", ILL, True),
        ("fl_raise", "New investment (₹ cr)", 10, CR, "Input", ILL, True),
        ("fl_post", "Post-money valuation (₹ cr)", "={fl_pre}+{fl_raise}", CR, "Pre-money + investment", "", False, True),
        ("fl_own", "New investor ownership", "={fl_raise}/{fl_post}", PCT, "Investment ÷ post-money", "", False, True),
        ("fl_f0", "Founder ownership before the round", 0.60, PCT, "Input", ILL, True),
        ("fl_f1", "Founder ownership after the round", "={fl_f0}*(1-{fl_own})", PCT, "Old % × (1 − new investor %)", "Dilution", False, True),
    ])
    r = block(ws, r, "M. Currency and Indian units", [
        ("fx", "₹ per US$", 88, NUM1, "Input", "Assumption — update to today's rate before quoting $ numbers", True),
        ("fl_usd", "Amount in US$ million", 5, USDM, "Input", ILL, True),
        ("fl_inrcr", "Same amount in ₹ crore", "={fl_usd}*{fx}/10", CR, "US$ M × rate ÷ 10", "$1M = ₹8.8 cr at ₹88/$", False, True),
        ("fl_cr", "Amount in ₹ crore", 100, CR, "Input", ILL, True),
        ("fl_usd2", "Same amount in US$ million", "={fl_cr}*10/{fx}", USDM, "₹ cr × 10 ÷ rate", "", False, True),
        ("fl_lakh", "1 crore in lakh", 100, NUM, "Fact", "1 lakh = 1,00,000; 1 crore = 1,00,00,000 = 10 million"),
    ])


def sheet_consumer(wb):
    ws = new_sheet(wb, "04 Consumer", "Consumer / D2C — how a consumption business runs (worked example)",
                   "Fictional brand 'CrunchKart' selling ₹500-MRP millet snack packs. Change yellow cells to test scenarios.",
                   [2, 44, 17, 17, 17, 17, 17, 17, 34], tab="C55A11")
    r = 5
    r = note(ws, r, "How a consumer brand runs, in one line: buy or make product cheaply → build a brand people trust → sell through "
                    "many channels → make customers come back. Money is made per unit sold, so the investor studies each layer of "
                    "cost per order (CM1 → CM2 → CM3), repeat behaviour (cohorts) and how much cash is locked in stock.", 2, 9)
    r += 1
    # --- Section 1: per order
    r = sec(ws, r, "1. Unit economics of one order on the brand's own website", 2, 9)
    r = header(ws, r, ["Line item", "₹ per order", "% of net revenue", "How it is calculated / what it means"])
    ws.merge_cells(start_row=r - 1, start_column=5, end_row=r - 1, end_column=9)

    def urow(r, key, label, val, inp=False, how="", pct=True, result=False, fmt=INR2):
        lab = ws.cell(r, 2, label)
        lab.font = font(result)
        lab.border = BOX
        lab.alignment = TOPWRAP
        if result:
            lab.fill = KEY
        setv(ws, r, 3, val, fmt, key, inp, result)
        if pct:
            setv(ws, r, 4, f"={{{key}}}/{{c_net}}" if key != "c_net" else "=1", PCT, None, False, result)
        else:
            ws.cell(r, 4).border = BOX
        ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=9)
        c = ws.cell(r, 5, how)
        c.font = font(False, GREY)
        c.alignment = TOPWRAP
        w = sum(width(ws, k) for k in range(5, 10))
        ws.row_dimensions[r].height = max(15, 12.8 * max(nlines(how, w), nlines(label, width(ws, 2))) + 3)
        return r + 1

    r = urow(r, "c_mrp", "MRP of the order (₹)", 500, True, "Input — maximum retail price printed on the pack. " + ILL, pct=False, fmt=INR)
    r = urow(r, "c_disc", "Average discount", 0.15, True, "Input — coupons and offers", pct=False, fmt=PCT)
    r = urow(r, "c_sp", "Price the customer pays (incl. GST)", "={c_mrp}*(1-{c_disc})", False, "MRP × (1 − discount)", pct=False)
    r = urow(r, "c_gst", "GST rate", 0.05, True, "Input — most packaged foods are 5% after GST 2.0 (Sept 2025); always check the HSN code", pct=False, fmt=PCT)
    REG["c_net"] = (ws.title, f"C{r}")
    r = urow(r, "c_net", "Net revenue (excluding GST)", "={c_sp}/(1+{c_gst})", False, "Price ÷ (1 + GST). GST is collected for the government, so it is never revenue.", result=True)
    r = urow(r, "c_cogs", "COGS: product + primary pack (₹)", 130, True, "Input — contract manufacturer price per pack")
    r = urow(r, "c_cm1", "CM1 (gross profit)", "={c_net}-{c_cogs}", False, "Net revenue − COGS. Benchmark gross margin for D2C food/beauty: 55–70%", result=True)
    r = urow(r, "c_pack", "Secondary packaging (₹)", 20, True, "Input — shipping box, tape, filler")
    r = urow(r, "c_ship", "Shipping & last-mile delivery (₹)", 65, True, "Input — courier/3PL cost per order")
    r = urow(r, "c_pgp", "Payment gateway fee (% of price paid)", 0.02, True, "Input — Razorpay/Cashfree style fee", pct=False, fmt=PCT)
    r = urow(r, "c_pg", "Payment gateway fee (₹)", "={c_sp}*{c_pgp}", False, "Price paid × gateway %")
    r = urow(r, "c_rto", "Returns / RTO provision (₹)", 12, True, "Input — cost of failed cash-on-delivery orders and returns, averaged over all orders")
    r = urow(r, "c_cm2", "CM2 (after fulfilment costs)", "={c_cm1}-{c_pack}-{c_ship}-{c_pg}-{c_rto}", False, "CM1 − packaging − shipping − gateway − returns. Benchmark: 35–40%+ of net revenue", result=True)
    r = urow(r, "c_mkt", "Performance marketing per order (₹)", 130, True, "Input — Meta/Google/influencer spend ÷ all orders (new + repeat)")
    r = urow(r, "c_cm3", "CM3 (after marketing)", "={c_cm2}-{c_mkt}", False, "CM2 − marketing. Must turn positive as repeat customers grow", result=True)
    r = crow(ws, r, "c_v1", "CM2 check", '=IF({c_cm2}/{c_net}>=0.35,"CM2 healthy (35% or more)","CM2 weak (below 35%) — fix logistics or pricing")', GEN, "", "", wide=9)
    r = crow(ws, r, "c_v2", "CM3 check", '=IF({c_cm3}>0,"CM3 positive — each order makes money after ads","CM3 negative — each order loses money after ads")', GEN, "", "", wide=9)
    r += 1
    # --- Section 2: channels
    r = sec(ws, r, "2. Same ₹500 pack, five channels — where does the brand make money?", 2, 9)
    chans = ["Own website", "Amazon / Flipkart", "Quick commerce", "Modern trade", "General trade"]
    r = header(ws, r, ["Per unit (₹)"] + chans + ["Notes"])
    cols = [3, 4, 5, 6, 7]
    L = [get_column_letter(c) for c in cols]
    rowmap = {}

    def chrow(r, name, vals, fmt, inp_flags, notes="", result=False):
        lab = ws.cell(r, 2, name)
        lab.font = font(result)
        lab.border = BOX
        lab.alignment = TOPWRAP
        if result:
            lab.fill = KEY
        for c, v, f in zip(cols, vals, inp_flags):
            setv(ws, r, c, v, fmt, None, f, result)
        n = ws.cell(r, 8, notes)
        ws.merge_cells(start_row=r, start_column=8, end_row=r, end_column=9)
        n.font = font(False, GREY)
        n.alignment = TOPWRAP
        ws.row_dimensions[r].height = max(15, 12.8 * max(nlines(notes, width(ws, 8) + width(ws, 9)), nlines(name, width(ws, 2))) + 3)
        return r + 1

    rowmap["price"] = r
    r = chrow(r, "Consumer price incl. GST", ["={c_sp}", 400, 450, 500, 500], INR2, [False, True, True, True, True],
              "Website links to section 1. Offline usually sells at MRP; promotions are paid as trade spend.")
    rowmap["netgst"] = r
    r = chrow(r, "Price excluding GST", [f"={x}{rowmap['price']}/(1+{{c_gst}})" for x in L], INR2, [False] * 5, "Price ÷ (1 + GST)")
    rowmap["margin"] = r
    r = chrow(r, "Channel margin / commission %", [0, 0.30, 0.32, 0.35, 0.30], PCT, [True] * 5,
              "Illustrative: marketplace commission + fees 25–35%; quick-commerce platform margin 25–35%; modern trade retailer + distributor 30–40% incl. listing; general trade distributor (~8–10%) + retailer (~15–20%)")
    rowmap["brandrev"] = r
    r = chrow(r, "Brand net revenue per unit", [f"={x}{rowmap['netgst']}*(1-{x}{rowmap['margin']})" for x in L], INR2, [False] * 5,
              "What actually reaches the brand", result=True)
    rowmap["cogs"] = r
    r = chrow(r, "COGS", ["={c_cogs}"] * 5, INR2, [False] * 5, "Same product, same cost")
    rowmap["log"] = r
    r = chrow(r, "Logistics, packaging & returns", ["={c_pack}+{c_ship}+{c_rto}", 45, 20, 15, 12], INR2, [False, True, True, True, True],
              "Website = section 1. Others: fulfilment fee / freight to warehouse / damage & expiry")
    rowmap["pg"] = r
    r = chrow(r, "Payment gateway", ["={c_pg}", 0, 0, 0, 0], INR2, [False, True, True, True, True], "Only on own website")
    rowmap["mktp"] = r
    r = chrow(r, "Marketing / trade spend (% of brand net revenue)", [f"={{c_mkt}}/C{rowmap['brandrev']}", 0.12, 0.15, 0.10, 0.05], PCT,
              [False, True, True, True, True], "Ads on marketplace & quick-commerce apps; schemes and promotions offline")
    rowmap["mkt"] = r
    r = chrow(r, "Marketing / trade spend (₹)", [f"={x}{rowmap['mktp']}*{x}{rowmap['brandrev']}" for x in L], INR2, [False] * 5, "% × brand net revenue")
    rowmap["ovh"] = r
    r = chrow(r, "Sales team & distribution overhead per unit", [0, 0, 5, 25, 45], INR2, [True] * 5,
              "Offline needs field sales, distributor management and merchandisers")
    rowmap["contr"] = r
    r = chrow(r, "Contribution per unit", [f"={x}{rowmap['brandrev']}-{x}{rowmap['cogs']}-{x}{rowmap['log']}-{x}{rowmap['pg']}-{x}{rowmap['mkt']}-{x}{rowmap['ovh']}" for x in L],
              INR2, [False] * 5, "Brand net revenue − all variable costs", result=True)
    r = chrow(r, "Contribution % of brand net revenue", [f"={x}{rowmap['contr']}/{x}{rowmap['brandrev']}" for x in L], PCT, [False] * 5, "", result=True)
    r = chrow(r, "Typical payment cycle to the brand", ["0–7 days", "7–15 days", "30–45 days", "45–90 days", "Advance – 30 days"], GEN, [False] * 5,
              "Longer cycles = more working capital needed")
    r = chrow(r, "Watch-outs", ["High CAC", "Ad-heavy, price wars", "Margins + ad pressure; data owned by platform", "Listing fees, slow payment", "Needs distributors and field force"],
              GEN, [False] * 5, "")
    r = note(ws, r, "Reading it: the brand's own website has the lowest contribution because it pays for every customer through ads, "
                    "but it owns the customer data. Offline earns more per unit but needs a sales force, distributor margins and "
                    "long credit. Good brands balance 2–3 channels and track contribution by channel.", 2, 9)
    r += 1
    # --- Section 3: cohorts
    r = sec(ws, r, "3. Cohort retention — % of each month's new customers who order again in later months", 2, 9)
    r = header(ws, r, ["Cohort (month of first order)", "New customers", "M0", "M1", "M2", "M3", "M4", "M5"])
    cohorts = [("Jan-2026", 1200, [1, .38, .30, .27, .26, .25]), ("Feb-2026", 1350, [1, .40, .31, .28, .27]),
               ("Mar-2026", 1500, [1, .42, .33, .30]), ("Apr-2026", 1800, [1, .41, .34]), ("May-2026", 2100, [1, .44]),
               ("Jun-2026", 2400, [1])]
    first = r
    for name, n, vals in cohorts:
        ws.cell(r, 2, name).font = font(True)
        ws.cell(r, 2).border = BOX
        setv(ws, r, 3, n, NUM, None, True)
        for j in range(6):
            if j < len(vals):
                setv(ws, r, 4 + j, vals[j], PCT, None, True)
            else:
                ws.cell(r, 4 + j).border = BOX
        r += 1
    last = r - 1
    ws.cell(r, 2, "Average retention").font = font(True)
    ws.cell(r, 2).fill = KEY
    setv(ws, r, 3, f"=SUM(C{first}:C{last})", NUM, None, False, True)
    for j in range(6):
        col = get_column_letter(4 + j)
        setv(ws, r, 4 + j, f"=AVERAGE({col}{first}:{col}{last})", PCT, None, False, True)
    REG["c_m3"] = (ws.title, f"G{r}")
    r += 1
    r = note(ws, r, "How to read: each row is a group of customers who first bought in that month. M1 = share who ordered again "
                    "one month later. The curve dropping fast then flattening around 25–30% (M3–M5) means there is a loyal core — "
                    "a product–market-fit signal. Newer cohorts retaining better (Mar–May M1 ≥ 41%) means the product or targeting "
                    "is improving. Always ask founders for this table; it is the truth serum.", 2, 9)
    r += 1
    # --- Section 4: LTV
    r = block(ws, r, "4. Customer LTV vs CAC (consumer)", [
        ("c_cac", "CAC for a brand-new customer (₹)", 450, INR, "Input", ILL, True),
        ("c_o12", "Expected orders per customer in 12 months", 3.0, NUM1, "Input", "Estimate from the cohort table: 1 first order + repeat orders", True),
        ("c_o24", "Expected orders per customer in 24 months", 5.0, NUM1, "Input", ILL, True),
        ("c_ltv12", "12-month LTV (₹, CM2 basis)", "={c_o12}*{c_cm2}", INR, "Orders × CM2 per order", "Use contribution, not revenue", False, True),
        ("c_ltv24", "24-month LTV (₹, CM2 basis)", "={c_o24}*{c_cm2}", INR, "Orders × CM2 per order", "", False, True),
        ("c_r12", "LTV:CAC at 12 months", "={c_ltv12}/{c_cac}", MULT, "LTV ÷ CAC", "", False, True),
        ("c_r24", "LTV:CAC at 24 months", "={c_ltv24}/{c_cac}", MULT, "LTV ÷ CAC", "Consumer target: 3x within 24–36 months", False, True),
        ("c_pbo", "Orders needed to pay back CAC", "={c_cac}/{c_cm2}", NUM2, "CAC ÷ CM2 per order", "Fewer than 2 orders is excellent"),
        ("c_v3", "Verdict", '=IF({c_r24}>=3,"Strong",IF({c_r24}>=1.5,"Acceptable — repeat rate must improve","Weak — brand is buying revenue"))', GEN, "", ""),
    ], wide=9)
    # --- Section 5: P&L
    r = block(ws, r, "5. Monthly brand P&L (website channel only, for simplicity)", [
        ("c_orders", "Orders per month", 30000, NUM, "Input", ILL, True),
        ("c_rev", "Net revenue (₹ lakh)", "={c_orders}*{c_net}/100000", LAKH, "Orders × net revenue per order", "", False, True),
        ("c_gp", "Gross profit / CM1 (₹ lakh)", "={c_orders}*{c_cm1}/100000", LAKH, "Orders × CM1", ""),
        ("c_cm2l", "CM2 (₹ lakh)", "={c_orders}*{c_cm2}/100000", LAKH, "Orders × CM2", ""),
        ("c_mktl", "Marketing (₹ lakh)", "={c_orders}*{c_mkt}/100000", LAKH, "Orders × marketing per order", ""),
        ("c_cm3l", "CM3 (₹ lakh)", "={c_cm2l}-{c_mktl}", LAKH, "CM2 − marketing", ""),
        ("c_team", "Team salaries (₹ lakh / month)", 25, LAKH, "Input", ILL, True),
        ("c_oth", "Rent, tech, admin (₹ lakh / month)", 10, LAKH, "Input", ILL, True),
        ("c_ebitda", "EBITDA (₹ lakh / month)", "={c_cm3l}-{c_team}-{c_oth}", LAKH, "CM3 − fixed costs", "Negative = monthly burn from operations", False, True),
        ("c_ebm", "EBITDA margin", "={c_ebitda}/{c_rev}", PCT, "EBITDA ÷ revenue", "", False, True),
        ("c_beo", "Break-even orders per month", "=({c_team}+{c_oth})*100000/{c_cm3}", NUM, "Fixed costs ÷ CM3 per order", "Lifting CM3 (better repeat, lower CAC) cuts this sharply", False, True),
        ("c_annual", "Annualised net revenue (₹ cr)", "={c_rev}*12/100", CR, "Monthly revenue × 12", "This is run-rate, not ARR"),
    ], wide=9)
    # --- Section 6: working capital
    r = block(ws, r, "6. Working capital — the hidden cash drain of consumer brands", [
        ("c_acogs", "Annual COGS (₹ cr)", "={c_orders}*{c_cogs}*12/10000000", CR, "Orders × COGS × 12", ""),
        ("c_dio", "Inventory days", 60, DAYS, "Input", "FMCG 30–60; fashion 90–150", True),
        ("c_dso", "Receivable days (marketplace / QC / MT dues)", 20, DAYS, "Input", ILL, True),
        ("c_dpo", "Payable days to manufacturer", 30, DAYS, "Input", "MSME suppliers must be paid within 45 days", True),
        ("c_inv", "Inventory (₹ cr)", "={c_acogs}*{c_dio}/365", CR, "COGS × DIO ÷ 365", ""),
        ("c_rec", "Receivables (₹ cr)", "={c_annual}*{c_dso}/365", CR, "Revenue × DSO ÷ 365", ""),
        ("c_pay", "Payables (₹ cr)", "={c_acogs}*{c_dpo}/365", CR, "COGS × DPO ÷ 365", ""),
        ("c_nwc", "Net working capital needed (₹ cr)", "={c_inv}+{c_rec}-{c_pay}", CR, "Inventory + receivables − payables", "Grows with revenue — fast growth eats cash", False, True),
        ("c_ccc", "Cash conversion cycle", "={c_dio}+{c_dso}-{c_dpo}", DAYS, "DIO + DSO − DPO", "", False, True),
    ], wide=9)
    r = sec(ws, r, "7. How an associate evaluates a consumer founder / brand", 2, 9)
    r, _ = table(ws, r, ["Area", "What to check", "Green flag", "Red flag", "Question to ask the founder"], CONSUMER_LENS)
    for rr in range(r - len(CONSUMER_LENS) - 1, r):
        for c in (7, 8):
            pass
    # widen: table spans B..F; merge F..I for question column readability is not needed (widths ok)


def sheet_deeptech(wb):
    ws = new_sheet(wb, "05 Deep Tech", "Deep tech — how an IP-led hardware/science company runs (worked example)",
                   "Fictional 'AeroSense': inspection drones + AI analytics for steel, power and oil & gas plants.",
                   [2, 34, 16, 16, 16, 16, 16, 40, 30, 34], tab="7030A0")
    r = 5
    r = note(ws, r, "How deep tech runs, in one line: spend years and lots of R&D money turning science into a working product, prove "
                    "it with paid pilots, get certified, then scale manufacturing so unit costs fall. Revenue comes late; value is "
                    "created by retiring risk step by step. So investors fund milestones (TRL levels), not revenue multiples.", 2, 10)
    r += 1
    r = sec(ws, r, "1. Technology Readiness Levels (TRL) — the deep tech ladder", 2, 10)
    r, _ = table(ws, r, ["TRL", "Meaning", "Drone example", "Typical funding source", "What the investor checks"],
                 [(a, b, c, d, e) for a, b, c, d, e in TRL])
    r += 1
    r = sec(ws, r, "2. Milestone-based funding plan and founder dilution", 2, 10)
    r = header(ws, r, ["Round", "Amount (₹ cr)", "Pre-money (₹ cr)", "Post-money (₹ cr)", "New investor %", "Founders after round", "Months", "Milestone this money must buy", "Use of funds"])
    plan = [
        ("Founding", None, None, None, None, 1.0, 0, "Lab prototype (TRL 4)", "Founders' savings"),
        ("Grant (iDEX / DST)", 1.5, None, None, 0, None, 9, "Outdoor prototype (TRL 5); non-dilutive", "Prototype parts, testing"),
        ("Pre-seed", 4, 16, None, None, None, 12, "Paid pilots at 2–3 plants (TRL 6)", "4 engineers, pilot units"),
        ("Seed", 15, 60, None, None, None, 18, "DGCA type certificate; 3 purchase orders (TRL 8)", "Certification, 20 units, sales hires"),
        ("Series A", 60, 240, None, None, None, 24, "100+ units deployed; software recurring revenue (TRL 9)", "Manufacturing line, service network"),
    ]
    first = r
    for i, (nm, amt, pre, _, pct, fo, mo, ms, use) in enumerate(plan):
        ws.cell(r, 2, nm).font = font(True)
        ws.cell(r, 2).border = BOX
        if amt is not None:
            setv(ws, r, 3, amt, CR, None, True)
        else:
            ws.cell(r, 3).border = BOX
        if pre is not None:
            setv(ws, r, 4, pre, CR, f"dt_pre{i}", True)
            setv(ws, r, 5, f"=C{r}+D{r}", CR)
            setv(ws, r, 6, f"=C{r}/E{r}", PCT)
        else:
            ws.cell(r, 4).border = BOX
            ws.cell(r, 5).border = BOX
            if pct is not None:
                setv(ws, r, 6, 0, PCT, None, True)
            else:
                ws.cell(r, 6).border = BOX
        if i == 0:
            setv(ws, r, 7, fo, PCT, None, True)
        else:
            setv(ws, r, 7, f"=G{r - 1}*(1-F{r})", PCT, None, False, i == len(plan) - 1)
        setv(ws, r, 8, mo, NUM, None, True)
        for c, t in ((9, ms), (10, use)):
            x = ws.cell(r, c, t)
            x.font = font()
            x.alignment = TOPWRAP
            x.border = BOX
        fit(ws, r, 2, 10)
        r += 1
    REG["dt_found"] = (ws.title, f"G{r - 1}")
    ws.cell(r, 2, "Total equity raised (₹ cr)").font = font(True)
    setv(ws, r, 3, f"=SUM(C{first + 2}:C{r - 1})", CR, None, False, True)
    ws.cell(r, 8, f"=SUM(H{first}:H{r - 1})").number_format = '0" months total"'
    ws.cell(r, 8).font = font(True)
    r += 1
    r = note(ws, r, "Why tranche by milestone: each round is priced after a big risk is retired (prototype works → customers pay → "
                    "certified → scales). Raising only what the next milestone needs keeps founders at a healthy stake (cell G above) "
                    "and lets investors re-price risk. Grants (non-dilutive) are gold for deep tech.", 2, 10)
    r += 1
    r = sec(ws, r, "3. Hardware unit economics with an 85% learning curve (cost falls 15% every time volume doubles)", 2, 10)
    r = crow(ws, r, "dt_bom0", "BOM per drone at base volume (₹ lakh)", 6.0, LAKH, "Input", ILL, True, wide=10)
    r = crow(ws, r, "dt_asm0", "Assembly & testing per drone at base volume (₹ lakh)", 0.6, LAKH, "Input", ILL, True, wide=10)
    r = crow(ws, r, "dt_base", "Base volume (units per year)", 50, NUM, "Input", "Today's volume", True, wide=10)
    r = crow(ws, r, "dt_lr", "Learning rate", 0.85, PCT, "Input", "85% = each doubling of volume cuts cost to 85%", True, wide=10)
    r = crow(ws, r, "dt_price", "Hardware price per drone (₹ lakh)", 12, LAKH, "Input", ILL, True, wide=10)
    r = crow(ws, r, "dt_sw", "Software & analytics per drone per year (₹ lakh)", 1.5, LAKH, "Input", "Recurring revenue", True, wide=10)
    r = crow(ws, r, "dt_swgm", "Software gross margin", 0.85, PCT, "Input", "", True, wide=10)
    r = header(ws, r, ["Per year", "Volume 1", "Volume 2", "Volume 3", "Volume 4", "", "How it is calculated"])
    vols = [50, 200, 500, 1000]
    vc = [3, 4, 5, 6]
    rows = {}

    def vrow(r, name, vals, fmt, how, inp=False, result=False):
        ws.cell(r, 2, name).font = font(result)
        ws.cell(r, 2).border = BOX
        ws.cell(r, 2).alignment = TOPWRAP
        if result:
            ws.cell(r, 2).fill = KEY
        for c, v in zip(vc, vals):
            setv(ws, r, c, v, fmt, None, inp, result)
        ws.merge_cells(start_row=r, start_column=8, end_row=r, end_column=10)
        x = ws.cell(r, 8, how)
        x.font = font(False, GREY)
        x.alignment = TOPWRAP
        fit(ws, r, 2, 8)
        return r + 1

    Lv = [get_column_letter(c) for c in vc]
    rows["u"] = r
    r = vrow(r, "Units sold per year", vols, NUM, "Input — volume scenarios", True)
    rows["f"] = r
    r = vrow(r, "Learning-curve cost factor", [f"=({x}{rows['u']}/{{dt_base}})^LOG({{dt_lr}},2)" for x in Lv], NUM2, "(Volume ÷ base)^log2(learning rate)")
    rows["bom"] = r
    r = vrow(r, "BOM per unit (₹ lakh)", [f"={{dt_bom0}}*{x}{rows['f']}" for x in Lv], LAKH, "Base BOM × factor")
    rows["asm"] = r
    r = vrow(r, "Assembly & testing per unit (₹ lakh)", [f"={{dt_asm0}}*{x}{rows['f']}" for x in Lv], LAKH, "Base assembly × factor")
    rows["hgm"] = r
    r = vrow(r, "Hardware gross margin", [f"=({{dt_price}}-{x}{rows['bom']}-{x}{rows['asm']})/{{dt_price}}" for x in Lv], PCT, "(Price − BOM − assembly) ÷ price", result=True)
    rows["hrev"] = r
    r = vrow(r, "Hardware revenue (₹ cr)", [f"={x}{rows['u']}*{{dt_price}}/100" for x in Lv], CR, "Units × price ÷ 100")
    rows["srev"] = r
    r = vrow(r, "Software revenue (₹ cr)", [f"={x}{rows['u']}*{{dt_sw}}/100" for x in Lv], CR, "Units × software fee ÷ 100 (simplified: fleet = this year's units)")
    rows["gp"] = r
    r = vrow(r, "Total gross profit (₹ cr)", [f"={x}{rows['hrev']}*{x}{rows['hgm']}+{x}{rows['srev']}*{{dt_swgm}}" for x in Lv], CR, "Hardware GP + software GP")
    r = vrow(r, "Blended gross margin", [f"={x}{rows['gp']}/({x}{rows['hrev']}+{x}{rows['srev']})" for x in Lv], PCT, "Gross profit ÷ total revenue", result=True)
    r = note(ws, r, "Reading it: at 50 units the business looks like a low-margin hardware shop; at 500–1,000 units costs fall and "
                    "recurring software lifts blended margin. The investor's job is to judge whether the company can really reach that "
                    "volume, and how much capital it needs to get there.", 2, 10)
    r += 1
    r = block(ws, r, "4. Risk-adjusted VC method — what is this pre-seed company worth today?", [
        ("dt_rev7", "Revenue in exit year if everything works (₹ cr)", 400, CR, "Input", ILL, True),
        ("dt_mult", "Exit EV / revenue multiple", 5, MULT1, "Input", "Use listed/strategic comps", True),
        ("dt_exit", "Exit value if successful (₹ cr)", "={dt_rev7}*{dt_mult}", CR, "Revenue × multiple", ""),
        ("dt_pt", "Probability technology works and is certified", 0.60, PCT, "Input", "Technical risk", True),
        ("dt_pc", "Probability of commercial success, given tech works", 0.50, PCT, "Input", "Market risk", True),
        ("dt_p", "Overall probability of success", "={dt_pt}*{dt_pc}", PCT, "P(tech) × P(commercial)", "", False, True),
        ("dt_eexit", "Probability-weighted exit value (₹ cr)", "={dt_exit}*{dt_p}", CR, "Exit value × probability", ""),
        ("dt_irr", "Required annual return", 0.45, PCT, "Input", "Early-stage VCs use 40–60%", True),
        ("dt_n", "Years to exit", 7, YEARS, "Input", "", True),
        ("dt_reqm", "Required multiple", "=(1+{dt_irr})^{dt_n}", MULT1, "(1 + required return)^years", ""),
        ("dt_ret", "Ownership retained after future dilution", 0.55, PCT, "Input", "Seed + A + B + C rounds dilute early investors", True),
        ("dt_post", "Fair post-money today (₹ cr)", "={dt_eexit}*{dt_ret}/{dt_reqm}", CR, "Weighted exit × retention ÷ required multiple", "", False, True),
        ("dt_chq", "Proposed cheque (₹ cr)", "=" + "{dt_amt_pre}", CR, "From the funding plan", ""),
        ("dt_fpre", "Fair pre-money today (₹ cr)", "={dt_post}-{dt_chq}", CR, "Post − cheque", "", False, True),
        ("dt_naive", "Post-money if you ignored risk (₹ cr)", "={dt_exit}*{dt_ret}/{dt_reqm}", CR, "Same formula without probabilities", "Shows why risk adjustment matters"),
        ("dt_v", "Verdict vs the asking price", '=IF({dt_fpre}>={dt_pre2},"Asking pre-money is below fair value — attractive","Asking pre-money is above fair value — negotiate")', GEN, "Compares with pre-seed pre-money in section 2", ""),
    ], wide=10)
    r = sec(ws, r, "5. How an associate evaluates a deep tech founder / company", 2, 10)
    r, _ = table(ws, r, ["Area", "What to check", "Green flag", "Red flag", "Question to ask the founder"], DEEPTECH_LENS)
    r += 1
    r = sec(ws, r, "6. Non-dilutive money for Indian deep tech (check current scheme rules before quoting)", 2, 10)
    grants = [
        ("iDEX (Ministry of Defence)", "Defence innovation challenges", "Grants up to ₹1.5 cr; iDEX Prime up to ₹10 cr"),
        ("Startup India Seed Fund Scheme", "Proof of concept, prototype, market entry", "Up to ₹20 L grant; up to ₹50 L via convertible/debt"),
        ("DST NIDHI-PRAYAS", "Prototyping via incubators", "Up to ₹10 L"),
        ("BIRAC BIG", "Biotech / medtech ideas", "Up to ₹50 L"),
        ("MeitY SAMRIDH / chip design schemes", "Electronics, semiconductors, software products", "Matching investment / design-linked incentives"),
        ("RDI scheme (approved 2025)", "Research, development & innovation in sunrise sectors", "₹1 lakh cr corpus for long-term, low-cost financing"),
        ("PLI schemes", "Manufacturing scale-up (drones, electronics, etc.)", "% of incremental sales"),
    ]
    r, _ = table(ws, r, ["Programme", "For what", "Size"], grants)
    # resolve plan references used above
    return ws


def fix_deeptech_refs():
    # pre-seed row is plan index 2 -> key dt_pre2 (pre-money). Amount is in column C of that row.
    sh, coord = REG["dt_pre2"]
    row = int(re.match(r"[A-Z]+(\d+)", coord).group(1))
    REG["dt_amt_pre"] = (sh, f"C{row}")


def sheet_health(wb):
    ws = new_sheet(wb, "06 Healthcare", "Healthcare — how healthcare businesses run (worked examples)",
                   "Segment map, a diagnostic-centre unit model, a medtech rNPV valuation and the regulatory map.",
                   [2, 34, 16, 16, 16, 16, 16, 16, 16, 16, 30], tab="00B0F0")
    r = 5
    r = note(ws, r, "How healthcare runs, in one line: trust and evidence come first, regulation sets the pace, and someone other "
                    "than the patient often pays (insurer, employer, government). Services (clinics, labs) scale centre by centre; "
                    "products (drugs, devices) must clear clinical and regulatory gates before earning anything — so investors use "
                    "centre payback for services and risk-adjusted NPV (rNPV) for products.", 2, 11)
    r += 1
    r = sec(ws, r, "1. Healthcare segment map", 2, 11)
    r, _ = table(ws, r, ["Segment", "How it makes money", "Key metrics", "Regulator / approvals", "Time to revenue", "Capital intensity", "Indian examples", "Investor lens"], HEALTH_SEGMENTS)
    r += 1
    r = block(ws, r, "2. Unit economics of one diagnostic / imaging centre (services example)", [
        ("h_capex", "Capex to set up one centre (₹ lakh)", 150, LAKH, "Input", "Machines, fit-out, IT. " + ILL, True),
        ("h_pd", "Patients per day (mature centre)", 80, NUM, "Input", ILL, True),
        ("h_arpp", "Average revenue per patient (₹)", 1200, INR, "Input", "Mix of blood tests + imaging", True),
        ("h_days", "Operating days per month", 26, NUM, "Input", "", True),
        ("h_rev", "Monthly revenue (₹ lakh)", "={h_pd}*{h_arpp}*{h_days}/100000", LAKH, "Patients × revenue × days", "", False, True),
        ("h_consp", "Consumables & reagents (% of revenue)", 0.25, PCT, "Input", "", True),
        ("h_cons", "Consumables (₹ lakh)", "={h_rev}*{h_consp}", LAKH, "Revenue × %", ""),
        ("h_staff", "Doctors, technicians, staff (₹ lakh / month)", 7, LAKH, "Input", "Radiologist/pathologist availability is the real constraint", True),
        ("h_rent", "Rent & utilities (₹ lakh / month)", 2.5, LAKH, "Input", "", True),
        ("h_mktp", "Marketing & doctor outreach (% of revenue)", 0.06, PCT, "Input", "", True),
        ("h_mkt", "Marketing (₹ lakh)", "={h_rev}*{h_mktp}", LAKH, "Revenue × %", ""),
        ("h_other", "Other opex (₹ lakh / month)", 1.0, LAKH, "Input", "", True),
        ("h_ebitda", "Centre EBITDA (₹ lakh / month)", "={h_rev}-{h_cons}-{h_staff}-{h_rent}-{h_mkt}-{h_other}", LAKH, "Revenue − all centre costs", "", False, True),
        ("h_ebm", "Centre EBITDA margin", "={h_ebitda}/{h_rev}", PCT, "EBITDA ÷ revenue", "Mature centres often 20–30%", False, True),
        ("h_pb", "Payback on capex (months)", "={h_capex}/{h_ebitda}", MONTHS, "Capex ÷ monthly EBITDA", "Under 24 months is healthy", False, True),
        ("h_roc", "Annual return on centre capex", "={h_ebitda}*12/{h_capex}", PCT, "Annual EBITDA ÷ capex", ""),
        ("h_be", "Break-even patients per day", "=({h_staff}+{h_rent}+{h_other})*100000/({h_days}*{h_arpp}*(1-{h_consp}-{h_mktp}))", NUM1, "Fixed costs ÷ contribution per patient-day", "How fast a new centre must ramp", False, True),
        ("h_v", "Verdict", '=IF({h_pb}<=24,"Healthy — payback within 24 months",IF({h_pb}<=36,"Acceptable","Too slow — rethink pricing or capex"))', GEN, "", ""),
    ], wide=11)
    r = sec(ws, r, "3. Medtech device valuation with rNPV (products example) — fictional AI-enabled cardiac monitor", 2, 11)
    r = crow(ws, r, "h_p1", "PoS — prototype & pre-clinical testing", 0.80, PCT, "Input", "Probability of passing this stage", True, wide=11)
    r = crow(ws, r, "h_p2", "PoS — pilot clinical study", 0.65, PCT, "Input", "", True, wide=11)
    r = crow(ws, r, "h_p3", "PoS — pivotal study + CDSCO/FDA approval", 0.75, PCT, "Input", "", True, wide=11)
    r = crow(ws, r, "h_r", "Discount rate", 0.15, PCT, "Input", "Lower than VC rates because risk is already in the probabilities", True, wide=11)
    r = crow(ws, r, "h_m", "EBITDA margin once commercial", 0.25, PCT, "Input", "", True, wide=11)
    r = crow(ws, r, "h_em", "Exit multiple on year-8 EBITDA", 10, MULT1, "Input", "Terminal value = EBITDA × multiple", True, wide=11)
    yrs = list(range(1, 9))
    yc = [3 + i for i in range(8)]
    YL = [get_column_letter(c) for c in yc]
    r = header(ws, r, ["Year"] + [f"Year {y}" for y in yrs] + ["How it is calculated"])
    R = {}

    def yrow(r, name, vals, fmt, how, inp_flags=None, result=False):
        ws.cell(r, 2, name).font = font(result)
        ws.cell(r, 2).border = BOX
        ws.cell(r, 2).alignment = TOPWRAP
        if result:
            ws.cell(r, 2).fill = KEY
        for i, (c, v) in enumerate(zip(yc, vals)):
            setv(ws, r, c, v, fmt, None, bool(inp_flags and inp_flags[i]), result)
        x = ws.cell(r, 11, how)
        x.font = font(False, GREY)
        x.alignment = TOPWRAP
        x.border = BOX
        fit(ws, r, 2, 11)
        return r + 1

    R["t"] = r
    r = yrow(r, "Phase", ["Prototype & pre-clinical", "Pilot clinical", "Pivotal + approval", "Launch", "Scale", "Scale", "Scale", "Scale + exit"], GEN, "")
    R["rev"] = r
    r = yrow(r, "Revenue (₹ cr)", [0, 0, 0, 10, 30, 60, 90, 110], CR, "Input — revenue if approved", [True] * 8)
    R["cost"] = r
    r = yrow(r, "Development cost (₹ cr)", [-4, -6, -12, 0, 0, 0, 0, 0], CR, "Input — R&D and trial spend (negative)", [True] * 8)
    R["cf"] = r
    r = yrow(r, "Operating cash flow (₹ cr)", [f"={x}{R['cost']}+{x}{R['rev']}*{{h_m}}" for x in YL], CR, "Cost + revenue × margin")
    R["tv"] = r
    r = yrow(r, "Exit / terminal value (₹ cr)", [0] * 7 + [f"={YL[7]}{R['rev']}*{{h_m}}*{{h_em}}"], CR, "Year-8 EBITDA × exit multiple", [True] * 7 + [False])
    R["tot"] = r
    r = yrow(r, "Total cash flow (₹ cr)", [f"={x}{R['cf']}+{x}{R['tv']}" for x in YL], CR, "")
    R["p"] = r
    r = yrow(r, "Probability this cash flow happens", ["=1", "={h_p1}", "={h_p1}*{h_p2}"] + ["={h_p1}*{h_p2}*{h_p3}"] * 5, PCT,
             "Year 1 is certain; later years need earlier stages to succeed")
    R["df"] = r
    r = yrow(r, "Discount factor", [f"=1/(1+{{h_r}})^{y}" for y in yrs], '0.000', "1 ÷ (1 + r)^year")
    R["pv"] = r
    r = yrow(r, "PV, ignoring risk (₹ cr)", [f"={x}{R['tot']}*{x}{R['df']}" for x in YL], CR, "Cash flow × discount factor")
    R["rpv"] = r
    r = yrow(r, "Risk-adjusted PV (₹ cr)", [f"={x}{R['tot']}*{x}{R['p']}*{x}{R['df']}" for x in YL], CR, "Cash flow × probability × discount factor")
    r = crow(ws, r, "h_npv", "NPV ignoring risk (₹ cr)", f"=SUM(C{R['pv']}:J{R['pv']})", CR, "Sum of PVs", "What an over-optimistic founder would claim", result=True, wide=11)
    r = crow(ws, r, "h_rnpv", "rNPV (₹ cr)", f"=SUM(C{R['rpv']}:J{R['rpv']})", CR, "Sum of risk-adjusted PVs", "A fair value for the company today", result=True, wide=11)
    r = crow(ws, r, "h_pall", "Cumulative probability of approval", "={h_p1}*{h_p2}*{h_p3}", PCT, "Product of stage PoS", "", wide=11)
    r += 1
    r = sec(ws, r, "4. Drug development success rates (all diseases)", 2, 11)
    r = header(ws, r, ["Transition", "Probability", "", "Source"])
    rates = [("Phase I → Phase II", 0.520), ("Phase II → Phase III", 0.289), ("Phase III → NDA/BLA filing", 0.578), ("NDA/BLA → approval", 0.906)]
    f0 = r
    for nm, p in rates:
        ws.cell(r, 2, nm).border = BOX
        setv(ws, r, 3, p, PCT, None, True)
        ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=11)
        ws.cell(r, 5, "BIO, Informa Pharma Intelligence & QLS, 'Clinical Development Success Rates 2011–2020' (Feb 2021)").font = font(False, GREY)
        r += 1
    r = crow(ws, r, "h_loa", "Likelihood of approval from Phase I", f"=PRODUCT(C{f0}:C{r - 1})", PCT, "Product of all transitions", "≈ 8 in 100 drugs entering Phase I get approved", result=True, wide=11)
    r += 1
    r = sec(ws, r, "5. Regulatory pathways to know", 2, 11)
    regs = [
        ("India — drugs", "CDSCO under New Drugs and Clinical Trials Rules, 2019", "Clinical-trial permission → Phase I–III → marketing authorisation"),
        ("India — medical devices", "CDSCO under Medical Devices Rules, 2017", "Risk Class A (low) → D (high). A/B licensed by state authority; C/D by central authority"),
        ("US — devices", "FDA", "Class I (mostly exempt), Class II (510(k) or De Novo), Class III (PMA with clinical trials)"),
        ("US — drugs", "FDA", "IND → Phase I–III → NDA (small molecule) / BLA (biologic)"),
        ("EU — devices", "EU MDR 2017/745 via notified bodies", "CE marking"),
        ("Labs", "NABL (ISO 15189)", "Accreditation — quality signal and often needed for insurers/hospitals"),
        ("Hospitals & clinics", "NABH; Clinical Establishments Act (adopting states)", "Accreditation and registration"),
        ("Digital health", "Telemedicine Practice Guidelines 2020; DPDP Act 2023; ABDM", "Consent, data protection, interoperability"),
        ("Insurance", "IRDAI", "Licences for insurers/brokers; product approvals"),
    ]
    r, _ = table(ws, r, ["Area", "Regulator / law", "What it means"], regs)
    r += 1
    r = sec(ws, r, "6. How an associate evaluates a healthcare founder / company", 2, 11)
    r, _ = table(ws, r, ["Area", "What to check", "Green flag", "Red flag", "Question to ask the founder"], HEALTH_LENS)


def sheet_sectors(wb):
    ws = new_sheet(wb, "07 Sector Playbook", f"Sector playbook — {len(SECTORS)} industries, one line each",
                   "How each industry runs, how it makes money, the metrics to ask for, good vs bad, and how an associate evaluates it. Filter the header row.",
                   [2, 24, 36, 28, 34, 28, 30, 30, 38], tab="BF8F00")
    r, hdr = table(ws, 5, ["Sector", "How it runs (one line)", "How it makes money", "Key metrics to ask", "What good looks like", "Red flags", "Indian examples (public)", "How an associate evaluates it"], SECTORS)
    ws.freeze_panes = ws.cell(hdr + 1, 3)
    ws.auto_filter.ref = f"B{hdr}:I{r - 1}"


def sheet_founder(wb):
    ws = new_sheet(wb, "08 Founder Evaluation", "Founder & startup evaluation scorecard",
                   "Score a startup 1–5 on each criterion (yellow cells). Weights add to 100%. Try it on a company you know.",
                   [2, 30, 12, 50, 12, 14, 40], tab="C00000")
    r = 5
    r = sec(ws, r, "1. Weighted scorecard (live)", 2, 7)
    r = header(ws, r, ["Criterion", "Weight", "What to look for", "Score (1–5)", "Weighted score", "Evidence / notes"])
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", showErrorMessage=True,
                        errorTitle="Score 1–5", error="Enter a whole number from 1 to 5")
    ws.add_data_validation(dv)
    first = r
    for crit, w, what, sc in SCORECARD:
        ws.cell(r, 2, crit).font = font(True)
        ws.cell(r, 2).border = BOX
        setv(ws, r, 3, w, PCT, None, True)
        x = ws.cell(r, 4, what)
        x.alignment = TOPWRAP
        x.border = BOX
        x.font = font()
        setv(ws, r, 5, sc, "0", None, True)
        dv.add(ws.cell(r, 5))
        setv(ws, r, 6, f"=C{r}*E{r}", NUM2)
        n = ws.cell(r, 7, "")
        n.fill = INP
        n.border = BOX
        fit(ws, r, 2, 7)
        r += 1
    last = r - 1
    r = crow(ws, r, "fe_w", "Total weight (must be 100%)", f"=SUM(C{first}:C{last})", PCT, "", "", wide=7)
    r = crow(ws, r, "fe_s", "Weighted score (out of 5)", f"=SUM(F{first}:F{last})", NUM2, "Σ weight × score", "", result=True, wide=7)
    r = crow(ws, r, "fe_d", "Decision guide", '=IF({fe_w}<>1,"Fix weights to total 100%",IF({fe_s}>=4,"Strong — push to IC",IF({fe_s}>=3,"Promising — do more diligence","Pass for now")))', GEN, "≥4 strong; 3–4 diligence; <3 pass", "", result=True, wide=7)
    r += 1
    r = sec(ws, r, "2. Founder signals — how to test each trait in a meeting", 2, 7)
    r, _ = table(ws, r, ["Trait", "Green flag", "Red flag", "Question that tests it"], FOUNDER_SIGNALS)
    r += 1
    r = sec(ws, r, "3. What to look for by founder type (incl. manufacturing founders)", 2, 7)
    r, _ = table(ws, r, ["Founder type", "Must-have strengths", "Proof to ask for", "Red flags"], FOUNDER_TYPES)
    r += 1
    r = sec(ws, r, "4. Reference-check questions (talk to 5–8 people, including some the founder didn't suggest)", 2, 7)
    for q in REFERENCE_QS:
        r = note(ws, r, "• " + q, 2, 7, f=None)


def sheet_mfg(wb):
    ws = new_sheet(wb, "09 Manufacturing", "Manufacturing — 5-year plant model (worked example)",
                   "Fictional precision-components plant supplying global auto/industrial OEMs (China+1). Yellow cells are inputs.",
                   [2, 40, 14, 14, 14, 14, 14, 14, 40], tab="806000")
    r = 5
    r = note(ws, r, "How manufacturing runs, in one line: spend capex on a plant, win orders from OEMs, push capacity utilisation up "
                    "so fixed costs spread over more units, and manage raw-material prices and working capital. Investors judge it on "
                    "utilisation, EBITDA margin, ROCE, asset turnover, customer concentration and order book.", 2, 9)
    r += 1
    r = block(ws, r, "1. Inputs", [
        ("m_capex", "Plant & machinery capex (₹ cr)", 20, CR, "Input", ILL, True),
        ("m_cap", "Installed capacity (units per year)", 120000, NUM, "Input", "", True),
        ("m_p", "Selling price per unit, year 1 (₹)", 2600, INR, "Input", "", True),
        ("m_pg", "Annual price change", 0.02, PCT, "Input", "Raw-material pass-through clauses help", True),
        ("m_rm", "Raw material per unit, year 1 (₹)", 1400, INR, "Input", "Steel/aluminium etc.", True),
        ("m_rmg", "Raw material inflation per year", 0.03, PCT, "Input", "", True),
        ("m_cc", "Conversion cost per unit (power, consumables, direct labour) (₹)", 200, INR, "Input", "", True),
        ("m_fo", "Fixed overheads, year 1 (₹ cr)", 2.5, CR, "Input", "Salaried staff, maintenance, admin", True),
        ("m_fog", "Fixed overhead growth per year", 0.06, PCT, "Input", "", True),
        ("m_life", "Depreciation life (years)", 10, YEARS, "Input", "Straight line", True),
        ("m_dio", "Raw-material inventory days", 60, DAYS, "Input", "", True),
        ("m_dso", "Receivable days (OEMs pay slowly)", 75, DAYS, "Input", "", True),
        ("m_dpo", "Payable days", 45, DAYS, "Input", "", True),
    ], wide=9)
    r = sec(ws, r, "2. Five-year model", 2, 9)
    yc = [4, 5, 6, 7, 8]
    YL = [get_column_letter(c) for c in yc]
    r = header(ws, r, ["Line", "Unit", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "How it is calculated"])
    R = {}

    def mrow(r, k, name, unit, vals, fmt, how, inp=False, result=False):
        ws.cell(r, 2, name).font = font(result)
        ws.cell(r, 2).border = BOX
        ws.cell(r, 2).alignment = TOPWRAP
        if result:
            ws.cell(r, 2).fill = KEY
        u = ws.cell(r, 3, unit)
        u.font = font(False, GREY)
        u.border = BOX
        for c, v in zip(yc, vals):
            setv(ws, r, c, v, fmt, None, inp, result)
        x = ws.cell(r, 9, how)
        x.font = font(False, GREY)
        x.alignment = TOPWRAP
        x.border = BOX
        fit(ws, r, 2, 9)
        R[k] = r
        return r + 1

    def prev_chain(first, k, growth):
        return [first] + [f"={YL[i - 1]}{{row}}*(1+{growth})" for i in range(1, 5)]

    r = mrow(r, "util", "Capacity utilisation", "%", [0.35, 0.55, 0.70, 0.80, 0.85], PCT, "Input — ramp-up as orders grow", True)
    r = mrow(r, "units", "Units sold", "units", [f"={{m_cap}}*{x}{R['util']}" for x in YL], NUM, "Capacity × utilisation")
    pr = r
    r = mrow(r, "price", "Price per unit", "₹", ["={m_p}"] + [f"={YL[i - 1]}{pr}*(1+{{m_pg}})" for i in range(1, 5)], INR, "Previous year × (1 + price change)")
    rr = r
    r = mrow(r, "rm", "Raw material per unit", "₹", ["={m_rm}"] + [f"={YL[i - 1]}{rr}*(1+{{m_rmg}})" for i in range(1, 5)], INR, "Previous year × (1 + inflation)")
    r = mrow(r, "rev", "Revenue", "₹ cr", [f"={x}{R['units']}*{x}{R['price']}/10000000" for x in YL], CR, "Units × price", result=True)
    r = mrow(r, "rmc", "Raw material cost", "₹ cr", [f"={x}{R['units']}*{x}{R['rm']}/10000000" for x in YL], CR, "Units × RM per unit")
    r = mrow(r, "cc", "Conversion cost", "₹ cr", [f"={x}{R['units']}*{{m_cc}}/10000000" for x in YL], CR, "Units × conversion cost")
    r = mrow(r, "gm", "Gross margin", "₹ cr", [f"={x}{R['rev']}-{x}{R['rmc']}-{x}{R['cc']}" for x in YL], CR, "Revenue − RM − conversion")
    r = mrow(r, "gmp", "Gross margin %", "%", [f"={x}{R['gm']}/{x}{R['rev']}" for x in YL], PCT, "Gross margin ÷ revenue")
    fr = r
    r = mrow(r, "fo", "Fixed overheads", "₹ cr", ["={m_fo}"] + [f"={YL[i - 1]}{fr}*(1+{{m_fog}})" for i in range(1, 5)], CR, "Previous year × (1 + growth)")
    r = mrow(r, "ebitda", "EBITDA", "₹ cr", [f"={x}{R['gm']}-{x}{R['fo']}" for x in YL], CR, "Gross margin − fixed overheads", result=True)
    r = mrow(r, "ebm", "EBITDA margin", "%", [f"={x}{R['ebitda']}/{x}{R['rev']}" for x in YL], PCT, "Precision engineering often 15–25%", result=True)
    r = mrow(r, "dep", "Depreciation", "₹ cr", ["={m_capex}/{m_life}"] * 5, CR, "Capex ÷ life")
    r = mrow(r, "ebit", "EBIT", "₹ cr", [f"={x}{R['ebitda']}-{x}{R['dep']}" for x in YL], CR, "EBITDA − depreciation")
    r = mrow(r, "nwc", "Net working capital", "₹ cr", [f"={x}{R['rev']}*{{m_dso}}/365+{x}{R['rmc']}*({{m_dio}}-{{m_dpo}})/365" for x in YL], CR, "Receivables + RM inventory − payables")
    nr = r
    r = mrow(r, "nfa", "Net fixed assets", "₹ cr", [f"={{m_capex}}-{YL[0]}{R['dep']}"] + [f"={YL[i - 1]}{nr}-{YL[i]}{R['dep']}" for i in range(1, 5)], CR, "Capex less accumulated depreciation")
    r = mrow(r, "ce", "Capital employed", "₹ cr", [f"={x}{R['nfa']}+{x}{R['nwc']}" for x in YL], CR, "Net fixed assets + working capital")
    r = mrow(r, "roce", "ROCE", "%", [f"={x}{R['ebit']}/{x}{R['ce']}" for x in YL], PCT, "EBIT ÷ capital employed; >20% is good", result=True)
    r = mrow(r, "at", "Asset turnover", "x", [f"={x}{R['rev']}/{{m_capex}}" for x in YL], MULT, "Revenue ÷ gross capex; >1.5x is good")
    r = mrow(r, "cpu", "Contribution per unit", "₹", [f"={x}{R['price']}-{x}{R['rm']}-{{m_cc}}" for x in YL], INR, "Price − RM − conversion")
    r = mrow(r, "beu", "Break-even utilisation", "%", [f"={x}{R['fo']}*10000000/({x}{R['cpu']}*{{m_cap}})" for x in YL], PCT, "Fixed overheads ÷ (contribution per unit × capacity)", result=True)
    cr_ = r
    r = mrow(r, "cum", "Cumulative EBITDA", "₹ cr", [f"={YL[0]}{R['ebitda']}"] + [f"={YL[i - 1]}{cr_}+{YL[i]}{R['ebitda']}" for i in range(1, 5)], CR, "Running total")
    r = mrow(r, "pb", "Capex paid back?", "", [f'=IF({x}{R["cum"]}>={{m_capex}},"Yes","Not yet")' for x in YL], GEN, "Cumulative EBITDA ≥ capex")
    r += 1
    r = sec(ws, r, "3. Manufacturing diligence checklist", 2, 9)
    mfg = [
        ("Order book & customers", "Order book ÷ annual revenue; top-customer share; quality of OEM customers; contract length", "Order book >1x revenue; top customer <30%", "One customer >40%; only trial orders"),
        ("Capacity & utilisation", "Installed vs used capacity; shifts; bottleneck machines", "Utilisation rising with orders", "Capex before orders"),
        ("Unit economics", "Contribution per unit, EBITDA margin, break-even utilisation", "Break-even utilisation <40%", "Margins depend on PLI or one-off price"),
        ("Returns on capital", "ROCE, asset turnover, payback", "ROCE >20%; asset turnover >1.5x", "Low turnover, high capex per ₹ of revenue"),
        ("Quality & certifications", "ISO 9001; IATF 16949 (auto); AS9100 (aerospace); customer audits passed", "Certified and audited by global OEMs", "No quality system; high rejection rates"),
        ("Operations", "OEE, scrap/rejection rate, on-time delivery", "OEE 75%+; OTD 95%+", "Frequent delays, rework"),
        ("Raw materials", "Price pass-through clauses; supplier concentration; imports", "Pass-through in contracts", "Absorbs RM inflation"),
        ("Working capital", "Inventory, receivable and payable days", "CCC under 90 days", "OEMs paying in 120+ days; rising inventory"),
        ("Policy", "PLI eligibility; import duties; export incentives", "Profitable without incentives", "Business case only works with PLI"),
        ("Founder", "Shop-floor depth, customer relationships, capital discipline, safety record", "Has run plants before; knows OEE and costs by heart", "Only a sales story, no ops depth"),
    ]
    r, _ = table(ws, r, ["Area", "What to check", "Green flag", "Red flag"], mfg)


def sheet_valuation(wb):
    ws = new_sheet(wb, "10 Valuation", "Valuation methods — six ways to value a startup (all live)",
                   "Early stage: VC method, Scorecard, Berkus, First Chicago. Later stage: comps and DCF. Use 2–3 methods and triangulate.",
                   [2, 44, 16, 16, 16, 16, 40], tab="2F5597")
    r = 5
    r = block(ws, r, "A. VC method (the one VCs actually use)", [
        ("v_rev", "Revenue in exit year (₹ cr)", 300, CR, "Input", ILL, True),
        ("v_mult", "Exit EV / revenue multiple", 4, MULT1, "Input", "From listed peers or recent M&A", True),
        ("v_ev", "Exit value (₹ cr)", "={v_rev}*{v_mult}", CR, "Revenue × multiple", ""),
        ("v_tm", "Target MOIC for this stage", 10, MULT1, "Input", "Seed 20–30x; Series A ~10x; growth 3–5x", True),
        ("v_ret", "Ownership retained after future rounds", 0.60, PCT, "Input", "Future dilution", True),
        ("v_inv", "Investment this round (₹ cr)", 10, CR, "Input", ILL, True),
        ("v_post", "Maximum post-money (₹ cr)", "={v_ev}*{v_ret}/{v_tm}", CR, "Exit value × retention ÷ target MOIC", "", False, True),
        ("v_pre", "Maximum pre-money (₹ cr)", "={v_post}-{v_inv}", CR, "Post − investment", "", False, True),
        ("v_own", "Ownership you need now", "={v_inv}/{v_post}", PCT, "Investment ÷ post-money", "", False, True),
        ("v_yrs", "Years to exit", 6, YEARS, "Input", "", True),
        ("v_irr", "Implied IRR if the plan works", "={v_tm}^(1/{v_yrs})-1", PCT, "MOIC^(1 ÷ years) − 1", ""),
    ], wide=7)
    r = sec(ws, r, "B. Comparable companies (comps) — fictional peers", 2, 7)
    r = header(ws, r, ["Peer", "EV (₹ cr)", "Revenue (₹ cr)", "Revenue growth", "EV / Revenue", "Note"])
    peers = [("Listed Peer A", 4000, 800, 0.25), ("Listed Peer B", 2500, 400, 0.35), ("Recent round C", 9000, 1200, 0.20),
             ("Recent round D", 1800, 360, 0.40), ("Listed Peer E", 6000, 750, 0.30)]
    f0 = r
    for nm, ev, rev, g in peers:
        ws.cell(r, 2, nm).border = BOX
        setv(ws, r, 3, ev, CR0, None, True)
        setv(ws, r, 4, rev, CR0, None, True)
        setv(ws, r, 5, g, PCT, None, True)
        setv(ws, r, 6, f"=C{r}/D{r}", MULT1)
        ws.cell(r, 7, ILL).font = font(False, GREY)
        r += 1
    r = crow(ws, r, "v_med", "Median EV / revenue", f"=MEDIAN(F{f0}:F{r - 1})", MULT1, "Median of peers", "Median resists outliers", result=True, wide=7)
    r = crow(ws, r, "v_trev", "Target company revenue (₹ cr)", 60, CR, "Input", ILL, True, wide=7)
    r = crow(ws, r, "v_disc", "Private-company / size discount", 0.25, PCT, "Input", "Smaller, illiquid, riskier than peers", True, wide=7)
    r = crow(ws, r, "v_comp", "Comps value (₹ cr)", "={v_trev}*{v_med}*(1-{v_disc})", CR, "Revenue × median multiple × (1 − discount)", "Adjust up if growing faster than peers", result=True, wide=7)
    r += 1
    r = sec(ws, r, "C. Discounted cash flow (DCF) — for mature, predictable businesses", 2, 7)
    r = crow(ws, r, "v_w", "Discount rate (WACC)", 0.14, PCT, "Input", "Indian mid-size company ~12–15%", True, wide=7)
    r = crow(ws, r, "v_g", "Terminal growth rate", 0.05, PCT, "Input", "Keep below long-run nominal GDP growth", True, wide=7)
    r = header(ws, r, ["Year", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"])
    yc = [3, 4, 5, 6, 7]
    YL = [get_column_letter(c) for c in yc]
    fcf_r = r
    ws.cell(r, 2, "Free cash flow (₹ cr)").border = BOX
    for c, v in zip(yc, [-5, 2, 8, 15, 22]):
        setv(ws, r, c, v, CR, None, True)
    r += 1
    df_r = r
    ws.cell(r, 2, "Discount factor").border = BOX
    for i, c in enumerate(yc, start=1):
        setv(ws, r, c, f"=1/(1+{{v_w}})^{i}", "0.000")
    r += 1
    pv_r = r
    ws.cell(r, 2, "Present value (₹ cr)").border = BOX
    for x, c in zip(YL, yc):
        setv(ws, r, c, f"={x}{fcf_r}*{x}{df_r}", CR)
    r += 1
    r = crow(ws, r, "v_spv", "Sum of PV of cash flows (₹ cr)", f"=SUM(C{pv_r}:G{pv_r})", CR, "", "", wide=7)
    r = crow(ws, r, "v_tv", "Terminal value at year 5 (₹ cr)", f"=G{fcf_r}*(1+{{v_g}})/({{v_w}}-{{v_g}})", CR, "FCF5 × (1 + g) ÷ (WACC − g)", "Gordon growth formula", wide=7)
    r = crow(ws, r, "v_pvtv", "PV of terminal value (₹ cr)", f"={{v_tv}}*G{df_r}", CR, "TV × year-5 discount factor", "", wide=7)
    r = crow(ws, r, "v_dcf", "Enterprise value (₹ cr)", "={v_spv}+{v_pvtv}", CR, "PV of cash flows + PV of TV", "", result=True, wide=7)
    r = crow(ws, r, "v_tvs", "Share of value from terminal value", "={v_pvtv}/{v_dcf}", PCT, "", "Often 60–85% — DCF is very sensitive to it", wide=7)
    r += 1
    r = sec(ws, r, "D. Scorecard method (Bill Payne) — pre-revenue", 2, 7)
    r = crow(ws, r, "v_avg", "Average pre-money of comparable seed deals in the region (₹ cr)", 25, CR, "Input", ILL, True, wide=7)
    r = header(ws, r, ["Factor", "Weight", "This startup vs average", "Weighted factor"])
    sc = [("Strength of team", 0.30, 1.25), ("Size of opportunity", 0.25, 1.50), ("Product / technology", 0.15, 1.00),
          ("Competitive environment", 0.10, 0.75), ("Marketing / sales channels / partnerships", 0.10, 0.80),
          ("Need for additional investment", 0.05, 1.00), ("Other", 0.05, 1.00)]
    s0 = r
    for nm, w, cmp_ in sc:
        ws.cell(r, 2, nm).border = BOX
        setv(ws, r, 3, w, PCT, None, True)
        setv(ws, r, 4, cmp_, PCT, None, True)
        setv(ws, r, 5, f"=C{r}*D{r}", NUM2)
        r += 1
    r = crow(ws, r, "v_scsum", "Sum of weighted factors", f"=SUM(E{s0}:E{r - 1})", NUM2, "", "Above 1.0 = better than average deal", wide=7)
    r = crow(ws, r, "v_sc", "Scorecard pre-money (₹ cr)", "={v_avg}*{v_scsum}", CR, "Average pre-money × sum", "", result=True, wide=7)
    r += 1
    r = sec(ws, r, "E. Berkus method — pre-revenue (value each risk retired)", 2, 7)
    r = crow(ws, r, "v_bmax", "Maximum value per factor (₹ cr)", 2.0, CR, "Input", "Original method: up to $0.5M per factor; adapt to the market", True, wide=7)
    r = header(ws, r, ["Factor (risk reduced)", "Value assigned (₹ cr)", "Max allowed", "Check"])
    bk = [("Sound idea (basic value, product risk)", 1.5), ("Prototype (technology risk)", 1.0), ("Quality management team (execution risk)", 2.0),
          ("Strategic relationships (market risk)", 0.5), ("Product rollout or sales (production risk)", 0.5)]
    b0 = r
    for nm, v in bk:
        ws.cell(r, 2, nm).border = BOX
        setv(ws, r, 3, v, CR, None, True)
        setv(ws, r, 4, "={v_bmax}", CR)
        setv(ws, r, 5, f'=IF(C{r}>D{r},"Above max","OK")', GEN)
        r += 1
    r = crow(ws, r, "v_bk", "Berkus pre-money (₹ cr)", f"=SUM(C{b0}:C{r - 1})", CR, "Sum of factor values", "", result=True, wide=7)
    r += 1
    r = sec(ws, r, "F. First Chicago method — scenario-weighted", 2, 7)
    r = header(ws, r, ["Scenario", "Probability", "Exit equity value (₹ cr)", "Weighted (₹ cr)"])
    fc = [("Bull: category leader, IPO", 0.25, 3000), ("Base: solid company, strategic sale", 0.50, 1200), ("Bear: small acqui-hire / wind-down", 0.25, 100)]
    c0 = r
    for nm, p, v in fc:
        ws.cell(r, 2, nm).border = BOX
        setv(ws, r, 3, p, PCT, None, True)
        setv(ws, r, 4, v, CR0, None, True)
        setv(ws, r, 5, f"=C{r}*D{r}", CR)
        r += 1
    r = crow(ws, r, "v_fcp", "Probabilities total", f"=SUM(C{c0}:C{r - 1})", PCT, "Must equal 100%", "", wide=7)
    r = crow(ws, r, "v_fcw", "Expected exit value (₹ cr)", f"=SUM(E{c0}:E{r - 1})", CR, "Σ probability × value", "", wide=7)
    r = crow(ws, r, "v_fcr", "Discount rate", 0.40, PCT, "Input", "Early-stage risk", True, wide=7)
    r = crow(ws, r, "v_fcn", "Years to exit", 6, YEARS, "Input", "", True, wide=7)
    r = crow(ws, r, "v_fcret", "Ownership retained after future rounds", 0.60, PCT, "Input", "", True, wide=7)
    r = crow(ws, r, "v_fc", "First Chicago post-money today (₹ cr)", "={v_fcw}*{v_fcret}/(1+{v_fcr})^{v_fcn}", CR, "Expected value × retention ÷ (1 + r)^years", "", result=True, wide=7)
    r += 1
    r = sec(ws, r, "G. Triangulate", 2, 7)
    r = header(ws, r, ["Method", "Value (₹ cr)", "Basis"])
    tri = [("VC method (post-money)", "={v_post}", "Post-money"), ("Comps", "={v_comp}", "Enterprise value"), ("DCF", "={v_dcf}", "Enterprise value"),
           ("Scorecard", "={v_sc}", "Pre-money"), ("Berkus", "={v_bk}", "Pre-money"), ("First Chicago", "={v_fc}", "Post-money")]
    for nm, f, b in tri:
        ws.cell(r, 2, nm).border = BOX
        setv(ws, r, 3, f, CR)
        ws.cell(r, 4, b).font = font(False, GREY)
        r += 1
    r = note(ws, r, "Each method answers a different question and uses different example inputs here, so the numbers differ. In a real "
                    "deal you run 2–3 methods on the SAME company and look for a sensible range — then negotiate.", 2, 7)


def sheet_cap(wb):
    ws = new_sheet(wb, "11 Cap Table", "Cap table & dilution — seed and Series A with an option-pool shuffle",
                   "Change round sizes and valuations; watch ownership, share price and founder value move.",
                   [2, 40, 16, 12, 16, 12, 16, 12, 16, 30], tab="2F5597")
    r = 5
    r = block(ws, r, "1. Inputs", [
        ("ct_a", "Founder A shares at founding", 600000, NUM, "Input", "", True),
        ("ct_b", "Founder B shares at founding", 400000, NUM, "Input", "", True),
        ("ct_spre", "Seed pre-money (₹ cr)", 20, CR, "Input", "Headline pre-money", True),
        ("ct_sinv", "Seed investment (₹ cr)", 5, CR, "Input", "", True),
        ("ct_pool", "ESOP pool target (% of post-seed, created in the pre-money)", 0.10, PCT, "Input", "Investors usually ask for this", True),
        ("ct_apre", "Series A pre-money (₹ cr)", 100, CR, "Input", "", True),
        ("ct_ainv", "Series A investment (₹ cr)", 25, CR, "Input", "", True),
    ], wide=10)
    r = block(ws, r, "2. Calculations", [
        ("ct_f", "Founder shares", "={ct_a}+{ct_b}", NUM, "A + B", ""),
        ("ct_spost", "Seed post-money (₹ cr)", "={ct_spre}+{ct_sinv}", CR, "Pre + investment", ""),
        ("ct_spct", "Seed investor %", "={ct_sinv}/{ct_spost}", PCT, "Investment ÷ post", ""),
        ("ct_stot", "Total shares after seed", "={ct_f}/(1-{ct_pool}-{ct_spct})", NUM, "Founder shares ÷ (1 − pool % − seed %)", "Pool and seed shares are set as % of post"),
        ("ct_pshares", "ESOP pool shares", "={ct_pool}*{ct_stot}", NUM, "Pool % × total", ""),
        ("ct_sshares", "Seed investor shares", "={ct_spct}*{ct_stot}", NUM, "Seed % × total", ""),
        ("ct_sprice", "Seed price per share (₹)", "={ct_spost}*10000000/{ct_stot}", INR2, "Post-money ÷ total shares", "", False, True),
        ("ct_eff", "Effective pre-money for founders (₹ cr)", "={ct_sprice}*{ct_f}/10000000", CR, "Price × founder shares", "Lower than the headline pre-money: that's the option-pool shuffle", False, True),
        ("ct_apost", "Series A post-money (₹ cr)", "={ct_apre}+{ct_ainv}", CR, "Pre + investment", ""),
        ("ct_apct", "Series A investor %", "={ct_ainv}/{ct_apost}", PCT, "Investment ÷ post", ""),
        ("ct_atot", "Total shares after Series A", "={ct_stot}/(1-{ct_apct})", NUM, "Post-seed shares ÷ (1 − A %)", "No new pool in this round (simplification)"),
        ("ct_ashares", "Series A investor shares", "={ct_atot}-{ct_stot}", NUM, "New shares issued", ""),
        ("ct_aprice", "Series A price per share (₹)", "={ct_apost}*10000000/{ct_atot}", INR2, "Post-money ÷ total shares", "", False, True),
        ("ct_step", "Seed investor paper MOIC at Series A", "={ct_aprice}/{ct_sprice}", MULT, "A price ÷ seed price", "A mark-up, not cash (raises TVPI, not DPI)", False, True),
    ], wide=10)
    r = sec(ws, r, "3. Cap table", 2, 10)
    r = header(ws, r, ["Shareholder", "Shares at founding", "%", "Shares after seed", "%", "Shares after Series A", "%", "Value at Series A price (₹ cr)"])
    holders = [("Founder A", "={ct_a}", "={ct_a}", "={ct_a}"), ("Founder B", "={ct_b}", "={ct_b}", "={ct_b}"),
               ("ESOP pool", 0, "={ct_pshares}", "={ct_pshares}"), ("Seed investor", 0, "={ct_sshares}", "={ct_sshares}"),
               ("Series A investor", 0, 0, "={ct_ashares}")]
    h0 = r
    tot = h0 + len(holders)
    for nm, s0, s1, s2 in holders:
        ws.cell(r, 2, nm).font = font(True)
        ws.cell(r, 2).border = BOX
        setv(ws, r, 3, s0, NUM)
        setv(ws, r, 4, f"=C{r}/C${tot}", PCT)
        setv(ws, r, 5, s1, NUM)
        setv(ws, r, 6, f"=E{r}/E${tot}", PCT)
        setv(ws, r, 7, s2, NUM)
        setv(ws, r, 8, f"=G{r}/G${tot}", PCT)
        setv(ws, r, 9, f"=G{r}*{{ct_aprice}}/10000000", CR)
        r += 1
    ws.cell(r, 2, "Total").font = font(True)
    ws.cell(r, 2).fill = KEY
    for c, fmt in ((3, NUM), (4, PCT), (5, NUM), (6, PCT), (7, NUM), (8, PCT), (9, CR)):
        L = get_column_letter(c)
        setv(ws, r, c, f"=SUM({L}{h0}:{L}{r - 1})", fmt, None, False, True)
    r += 1
    r = crow(ws, r, "ct_fpct", "Founders together after Series A", f"=H{h0}+H{h0 + 1}", PCT, "", "Healthy if founders still hold ~50% after Series A", result=True, wide=10)
    r += 1
    r = block(ws, r, "4. SAFE / convertible conversion at the seed round (standalone example)", [
        ("sf_amt", "SAFE amount (₹ cr)", 2, CR, "Input", "Raised before the seed round", True),
        ("sf_cap", "Valuation cap (₹ cr)", 15, CR, "Input", "", True),
        ("sf_disc", "Discount", 0.20, PCT, "Input", "", True),
        ("sf_capp", "Cap price per share (₹)", "={sf_cap}*10000000/({ct_f}+{ct_pshares})", INR2, "Cap ÷ pre-money shares (founders + pool)", ""),
        ("sf_dp", "Discounted round price (₹)", "={ct_sprice}*(1-{sf_disc})", INR2, "Seed price × (1 − discount)", ""),
        ("sf_cp", "Conversion price (₹)", "=MIN({sf_capp},{sf_dp})", INR2, "Lower of cap price and discounted price", "", False, True),
        ("sf_sh", "Shares issued to SAFE holder", "={sf_amt}*10000000/{sf_cp}", NUM, "Amount ÷ conversion price", "", False, True),
        ("sf_which", "Which term applied?", '=IF({sf_capp}<{sf_dp},"Valuation cap","Discount")', GEN, "", "Simplified: real rounds also count SAFE shares in the pre-money, which moves the price slightly"),
    ], wide=10)
    r = sec(ws, r, "5. Founder dilution across a typical journey", 2, 10)
    r = header(ws, r, ["Event", "Dilution in this event", "Founders' stake after"])
    jour = [("Founding", None), ("Pre-seed", 0.10), ("Seed", 0.20), ("ESOP pool top-up", 0.08), ("Series A", 0.20), ("Series B", 0.15), ("Series C", 0.10)]
    j0 = r
    for i, (nm, d) in enumerate(jour):
        ws.cell(r, 2, nm).border = BOX
        if d is None:
            ws.cell(r, 3).border = BOX
            setv(ws, r, 4, 1.0, PCT, None, True)
        else:
            setv(ws, r, 3, d, PCT, None, True)
            setv(ws, r, 4, f"=D{r - 1}*(1-C{r})", PCT, None, False, i == len(jour) - 1)
        r += 1
    r = note(ws, r, "Each round multiplies the founders' stake by (1 − dilution). Typical founders own ~30–45% by Series C — "
                    "which is why VCs watch dilution early: founders must stay motivated.", 2, 10)


def sheet_waterfall(wb):
    ws = new_sheet(wb, "12 Waterfall", "Liquidation preference waterfall — who gets paid at exit",
                   "One investor (Series A) and everyone else (founders, ESOP, earlier investors as common). Change the inputs.",
                   [2, 44, 13, 13, 13, 13, 13, 13, 13, 30], tab="2F5597")
    r = 5
    r = block(ws, r, "Inputs", [
        ("w_inv", "Investor's investment (₹ cr)", 25, CR, "Input", "", True),
        ("w_own", "Investor's ownership if converted to equity", 0.20, PCT, "Input", "", True),
        ("w_mult", "Liquidation preference multiple", 1, MULT1, "Input", "1x is market standard", True),
        ("w_cap", "Participation cap (for the capped version)", 3, MULT1, "Input", "Total payout capped at this × investment", True),
        ("w_pref", "Preference amount (₹ cr)", "={w_inv}*{w_mult}", CR, "Investment × multiple", ""),
        ("w_ind", "Exit value where converting = taking preference (₹ cr)", "={w_pref}/{w_own}", CR, "Preference ÷ ownership", "Below this, the investor takes the preference", False, True),
    ], wide=10)
    cols = list(range(3, 10))
    L = [get_column_letter(c) for c in cols]
    r = header(ws, r, ["Scenario"] + [f"Exit {i}" for i in range(1, 8)] + ["What it shows"])
    ex_r = r
    ws.cell(r, 2, "Exit value (₹ cr)").font = font(True)
    for c, v in zip(cols, [20, 50, 100, 125, 200, 500, 1000]):
        setv(ws, r, c, v, CR0, None, True)
    r += 1

    def wrow(r, name, fs, fmt, how="", result=False):
        ws.cell(r, 2, name).font = font(result)
        ws.cell(r, 2).border = BOX
        ws.cell(r, 2).alignment = TOPWRAP
        if result:
            ws.cell(r, 2).fill = KEY
        for c, f in zip(cols, fs):
            setv(ws, r, c, f, fmt, None, False, result)
        x = ws.cell(r, 10, how)
        x.font = font(False, GREY)
        x.alignment = TOPWRAP
        fit(ws, r, 2, 10)
        return r + 1

    r = sec(ws, r, "A. 1x non-participating (market standard) — investor takes the HIGHER of preference or its % of the exit", 2, 10)
    a_r = r
    r = wrow(r, "Investor gets (₹ cr)", [f"=MAX(MIN({x}{ex_r},{{w_pref}}),{{w_own}}*{x}{ex_r})" for x in L], CR, "MAX(preference, ownership × exit)", True)
    r = wrow(r, "Founders & others get (₹ cr)", [f"={x}{ex_r}-{x}{a_r}" for x in L], CR, "Exit − investor")
    r = wrow(r, "Investor's share of exit", [f"={x}{a_r}/{x}{ex_r}" for x in L], PCT, "Above 20% at low exits = preference protecting the investor")
    r = wrow(r, "Investor converts or takes preference?", [f'=IF({{w_own}}*{x}{ex_r}>{{w_pref}},"Converts","Preference")' for x in L], GEN, "")
    r = wrow(r, "Investor MOIC", [f"={x}{a_r}/{{w_inv}}" for x in L], MULT, "")
    r = sec(ws, r, "B. Participating (no cap) — investor takes preference AND its % of what's left ('double dip')", 2, 10)
    b_r = r
    r = wrow(r, "Investor gets (₹ cr)", [f"=MIN({x}{ex_r},{{w_pref}})+{{w_own}}*MAX(0,{x}{ex_r}-{{w_pref}})" for x in L], CR, "Preference + ownership × (exit − preference)", True)
    r = wrow(r, "Founders & others get (₹ cr)", [f"={x}{ex_r}-{x}{b_r}" for x in L], CR, "Exit − investor")
    r = wrow(r, "Investor's share of exit", [f"={x}{b_r}/{x}{ex_r}" for x in L], PCT, "Always above 20% — founder-unfriendly")
    r = sec(ws, r, "C. Participating with a cap — participation stops at cap × investment, unless converting pays more", 2, 10)
    c_r = r
    r = wrow(r, "Investor gets (₹ cr)", [f"=MAX(MIN(MIN({x}{ex_r},{{w_pref}})+{{w_own}}*MAX(0,{x}{ex_r}-{{w_pref}}),{{w_cap}}*{{w_inv}}),{{w_own}}*{x}{ex_r})" for x in L], CR, "MAX(MIN(participating payout, cap), ownership × exit)", True)
    r = wrow(r, "Founders & others get (₹ cr)", [f"={x}{ex_r}-{x}{c_r}" for x in L], CR, "Exit − investor")
    r = note(ws, r, "Say it in the interview: 'With 1x non-participating, below a ₹125 cr exit the investor just gets its ₹25 cr back; "
                    "above ₹125 cr it converts and takes 20%. Participation makes the investor win twice, so founders resist it.'", 2, 10)


def sheet_terms(wb):
    ws = new_sheet(wb, "13 Term Sheet", "Term sheet decoder", "Every clause in plain words, what founders vs investors want, and the Indian market norm.",
                   [2, 30, 40, 30, 30, 40], tab="2F5597")
    r = 5
    r, hdr = table(ws, r, ["Clause", "What it means", "Founder-friendly version", "Investor-friendly version", "Indian market norm / note"], TERM_SHEET)
    r += 1
    r = sec(ws, r, "Anti-dilution worked example — a down round", 2, 6)
    r = crow(ws, r, "ad_cp1", "Series A conversion price (₹ per share)", 700, INR2, "Input", "Matches tab 11", True, wide=6)
    r = crow(ws, r, "ad_a", "Fully diluted shares before the new round (A)", 1785714, NUM, "Input", "Matches tab 11", True, wide=6)
    r = crow(ws, r, "ad_new", "New money raised in the down round (₹ cr)", 20, CR, "Input", "", True, wide=6)
    r = crow(ws, r, "ad_np", "Down-round price (₹ per share)", 500, INR2, "Input", "", True, wide=6)
    r = crow(ws, r, "ad_b", "Shares the new money would buy at the OLD price (B)", "={ad_new}*10000000/{ad_cp1}", NUM, "New money ÷ old price", "", wide=6)
    r = crow(ws, r, "ad_c", "Shares actually issued at the NEW price (C)", "={ad_new}*10000000/{ad_np}", NUM, "New money ÷ new price", "", wide=6)
    r = crow(ws, r, "ad_wa", "New conversion price — broad-based weighted average (₹)", "={ad_cp1}*({ad_a}+{ad_b})/({ad_a}+{ad_c})", INR2, "CP1 × (A + B) ÷ (A + C)", "Market standard: partial protection", result=True, wide=6)
    r = crow(ws, r, "ad_fr", "New conversion price — full ratchet (₹)", "={ad_np}", INR2, "Resets to the new price", "Harsh on founders", result=True, wide=6)
    r = crow(ws, r, "ad_inv", "Series A investment (₹ cr)", 25, CR, "Input", "", True, wide=6)
    r = crow(ws, r, "ad_s0", "Series A shares before adjustment", "={ad_inv}*10000000/{ad_cp1}", NUM, "Investment ÷ old price", "", wide=6)
    r = crow(ws, r, "ad_s1", "Series A shares after weighted-average adjustment", "={ad_inv}*10000000/{ad_wa}", NUM, "Investment ÷ new WA price", "", wide=6)
    r = crow(ws, r, "ad_s2", "Series A shares after full ratchet", "={ad_inv}*10000000/{ad_fr}", NUM, "Investment ÷ new price", "Extra shares come out of founders' and others' stakes", wide=6)


def sheet_fund(wb):
    ws = new_sheet(wb, "14 Fund Economics", "Fund economics — how a VC fund makes money",
                   "A fictional ₹200 cr early-stage fund: fees, portfolio construction, power-law outcomes, carry, LP waterfall, J-curve.",
                   [2, 46, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], tab="375623")
    r = 5
    W = 8
    r = block(ws, r, "1. Fund size, fees and portfolio construction", [
        ("fu_size", "Fund size / committed capital (₹ cr)", 200, CR, "Input", ILL, True),
        ("fu_f1", "Management fee during investment period (per year)", 0.02, PCT, "Input", "", True),
        ("fu_y1", "Investment period (years)", 5, YEARS, "Input", "", True),
        ("fu_f2", "Management fee after investment period (per year)", 0.015, PCT, "Input", "Fee usually steps down", True),
        ("fu_y2", "Remaining fund life (years)", 5, YEARS, "Input", "", True),
        ("fu_expp", "Set-up & fund expenses (% of fund, one-time)", 0.005, PCT, "Input", "Legal, admin, audit", True),
        ("fu_fees", "Total management fees over fund life (₹ cr)", "={fu_size}*({fu_f1}*{fu_y1}+{fu_f2}*{fu_y2})", CR, "Size × (fee1 × years1 + fee2 × years2)", "Pays the team and running costs"),
        ("fu_exp", "Fund expenses (₹ cr)", "={fu_size}*{fu_expp}", CR, "Size × expense %", ""),
        ("fu_inv", "Investable capital (₹ cr)", "={fu_size}-{fu_fees}-{fu_exp}", CR, "Size − fees − expenses", "Not all LP money reaches startups", False, True),
        ("fu_res", "Reserve ratio (kept for follow-ons)", 0.50, PCT, "Input", "Seed funds often 40–60%", True),
        ("fu_init", "Capital for first cheques (₹ cr)", "={fu_inv}*(1-{fu_res})", CR, "Investable × (1 − reserve)", ""),
        ("fu_resv", "Capital for follow-ons (₹ cr)", "={fu_inv}*{fu_res}", CR, "Investable × reserve", ""),
        ("fu_chq", "Average first cheque (₹ cr)", 3, CR, "Input", "", True),
        ("fu_n", "Number of portfolio companies", "={fu_init}/{fu_chq}", NUM1, "First-cheque capital ÷ cheque size", "", False, True),
        ("fu_eo", "Target ownership at entry", 0.12, PCT, "Input", "", True),
        ("fu_dil", "Dilution from entry to exit (after pro-rata)", 0.40, PCT, "Input", "", True),
        ("fu_xo", "Ownership at exit", "={fu_eo}*(1-{fu_dil})", PCT, "Entry × (1 − dilution)", ""),
        ("fu_ret", "Fund-returner exit value (₹ cr)", "={fu_size}/{fu_xo}", CR, "Fund size ÷ exit ownership", "One company must be able to reach this", False, True),
        ("fu_retusd", "Fund-returner exit value (US$ million)", "={fu_ret}*10/{fx}", USDM, "₹ cr × 10 ÷ ₹/$ (rate from tab 03)", ""),
    ], wide=W)
    r = sec(ws, r, "2. Power-law outcomes — how the portfolio actually returns money", 2, W)
    r = header(ws, r, ["Outcome bucket", "% of companies", "# companies", "MOIC on capital in them", "Capital deployed (₹ cr)", "Value returned (₹ cr)", "Share of all value"])
    buckets = [("Write-off", 0.45, 0), ("Return capital", 0.25, 1), ("Modest win", 0.15, 3), ("Big win", 0.10, 10), ("Outlier", 0.05, 30)]
    b0 = r
    bt = b0 + len(buckets)
    for nm, p, m in buckets:
        ws.cell(r, 2, nm).font = font(True)
        ws.cell(r, 2).border = BOX
        setv(ws, r, 3, p, PCT, None, True)
        setv(ws, r, 4, f"=C{r}*{{fu_n}}", NUM1)
        setv(ws, r, 5, m, MULT1, None, True)
        setv(ws, r, 6, f"=C{r}*{{fu_inv}}", CR)
        setv(ws, r, 7, f"=F{r}*E{r}", CR)
        setv(ws, r, 8, f"=G{r}/G${bt}", PCT)
        r += 1
    ws.cell(r, 2, "Total").font = font(True)
    ws.cell(r, 2).fill = KEY
    for c, fmt in ((3, PCT), (4, NUM1), (6, CR), (7, CR), (8, PCT)):
        Lc = get_column_letter(c)
        setv(ws, r, c, f"=SUM({Lc}{b0}:{Lc}{r - 1})", fmt, None, False, True)
    REG["fu_proc"] = (ws.title, f"G{r}")
    r += 1
    r = crow(ws, r, "fu_gm", "Gross MOIC on investable capital", "={fu_proc}/{fu_inv}", MULT, "Value returned ÷ investable", "", result=True, wide=W)
    r = crow(ws, r, "fu_carry_p", "Carried interest", 0.20, PCT, "Input", "", True, wide=W)
    r = crow(ws, r, "fu_profit", "Profit over committed capital (₹ cr)", "={fu_proc}-{fu_size}", CR, "Proceeds − fund size", "", wide=W)
    r = crow(ws, r, "fu_carry", "Carry to GP (₹ cr, simple)", "={fu_carry_p}*MAX(0,{fu_profit})", CR, "Carry % × profit", "See the waterfall below for the hurdle version", wide=W)
    r = crow(ws, r, "fu_net", "Net to LPs (₹ cr)", "={fu_proc}-{fu_carry}", CR, "Proceeds − carry", "", wide=W)
    r = crow(ws, r, "fu_tvpi", "Net TVPI / net MOIC to LPs", "={fu_net}/{fu_size}", MULT, "Net to LPs ÷ fund size", "Top-quartile VC: 3x+ net", result=True, wide=W)
    r = note(ws, r, "Power law: the 5% 'outliers' produce the largest share of all value (see 'Share of all value'). Remove them and the fund "
                    "barely returns capital. That's why every early-stage cheque must have fund-returner potential.", 2, W)
    r += 1
    r = sec(ws, r, "3. LP distribution waterfall (European / whole-fund) with an 8% hurdle and full GP catch-up", 2, W)
    r = crow(ws, r, "lw_paid", "Paid-in capital (₹ cr)", "={fu_size}", CR, "", "Assumes the full fund is called", wide=W)
    r = crow(ws, r, "lw_dist", "Total distributions available (₹ cr)", "={fu_proc}", CR, "From section 2", "", wide=W)
    r = crow(ws, r, "lw_h", "Hurdle (preferred return) per year", 0.08, PCT, "Input", "", True, wide=W)
    r = crow(ws, r, "lw_y", "Average years capital is outstanding", 6, YEARS, "Input", "Simplification of timing", True, wide=W)
    r = crow(ws, r, "lw_pref", "Preferred return owed to LPs (₹ cr)", "={lw_paid}*((1+{lw_h})^{lw_y}-1)", CR, "Capital × ((1 + hurdle)^years − 1)", "", wide=W)
    r = crow(ws, r, "lw_t1", "Tier 1 — return of capital to LPs (₹ cr)", "=MIN({lw_dist},{lw_paid})", CR, "", "", wide=W)
    r = crow(ws, r, "lw_t2", "Tier 2 — preferred return to LPs (₹ cr)", "=MIN({lw_dist}-{lw_t1},{lw_pref})", CR, "", "", wide=W)
    r = crow(ws, r, "lw_t3", "Tier 3 — GP catch-up (₹ cr)", "=MIN({lw_dist}-{lw_t1}-{lw_t2},{lw_t2}*{fu_carry_p}/(1-{fu_carry_p}))", CR, "Until GP has 20% of profits so far", "", wide=W)
    r = crow(ws, r, "lw_t4", "Tier 4 — remaining profit to split 80/20 (₹ cr)", "={lw_dist}-{lw_t1}-{lw_t2}-{lw_t3}", CR, "", "", wide=W)
    r = crow(ws, r, "lw_lp", "Total to LPs (₹ cr)", "={lw_t1}+{lw_t2}+{lw_t4}*(1-{fu_carry_p})", CR, "Tiers 1 + 2 + 80% of tier 4", "", result=True, wide=W)
    r = crow(ws, r, "lw_gp", "Total carry to GP (₹ cr)", "={lw_t3}+{lw_t4}*{fu_carry_p}", CR, "Tier 3 + 20% of tier 4", "", result=True, wide=W)
    r = crow(ws, r, "lw_chk", "GP share of total profit", "={lw_gp}/({lw_dist}-{lw_paid})", PCT, "Should equal carry % once fully caught up", "", wide=W)
    r += 1
    r = sec(ws, r, "4. Fund cash flows, J-curve and IRR", 2, 13)
    yc = list(range(3, 13))
    YL = [get_column_letter(c) for c in yc]
    r = header(ws, r, ["₹ cr"] + [f"Year {i}" for i in range(1, 11)] + ["Total"])
    calls = [-40, -40, -35, -35, -25, -25, 0, 0, 0, 0]
    dists = [0, 0, 0, 10, 20, 40, 80, 120, 130, 125]
    rows = {}
    for nm, vals, k in (("Capital calls (paid in)", calls, "c"), ("Distributions to LPs", dists, "d")):
        ws.cell(r, 2, nm).border = BOX
        for c, v in zip(yc, vals):
            setv(ws, r, c, v, CR0, None, True)
        setv(ws, r, 13, f"=SUM(C{r}:L{r})", CR0)
        rows[k] = r
        r += 1
    ws.cell(r, 2, "Net cash flow").border = BOX
    for x, c in zip(YL, yc):
        setv(ws, r, c, f"={x}{rows['c']}+{x}{rows['d']}", CR0)
    rows["n"] = r
    r += 1
    ws.cell(r, 2, "Cumulative net cash flow (the J-curve)").font = font(True)
    ws.cell(r, 2).fill = KEY
    for i, (x, c) in enumerate(zip(YL, yc)):
        setv(ws, r, c, f"={x}{rows['n']}" if i == 0 else f"={YL[i - 1]}{r}+{x}{rows['n']}", CR0, None, False, True)
    r += 1
    r = crow(ws, r, "fu_irr", "Fund IRR", f"=IRR(C{rows['n']}:L{rows['n']})", PCT, "Excel IRR on yearly net cash flows", "Dips negative early, then climbs: the J-curve", result=True, wide=W)
    r = crow(ws, r, "fu_m", "Fund cash multiple (distributions ÷ paid in)", f"=M{rows['d']}/-M{rows['c']}", MULT, "", "", wide=W)
    r = crow(ws, r, "fu_nav6", "NAV of remaining holdings at end of year 6 (₹ cr)", 380, CR, "Input", "Fair value of unsold stakes", True, wide=W)
    r = crow(ws, r, "fu_dpi6", "DPI at year 6", f"=SUM(C{rows['d']}:H{rows['d']})/-SUM(C{rows['c']}:H{rows['c']})", MULT, "Distributions ÷ paid-in so far", "Real cash back", wide=W)
    r = crow(ws, r, "fu_rvpi6", "RVPI at year 6", f"={{fu_nav6}}/-SUM(C{rows['c']}:H{rows['c']})", MULT, "NAV ÷ paid-in", "Paper value", wide=W)
    r = crow(ws, r, "fu_tvpi6", "TVPI at year 6", "={fu_dpi6}+{fu_rvpi6}", MULT, "DPI + RVPI", "", result=True, wide=W)
    r += 1
    r = sec(ws, r, "5. MOIC → IRR grid (why time matters)", 2, W)
    r = header(ws, r, ["MOIC ↓ / years →", "3 years", "5 years", "7 years", "10 years"])
    yrs_r = r
    ws.cell(r, 2, "Years (input)").font = font(False, GREY)
    for c, y in zip([3, 4, 5, 6], [3, 5, 7, 10]):
        setv(ws, r, c, y, NUM, None, True)
    r += 1
    for m in [2, 3, 5, 10, 20]:
        setv(ws, r, 2, m, MULT1, None, True, align="left")
        for c in [3, 4, 5, 6]:
            Lc = get_column_letter(c)
            setv(ws, r, c, f"=B{r}^(1/{Lc}${yrs_r})-1", PCT)
        r += 1


def sheet_fin(wb):
    ws = new_sheet(wb, "15 Financial Statements", "Reading startup financial statements (linked P&L, balance sheet, cash flow)",
                   "Fictional D2C brand, FY26, ₹ crore. The three statements tie together — the check row shows whether they do.",
                   [2, 46, 16, 70], tab="7F6000")
    r = 5
    r = block(ws, r, "1. Profit & loss (FY26)", [
        ("p_rev", "Revenue from operations", 40, CR, "Input", "Net of GST, discounts, returns", True),
        ("p_cogs", "Cost of goods sold", 14, CR, "Input", "", True),
        ("p_gp", "Gross profit", "={p_rev}-{p_cogs}", CR, "Revenue − COGS", "", False, True),
        ("p_gm", "Gross margin", "={p_gp}/{p_rev}", PCT, "", ""),
        ("p_emp", "Employee benefit expense", 8, CR, "Input", "Includes ESOP cost (non-cash)", True),
        ("p_mkt", "Marketing & advertising", 12, CR, "Input", "", True),
        ("p_log", "Logistics & fulfilment", 4, CR, "Input", "", True),
        ("p_oth", "Other expenses (rent, tech, admin)", 4, CR, "Input", "", True),
        ("p_ebitda", "EBITDA", "={p_gp}-{p_emp}-{p_mkt}-{p_log}-{p_oth}", CR, "Gross profit − operating expenses", "", False, True),
        ("p_ebm", "EBITDA margin", "={p_ebitda}/{p_rev}", PCT, "", ""),
        ("p_da", "Depreciation & amortisation", 1, CR, "Input", "", True),
        ("p_ebit", "EBIT", "={p_ebitda}-{p_da}", CR, "EBITDA − D&A", ""),
        ("p_fin", "Finance costs", 0.5, CR, "Input", "Interest on debt", True),
        ("p_oi", "Other income", 0.8, CR, "Input", "Interest on deposits — not operating!", True),
        ("p_pbt", "Profit before tax", "={p_ebit}-{p_fin}+{p_oi}", CR, "", ""),
        ("p_tax", "Tax", 0, CR, "Input", "Nil — carried-forward losses", True),
        ("p_pat", "Profit after tax (PAT)", "={p_pbt}-{p_tax}", CR, "", "", False, True),
    ])
    r = block(ws, r, "2. Cash flow statement (FY26)", [
        ("cf_pat", "Profit after tax", "={p_pat}", CR, "From P&L", ""),
        ("cf_da", "Add back D&A (non-cash)", "={p_da}", CR, "From P&L", ""),
        ("cf_wc", "Change in working capital", -3.5, CR, "Input", "Negative = more cash tied in stock/receivables", True),
        ("cf_cfo", "Cash flow from operations (CFO)", "={cf_pat}+{cf_da}+{cf_wc}", CR, "", "", False, True),
        ("cf_capex", "Capex", -1.5, CR, "Input", "", True),
        ("cf_cfi", "Cash flow from investing (CFI)", "={cf_capex}", CR, "", ""),
        ("cf_eq", "Equity raised", 20, CR, "Input", "Series A money", True),
        ("cf_debt", "Debt raised / (repaid)", 2, CR, "Input", "", True),
        ("cf_cff", "Cash flow from financing (CFF)", "={cf_eq}+{cf_debt}", CR, "", ""),
        ("cf_net", "Net change in cash", "={cf_cfo}+{cf_cfi}+{cf_cff}", CR, "CFO + CFI + CFF", ""),
        ("cf_open", "Opening cash", 10.7, CR, "Input", "", True),
        ("cf_close", "Closing cash", "={cf_open}+{cf_net}", CR, "Opening + net change", "Flows to the balance sheet", False, True),
    ])
    r = block(ws, r, "3. Balance sheet (31 March 2026)", [
        ("b_cap", "Share capital + securities premium (all equity raised)", 60, CR, "Input", "", True),
        ("b_open", "Opening reserves (accumulated losses)", -25.3, CR, "Input", "", True),
        ("b_res", "Closing reserves & surplus", "={b_open}+{p_pat}", CR, "Opening + PAT", "Links to P&L"),
        ("b_nw", "Net worth (shareholders' funds)", "={b_cap}+{b_res}", CR, "", ""),
        ("b_debt", "Borrowings", 5, CR, "Input", "", True),
        ("b_pay", "Trade payables", 3, CR, "Input", "", True),
        ("b_ocl", "Other current liabilities", 2, CR, "Input", "", True),
        ("b_tl", "Total equity & liabilities", "={b_nw}+{b_debt}+{b_pay}+{b_ocl}", CR, "", "", False, True),
        ("b_fa", "Fixed assets (net)", 4, CR, "Input", "", True),
        ("b_inv", "Inventory", 3, CR, "Input", "", True),
        ("b_rec", "Trade receivables", 4, CR, "Input", "", True),
        ("b_cash", "Cash & bank", "={cf_close}", CR, "From cash flow statement", ""),
        ("b_oca", "Other current assets", 5, CR, "Input", "Deposits, GST input credit, advances", True),
        ("b_ta", "Total assets", "={b_fa}+{b_inv}+{b_rec}+{b_cash}+{b_oca}", CR, "", "", False, True),
        ("b_chk", "Check: assets − liabilities (should be 0)", "=ROUND({b_ta}-{b_tl},2)", CR, "", "If not zero, a number doesn't tie — exactly what diligence catches. Change inputs in matching pairs."),
    ])
    r = block(ws, r, "4. Ratios an associate pulls from these statements", [
        ("fs_burn", "Monthly net burn (operating + investing)", "=-({cf_cfo}+{cf_cfi})/12", CR, "−(CFO + CFI) ÷ 12", ""),
        ("fs_run", "Runway at that burn", "={b_cash}/{fs_burn}", MONTHS, "Cash ÷ monthly burn", "", False, True),
        ("fs_dio", "Inventory days", "={b_inv}/{p_cogs}*365", DAYS, "Inventory ÷ COGS × 365", "Packaged food 30–60 days; above 90 is a flag (expiry, dead stock)"),
        ("fs_dso", "Receivable days", "={b_rec}/{p_rev}*365", DAYS, "Receivables ÷ revenue × 365", ""),
        ("fs_mktp", "Marketing as % of revenue", "={p_mkt}/{p_rev}", PCT, "", "30% is heavy; should fall with scale"),
        ("fs_de", "Debt / equity", "={b_debt}/{b_nw}", MULT, "Borrowings ÷ net worth", ""),
    ])
    r = sec(ws, r, "5. Red flags when reading startup financials", 2, 4)
    flags = [
        ("GMV shown as revenue", "Ask for revenue as per audited financials (Ind AS 115)"),
        ("Revenue growing but receivables growing faster", "Customers aren't paying, or sales are pushed (channel stuffing)"),
        ("Inventory piling up", "Slow-moving or dead stock; check ageing"),
        ("Big 'other income'", "Profit from interest on deposits, not from the business"),
        ("Capitalised R&D or marketing", "Expenses moved to the balance sheet to make P&L look better"),
        ("Related-party transactions", "Sales to or purchases from founders' other companies"),
        ("MIS numbers don't match audited numbers", "Integrity or process issue — ask why"),
        ("Auditor qualifications / frequent auditor changes", "Serious governance flag"),
        ("Short-term debt funding long-term assets", "Liquidity risk"),
        ("Delayed statutory dues (GST, TDS, PF)", "Cash stress and legal risk"),
    ]
    r, _ = table(ws, r, ["Red flag", "What it might mean"], flags)
    r += 1
    r = sec(ws, r, "6. Where to find Indian private-company financials", 2, 4)
    src = [("MCA21 (Ministry of Corporate Affairs)", "Annual filings (AOC-4, MGT-7) of every Indian company"), ("Tofler / PrivateCircle / Tracxn", "Paid platforms that clean up MCA data"),
           ("Entrackr / Inc42 / The Ken", "Coverage of startup annual results"), ("Company data room", "Monthly MIS, audited accounts, management accounts during diligence")]
    r, _ = table(ws, r, ["Source", "What you get"], src)


def sheet_process(wb):
    ws = new_sheet(wb, "16 Deal Process", "The deal process — and what the associate does at each step",
                   "From first email to exit, plus how the money moves and where it gets spent in each sector.",
                   [2, 24, 40, 44, 30, 18], tab="7030A0")
    r = 5
    r = sec(ws, r, "1. Ten steps of a VC deal", 2, 6)
    r, _ = table(ws, r, ["Step", "What happens", "Associate's job", "Output / document", "Typical time"], DEAL_PROCESS)
    r += 1
    r = sec(ws, r, "2. Quick screening checklist (first 15 minutes with a deck)", 2, 6)
    scr = [("Thesis fit", "Sector, stage, geography and cheque size match the fund?"), ("Team", "Founder–market fit; full-time; complementary skills?"),
           ("Problem", "Painful, frequent, expensive problem? Who has it?"), ("Market", "Can this be a ₹2,500 cr+ company?"),
           ("Traction", "Revenue, growth, retention, pilots — what's real?"), ("Business model", "How it makes money; unit-economics sanity"),
           ("Round", "Amount, valuation expectation, who else is in, runway after the round"), ("Red flags", "Messy cap table, legal issues, inconsistent numbers, no focus")]
    r, _ = table(ws, r, ["Check", "Question"], scr)
    r += 1
    r = sec(ws, r, "3. How the money flows", 2, 6)
    r, _ = table(ws, r, ["Step", "What happens", "Detail"], MONEY_FLOW)
    r += 1
    r = sec(ws, r, "4. Where the money goes in each sector (typical use of funds)", 2, 6)
    r, _ = table(ws, r, ["Sector", "Where the money mostly goes", "How it is released", "What the investor tracks"], USE_OF_FUNDS)
    r += 1
    r = sec(ws, r, "5. What the fund monitors after investing (monthly MIS)", 2, 6)
    mis = [("Every company", "Revenue, gross margin, burn, runway, cash, headcount, key hires, top risks"),
           ("SaaS", "ARR, net new ARR, NRR, logo churn, pipeline, CAC payback"),
           ("Consumer", "Net revenue by channel, CM2 by channel, repeat rate, CAC, inventory days"),
           ("Deep tech", "Milestones vs plan, pilots and conversions, BOM, certification status"),
           ("Healthcare", "Patients/tests, utilisation, centre-level EBITDA, approvals, clinical milestones"),
           ("Manufacturing", "Order book, utilisation, EBITDA margin, OEE, receivable days")]
    r, _ = table(ws, r, ["Company type", "KPIs to track monthly"], mis)


def sheet_market(wb):
    ws = new_sheet(wb, "17 Market Sizing", "Market sizing — TAM, SAM, SOM (live)",
                   "Top-down and bottom-up examples. Every input is an assumption: state it out loud in the interview.",
                   [2, 50, 18, 46, 52], tab="BF8F00")
    r = 5
    r = block(ws, r, "A. Top-down (consumer): healthy packaged snacks in urban India", [
        ("ms_hh", "Urban households (crore)", 10, NUM1, "Input", "Assumption — verify with Census/NFHS-based estimates", True),
        ("ms_pct", "Share that buy packaged 'healthy' snacks", 0.25, PCT, "Input", "Assumption", True),
        ("ms_sp", "Annual spend per buying household (₹)", 2400, INR, "Input", "₹200 a month — assumption", True),
        ("ms_tam", "TAM (₹ cr)", "={ms_hh}*{ms_pct}*{ms_sp}", CR0, "Households (cr) × share × spend", "₹ cr because households are already in crore", False, True),
        ("ms_samp", "Share reachable via online + quick commerce + metro modern trade", 0.35, PCT, "Input", "Assumption", True),
        ("ms_sam", "SAM (₹ cr)", "={ms_tam}*{ms_samp}", CR0, "TAM × reachable share", "", False, True),
        ("ms_somp", "Market share achievable in 5 years", 0.05, PCT, "Input", "Assumption", True),
        ("ms_som", "SOM — revenue potential in 5 years (₹ cr)", "={ms_sam}*{ms_somp}", CR0, "SAM × share", "", False, True),
    ])
    r = block(ws, r, "B. Bottom-up (B2B): practice-management software for small clinics", [
        ("ms_cl", "Small clinics & nursing homes (number)", 150000, NUM, "Input", "Assumption — validate before using", True),
        ("ms_price", "Price per clinic per year (₹)", 30000, INR, "Input", "", True),
        ("ms_tam2", "TAM (₹ cr)", "={ms_cl}*{ms_price}/10000000", CR0, "Clinics × price", "", False, True),
        ("ms_dig", "Share that are digitally ready (urban, use software)", 0.40, PCT, "Input", "", True),
        ("ms_sam2", "SAM (₹ cr)", "={ms_tam2}*{ms_dig}", CR0, "TAM × reachable", "", False, True),
        ("ms_win", "Share won in 5 years", 0.10, PCT, "Input", "", True),
        ("ms_som2", "SOM (₹ cr)", "={ms_sam2}*{ms_win}", CR0, "SAM × share", "Small: India-only SMB SaaS often needs payments, supplies or global markets to be venture-scale", False, True),
    ])
    r = block(ws, r, "C. Venture-scale check — can the leader here be a fund returner?", [
        ("ms_mult", "Revenue multiple at exit", 3, MULT1, "Input", "Consumer brands", True),
        ("ms_val", "Implied company value from SOM (₹ cr)", "={ms_som}*{ms_mult}", CR0, "SOM × multiple", ""),
        ("ms_fr", "Fund-returner exit needed (₹ cr)", "={fu_ret}", CR0, "From tab 14", ""),
        ("ms_v", "Verdict", '=IF({ms_val}>={ms_fr},"Venture-scale: can return the fund","Too small unless the company expands beyond this market")', GEN, "", ""),
    ])
    r = sec(ws, r, "D. How to answer any guesstimate in the interview", 2, 5)
    steps = [("1. Clarify", "Which geography, which customer, which year, revenue or volume?"),
             ("2. Choose the method", "Top-down (population → share → spend) or bottom-up (number of buyers × price × frequency). Do both if time allows."),
             ("3. Segment", "Split by city tier, income, age or business size — shows structured thinking."),
             ("4. State assumptions", "Round numbers, say them out loud, and explain why each is reasonable."),
             ("5. Calculate", "Keep the maths simple; write it down."),
             ("6. Sanity-check", "Compare with a known number (e.g., a listed company's revenue)."),
             ("7. So what?", "Is it venture-scale? What does it mean for the startup?")]
    r, _ = table(ws, r, ["Step", "What to do"], steps)


def sheet_landscape(wb):
    ws = new_sheet(wb, "18 India Landscape", "Indian VC landscape and 2026 themes",
                   "Who's who in Indian venture capital, government programmes, research sources and themes to have a view on.",
                   [2, 30, 60, 60], tab="BF8F00")
    r = 5
    r = sec(ws, r, "1. Who's who", 2, 4)
    r, _ = table(ws, r, ["Type", "Names", "Focus / notes"], INDIA_LANDSCAPE)
    r += 1
    r = sec(ws, r, "2. Themes to have a view on (check the latest numbers tonight in Tracxn / Inc42)", 2, 4)
    r, _ = table(ws, r, ["Theme", "What's happening", "Your investor angle"], THEMES)


def sheet_qa(wb):
    ws = new_sheet(wb, "19 Interview Q&A", f"Interview Q&A — {len(QA)} questions",
                   "Practise each answer out loud in ~90 seconds. Mark your progress in the last column.",
                   [2, 6, 20, 40, 26, 40, 70, 14], tab="C00000")
    rows = [(i, *q) for i, q in enumerate(QA, start=1)]
    rows = [(i, c, q, t, h, a, "Not yet") for (i, c, q, t, h, a) in rows]
    r, hdr = table(ws, 5, ["#", "Category", "Question", "What he's testing", "How to structure", "Sample answer / key points", "Practised?"], rows,
                   bold_first=False, input_cols=(6,))
    for rr in range(hdr + 1, r):
        ws.cell(rr, 4).font = font(True)
    dv = DataValidation(type="list", formula1='"Not yet,Practised,Confident"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"H{hdr + 1}:H{r - 1}")
    ws.freeze_panes = ws.cell(hdr + 1, 5)
    ws.auto_filter.ref = f"B{hdr}:H{r - 1}"


def sheet_cases(wb):
    ws = new_sheet(wb, "20 Mini Cases", "Mini cases — worked answers",
                   "Use the 6-step framework on every case. Numbers for cases 2 and 3 tie to tabs 05 and 06.",
                   [2, 28, 34, 44, 60, 50], tab="C00000")
    r = 5
    r = sec(ws, r, "The 6-step case framework", 2, 6)
    r, _ = table(ws, r, ["Step", "What to do"], CASE_FRAMEWORK)
    r += 1
    r = sec(ws, r, "Five cases", 2, 6)
    r, _ = table(ws, r, ["Case", "Situation", "Numbers given", "Step-by-step analysis", "Verdict / what to say"], CASES)


def sheet_ic(wb):
    ws = new_sheet(wb, "21 IC Memo", "Investment committee (IC) memo template",
                   "Recommendation first. Column D is a worked example (fictional); use column E to draft one for a company you like.",
                   [2, 30, 50, 50, 50], tab="7030A0")
    rows = [(a, b, c, "") for a, b, c in IC_MEMO]
    table(ws, 5, ["Section", "What to write", "Example (fictional AeroSense)", "Your draft"], rows, input_cols=(3,))


def sheet_dd(wb):
    ws = new_sheet(wb, "22 DD Checklist", "Due diligence checklist", "Use the Status dropdown to track progress on a live deal.",
                   [2, 20, 60, 34, 16, 30], tab="7030A0")
    rows = [(a, b, c, "Not started", "") for a, b, c in DD_CHECKLIST]
    r, hdr = table(ws, 5, ["Area", "Item", "Why it matters", "Status", "Notes"], rows, input_cols=(3, 4))
    dv = DataValidation(type="list", formula1='"Not started,In progress,Done,Issue found"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"E{hdr + 1}:E{r - 1}")
    ws.freeze_panes = ws.cell(hdr + 1, 3)
    ws.auto_filter.ref = f"B{hdr}:F{r - 1}"


def sheet_firm(wb):
    ws = new_sheet(wb, "23 Firm & Questions", "The firm, the CEO and your questions",
                   "Fill the yellow cells tonight. Then pick 3–4 questions to ask at the end.",
                   [2, 44, 50, 60], tab="C00000")
    r = 5
    r = sec(ws, r, "1. Firm research (fill in tonight)", 2, 4)
    r, _ = table(ws, r, ["What to find", "Your notes", "Where / why"], FIRM_RESEARCH, input_cols=(1,))
    r += 1
    r = sec(ws, r, "2. Questions to ask Chandru (pick 3–4)", 2, 4)
    r, _ = table(ws, r, ["Theme", "Question"], QUESTIONS_TO_ASK)
    r += 1
    r = sec(ws, r, "3. Your 90-second 'tell me about yourself' (draft it here)", 2, 4)
    for lab in ("Present: what I do now (role, company, one result with a number)", "Past: 1–2 experiences that taught me how businesses make money",
                "Why investing: what pulls me to VC", "Why this firm / new arm: one specific reason", "Closing line"):
        ws.cell(r, 2, lab).font = font(True)
        ws.cell(r, 2).alignment = TOPWRAP
        ws.cell(r, 2).border = BOX
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        c = ws.cell(r, 3, "")
        c.fill = INP
        c.border = BOX
        ws.row_dimensions[r].height = 42
        r += 1
    r += 1
    r = sec(ws, r, "4. Avoid these", 2, 4)
    for line in DONT_DO:
        r = note(ws, r, "✗ " + line, 2, 4, f=None)


def main(out):
    wb = Workbook()
    wb.remove(wb.active)
    sheet_start(wb)
    sheet_vc(wb)
    sheet_glossary(wb)
    sheet_lab(wb)            # registers fx (₹/$) used later
    sheet_consumer(wb)
    # deep tech needs pre-seed refs resolved before the valuation block is written; build in two passes
    build_deeptech(wb)
    sheet_health(wb)
    sheet_sectors(wb)
    sheet_founder(wb)
    sheet_mfg(wb)
    sheet_valuation(wb)
    sheet_cap(wb)
    sheet_waterfall(wb)
    sheet_terms(wb)
    sheet_fund(wb)
    sheet_fin(wb)
    sheet_process(wb)
    sheet_market(wb)
    sheet_landscape(wb)
    sheet_qa(wb)
    sheet_cases(wb)
    sheet_ic(wb)
    sheet_dd(wb)
    sheet_firm(wb)
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.value is not None and c.font is not None and c.font.name != FONT:
                    c.font = font()
    wb.active = 0
    wb.save(out)
    print("saved", out, "sheets:", len(wb.sheetnames))


def build_deeptech(wb):
    # The pre-seed row (plan index 2) registers dt_pre2 while section 2 is written; section 4 then needs
    # dt_amt_pre, which we register right after section 2 by hooking REG lookups lazily.
    orig_fx = globals()["fx"]

    def lazy_fx(s, sheet):
        if "{dt_amt_pre}" in s and "dt_amt_pre" not in REG:
            fix_deeptech_refs()
        return orig_fx(s, sheet)

    globals()["fx"] = lazy_fx
    try:
        sheet_deeptech(wb)
    finally:
        globals()["fx"] = orig_fx


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "VC-Investment-Associate-Prep.xlsx")
