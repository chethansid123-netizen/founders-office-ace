"""Kishlay modern-trade-first plan: live Excel model (fix EBITDA first, then scale with the market).
Usage: python3 build_mt_model.py <out.xlsx>
Blue = input (with basis and source) · black = formula · green = link to another sheet · yellow = validate first.
"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

OUT = sys.argv[1] if len(sys.argv) > 1 else 'Kishlay-MT-Model.xlsx'
F = 'Arial'
BLUE = Font(name=F, size=10, color='0000FF')
BLK = Font(name=F, size=10, color='000000')
GRN = Font(name=F, size=10, color='008000')
BOLD = Font(name=F, size=10, bold=True)
HDR = Font(name=F, size=10, bold=True, color='FFFFFF')
TITLE = Font(name=F, size=14, bold=True, color='C8141C')
SUB = Font(name=F, size=10, italic=True, color='5E5147')
INK = PatternFill('solid', fgColor='1E1712')
SAND = PatternFill('solid', fgColor='FBF3E6')
YEL = PatternFill('solid', fgColor='FFFF00')
GREY = PatternFill('solid', fgColor='F2EEE8')
THIN = Side(style='thin', color='D9CBB5')
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
WRAP = Alignment(wrap_text=True, vertical='top')
CR = '#,##0.0;(#,##0.0);"-"'
CR2 = '#,##0.00;(#,##0.00);"-"'
PCT = '0.0%;(0.0%);"-"'
INT = '#,##0;(#,##0);"-"'
RS = '"₹"#,##0;("₹"#,##0);"-"'
RS2 = '"₹"#,##0.00;("₹"#,##0.00);"-"'
MULT = '0.00"x"'

wb = Workbook()


def sheet(nm, title, subtitle, widths):
    ws = wb.create_sheet(nm)
    ws['A1'] = title
    ws['A1'].font = TITLE
    ws['A2'] = subtitle
    ws['A2'].font = SUB
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.sheet_view.showGridLines = False
    return ws


def header(ws, row, labels):
    for i, lab in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=lab)
        c.font = HDR
        c.fill = INK
        c.alignment = Alignment(wrap_text=True, vertical='center')
        c.border = BOX


def put(ws, ref, val, font=BLK, fmt=None, fill=None, wrap=False, bold=False):
    c = ws[ref]
    c.value = val
    c.font = Font(name=F, size=10, bold=bold, color=font.color) if bold else font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if wrap:
        c.alignment = WRAP
    c.border = BOX
    return c


def name(n, ref):
    wb.defined_names[n] = DefinedName(n, attr_text=ref)


YEARS = ['FY25A', 'FY26E', 'FY27E', 'FY28P', 'FY29P', 'FY30P', 'FY31P']
YC = 'BCDEFGH'  # year columns on time-series sheets

# =====================================================================================  Inputs
inp = sheet('Inputs', 'Inputs and scenario levers',
            'Change B3: 1 Slow, 2 Base, 3 Fast. Blue = input; yellow = validate first. Revenue grows with the market; modern trade (MT) is the focus, quick commerce (QC) second.',
            [14, 54, 11, 11, 11, 12, 11, 13, 92])
put(inp, 'A3', 'Scenario', bold=True)
put(inp, 'B3', 2, BLUE, fill=YEL)
inp['B3'].number_format = '0'
put(inp, 'C3', '=CHOOSE(B3,"Slow","Base","Fast")')
dv = DataValidation(type='whole', operator='between', formula1='1', formula2='3')
inp.add_data_validation(dv)
dv.add('B3')
name('Scenario', 'Inputs!$B$3')
header(inp, 5, ['ID', 'Parameter', 'Slow', 'Base', 'Fast', 'Active', 'Unit', 'Label', 'Basis and source'])
INPUTS = [
    ('A', 'Company baseline'),
    ('Rev_FY25', 'FY25 revenue, Kishlay Foods Pvt Ltd (actual)', 288, 288, 288, '₹ Cr', 'External', 'Tracxn profile from the MCA filing: ₹288 Cr, −16% YoY, net loss ₹6.31 Cr [V08].', True, CR),
    ('g_FY26', 'Revenue growth FY26 (recovery after FY25’s −16%)', 0.0, 0.08, 0.12, '%', 'Hypothesis', 'FY26 not public; Tulsi headcount +15% YoY (Feb 2026) suggests recovery [V08]. Replace with FY26 sales.', True, PCT),
    ('g_mkt', 'Revenue growth FY27–FY31 = the market', 0.08, 0.10, 0.12, '%', 'Hypothesis', 'Brief: grow with the market. Savoury-snack category growth estimates 8–12% a year [V24]; NIQ FMCG value +7.8% in OND 2025 [V01].', True, PCT),
    ('EB_start', 'Starting EBITDA margin (FY26E–FY27E)', 0.06, 0.06, 0.06, '%', 'Hypothesis', 'Not disclosed; FY25 net margin −2.2% [V08]. Same in every scenario: a fact to confirm with finance in week 1, not a lever (EBITDA sheet shows 4–7%).', True, PCT),
    ('Target_corr', 'EBITDA margin that counts as “corrected”', 0.07, 0.07, 0.07, '%', 'Hypothesis', 'Above Gopal Snacks’ 6.7% (FY26) [V12]; the gate before scaling stores.', True, PCT),
    ('Share_MTnow', 'Existing MT + e-commerce share of revenue (FY26E)', 0.02, 0.02, 0.02, '%', 'Hypothesis', 'BigBasket listings exist; MT/e-com share not disclosed. Replace with distributor data.', True, PCT),
    ('B', 'Modern trade: stores and terms'),
    ('Live_FY27', 'Months the test stores sell in FY27 (Jan–Mar 2027)', 3, 3, 3, 'months', 'Hypothesis', 'Plan month 1 = Jan 2027.', False, INT),
    ('MT_st_FY27', 'MT stores selling, end FY27 (test stores)', 5, 5, 5, 'stores', 'Hypothesis', 'Five high-performing Guwahati test stores (Test_Stores sheet), live Jan–Mar 2027.', True, INT),
    ('MT_st_FY28', 'MT stores selling, end FY28', 15, 25, 40, 'stores', 'Hypothesis', 'Only after ≥2 of 5 test stores clear the gate; Guwahati + Assam Vishal first.', True, INT),
    ('MT_st_FY29', 'MT stores selling, end FY29', 40, 74, 100, 'stores', 'Hypothesis', '74 = all Vishal Northeast stores (44 in Assam) [V02].', True, INT),
    ('MT_st_FY30', 'MT stores selling, end FY30', 74, 120, 160, 'stores', 'Hypothesis', 'Add Reliance Smart, regional chains in NE; North Bengal.', False, INT),
    ('MT_st_FY31', 'MT stores selling, end FY31', 100, 180, 240, 'stores', 'Hypothesis', 'East: Vishal West Bengal 34, Bihar 32, Jharkhand 18 [V02]; Spencer’s, More.', False, INT),
    ('Maturity', 'Productivity of stores in their opening year', 0.85, 0.85, 0.85, '×', 'Hypothesis', 'New stores ramp for ~3 months; new SKUs turn 11% slower and age 16 days more (HBS, Colombian chain) [V05].', False, CR2),
    ('ROS_mult', 'Rate of sale vs SKU_Plan base', 0.6, 1.0, 1.4, '×', 'Hypothesis', 'Scales every SKU’s weekly units per store. Base ≈ 8% of a Vishal Assam store’s snack sales (Market sheet check).', True, CR2),
    ('Ret_avg', 'Blended MT retailer margin (% of MRP)', 0.25, 0.23, 0.22, '%', 'Hypothesis', 'Terra Insight: DMart 18–28%, Reliance Smart 22–32%, More 22–30%, Spencer’s 25–35% [V04]; Vishal not published.', True, PCT),
    ('Dist_MT', 'MT distributor margin (% of MRP)', 0.04, 0.04, 0.04, '%', 'Hypothesis', 'Snack/biscuit trade margins ~3–5% [V21]; one Guwahati MT distributor carries credit early.', False, PCT),
    ('Promo_MT', 'MT promotions (% of MRP)', 0.04, 0.03, 0.03, '%', 'Hypothesis', 'Capped; promo claims audited against PO + store photo (Terra: brands over-fund promos 4–9% without audit) [V04].', False, PCT),
    ('Recv_MT', 'Blended MT receivable days', 60, 50, 45, 'days', 'External/Hyp', 'Vishal payable days 50 (FY25), DMart 6 [V02]; Terra cycles T+30 to T+75 [V04].', True, INT),
    ('Recv_QC', 'QC payout days', 15, 10, 7, 'days', 'Hypothesis', 'Marketplace settlement cycles; confirm in platform terms.', False, INT),
    ('CostFunds', 'Cost of working capital (a year)', 0.11, 0.11, 0.11, '%', 'Hypothesis', 'Bank limits ~93% used in 2023 [V09]; working capital is scarce.', False, PCT),
    ('C', 'Quick commerce (second priority)'),
    ('QC_st_FY28', 'Dark stores listing Kishlay, end FY28', 20, 30, 50, 'stores', 'Hypothesis', 'Guwahati first (Blinkit live since Jan 2025) [V21].', False, INT),
    ('QC_st_FY29', 'Dark stores, end FY29', 60, 120, 200, 'stores', 'Hypothesis', 'Add Kolkata, Siliguri.', False, INT),
    ('QC_st_FY30', 'Dark stores, end FY30', 120, 250, 400, 'stores', 'Hypothesis', 'East + NE cities.', False, INT),
    ('QC_st_FY31', 'Dark stores, end FY31', 200, 400, 600, 'stores', 'Hypothesis', '', False, INT),
    ('QC_units', 'Average units per listed SKU per dark store a day', 0.6, 0.8, 1.0, 'units', 'Hypothesis', 'Weighted by SKU_Plan rate of sale. Prataap: QC 1.2–1.5% of sales, aiming ~5% in 3 years [V11]; Bikaji e-com+QC ~3% [V10].', True, CR2),
    ('QC_fee', 'Platform commission (% of MRP)', 0.22, 0.22, 0.22, '%', 'External', 'Commissions 20–23% reported [V21].', False, PCT),
    ('QC_ads', 'QC ads (% of MRP)', 0.07, 0.06, 0.05, '%', 'Hypothesis', '', False, PCT),
    ('D', 'EBITDA levers (bps of revenue at full effect)'),
    ('L_proc', 'Procurement: gram at harvest, oil forward cover, local potato', 40, 60, 90, 'bps', 'Hypothesis', 'Raw materials are 70–75% of cost [V09]: a 1% RM saving ≈ 70 bps.', True, INT),
    ('L_pack', 'Packaging: down-gauge film, standard widths, reverse auction', 20, 30, 45, 'bps', 'Hypothesis', 'See Procurement sheet (film ₹/kg by pack size).', False, INT),
    ('L_sku', 'SKU tail cut (236 items) and fewer changeovers', 25, 40, 60, 'bps', 'Hypothesis', '236 products listed [V20]; category managers rank SKUs A/B/C.', False, INT),
    ('L_yield', 'Yield and oil uptake control', 20, 30, 45, 'bps', 'Hypothesis', 'Frying oil management; TPC ≤25% rule.', False, INT),
    ('L_frt', 'Freight: milk-runs, full loads, distance routing', 15, 25, 40, 'bps', 'Hypothesis', 'Supply_Chain sheet.', False, INT),
    ('L_trade', 'Trade spend paid on sell-out, not sell-in', 25, 40, 60, 'bps', 'Hypothesis', '', False, INT),
    ('L_mix', 'Mix: more kilos in MT and QC packs', 5, 15, 30, 'bps', 'Calculation', 'MT/QC earn more per kilo (Unit_Econ) but stay a small share of sales.', False, INT),
    ('L_audit', 'MT deduction audit (PO + photo + debit note)', 3, 5, 8, 'bps', 'External', 'Recovers 60–85 bps of MT turnover [V04]; small at company level.', False, INT),
    ('L_copack', 'Optional: co-pack Vishal own-label namkeen', 0, 0, 40, 'bps', 'Hypothesis', 'Upside only, not in Base. Vishal sources 100% of own label from vendors (839 in FY25) [V02]; would fill Amingaon lines.', False, INT),
    ('L_invest', 'Less: MT/QC team, promoters, listing, ads', -40, -30, -30, 'bps', 'Hypothesis', '', False, INT),
    ('OpLev31', 'Operating leverage in FY31', 0, 20, 40, 'bps', 'Hypothesis', 'Fixed costs over a larger base.', False, INT),
]
r = 6
ROW = {}
for it in INPUTS:
    if len(it) == 2:
        put(inp, f'A{r}', it[0], bold=True)
        put(inp, f'B{r}', it[1], bold=True)
        for col in 'ABCDEFGHI':
            inp[f'{col}{r}'].fill = GREY
        r += 1
        continue
    nid, par, s, b, f_, unit, lab, basis, key, fmt = it
    put(inp, f'A{r}', nid)
    put(inp, f'B{r}', par, wrap=True)
    for col, v in zip('CDE', (s, b, f_)):
        put(inp, f'{col}{r}', v, BLUE, fmt, YEL if key else None)
    put(inp, f'F{r}', f'=CHOOSE(Scenario,C{r},D{r},E{r})', BLK, fmt)
    put(inp, f'G{r}', unit)
    put(inp, f'H{r}', lab)
    put(inp, f'I{r}', basis, wrap=True)
    name(nid, f'Inputs!$F${r}')
    ROW[nid] = r
    r += 1
put(inp, f'A{r}', 'L_total')
put(inp, f'B{r}', 'Total lever effect at full ramp (excl. FY31 leverage)')
put(inp, f'F{r}', '=L_proc+L_pack+L_sku+L_yield+L_frt+L_trade+L_mix+L_audit+L_copack+L_invest', BLK, INT, SAND)
put(inp, f'G{r}', 'bps')
name('L_total', f'Inputs!$F${r}')
inp.freeze_panes = 'C6'

# =====================================================================================  Procurement and ₹/kg
pr = sheet('Procurement', 'Raw materials, packaging and ₹ per kilo',
           'Recipes are planning assumptions to replace with plant costing in week 1. Raw materials are 70–75% of operating cost (CRISIL).',
           [30, 12, 14, 12, 12, 12, 12, 12, 12, 60])
header(pr, 4, ['Raw material', '₹/kg', 'Label', '', '', '', '', '', '', 'Basis and source'])
RM = [
    ('Gram flour (besan)', 80, 'Hypothesis', 'Gram MSP ₹5,650/q (2025-26) → ₹5,875/q (2026-27) [V15] + milling; buy at harvest (Mar–May).'),
    ('Moth bean flour', 95, 'Hypothesis', 'For Bikaneri bhujia.'),
    ('Potato, fresh', 14, 'Hypothesis', 'Cold-store potato ₹12–20/kg in Assam/Bengal; ~4 kg fresh potato per kg of chips.'),
    ('Palm oil (palmolein)', 140, 'External', 'DCA retail ₹129.6–145/kg (12 Feb 2026); Ahmedabad ~₹149/kg (Feb 2026) [V16].'),
    ('Peanuts', 110, 'Hypothesis', ''),
    ('Rice flakes (chira)', 45, 'Hypothesis', 'For jhalmuri and chanachur.'),
    ('Corn grits', 32, 'Hypothesis', 'For extruded rings.'),
    ('Maida (refined wheat flour)', 32, 'Hypothesis', 'Noodles, cookies.'),
    ('Sugar', 42, 'Hypothesis', 'Cookies.'),
    ('Spices and seasoning', 280, 'Hypothesis', 'Incl. Assam bhoot jolokia (GI).'),
    ('Other (salt, milk solids, additives)', 40, 'Hypothesis', ''),
    ('Laminate film (BOPP / MET-PET)', 220, 'Hypothesis', 'Reverse auction among 3 converters; down-gauge 5–10%.'),
    ('Paperboard (cartons, boxes)', 70, 'Hypothesis', ''),
]
RMROW = {}
for i, (n_, v, lab, src) in enumerate(RM):
    rr = 5 + i
    put(pr, f'A{rr}', n_)
    put(pr, f'B{rr}', v, BLUE, RS)
    put(pr, f'C{rr}', lab)
    put(pr, f'J{rr}', src, wrap=True)
    RMROW[n_] = rr
FAM = ['bhujia', 'mixture', 'extruded', 'noodles', 'cookies', 'chips']
f0 = 5 + len(RM) + 2
header(pr, f0, ['Recipe: kg of raw material per kg of product'] + FAM + ['', '', 'Note'])
RECIPE = {
    'Gram flour (besan)':                   [0.38, 0.30, 0, 0, 0, 0],
    'Moth bean flour':                      [0.05, 0, 0, 0, 0, 0],
    'Potato, fresh':                        [0.50, 0, 0, 0, 0, 4.00],
    'Palm oil (palmolein)':                 [0.36, 0.33, 0.22, 0.18, 0.22, 0.35],
    'Peanuts':                              [0, 0.15, 0, 0, 0, 0],
    'Rice flakes (chira)':                  [0, 0.10, 0, 0, 0, 0],
    'Corn grits':                           [0, 0, 0.65, 0, 0, 0],
    'Maida (refined wheat flour)':          [0, 0, 0.05, 0.78, 0.47, 0],
    'Sugar':                                [0, 0, 0, 0, 0.25, 0],
    'Spices and seasoning':                 [0.05, 0.06, 0.08, 0.04, 0, 0.06],
    'Other (salt, milk solids, additives)': [0.06, 0.06, 0, 0, 0.06, 0],
}
rr = f0
for n_, vals in RECIPE.items():
    rr += 1
    put(pr, f'A{rr}', n_)
    for j, v in enumerate(vals):
        put(pr, f'{get_column_letter(2+j)}{rr}', v, BLUE, CR2)
REC_FIRST, REC_LAST = f0 + 1, rr
rr += 1
put(pr, f'A{rr}', 'Raw-material cost per kg of product (₹)', bold=True)
names_list = list(RECIPE.keys())
for j in range(len(FAM)):
    col = get_column_letter(2 + j)
    terms = '+'.join(f'{col}{REC_FIRST+k}*$B${RMROW[n_]}' for k, n_ in enumerate(names_list))
    put(pr, f'{col}{rr}', f'={terms}', BLK, RS2, SAND)
    name(f'RMkg_{FAM[j]}', f'Procurement!${col}${rr}')
RMKG_ROW = rr
put(pr, f'J{rr}', 'Feeds SKU_Plan and Unit_Econ.')

p0 = rr + 2
header(pr, p0, ['Packaging by pack', 'Pack (g)', 'Film (g)', 'Board (g)', 'Tin (₹)', 'Pack ₹', '₹/kg', '', '', 'Note'])
PACKS = [('pk32', '₹10 rings pouch, 32 g', 32, 3.0, 0, 0),
         ('pk40', '₹10 namkeen pouch, 40 g (assumed)', 40, 3.5, 0, 0),
         ('pk150', '150 g cookies (tray + wrap)', 150, 6.0, 25, 0),
         ('pk200', '200 g pouch', 200, 7.0, 0, 0),
         ('pk400', '400 g stand-up zipper pouch', 400, 13.0, 0, 0),
         ('pk180', 'Multipack 12 × ₹5 rings (180 g)', 180, 26.0, 0, 0),
         ('pk240', 'Multipack 6 × ₹10 noodles (240 g)', 240, 20.0, 0, 0),
         ('pk384', 'Party box 12 × ₹10 assorted (384 g)', 384, 36.4, 60, 0),
         ('pk500', 'Festive tin 500 g', 500, 8.0, 0, 25),
         ('pk1000', 'Family pack 1 kg pouch', 1000, 25.0, 0, 0)]
for i, (pid, lab, g, film, board, tin) in enumerate(PACKS):
    rr = p0 + 1 + i
    put(pr, f'A{rr}', lab)
    put(pr, f'B{rr}', g, BLUE, INT)
    put(pr, f'C{rr}', film, BLUE, CR2)
    put(pr, f'D{rr}', board, BLUE, INT)
    put(pr, f'E{rr}', tin, BLUE, RS)
    put(pr, f'F{rr}', f'=C{rr}/1000*$B${RMROW["Laminate film (BOPP / MET-PET)"]}+D{rr}/1000*$B${RMROW["Paperboard (cartons, boxes)"]}+E{rr}+B{rr}/1000*3', BLK, RS2)
    put(pr, f'G{rr}', f'=F{rr}/(B{rr}/1000)', BLK, RS2, SAND)
    name(f'PK_{pid}', f'Procurement!$G${rr}')
put(pr, f'J{p0+1}', 'Includes ₹3/kg for shipper cartons. Small packs carry 2–3× more packaging per kilo.', wrap=True)

k0 = p0 + len(PACKS) + 3
header(pr, k0, ['Price per kilo on the shelf', 'Pack (g)', 'MRP ₹', '₹/kg', 'vs Haldiram’s 400 g', '', '', '', '', 'Source'])
KG = [('Kishlay ₹10 namkeen pouch (assumed 40 g)', 40, 10, 'Assumed grammage: check the pack'),
      ('Kishlay 200 g (Aloo Bhujia)', 200, 55, 'BigBasket listing [V22]'),
      ('Kishlay 400 g (Bikaneri / Paneer Bhujia)', 400, 110, 'BigBasket listing [V22]'),
      ('Haldiram’s Aloo Bhujia 400 g', 400, 100, 'JM Financial Exhibit 28 [V02]'),
      ('Vishal own label First Crop Aloo Bhujia 150 g', 150, 40.2, 'JM Financial Exhibit 28 [V02]'),
      ('Bikano salted peanuts 200 g', 200, 60, 'JM Financial Exhibit 28 [V02]'),
      ('Option: Kishlay 400 g at ₹99', 400, 99, 'Price-match option tested in Unit_Econ'),
      ('Proposed: Kishlay family pack 1 kg at ₹249', 1000, 249, 'Proposed SKU: matches Haldiram’s per gram without cutting 400 g')]
for i, (lab, g, mrp, src) in enumerate(KG):
    rr = k0 + 1 + i
    put(pr, f'A{rr}', lab)
    put(pr, f'B{rr}', g, BLUE, INT)
    put(pr, f'C{rr}', mrp, BLUE, RS2)
    put(pr, f'D{rr}', f'=C{rr}/B{rr}*1000', BLK, RS)
    put(pr, f'E{rr}', f'=D{rr}/$D${k0+4}-1', BLK, PCT)
    put(pr, f'J{rr}', src)
KG_FIRST = k0 + 1

l0 = k0 + len(KG) + 3
header(pr, l0, ['Procurement lever', 'Saving on that input', 'Share of RM+pack', 'Effect on cost', '', '', '', '', '', 'How, and when'])
PL = [('Gram flour bought at harvest + forward cover', 0.04, 0.25, 'Buy 3–4 months’ need in Mar–May near MSP; mill tie-ups in Rajasthan/MP.'),
      ('Palm oil monthly contracts + 60–90 day cover', 0.03, 0.40, 'Contract with Haldia/Kolkata refiners; switch palmolein/rice bran on spread.'),
      ('Potato contract farming within 150 km', 0.08, 0.05, 'Assam/North Bengal growers; cuts inward freight.'),
      ('Film down-gauge + reverse auction', 0.08, 0.08, '3 converters, standard roll widths for 200/400 g.'),
      ('Spices annual contract; local bhoot jolokia', 0.05, 0.08, 'GI Assam jolokia direct from growers.')]
for i, (lab, sav, share, how) in enumerate(PL):
    rr = l0 + 1 + i
    put(pr, f'A{rr}', lab, wrap=True)
    put(pr, f'B{rr}', sav, BLUE, PCT)
    put(pr, f'C{rr}', share, BLUE, PCT)
    put(pr, f'D{rr}', f'=B{rr}*C{rr}', BLK, PCT)
    put(pr, f'J{rr}', how, wrap=True)
rr = l0 + len(PL) + 1
put(pr, f'A{rr}', 'Total saving on RM + packaging', bold=True)
put(pr, f'D{rr}', f'=SUM(D{l0+1}:D{rr-1})', BLK, PCT, SAND)
put(pr, f'A{rr+1}', '… in EBITDA bps (RM+pack ≈ 72% of revenue)')
put(pr, f'D{rr+1}', f'=D{rr}*0.72*10000', BLK, INT, SAND)
put(pr, f'J{rr+1}', 'Cross-check for L_proc + L_pack in Inputs.')
put(pr, f'A{rr+2}', 'Share of that gross saving assumed captured (prices also move against us)')
put(pr, f'D{rr+2}', 0.35, BLUE, PCT, YEL)
put(pr, f'A{rr+3}', 'Captured saving (bps) · Base L_proc + L_pack in Inputs', bold=True)
put(pr, f'D{rr+3}', f'=D{rr+1}*D{rr+2}', BLK, INT, SAND)
put(pr, f'E{rr+3}', f"=Inputs!D{ROW['L_proc']}+Inputs!D{ROW['L_pack']}", GRN, INT)
PROC_BPS = rr + 1
pr.freeze_panes = 'B5'

# =====================================================================================  Supply chain
sc = sheet('Supply_Chain', 'Distance, vehicles, replenishment and quality',
           'Plant: Tulsi Speciality Foods, Brahmaputra Industrial Park, Amingaon (North Guwahati). Distances are approximate road km — verify with route data. Vehicles are what to confirm with logistics.',
           [34, 14, 14, 14, 14, 14, 14, 16, 58])
header(sc, 4, ['Vehicle and cost inputs', 'Value', 'Unit', '', '', '', '', '', 'Basis'])
VEH = [('scv_day', 'City milk-run van (SCV, e.g. 0.75–1 t): cost a day', 2000, '₹/day', 'Hypothesis: driver + fuel + vehicle; confirm current contract.'),
       ('scv_kg', 'SCV kilos delivered a day (light, bulky cartons)', 500, 'kg/day', 'Hypothesis: 15–20 store drops a day.'),
       ('lcv_rate', 'Upcountry 17-ft truck: rate per km', 38, '₹/km', 'Hypothesis.'),
       ('lcv_kg', 'Upcountry truck payload (snack cartons)', 1800, 'kg', 'Hypothesis: volume-limited.'),
       ('ret_factor', 'Return-trip factor (partial backhaul)', 1.5, '×', 'Hypothesis.'),
       ('drop_kg', 'Town distributor’s local delivery to stores', 1.5, '₹/kg', 'Hypothesis.')]
VR = {}
for i, (k, lab, v, u, b) in enumerate(VEH):
    rr = 5 + i
    put(sc, f'A{rr}', lab, wrap=True)
    put(sc, f'B{rr}', v, BLUE, INT if v >= 10 else CR2)
    put(sc, f'C{rr}', u)
    put(sc, f'I{rr}', b, wrap=True)
    VR[k] = rr
    name(k, f'Supply_Chain!$B${rr}')
c0 = 5 + len(VEH) + 2
header(sc, c0, ['City', 'State', 'Road km from Amingaon', 'Band', 'Freight ₹/kg', 'Lead time (days)', 'Drops a week', 'Phase', 'Why'])
CITIES = [('Guwahati (city stores)', 'Assam', 15, 'Test stores: Vishal, Reliance Smart, independents'),
          ('Nalbari', 'Assam', 60, ''), ('Mangaldoi', 'Assam', 75, ''), ('Shillong', 'Meghalaya', 100, 'Vishal Meghalaya: 4 stores'),
          ('Barpeta', 'Assam', 100, ''), ('Nagaon', 'Assam', 120, 'Large town, central Assam'), ('Goalpara', 'Assam', 140, ''),
          ('Hojai', 'Assam', 170, ''), ('Tezpur', 'Assam', 180, ''), ('Bongaigaon', 'Assam', 180, ''), ('Kokrajhar', 'Assam', 220, ''),
          ('Dhubri', 'Assam', 270, ''), ('Diphu', 'Assam', 270, ''), ('Dimapur', 'Nagaland', 280, 'Vishal Nagaland: 6'), ('Golaghat', 'Assam', 280, ''),
          ('Jorhat', 'Assam', 310, 'Upper Assam hub'), ('Silchar', 'Assam', 320, 'Barak Valley'), ('Itanagar', 'Arunachal', 330, 'Vishal Arunachal: 7'),
          ('Sivasagar', 'Assam', 360, ''), ('North Lakhimpur', 'Assam', 380, ''), ('Dibrugarh', 'Assam', 440, 'Upper Assam'),
          ('Siliguri', 'West Bengal', 450, 'Gateway to North Bengal'), ('Tinsukia', 'Assam', 480, ''), ('Imphal', 'Manipur', 480, 'Vishal Manipur: 6'),
          ('Agartala', 'Tripura', 540, 'Vishal Tripura: 2'), ('Kolkata', 'West Bengal', 1050, 'Later: Spencer’s, More, Vishal WB 34')]
for i, (c, st, km, why) in enumerate(CITIES):
    rr = c0 + 1 + i
    put(sc, f'A{rr}', c)
    put(sc, f'B{rr}', st)
    put(sc, f'C{rr}', km, BLUE, INT)
    put(sc, f'D{rr}', f'=IF(C{rr}<=30,"City",IF(C{rr}<=150,"Near",IF(C{rr}<=350,"Mid","Far")))')
    put(sc, f'E{rr}', f'=IF(C{rr}<=30,scv_day/scv_kg,C{rr}*lcv_rate*ret_factor/lcv_kg+drop_kg)', BLK, RS2, SAND)
    put(sc, f'F{rr}', f'=IF(C{rr}<=30,0,IF(C{rr}<=150,1,IF(C{rr}<=350,2,IF(C{rr}<=600,3,4))))', BLK, INT)
    put(sc, f'G{rr}', f'=IF(C{rr}<=30,3,IF(C{rr}<=150,2,IF(C{rr}<=350,1,1)))', BLK, INT)
    put(sc, f'H{rr}', f'=IF(C{rr}<=30,"1 · Test",IF(AND(B{rr}="Assam",C{rr}<=350),"2 · Assam",IF(C{rr}<=600,"3 · NE + N. Bengal","4 · East")))')
    put(sc, f'I{rr}', why)
CITY_G = c0 + 1
name('Frt_city', f'Supply_Chain!$E${CITY_G}')
q0 = c0 + len(CITIES) + 3
header(sc, q0, ['Quality and supply rules for modern trade', 'Standard', '', '', '', '', '', '', 'Why'])
QA = [('Shelf life left at delivery to chain DC/store', '≥ 2/3 of printed life', 'Chains reject short-dated stock; plan FEFO.'),
      ('Moisture (namkeen)', '≤ 2–3%', 'Crispness; checked per batch.'),
      ('Frying-oil total polar compounds (TPC)', '≤ 25%', 'FSSAI limit for reused oil.'),
      ('Peroxide value in finished goods', 'Low; trend weekly', 'Rancidity drives returns.'),
      ('Nitrogen flush / seal strength', 'Per batch', 'Prevents stale, crushed packs.'),
      ('Labels: FSSAI, Legal Metrology MRP, GS1 barcode', '100% of SKUs', 'Listing requirement.'),
      ('Fill rate to chain orders (OTIF)', '≥ 95%', 'Out-of-stocks: 31% of shoppers switch store, 26% switch brand (Gruen et al.) [V07].'),
      ('Returns and expiry', '≤ 3% of MT sales', 'Expiry-return clauses in chain terms.'),
      ('Replenishment, Guwahati stores', '2–3 drops a week', 'Same-day from Amingaon; distributor holds ~10 days’ stock.')]
for i, (a, b, c) in enumerate(QA):
    rr = q0 + 1 + i
    put(sc, f'A{rr}', a, wrap=True)
    put(sc, f'B{rr}', b, BLUE)
    sc.merge_cells(f'B{rr}:H{rr}')
    put(sc, f'I{rr}', c, wrap=True)
b0 = q0 + len(QA) + 3
header(sc, b0, ['Freight bulk factor by product family', 'Factor', '', '', '', '', '', '', 'Why'])
BFS = [('bhujia', 1.0, 'Dense; trucks fill by weight'), ('mixture', 1.0, 'Dense'), ('extruded', 2.5, 'Mostly air: trucks fill by volume, so each kg costs more to move'),
       ('noodles', 0.8, 'Dense blocks'), ('cookies', 0.9, 'Trays and cartons'), ('chips', 2.0, 'Bulky, nitrogen-filled')]
for i, (fam_, fac, why) in enumerate(BFS):
    rr = b0 + 1 + i
    put(sc, f'A{rr}', fam_)
    put(sc, f'B{rr}', fac, BLUE, CR2)
    put(sc, f'I{rr}', why, wrap=True)
    name(f'BF_{fam_}', f'Supply_Chain!$B${rr}')
sc.freeze_panes = 'A5'

# =====================================================================================  SKU plan (value + volume)
sk = sheet('SKU_Plan', 'What we release into modern trade: SKUs by value and volume',
           'Base weekly units per store are planning assumptions for the test stores; scenario multiplier in Inputs (ROS_mult). Contribution uses Unit_Econ logic per SKU.',
           [5, 30, 11, 22, 10, 9, 9, 10, 10, 11, 20, 11, 11, 12, 12, 12, 12, 12, 12, 10, 8])
header(sk, 4, ['#', 'SKU', 'Role', 'Shopper it serves', 'Family', 'Pack (g)', 'MRP ₹', '₹/kg (MRP)', 'Shelf life (months)', 'Base units / store / week', 'Shelf zone',
               'Active units / week', 'Units / store / month', 'MRP sales / store / month', 'kg / store / month', 'RM+pack ₹/kg', 'Realisation / pack', 'Contribution / pack', 'Contribution ₹/kg',
               'QC listed (1/0)', 'ABC goal', 'Wave', 'Small packs inside (1/0)', 'QC units / dark store / day', 'QC net / unit'])
sk.column_dimensions['X'].width = 12
sk.column_dimensions['Y'].width = 11
sk.column_dimensions['V'].width = 8
sk.column_dimensions['W'].width = 11
SKUS = [
    ('Bikaneri Bhujia 400 g', 'A · anchor', 'Planner mother, 30–45', 'bhujia', 400, 110, 6, 12, 'Adult eye level', 1, 'A', 1, 0, 'pk400'),
    ('Paneer Bhujia 400 g', 'A · anchor', 'Planner mother, 30–45', 'bhujia', 400, 110, 6, 12, 'Adult eye level', 1, 'A', 1, 0, 'pk400'),
    ('Aloo Bhujia 200 g', 'A · anchor', 'Mother; young adults', 'bhujia', 200, 55, 6, 10, 'Adult eye level', 0, 'A', 1, 0, 'pk200'),
    ('Jolokia Chanachur 200 g', 'B · regional hero', 'Young snackers, 18–30', 'mixture', 200, 55, 5, 8, 'Grab level / end cap', 1, 'B', 1, 0, 'pk200'),
    ('Jhalmuri 200 g', 'B · regional hero', 'Young snackers; mothers', 'mixture', 200, 55, 4, 8, 'Grab level', 0, 'B', 1, 0, 'pk200'),
    ('40 Aana Chanachur 200 g', 'B · regional hero', 'Bengali-taste families', 'mixture', 200, 55, 5, 6, 'Grab level', 0, 'B', 2, 0, 'pk200'),
    ('Water Toy Rings 12 × ₹5', 'Kids multipack', 'Kids 5–12 (pester power)', 'extruded', 180, 60, 4, 10, 'Kids’ eye level', 1, 'B', 1, 1, 'pk180'),
    ('Masala Noodles 6 × ₹10', 'Kids multipack', 'Kids; mothers (tiffin)', 'noodles', 240, 60, 9, 8, 'Kids’ eye level', 1, 'B', 1, 1, 'pk240'),
    ('Butter Cookies 150 g', 'Kids · tea time', 'Kids; tea-time', 'cookies', 150, 40, 6, 6, 'Kids’ eye level', 0, 'C', 2, 0, 'pk150'),
    ('Family Pack Bikaneri Bhujia 1 kg', 'Bulk · per-gram value', 'Stock-up families (₹30–50k)', 'bhujia', 1000, 249, 6, 4, 'Bottom shelf', 1, 'B', 1, 0, 'pk1000'),
    ('Party Box 12 × ₹10 assorted', 'Bulk · basket builder', 'Hosts, families (₹50k–1L)', 'mixture', 384, 120, 4, 3, 'Bottom shelf / end cap', 1, 'B', 2, 1, 'pk384'),
    ('Festive Tin 500 g', 'Premium · gifting', 'Premium homes (₹1–1.5L)', 'mixture', 500, 199, 6, 2, 'Top shelf / festive end cap', 1, 'C', 2, 0, 'pk500'),
]
for i, (nm_, role, seg, fam, g, mrp, life, ros, zone, qc, abc, wave, small, pk) in enumerate(SKUS):
    rr = 5 + i
    put(sk, f'A{rr}', i + 1)
    put(sk, f'B{rr}', nm_)
    put(sk, f'C{rr}', role)
    put(sk, f'D{rr}', seg, wrap=True)
    put(sk, f'E{rr}', fam)
    put(sk, f'F{rr}', g, BLUE, INT)
    put(sk, f'G{rr}', mrp, BLUE, RS)
    put(sk, f'H{rr}', f'=G{rr}/F{rr}*1000', BLK, RS)
    put(sk, f'I{rr}', life, BLUE, INT)
    put(sk, f'J{rr}', ros, BLUE, INT, YEL)
    put(sk, f'K{rr}', zone)
    put(sk, f'L{rr}', f'=J{rr}*ROS_mult', BLK, CR)
    put(sk, f'M{rr}', f'=L{rr}*52/12', BLK, CR)
    put(sk, f'N{rr}', f'=M{rr}*G{rr}', BLK, RS)
    put(sk, f'O{rr}', f'=M{rr}*F{rr}/1000', BLK, CR)
    put(sk, f'P{rr}', f'=RMkg_{fam}+PK_{pk}', BLK, RS2)
    put(sk, f'Q{rr}', f'=G{rr}*(1-GST_rate/(1+GST_rate)-Ret_avg-Dist_MT)', BLK, RS2)
    put(sk, f'R{rr}', f'=Q{rr}-F{rr}/1000*(P{rr}+IF(W{rr}=1,Conv_small,Conv_kg)+Frt_city*BF_{fam})-Promo_MT*G{rr}', BLK, RS2, SAND)
    put(sk, f'S{rr}', f'=R{rr}/(F{rr}/1000)', BLK, RS)
    put(sk, f'T{rr}', qc, BLUE, INT)
    put(sk, f'U{rr}', abc, BLUE)
    put(sk, f'V{rr}', wave, BLUE, INT)
    put(sk, f'W{rr}', small, BLUE, INT)
    put(sk, f'X{rr}', f'=IF(T{rr}=1,QC_units*J{rr}/(SUMPRODUCT($T$5:$T${4+len(SKUS)},$J$5:$J${4+len(SKUS)})/SUM($T$5:$T${4+len(SKUS)})),0)', BLK, CR2)
    put(sk, f'Y{rr}', f'=G{rr}*(1/(1+GST_rate)-QC_fee)', BLK, RS2)
SK_FIRST, SK_LAST = 5, 5 + len(SKUS) - 1
tr = SK_LAST + 1
put(sk, f'B{tr}', 'Per store, a month', bold=True)
for col, fmt in (('L', CR), ('M', CR), ('N', RS), ('O', CR)):
    put(sk, f'{col}{tr}', f'=SUM({col}{SK_FIRST}:{col}{SK_LAST})', BLK, fmt, SAND)
put(sk, f'Q{tr}', f'=SUMPRODUCT(M{SK_FIRST}:M{SK_LAST},Q{SK_FIRST}:Q{SK_LAST})', BLK, RS, SAND)
put(sk, f'R{tr}', f'=SUMPRODUCT(M{SK_FIRST}:M{SK_LAST},R{SK_FIRST}:R{SK_LAST})', BLK, RS, SAND)
put(sk, f'S{tr}', f'=R{tr}/O{tr}', BLK, RS, SAND)
name('Store_MRP_m', f'SKU_Plan!$N${tr}')
name('Store_real_m', f'SKU_Plan!$Q${tr}')
name('Store_contr_m', f'SKU_Plan!$R${tr}')
name('Store_kg_m', f'SKU_Plan!$O${tr}')
name('Store_units_m', f'SKU_Plan!$M${tr}')
put(sk, f'B{tr+1}', 'Columns Q–S are per pack at the blended MT margin; the totals row is per store per month (all 12 SKUs, steady state).')
put(sk, f'B{tr+2}', 'Contribution as % of realisation')
put(sk, f'R{tr+2}', f'=R{tr}/Q{tr}', BLK, PCT, SAND)
name('MT_contr_pct', f'SKU_Plan!$R${tr+2}')
put(sk, f'B{tr+4}', 'SKUs listed on quick commerce')
put(sk, f'Q{tr+4}', f'=SUM(T{SK_FIRST}:T{SK_LAST})', BLK, INT, SAND)
name('QC_SKUs', f'SKU_Plan!$Q${tr+4}')
put(sk, f'B{tr+5}', 'Wave 1 = launch in the 5 test stores; wave 2 = after the gate or in festive months.')

v0 = tr + 8
put(sk, f'A{v0-1}', 'Value (MRP ₹ lakh) and volume (tonnes) by SKU and year, all MT stores selling', bold=True)
header(sk, v0, ['#', 'SKU'] + [f'Value {y}' for y in YEARS[2:]] + [f'Tonnes {y}' for y in YEARS[2:]])
for i in range(len(SKUS)):
    rr = v0 + 1 + i
    put(sk, f'A{rr}', i + 1)
    put(sk, f'B{rr}', f'=B{SK_FIRST+i}')
    for j, y in enumerate(YEARS[2:]):
        yc = YC[2 + j]
        put(sk, f'{get_column_letter(3+j)}{rr}', f'=M{SK_FIRST+i}*G{SK_FIRST+i}*12*Scale!{yc}$13/10^5', BLK, CR)
        put(sk, f'{get_column_letter(8+j)}{rr}', f'=M{SK_FIRST+i}*F{SK_FIRST+i}/1000*12*Scale!{yc}$13/1000', BLK, CR)
rr = v0 + 1 + len(SKUS)
put(sk, f'B{rr}', 'Total', bold=True)
for j in range(10):
    col = get_column_letter(3 + j)
    put(sk, f'{col}{rr}', f'=SUM({col}{v0+1}:{col}{rr-1})', BLK, CR, SAND)
sk.freeze_panes = 'C5'

# extra named inputs used above
gi = sheet('Unit_Econ', 'Unit economics per pack: the pack, not the channel, makes the money',
           'GST 5% on snacks since 22 Sep 2025. Retailer, distributor and platform cuts are % of MRP; conversion and freight per kg. Costs are hypotheses to replace with plant costing.',
           [44, 14, 14, 14, 14, 14, 14, 14, 52])
put(gi, 'A3', 'GST rate on snacks', bold=True)
put(gi, 'B3', 0.05, BLUE, PCT)
name('GST_rate', 'Unit_Econ!$B$3')
put(gi, 'C3', 'GST 2.0 from 22 Sep 2025 [V23]')
put(gi, 'A4', 'Conversion, take-home packs (₹/kg)', bold=True)
put(gi, 'B4', 11.25, BLUE, RS2)
name('Conv_kg', 'Unit_Econ!$B$4')
put(gi, 'C4', 'Labour, power, overheads: plant estimate')
put(gi, 'A5', 'Conversion, ₹5/₹10 packs and multipacks (₹/kg)', bold=True)
put(gi, 'B5', 15, BLUE, RS2)
name('Conv_small', 'Unit_Econ!$B$5')
put(gi, 'C5', 'Slower packing of small packs')
put(gi, 'A6', 'GT retailer · stockist + distributor (% of MRP)', bold=True)
put(gi, 'B6', 0.16, BLUE, PCT)
put(gi, 'C6', 0.07, BLUE, PCT)
put(gi, 'D6', 'Industry-typical [V21]; replace with Kishlay terms')
put(gi, 'A7', 'GT freight to outlet, dense goods (₹/kg)', bold=True)
put(gi, 'B7', 11.0, BLUE, RS2)
name('Frt_GT', 'Unit_Econ!$B$7')
put(gi, 'C7', 'Upcountry Northeast routes; × bulk factor (Supply_Chain)')
put(gi, 'A8', 'GT schemes (% of MRP)', bold=True)
put(gi, 'B8', 0.04, BLUE, PCT)
name('Sch_GT', 'Unit_Econ!$B$8')
CASES = [('GT ₹10 namkeen 40 g', 10, 40, 'bhujia', 'PK_pk40', 'GT', 1),
         ('GT ₹10 rings 32 g', 10, 32, 'extruded', 'PK_pk32', 'GT', 1),
         ('GT 400 g ₹110', 110, 400, 'bhujia', 'PK_pk400', 'GT', 0),
         ('MT 400 g ₹110', 110, 400, 'bhujia', 'PK_pk400', 'MT', 0),
         ('MT 400 g at ₹99', 99, 400, 'bhujia', 'PK_pk400', 'MT', 0),
         ('MT 1 kg ₹249', 249, 1000, 'bhujia', 'PK_pk1000', 'MT', 0),
         ('QC 400 g ₹110', 110, 400, 'bhujia', 'PK_pk400', 'QC', 0)]
header(gi, 10, ['Per pack (₹)'] + [c[0] for c in CASES] + ['Note'])
LINES = {11: 'MRP', 12: 'Pack (g)', 13: 'Less GST', 14: 'Less retailer', 15: 'Less stockist / distributor', 16: 'Less platform fee', 17: 'Realisation',
         18: 'Raw material + packaging', 19: 'Conversion', 20: 'Freight', 21: 'Schemes / promotions / ads', 22: 'Contribution',
         23: 'Contribution % of realisation', 24: 'Contribution ₹/kg', 25: 'Index vs GT 400 g (per kg)'}
for r_, l in LINES.items():
    put(gi, f'A{r_}', l, bold=r_ in (17, 22, 24))
for j, (lab, mrp, g, fam, pk, ch, small) in enumerate(CASES):
    c = get_column_letter(2 + j)
    put(gi, f'{c}11', mrp, BLUE, RS2)
    put(gi, f'{c}12', g, BLUE, INT)
    put(gi, f'{c}13', f'={c}11*GST_rate/(1+GST_rate)', BLK, RS2)
    put(gi, f'{c}14', f'={c}11*$B$6' if ch == 'GT' else (f'={c}11*Ret_avg' if ch == 'MT' else 0), BLK, RS2)
    put(gi, f'{c}15', f'={c}11*$C$6' if ch == 'GT' else (f'={c}11*Dist_MT' if ch == 'MT' else 0), BLK, RS2)
    put(gi, f'{c}16', f'={c}11*QC_fee' if ch == 'QC' else 0, BLK, RS2)
    put(gi, f'{c}17', f'={c}11-{c}13-{c}14-{c}15-{c}16', BLK, RS2, SAND)
    put(gi, f'{c}18', f'={c}12/1000*(RMkg_{fam}+{pk})', BLK, RS2)
    put(gi, f'{c}19', f'={c}12/1000*{"Conv_small" if small else "Conv_kg"}', BLK, RS2)
    put(gi, f'{c}20', f'={c}12/1000*{"Frt_GT" if ch == "GT" else "Frt_city"}*BF_{fam}', BLK, RS2)
    put(gi, f'{c}21', f'={c}11*Sch_GT' if ch == 'GT' else (f'={c}11*Promo_MT' if ch == 'MT' else f'={c}11*QC_ads'), BLK, RS2)
    put(gi, f'{c}22', f'={c}17-{c}18-{c}19-{c}20-{c}21', BLK, RS2, SAND)
    put(gi, f'{c}23', f'=IFERROR({c}22/{c}17,0)', BLK, PCT)
    put(gi, f'{c}24', f'={c}22/({c}12/1000)', BLK, RS, SAND)
    put(gi, f'{c}25', f'={c}24/$D$24', BLK, MULT)
put(gi, 'I18', 'Recipes and packaging from Procurement.', wrap=True)
put(gi, 'I20', 'GT upcountry vs MT city milk-run (Supply_Chain), × bulk factor.', wrap=True)
for nm_, c in (('UE_GT10_kg', 'B'), ('UE_GTrings_kg', 'C'), ('UE_GT400_kg', 'D'), ('UE_MT400_kg', 'E'), ('UE_MT99_kg', 'F'), ('UE_MT1kg_kg', 'G'), ('UE_QC_kg', 'H')):
    name(nm_, f'Unit_Econ!${c}$24')
name('UE_QC_pct', 'Unit_Econ!$H$23')
name('UE_MT400_pack', 'Unit_Econ!$E$22')
name('UE_MT99_pack', 'Unit_Econ!$F$22')
name('UE_MT1kg_pack', 'Unit_Econ!$G$22')
put(gi, 'A27', 'Reading', bold=True)
put(gi, 'B27', '="A ₹10 namkeen pouch leaves ₹"&TEXT(B24,"0")&"/kg; the same bhujia in a 400 g pack leaves ₹"&TEXT(D24,"0")&"/kg in GT and ₹"&TEXT(E24,"0")&"/kg in MT. Pack size, not channel, makes the money — and MT and QC are where take-home packs sell."', wrap=True)
gi.merge_cells('B27:I27')
put(gi, 'B28', '="Price-matching Haldiram’s by cutting 400 g to ₹99 keeps only "&TEXT(F24/E24,"0%")&" of the per-kg contribution. A 1 kg pack at ₹249 matches the per-gram price and earns ₹"&TEXT(G22,"0")&" a pack."', wrap=True)
gi.merge_cells('B28:I28')
gi.row_dimensions[27].height = 30
gi.row_dimensions[28].height = 30
s0 = 31
header(gi, s0, ['Retailer margin sensitivity, MT 400 g ₹110', '18%', '22%', '25%', '28%', '32%', '', '', 'Chains (Terra Insight [V04])'])
put(gi, f'A{s0+1}', 'Retailer margin (% of MRP)')
put(gi, f'A{s0+2}', 'Contribution per pack (₹)')
put(gi, f'A{s0+3}', 'Contribution ₹/kg')
for col, m in zip('BCDEF', (0.18, 0.22, 0.25, 0.28, 0.32)):
    put(gi, f'{col}{s0+1}', m, BLUE, PCT)
    put(gi, f'{col}{s0+2}', f'=$E$11-$E$13-$E$11*{col}{s0+1}-$E$15-$E$18-$E$19-$E$20-$E$21', BLK, RS2)
    put(gi, f'{col}{s0+3}', f'={col}{s0+2}/($E$12/1000)', BLK, RS)
put(gi, f'I{s0+1}', 'DMart 18–28% · Reliance Smart 22–32% · More 22–30% · Spencer’s 25–35%', wrap=True)

# =====================================================================================  Store P&L and negotiation
sp = sheet('Store_PnL', 'One store: P&L, payback, and what to negotiate after the test',
           'Test five strong stores first. Once at least 2 of 5 clear the gate for two 4-week cycles, the category manager calls — negotiate better terms for stores 6+.',
           [46, 16, 16, 16, 60])
header(sp, 4, ['Per store, a month', 'Pilot terms', 'Proven terms', 'Difference', 'Basis'])
put(sp, 'A5', 'Retailer margin (% of MRP)')
put(sp, 'B5', 0.25, BLUE, PCT, YEL)
put(sp, 'C5', 0.22, BLUE, PCT, YEL)
put(sp, 'E5', 'Concede margin in the pilot; earn it back with sell-out data. Terra ranges 18–35% [V04].', wrap=True)
put(sp, 'A6', 'Credit days')
put(sp, 'B6', 60, BLUE, INT)
put(sp, 'C6', 45, BLUE, INT)
put(sp, 'E6', 'Vishal payable days 50 (FY25) [V02].')
put(sp, 'A7', 'MRP sales')
put(sp, 'B7', '=Store_MRP_m', GRN, RS)
put(sp, 'C7', '=Store_MRP_m', GRN, RS)
put(sp, 'A8', 'Realisation')
put(sp, 'B8', '=B7*(1-GST_rate/(1+GST_rate)-B5-Dist_MT)', BLK, RS)
put(sp, 'C8', '=C7*(1-GST_rate/(1+GST_rate)-C5-Dist_MT)', BLK, RS)
put(sp, 'A9', 'Product cost (RM, pack, conversion, freight, promo)')
put(sp, 'B9', '=Store_real_m-Store_contr_m', BLK, RS)
put(sp, 'C9', '=B9', BLK, RS)
put(sp, 'A10', 'Contribution', bold=True)
put(sp, 'B10', '=B8-B9', BLK, RS, SAND)
put(sp, 'C10', '=C8-C9', BLK, RS, SAND)
put(sp, 'D10', '=C10-B10', BLK, RS, SAND)
put(sp, 'E10', 'Uplift per store from 3 points of margin.')
put(sp, 'A11', 'Receivable held per store')
put(sp, 'B11', '=B8*B6/30', BLK, RS)
put(sp, 'C11', '=C8*C6/30', BLK, RS)
put(sp, 'D11', '=C11-B11', BLK, RS)
put(sp, 'A13', 'Pilot spend per store (one-time, first 3 months)', bold=True)
SP = [('Weekend promoter, ₹6,000 a month × 3 months', 18000), ('Sampling, ₹3,000 a month × 3 months', 9000), ('Shelf strips, wobblers, POSM', 3000),
      ('Listing fee: ₹2,500 × 6 SKUs for the 1 independent in 5 (chains waived)', 3000)]
for i, (lab, v) in enumerate(SP):
    put(sp, f'A{14+i}', lab)
    put(sp, f'B{14+i}', v, BLUE, RS)
put(sp, 'A18', 'Total pilot spend per store', bold=True)
put(sp, 'B18', '=SUM(B14:B17)', BLK, RS, SAND)
put(sp, 'A19', 'Payback at pilot terms (months)', bold=True)
put(sp, 'B19', '=B18/B10', BLK, CR, SAND)
put(sp, 'A20', 'Break-even MRP sales a month (recover spend in 6 months)')
put(sp, 'B20', '=B18/6/(B10/B7)', BLK, RS)
put(sp, 'A22', 'Value of proven terms across the plan', bold=True)
put(sp, 'A23', 'Stores at end FY29 (Inputs)')
put(sp, 'B23', '=MT_st_FY29', GRN, INT)
put(sp, 'A24', 'Extra contribution a year from proven terms (₹ lakh)')
put(sp, 'B24', '=D10*12*B23/10^5', BLK, CR, SAND)
put(sp, 'A25', 'Cash released from shorter credit (₹ lakh)')
put(sp, 'B25', '=-D11*B23/10^5', BLK, CR, SAND)
header(sp, 27, ['Give (what we offer)', 'Get (what we ask)', '', '', 'When'])
GG = [('Promoters and sampling in the test stores', 'Listing fee waived; eye-level slot', 'Pilot'),
      ('Weekly sell-out and stock reports we compile', 'Store-level POS data shared weekly', 'Pilot'),
      ('≥95% fill rate, next-day supply from Amingaon', 'Credit 60 → 45 days for stores 6+', 'After 2 of 5 stores clear the gate'),
      ('Co-funded festive promotions (50:50)', 'End-cap in Bihu, Puja, Diwali months', 'Proven'),
      ('Own-label namkeen co-packing quote', 'Range listing across all 74 NE stores', 'Proven'),
      ('Audit-ready claims: PO + store photo + debit note', 'No unapproved deductions', 'Always')]
for i, (g_, gt, w) in enumerate(GG):
    put(sp, f'A{28+i}', g_, wrap=True)
    put(sp, f'B{28+i}', gt, wrap=True)
    sp.merge_cells(f'B{28+i}:D{28+i}')
    put(sp, f'E{28+i}', w)

# =====================================================================================  EBITDA first (timeline)
eb = sheet('EBITDA', 'Fix EBITDA first: the quarterly ramp and when it is “corrected”',
           'Plan month 1 = Jan 2027. Levers ramp quarter by quarter; scaling stores waits for the corrected margin.',
           [34, 11, 11, 11, 11, 11, 11, 11, 11, 11, 40])
Q = ['Q4 FY27', 'Q1 FY28', 'Q2 FY28', 'Q3 FY28', 'Q4 FY28', 'Q1 FY29', 'Q2 FY29', 'Q3 FY29', 'Q4 FY29']
QM = [3, 6, 9, 12, 15, 18, 21, 24, 27]
RAMP = [0.05, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.0, 1.0]
header(eb, 4, ['Quarter'] + Q + ['Note'])
put(eb, 'A5', 'Months from start (end of quarter)')
put(eb, 'A6', 'Lever ramp (% of full effect)')
put(eb, 'A7', 'Cumulative lever effect (bps)')
put(eb, 'A8', 'EBITDA margin', bold=True)
put(eb, 'A9', 'Corrected? (≥ target)')
for j, (q, m, rp) in enumerate(zip(Q, QM, RAMP)):
    col = get_column_letter(2 + j)
    put(eb, f'{col}5', m, BLUE, INT)
    put(eb, f'{col}6', rp, BLUE, PCT)
    put(eb, f'{col}7', f'=L_total*{col}6', BLK, INT)
    put(eb, f'{col}8', f'=EB_start+{col}7/10000', BLK, PCT, SAND)
    put(eb, f'{col}9', f'=IF({col}8>=Target_corr,1,0)', BLK, INT)
put(eb, 'A11', 'First quarter at or above target', bold=True)
put(eb, 'B11', '=IFERROR(INDEX(B4:J4,1,MATCH(1,B9:J9,0)),"Not within 27 months")', BLK, None, SAND)
put(eb, 'A12', 'Months to correct', bold=True)
put(eb, 'B12', '=IFERROR(INDEX(B5:J5,1,MATCH(1,B9:J9,0)),"> 27")', BLK, INT, SAND)
name('Corr_q', 'EBITDA!$B$11')
name('Corr_m', 'EBITDA!$B$12')
put(eb, 'A14', 'Annual ramp (average of its quarters)', bold=True)
header(eb, 15, ['Year', 'FY27E', 'FY28P', 'FY29P', 'FY30P', 'FY31P', '', '', '', '', ''])
put(eb, 'A16', 'Ramp')
put(eb, 'B16', '=(0+0+0+B6)/4', BLK, PCT)
put(eb, 'C16', '=AVERAGE(C6:F6)', BLK, PCT)
put(eb, 'D16', '=AVERAGE(G6:J6)', BLK, PCT)
put(eb, 'E16', 1, BLUE, PCT)
put(eb, 'F16', 1, BLUE, PCT)
put(eb, 'A17', 'EBITDA margin')
for col in 'BCDE':
    put(eb, f'{col}17', f'=EB_start+L_total*{col}16/10000', BLK, PCT, SAND)
put(eb, 'F17', '=EB_start+(L_total*F16+OpLev31)/10000', BLK, PCT, SAND)
header(eb, 19, ['Lever (bps at full effect)', 'Active', '', '', '', '', '', '', '', '', 'Owner · how'])
LEV = [('L_proc', 'Purchase · gram at harvest, oil cover, local potato'), ('L_pack', 'Purchase · film gauge, reverse auction'),
       ('L_sku', 'Sales + Finance · cut tail of 236 SKUs'), ('L_yield', 'Plant · oil uptake, yield'), ('L_frt', 'Logistics · milk-runs, full loads'),
       ('L_trade', 'Sales · schemes on sell-out'), ('L_mix', 'Founder’s Office · MT and QC packs'), ('L_audit', 'Finance · 3-way claim audit'),
       ('L_copack', 'Founders · optional own-label co-pack'), ('L_invest', 'MT/QC team, promoters, ads')]
for i, (k, own) in enumerate(LEV):
    put(eb, f'A{20+i}', f'=Inputs!B{ROW[k]}', GRN, wrap=True)
    put(eb, f'B{20+i}', f'={k}', GRN, INT)
    put(eb, f'K{20+i}', own, wrap=True)
put(eb, f'A{20+len(LEV)}', 'Total', bold=True)
put(eb, f'B{20+len(LEV)}', '=L_total', GRN, INT, SAND)
g0 = 20 + len(LEV) + 3
put(eb, f'A{g0}', 'If the starting margin is different (1 = at or above target that quarter)', bold=True)
header(eb, g0 + 1, ['Starting EBITDA margin'] + Q + ['Months to correct'])
for i, st in enumerate([0.04, 0.05, 0.06, 0.07]):
    rr = g0 + 2 + i
    put(eb, f'A{rr}', st, BLUE, PCT)
    for j in range(9):
        col = get_column_letter(2 + j)
        put(eb, f'{col}{rr}', f'=IF($A{rr}+L_total*{col}$6/10000>=Target_corr,1,0)', BLK, INT)
    put(eb, f'K{rr}', f'=IFERROR(INDEX($B$5:$J$5,1,MATCH(1,B{rr}:J{rr},0)),"Not by month 27")', BLK, INT, SAND)
h0 = g0 + 7
put(eb, f'A{h0}', 'Months to correct by scenario (same starting margin; each scenario’s own levers)', bold=True)
header(eb, h0 + 1, ['Scenario'] + Q + ['Months to correct', 'Full-effect margin'])
LEVKEYS = ['L_proc', 'L_pack', 'L_sku', 'L_yield', 'L_frt', 'L_trade', 'L_mix', 'L_audit', 'L_copack', 'L_invest']
for i, (lab, colL) in enumerate([('Slow', 'C'), ('Base', 'D'), ('Fast', 'E')]):
    rr = h0 + 2 + i
    ltot = '+'.join(f'Inputs!${colL}${ROW[k]}' for k in LEVKEYS)
    put(eb, f'A{rr}', lab)
    for j in range(9):
        col = get_column_letter(2 + j)
        put(eb, f'{col}{rr}', f'=IF(EB_start+({ltot})*{col}$6/10000>=Target_corr,1,0)', BLK, INT)
    put(eb, f'K{rr}', f'=IFERROR(INDEX($B$5:$J$5,1,MATCH(1,B{rr}:J{rr},0)),"Not by month 27")', BLK, INT, SAND)
    put(eb, f'L{rr}', f'=EB_start+({ltot})/10000', BLK, PCT, SAND)
    name(f'Corr_m_{lab}', f'EBITDA!$K${rr}')
eb.column_dimensions['L'].width = 14

# =====================================================================================  Scale (annual)
s = sheet('Scale', 'Scale with the market: revenue, MT and QC, EBITDA, cash (FY25A–FY31P)',
          'Total revenue grows with the market; MT and QC grow inside it. FY27 is the current year (Apr 2026–Mar 2027); the plan starts Jan 2027.',
          [42] + [12] * 7 + [44])
header(s, 4, ['₹ Cr unless stated'] + YEARS + ['How'])
put(s, 'A5', 'Total revenue', bold=True)
put(s, 'B5', '=Rev_FY25', GRN, CR)
put(s, 'C5', '=B5*(1+g_FY26)', BLK, CR)
for k in range(2, 7):
    put(s, f'{YC[k]}5', f'={YC[k-1]}5*(1+g_mkt)', BLK, CR)
put(s, 'I5', 'FY25 actual; FY26 recovery; then the market rate.')
put(s, 'A6', 'Growth')
for k in range(1, 7):
    put(s, f'{YC[k]}6', f'={YC[k]}5/{YC[k-1]}5-1', BLK, PCT)
put(s, 'A8', 'MT stores selling (end of year)')
st_vals = ['0', '0', '=MT_st_FY27', '=MT_st_FY28', '=MT_st_FY29', '=MT_st_FY30', '=MT_st_FY31']
for k, v in enumerate(st_vals):
    put(s, f'{YC[k]}8', int(v) if v.isdigit() else v, BLUE if v.isdigit() else GRN, INT)
put(s, 'A9', 'Average MT stores in the year')
put(s, 'C9', 0, BLUE, CR)
put(s, 'D9', '=D8*Live_FY27/12', BLK, CR)
for k in range(3, 7):
    put(s, f'{YC[k]}9', f'=({YC[k-1]}8+{YC[k]}8)/2', BLK, CR)
put(s, 'I9', 'FY27: 5 test stores for Jan–Mar 2027 only.')
put(s, 'A10', 'Realisation per store a month (₹)')
for k in range(2, 7):
    put(s, f'{YC[k]}10', '=Store_real_m', GRN, RS)
put(s, 'A11', 'New-chain MT revenue')
for k in range(2, 7):
    put(s, f'{YC[k]}11', f'={YC[k]}9*{YC[k]}10*12*IF({YC[k]}8>{YC[k-1]}8,Maturity,1)/10^7', BLK, CR2)
put(s, 'A12', 'Existing MT + e-commerce')
put(s, 'B12', '=B5*Share_MTnow', BLK, CR2)
put(s, 'C12', '=B12*(1+g_FY26)', BLK, CR2)
for k in range(2, 7):
    put(s, f'{YC[k]}12', f'={YC[k-1]}12*(1+g_mkt)', BLK, CR2)
put(s, 'A13', 'Stores counted for SKU value/volume (average)')
for k in range(2, 7):
    put(s, f'{YC[k]}13', f'={YC[k]}9*IF({YC[k]}8>{YC[k-1]}8,Maturity,1)', BLK, CR)
put(s, 'A14', 'Modern trade revenue', bold=True)
for k in range(7):
    put(s, f'{YC[k]}14', f'=IFERROR({YC[k]}11,0)+{YC[k]}12', BLK, CR2, SAND)
put(s, 'A16', 'Dark stores listing Kishlay (end of year)')
qv = ['0', '0', '0', '=QC_st_FY28', '=QC_st_FY29', '=QC_st_FY30', '=QC_st_FY31']
for k, v in enumerate(qv):
    put(s, f'{YC[k]}16', int(v) if v.isdigit() else v, BLUE if v.isdigit() else GRN, INT)
put(s, 'A17', 'Average dark stores')
for k in range(1, 7):
    put(s, f'{YC[k]}17', f'=({YC[k-1]}16+{YC[k]}16)/2', BLK, CR)
put(s, 'A18', 'QC net sales per dark store a day (₹)')
for k in range(3, 7):
    put(s, f'{YC[k]}18', '=QC_day_net', GRN, RS2)
put(s, 'A19', 'Quick commerce revenue', bold=True)
for k in range(7):
    put(s, f'{YC[k]}19', f'=IFERROR({YC[k]}17*{YC[k]}18*365/10^7,0)', BLK, CR2, SAND)
put(s, 'A21', 'General trade and other')
for k in range(7):
    put(s, f'{YC[k]}21', f'={YC[k]}5-{YC[k]}14-{YC[k]}19', BLK, CR)
put(s, 'A22', 'MT + QC share of revenue', bold=True)
for k in range(7):
    put(s, f'{YC[k]}22', f'=({YC[k]}14+{YC[k]}19)/{YC[k]}5', BLK, PCT, SAND)
put(s, 'A24', 'EBITDA margin', bold=True)
put(s, 'B24', 'n/a')
put(s, 'C24', '=EB_start', GRN, PCT)
for k, col in zip(range(2, 7), 'BCDEF'):
    put(s, f'{YC[k]}24', f'=EBITDA!{col}17', GRN, PCT, SAND)
put(s, 'A25', 'EBITDA', bold=True)
for k in range(1, 7):
    put(s, f'{YC[k]}25', f'={YC[k]}5*{YC[k]}24', BLK, CR, SAND)
put(s, 'I24', 'FY25: net loss ₹6.31 Cr (−2.2%); EBITDA not disclosed.')
put(s, 'A27', 'MT receivables', bold=True)
for k in range(2, 7):
    put(s, f'{YC[k]}27', f'={YC[k]}14*Recv_MT/365', BLK, CR2)
put(s, 'A28', 'QC receivables')
for k in range(2, 7):
    put(s, f'{YC[k]}28', f'={YC[k]}19*Recv_QC/365', BLK, CR2)
put(s, 'A29', 'Carrying cost of receivables (₹ lakh)')
for k in range(2, 7):
    put(s, f'{YC[k]}29', f'=({YC[k]}27+{YC[k]}28)*CostFunds*100', BLK, CR)
put(s, 'A31', 'MT + QC contribution (₹ Cr)')
for k in range(2, 7):
    put(s, f'{YC[k]}31', f'={YC[k]}14*MT_contr_pct+{YC[k]}19*UE_QC_pct', BLK, CR2)
put(s, 'A32', 'MT volume (tonnes, new chains)')
for k in range(2, 7):
    put(s, f'{YC[k]}32', f'=Store_kg_m*12*{YC[k]}13/1000', BLK, CR)
put(s, 'A34', 'What MT could be: new-chain revenue at full maturity (₹ Cr a year)', bold=True)
put(s, 'A35', 'MRP sales per store a month (₹) ↓ · stores →', bold=True)
for j, n_st in enumerate([74, 180, 300, 500]):
    put(s, f'{get_column_letter(2+j)}35', n_st, BLUE, INT)
for i, mrp_m in enumerate([20000, '=Store_MRP_m', 45000, 60000]):
    rr = 36 + i
    put(s, f'A{rr}', mrp_m, BLUE if isinstance(mrp_m, int) else GRN, RS)
    for j in range(4):
        col = get_column_letter(2 + j)
        put(s, f'{col}{rr}', f'={col}$35*$A{rr}*(Store_real_m/Store_MRP_m)*12/10^7', BLK, CR2, SAND if i == 1 else None)
put(s, 'I35', '74 = Vishal’s Northeast stores; 180 = Base FY31; 300–500 needs East chains.', wrap=True)
s.freeze_panes = 'B5'

put(sk, f'B{tr+3}', 'QC net sales per dark store a day (₹, after GST and platform fee)')
put(sk, f'Q{tr+3}', f'=SUMPRODUCT(X{SK_FIRST}:X{SK_LAST},Y{SK_FIRST}:Y{SK_LAST})', BLK, RS2, SAND)
name('QC_day_net', f'SKU_Plan!$Q${tr+3}')
put(sk, f'X{tr}', f'=SUM(X{SK_FIRST}:X{SK_LAST})', BLK, CR2, SAND)

# =====================================================================================  Market and benchmarks
mk = sheet('Market', 'Market facts, chains and peers (verified unless marked)',
           'Each row has its source ID (Sources sheet). “Unverified” = from the shared research compendium, not re-checked against the original.',
           [52, 14, 14, 14, 14, 50])
header(mk, 4, ['Channel facts', 'Value', '', '', '', 'Source'])
CH = [('Brief: general trade share of the market', 0.76, 'User brief (to verify nationally)'),
      ('Brief: modern trade share', 0.17, 'User brief (to verify nationally)'),
      ('Brief: quick commerce share', 0.07, 'User brief (to verify nationally)'),
      ('E-commerce share of urban India FMCG, OND 2025', 0.06, 'NIQ [V01]'),
      ('E-commerce share, all metros', 0.14, 'NIQ [V01]'),
      ('E-commerce share, top 8 metros', 0.18, 'NIQ [V01]'),
      ('Quick commerce share of e-commerce FMCG (over)', 0.75, 'NIQ [V01]'),
      ('FMCG value growth, OND 2025', 0.078, 'NIQ [V01]; MT growth accelerated threefold vs Q3')]
for i, (lab, v, src) in enumerate(CH):
    put(mk, f'A{5+i}', lab)
    put(mk, f'B{5+i}', v, BLUE, PCT)
    put(mk, f'F{5+i}', src)
m0 = 5 + len(CH) + 1
header(mk, m0, ['Vishal Mega Mart, Northeast and East (26 Sep 2025)', 'Stores', 'Cities', '', '', 'Source'])
VM = [('Assam', 44, 34), ('Arunachal Pradesh', 7, 6), ('Manipur', 6, 6), ('Nagaland', 6, 5), ('Meghalaya', 4, 3), ('Sikkim', 4, 4), ('Tripura', 2, 2), ('Mizoram', 1, 1)]
for i, (stt, n_, cities) in enumerate(VM):
    put(mk, f'A{m0+1+i}', stt)
    put(mk, f'B{m0+1+i}', n_, BLUE, INT)
    put(mk, f'C{m0+1+i}', cities, BLUE, INT)
    put(mk, f'F{m0+1+i}', 'JM Financial Exhibit 39 [V02]')
ne = m0 + 1 + len(VM)
put(mk, f'A{ne}', 'Northeast total', bold=True)
put(mk, f'B{ne}', f'=SUM(B{m0+1}:B{ne-1})', BLK, INT, SAND)
put(mk, f'C{ne}', f'=SUM(C{m0+1}:C{ne-1})', BLK, INT, SAND)
EAST = [('West Bengal', 34, 26), ('Bihar', 32, 24), ('Odisha', 30, 25), ('Jharkhand', 18, 11), ('All India', 739, 469)]
for i, (stt, n_, cities) in enumerate(EAST):
    put(mk, f'A{ne+1+i}', stt)
    put(mk, f'B{ne+1+i}', n_, BLUE, INT)
    put(mk, f'C{ne+1+i}', cities, BLUE, INT)
    put(mk, f'F{ne+1+i}', 'JM Financial Exhibit 39 [V02]')
put(mk, f'A{ne+6}', 'DMart stores in East India')
put(mk, f'B{ne+6}', 0, BLUE, INT)
put(mk, f'F{ne+6}', 'JM Financial store mapping [V02]')
a0 = ne + 8
header(mk, a0, ['Vishal in Assam, FY24', 'Assam', 'Company avg', 'vs avg', '', 'Source'])
put(mk, f'A{a0+1}', 'Revenue per sq ft (₹)')
put(mk, f'B{a0+1}', 10551, BLUE, INT)
put(mk, f'C{a0+1}', 8084, BLUE, INT)
put(mk, f'D{a0+1}', f'=B{a0+1}/C{a0+1}-1', BLK, PCT)
put(mk, f'A{a0+2}', 'FMCG revenue per sq ft (₹)')
put(mk, f'B{a0+2}', 2829, BLUE, INT)
put(mk, f'C{a0+2}', 2225, BLUE, INT)
put(mk, f'D{a0+2}', f'=B{a0+2}/C{a0+2}-1', BLK, PCT)
put(mk, f'A{a0+3}', 'Assam stores (FY24) · FMCG sales (₹ mn)')
put(mk, f'B{a0+3}', 40, BLUE, INT)
put(mk, f'C{a0+3}', 2323, BLUE, INT)
put(mk, f'A{a0+4}', 'FMCG sales per Assam store a month (₹)')
put(mk, f'B{a0+4}', f'=C{a0+3}*10^6/B{a0+3}/12', BLK, RS)
put(mk, f'A{a0+5}', 'Snacks and namkeen share of FMCG (hypothesis)')
put(mk, f'B{a0+5}', 0.08, BLUE, PCT, YEL)
put(mk, f'A{a0+6}', 'Snack sales per Assam store a month (₹)')
put(mk, f'B{a0+6}', f'=B{a0+4}*B{a0+5}', BLK, RS)
put(mk, f'A{a0+7}', 'Kishlay share of that shelf implied by SKU_Plan', bold=True)
put(mk, f'B{a0+7}', f'=Store_MRP_m/B{a0+6}', BLK, PCT, SAND)
for k in range(1, 4):
    put(mk, f'F{a0+k}', 'JM Financial Exhibit 45 [V02]')
put(mk, f'F{a0+7}', 'Sanity check on the ROS assumption.')
t0 = a0 + 9
header(mk, t0, ['Modern-trade terms by chain', 'Margin low', 'Margin high', 'Pay days low', 'Pay days high', 'Source'])
TT = [('DMart', 0.18, 0.28, 45, 60), ('Reliance Smart', 0.22, 0.32, 45, 75), ('More Retail', 0.22, 0.30, 30, 60), ('Spencer’s', 0.25, 0.35, 45, 75), ('Star Bazaar', 0.22, 0.32, 45, 60)]
for i, (c, lo, hi, d1, d2) in enumerate(TT):
    put(mk, f'A{t0+1+i}', c)
    put(mk, f'B{t0+1+i}', lo, BLUE, PCT)
    put(mk, f'C{t0+1+i}', hi, BLUE, PCT)
    put(mk, f'D{t0+1+i}', d1, BLUE, INT)
    put(mk, f'E{t0+1+i}', d2, BLUE, INT)
    put(mk, f'F{t0+1+i}', 'Terra Insight, 12 Jun 2026 [V04]')
x0 = t0 + 7
header(mk, x0, ['Retailer cash and basket facts', 'Value', '', '', '', 'Source'])
RX = [('Vishal payable days, FY25', 50, INT, 'JM Financial Exhibit 37 [V02]'),
      ('DMart payable days, FY25', 6, INT, 'JM Financial Exhibit 37 [V02]'),
      ('Vishal vendor credit linked to ~80% sell-through (days)', 90, INT, 'JM Financial [V02]'),
      ('DMart average bill value FY26 (₹)', 1683, INT, 'PL Capital, 28 Jul 2026 [V03]'),
      ('DMart bills per store a day FY26', 2383, INT, 'PL Capital [V03]'),
      ('Vishal average bill value, Q4 FY25 (₹)', 875, INT, 'Aggregator of management comment [V13]'),
      ('Vishal stores, June 2026 (East region 204)', 819, INT, 'Company update via news [V13]')]
for i, (lab, v, fmt, src) in enumerate(RX):
    put(mk, f'A{x0+1+i}', lab)
    put(mk, f'B{x0+1+i}', v, BLUE, fmt)
    put(mk, f'F{x0+1+i}', src)
p0 = x0 + 9
header(mk, p0, ['Own-label namkeen price per gram (JM Exhibit 28)', '₹/g own label', '₹/g brand', 'Own label dearer by', '', 'Pair'])
OL = [('First Crop Aloo Bhujia 150 g vs Haldiram’s 400 g', 40.2 / 150, 100 / 400), ('First Crop Khatta Meetha 150 g vs Haldiram’s 420 g', 40.2 / 150, 100 / 420),
      ('First Crop salted peanuts 130 g vs Bikano 200 g', 43.6 / 130, 60 / 200), ('First Crop coated peanuts 130 g vs Bikano 200 g', 40.2 / 130, 60 / 200)]
for i, (lab, a, b) in enumerate(OL):
    put(mk, f'A{p0+1+i}', lab)
    put(mk, f'B{p0+1+i}', round(a, 4), BLUE, '0.000')
    put(mk, f'C{p0+1+i}', round(b, 4), BLUE, '0.000')
    put(mk, f'D{p0+1+i}', f'=B{p0+1+i}/C{p0+1+i}-1', BLK, PCT)
    put(mk, f'F{p0+1+i}', '[V02]')
b0 = p0 + 6
header(mk, b0, ['Peers: how they are scaling MT and QC', 'Value', '', '', '', 'Source'])
PEER = [('Bikaji: e-com + QC share of business (FY26 exit, ~100% growth)', 0.03, PCT, 'Q4 FY26 call coverage [V10]'),
        ('Bikaji FY26 EBITDA margin', 0.137, PCT, 'FY26 results [V10]'),
        ('Prataap: QC share of sales today (1.2–1.5%)', 0.0135, PCT, 'Concall coverage [V11]'),
        ('Prataap: QC target in ~3 years', 0.05, PCT, 'Concall coverage [V11]'),
        ('Gopal FY26 EBITDA margin', 0.067, PCT, 'FY26 results [V12]'),
        ('Gopal e-commerce sales (₹ Cr, from ₹0.37 Cr)', 1.92, CR2, 'Q3 FY26 coverage [V12]')]
for i, (lab, v, fmt, src) in enumerate(PEER):
    put(mk, f'A{b0+1+i}', lab, wrap=True)
    put(mk, f'B{b0+1+i}', v, BLUE, fmt)
    put(mk, f'F{b0+1+i}', src)
e0 = b0 + 8
header(mk, e0, ['Shopper and shelf science', 'Finding', '', '', '', 'Source · status'])
SCI = [('Shelf location vs facings', 'Location had a large impact on sales; extra facings much less once out-of-stocks are avoided. Customised shelf sets +4%; reorganisation 5–6%.', 'Drèze, Hoch & Purk 1994 [V06] · abstract verified; “+39% at eye level” not verified'),
       ('Store-manager quality and rollout', 'New products first placed with high-quality managers reach 28.5% more stores in 11 months; entry odds 24.25% vs 5.28%.', 'Amano & Tamayo, HBS 2025 [V05] · verified; Colombian chain'),
       ('New products are slower', 'New items: inventory age 94.4 days vs 78.1 for existing items.', '[V05] · verified'),
       ('Out-of-stocks', 'When an item is missing, 31% of shoppers buy elsewhere and 26% switch brand; average OOS 8.3%.', 'Gruen, Corsten & Bharadwaj 2002 [V07] · not re-checked'),
       ('Eye level by shopper (India)', 'Adult women ~152 cm → eye ~140 cm; children 6–10 years ~115–138 cm tall → eye ~105–128 cm.', 'Height studies [V25] · approximate')]
for i, (a, b, c) in enumerate(SCI):
    put(mk, f'A{e0+1+i}', a, wrap=True)
    put(mk, f'B{e0+1+i}', b, wrap=True)
    mk.merge_cells(f'B{e0+1+i}:E{e0+1+i}')
    put(mk, f'F{e0+1+i}', c, wrap=True)
    mk.row_dimensions[e0 + 1 + i].height = 42

# =====================================================================================  Chains scorecard + test stores
ch = sheet('Chains', 'Which chain first: weighted scorecard',
           'Scores 1–5 are judgement calls to revisit after the first buyer meetings. Weights in row 5.',
           [30, 12, 12, 12, 12, 12, 12, 12, 12, 10, 50])
crit = ['NE / Assam stores', 'Store productivity', 'Shopper fit (₹55–₹110)', 'Margin asked', 'Payment speed', 'Distance from Amingaon', 'Ease of entry']
header(ch, 4, ['Chain'] + crit + ['Weighted score', 'Rank', 'Why'])
W = [0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05]
put(ch, 'A5', 'Weight', bold=True)
for j, w in enumerate(W):
    put(ch, f'{get_column_letter(2+j)}5', w, BLUE, PCT)
CHS = [('Vishal Mega Mart', [5, 5, 5, 3, 2, 5, 3], '74 NE stores, 44 in Assam; Assam #1 revenue/sq ft; value shoppers; own-label namkeen dearer per gram than brands.'),
       ('Guwahati independents', [2, 2, 4, 4, 4, 5, 5], 'Fast, cheap pilot doors; small scale.'),
       ('Reliance Smart / Smart Point', [3, 4, 4, 2, 2, 4, 2], 'Central buying, 22–32% margin, T+45–75.'),
       ('DMart', [1, 5, 4, 3, 5, 1, 2], 'No East/NE stores today; benchmark for later.'),
       ('More Retail', [2, 3, 4, 2, 3, 2, 3], '22–30%, T+30–60; Bengal and Odisha.'),
       ('Spencer’s', [1, 3, 3, 1, 2, 2, 4], '25–35%, T+45–75; Kolkata-focused.')]
for i, (c, sc_, why) in enumerate(CHS):
    rr = 6 + i
    put(ch, f'A{rr}', c)
    for j, v in enumerate(sc_):
        put(ch, f'{get_column_letter(2+j)}{rr}', v, BLUE, INT)
    put(ch, f'I{rr}', f'=SUMPRODUCT($B$5:$H$5,B{rr}:H{rr})', BLK, CR2, SAND)
    put(ch, f'J{rr}', f'=RANK(I{rr},$I$6:$I${5+len(CHS)})', BLK, INT)
    put(ch, f'K{rr}', why, wrap=True)
ts0 = 6 + len(CHS) + 2
put(ch, f'A{ts0}', 'Test stores: pick 5 strong stores, not every store', bold=True)
header(ch, ts0 + 1, ['Criterion', 'Weight', 'Store 1', 'Store 2', 'Store 3', 'Store 4', 'Store 5', 'Control A', 'Control B', '', 'How to score'])
TS = [('Bills a day / footfall', 0.25, 'Chain data or entry counts at peak hours'), ('FMCG sales density', 0.25, 'Chain category data'),
      ('Store-manager quality', 0.20, 'Manager tenure, store rank; HBS: managers drive rollout'), ('Distance ≤ 30 km from Amingaon', 0.15, 'Same-day refill'),
      ('Shopper mix: families with kids', 0.15, 'Weekend audit')]
for i, (c, w, how) in enumerate(TS):
    rr = ts0 + 2 + i
    put(ch, f'A{rr}', c)
    put(ch, f'B{rr}', w, BLUE, PCT)
    for col in 'CDEFGHI':
        put(ch, f'{col}{rr}', None, BLUE, INT, YEL)
    put(ch, f'K{rr}', how, wrap=True)
rr = ts0 + 2 + len(TS)
put(ch, f'A{rr}', 'Score (fill 1–5 above)', bold=True)
for col in 'CDEFGHI':
    put(ch, f'{col}{rr}', f'=SUMPRODUCT($B${ts0+2}:$B${rr-1},{col}{ts0+2}:{col}{rr-1})', BLK, CR2, SAND)
put(ch, f'A{rr+1}', 'Suggested: 3 Vishal Guwahati stores, 1 Reliance Smart, 1 independent; 2 matched control stores without the range.')
put(ch, f'A{rr+2}', 'Gate to expand: ≥2 of 5 stores at ≥ target units per SKU per week for two 4-week cycles, fill rate ≥95%, contribution after promotions ≥ GT.')

# =====================================================================================  Segments
sg = sheet('Segments', 'Who buys in modern trade: behaviour and psychographics first, then demographics',
           'Personas are hypotheses to confirm with the shopper intercepts on the Primary_Research sheet.',
           [26, 34, 34, 30, 26, 22, 26])
header(sg, 4, ['Persona', 'Behaviour (what they do)', 'Psychographic (why)', 'Hero SKUs', 'Shelf zone', 'Price point', 'Demographics'])
PER = [('Planner mother', 'Monthly stock-up with a list; compares ₹ per gram; buys for the family and guests', 'Trust, value, hospitality (chai-time)', '400 g Bikaneri / Paneer Bhujia; Aloo Bhujia 200 g', 'Adult eye level (~120–150 cm)', '₹55–₹110', 'Women 30–45; household ₹30k–1L a month'),
       ('Kids with parents', 'Spot colourful packs; ask; parents trade up to multipacks', 'Fun, characters, “my snack”', 'Rings 12 × ₹5; Noodles 6 × ₹10; Butter Cookies', 'Kids’ eye level (~90–125 cm)', '₹40–₹60 multipacks', 'Children 5–12'),
       ('Young snacker', 'Impulse; tries new flavours; also on quick commerce', 'Heat, regional pride, novelty', 'Jolokia Chanachur; Jhalmuri', 'Grab level, end caps; QC apps', '₹55', '18–30; students, young professionals'),
       ('Host / premium buyer', 'Festival and guest purchases; gifts', 'Status, assortment, quality', 'Party Box 12 × ₹10; Festive Tin 500 g', 'Festive end caps; bottom shelf for boxes', '₹120–₹199', 'Household ₹1–1.5L a month')]
for i, row in enumerate(PER):
    for j, v in enumerate(row):
        put(sg, f'{get_column_letter(1+j)}{5+i}', v, wrap=True)
    sg.row_dimensions[5 + i].height = 46
put(sg, 'A11', 'Price-per-gram ladder: Haldiram’s 400 g ₹0.25/g · Vishal own label ₹0.27/g · Kishlay 200/400 g ₹0.275/g (Procurement sheet). Compete on taste and range, not on per-gram price.', wrap=True)
sg.merge_cells('A11:G11')
sg.row_dimensions[11].height = 30

# =====================================================================================  QC plan
qc = sheet('QC_Plan', 'Quick commerce: second priority, Guwahati first',
           'Only basket-building packs; ₹5/₹10 singles do not pay for picking. Fees and units are inputs.',
           [40, 16, 16, 60])
header(qc, 4, ['Item', 'Value', 'Unit', 'Note'])
QCR = [('Net sales per dark store a day', '=QC_day_net', '₹', 'MRP less GST and platform fee, weighted by rate of sale'),
       ('Contribution % (400 g, after ads)', '=UE_QC_pct', '%', 'Unit_Econ'),
       ('Contribution ₹/kg (400 g)', '=UE_QC_kg', '₹/kg', 'vs GT and MT in Unit_Econ'),
       ('SKUs listed per dark store', '=QC_SKUs', 'SKUs', 'SKU_Plan column T'),
       ('Units per SKU per dark store a day', '=QC_units', 'units', 'Gate ≥1.0 to scale'),
       ('Revenue FY31 (₹ Cr)', '=Scale!H19', '₹ Cr', 'Scale sheet')]
for i, (a, f_, u, n_) in enumerate(QCR):
    put(qc, f'A{5+i}', a)
    put(qc, f'B{5+i}', f_, GRN, PCT if '%' in u else (CR2 if '₹ Cr' in u else RS2))
    put(qc, f'C{5+i}', u)
    put(qc, f'D{5+i}', n_)

# =====================================================================================  Data capture
dc = sheet('Data_Capture', 'What data to capture, from where, how often, and the decision it drives',
           'Modern trade and quick commerce generate store-level data that general trade never gives. Capture it from week 1.',
           [32, 30, 14, 20, 50])
header(dc, 4, ['Data point', 'Source', 'Frequency', 'Owner', 'Decision it drives'])
DCR = [('Sell-out by SKU × store', 'Chain vendor portal / store reports', 'Weekly', 'MT lead', 'Keep, fix or drop each SKU (A/B/C)'),
       ('Units per SKU per store a week', 'Same', 'Weekly', 'MT lead', 'Expansion gate; facings'),
       ('Out-of-stock and fill rate (OTIF)', 'Distributor + store checks', 'Twice a week', 'Supply chain', 'Refill frequency, safety stock'),
       ('Shelf position and facings (photo)', 'Merchandiser app, geotagged photos', 'Weekly', 'Merchandiser', 'Planogram compliance; claim audit'),
       ('Price per gram vs Haldiram’s, Bikaji, own label', 'Store audit', 'Monthly', 'Founder’s Office', 'Pack-price changes'),
       ('Promotion uplift and claims vs PO', 'Retailer debit notes + PO + photos', 'Per promo', 'Finance', 'Approve/dispute claims (Terra 3-way)'),
       ('Basket attach (tea, biscuits)', 'Chain basket data if shared', 'Monthly', 'Founder’s Office', 'Cross-merchandising, combos'),
       ('Receivable ageing by chain', 'ERP', 'Weekly', 'Finance', 'Credit limits, follow-ups'),
       ('Expiry and returns', 'Store returns', 'Monthly', 'QA', 'Batch sizes, FEFO'),
       ('QC: search rank, availability, ratings, conversion, repeat', 'Platform seller dashboards', 'Daily/weekly', 'E-com executive', 'Ads, listings, packs'),
       ('Digital presence today (BigBasket, Amazon, Blinkit)', 'Listing audit', 'Week 1', 'Founder’s Office', 'Baseline before launch')]
for i, row in enumerate(DCR):
    for j, v in enumerate(row):
        put(dc, f'{get_column_letter(1+j)}{5+i}', v, wrap=True)

# =====================================================================================  Primary research
rs = sheet('Primary_Research', 'Primary research to run before and during the test (none done yet)',
           'Every persona, ROS and price assumption above is a hypothesis until these are done.',
           [36, 18, 14, 22, 60])
header(rs, 4, ['Study', 'Sample', 'When', 'Owner', 'What we learn'])
PRS = [('Shelf audit in 10 Guwahati MT stores', '10 stores', 'Week 1–2', 'Founder’s Office', 'Who sits at eye level, facings, price per gram, gaps'),
       ('Shopper intercepts at snack aisles', '300 shoppers', 'Week 2–4', 'Agency / interns', 'Age, income band, trip type, kids along, brands, flavours, price sensitivity'),
       ('Store-manager interviews', '10 managers', 'Week 2–3', 'MT lead', 'What sells, who shops when, refill pain points'),
       ('Category-manager meetings (Vishal NE, Reliance)', '2–3 buyers', 'Week 3–6', 'Founders + MT lead', 'Terms, listing, data sharing, private-label needs'),
       ('Quick-commerce listing and price check', '10 SKUs × 4 apps × 2 cities', 'Tonight / week 1', 'Founder’s Office', 'Are we listed? Price and rank vs rivals'),
       ('Internal data pull', 'SKU sales, margins, distributor towns', 'Week 1', 'Finance + Sales', 'Replace every hypothesis in Inputs'),
       ('Logistics check', 'Vehicles, cost per trip, drop counts', 'Week 1', 'Logistics', 'Real freight ₹/kg by city')]
for i, row in enumerate(PRS):
    for j, v in enumerate(row):
        put(rs, f'{get_column_letter(1+j)}{5+i}', v, wrap=True)

# =====================================================================================  Sources
so = sheet('Sources', 'Sources (verified this session unless marked)', 'Links open the original. “Not re-checked” items come from the shared compendium or prior work.', [7, 70, 18, 16, 80])
header(so, 4, ['ID', 'Source', 'Status', 'Date', 'Link'])
SRC = [('V01', 'NIQ: GST 2.0 transition reshapes India’s FMCG growth (OND 2025): FMCG +7.8%; MT 3× acceleration; e-com 6% urban, 14% metros, 18% top-8; QC >¾ of e-com FMCG', 'Verified', 'Feb 2026', 'https://nielseniq.com/global/en/news-center/2026/niq-gst-2-0-transition-reshapes-indias-fmcg-growth-landscape/'),
       ('V02', 'JM Financial: Vishal Mega Mart (store map by state, Assam productivity, payables, own-label prices)', 'Verified', '28 Sep 2025', 'https://bsmedia.business-standard.com/_media/bs/data/market-reports/equity-brokertips/2025-09/17591383890.14170200.pdf'),
       ('V03', 'PL Capital: Avenue Supermarts (DMart) analyst meet: 500 stores FY26, 398 mn bills, ABV ₹1,683', 'Verified', '28 Jul 2026', 'https://plindia.com/ResReport/DMART-28-7-26-PL.pdf'),
       ('V04', 'Terra Insight: Modern trade channel reconciliation (margins, payment cycles, promo over-funding 4–9%, 60–85 bps recovery)', 'Verified', '12 Jun 2026', 'https://www.terra-insight.com/insights/modern-trade-channel-reconciliation-d2c-india/'),
       ('V05', 'Amano & Tamayo (HBS WP): New product diffusion within retailers (Colombian chain)', 'Verified', 'Feb 2025', 'https://www.jorge-tamayo.com/s/New-Products-Diffusion-within-Retailers-The-Effect-of-Managerial-Quality-on-Rollout.pdf'),
       ('V06', 'Drèze, Hoch & Purk: Shelf management and space elasticity, Journal of Retailing', 'Abstract verified', '1994', 'https://repository.upenn.edu/handle/20.500.14332/39417'),
       ('V07', 'Gruen, Corsten & Bharadwaj: Retail out-of-stocks, a worldwide examination (GMA)', 'Not re-checked', '2002', ''),
       ('V08', 'Tracxn profiles: Kishlay Foods (FY25 ₹288 Cr, −16%, loss ₹6.31 Cr) and Tulsi Speciality Foods (supplied PDFs)', 'Verified', 'Nov 2026', 'Supplied by the user; not redistributed'),
       ('V09', 'CRISIL rating rationales (raw materials 70–75% of cost; bank limits 93%; FY23 PAT −₹11.50 Cr)', 'Verified earlier', '2021–2026', 'https://www.crisilratings.com'),
       ('V10', 'Bikaji FY26 results and Q4 FY26 call coverage (EBITDA 13.7%; e-com + QC ~3%)', 'Secondary', 'May 2026', 'https://www.bikaji.com/pub/media/Investor-Presentation-21-05-2026.pdf'),
       ('V11', 'Prataap Snacks concall coverage (QC 1.2–1.5%, ~5% target)', 'Secondary', '2026', 'https://www.multibagg.ai/market-pulse/articles/prataap-snacks-namkeen-chips-availability-concall-cmw549f19002m2wobcfg1bakl'),
       ('V12', 'Gopal Snacks FY26 (₹1,508 Cr, EBITDA 6.7%; e-com ₹1.92 Cr)', 'Secondary', 'May 2026', 'https://www.multibagg.ai/market-pulse/articles/gopal-fy26-93790'),
       ('V13', 'Vishal Mega Mart: 819 stores (Jun 2026, East 204); ABV ₹875 (Q4 FY25)', 'Secondary', '2025–2026', 'https://www.kotakneo.com/news/stocks/vishal-mega-mart-q1-fy27-results-net-profit-jumps-25-6-revenue-up-18-7/'),
       ('V15', 'Gram (chana) MSP ₹5,650/q 2025-26; ₹5,875/q 2026-27', 'Verified', 'Oct 2024 / Oct 2025', 'https://www.tribuneindia.com/news/india/centre-hikes-wheat-msp-by-rs-160-to-rs-2585-per-quintal'),
       ('V16', 'Palm oil prices: DCA retail ₹129.6–145/kg; Ahmedabad ~₹149/kg (Feb 2026)', 'Secondary', 'Feb 2026', 'https://www.ceicdata.com/en/india/retail-price-department-of-consumer-affairs-agriculture-commodities-daily-by-states-palm-oil'),
       ('V20', 'Kishlay Foods website: 236 products in 18 categories', 'Verified earlier', 'Nov 2026', 'https://kishlayfoods.com'),
       ('V21', 'Trade margins and QC: snack trade margins 3–5%; QC commissions 20–23%; Blinkit in Guwahati since Jan 2025', 'Secondary', '2024–2026', 'https://business-standard.com/companies/news/reliance-consumer-targets-chips-biscuits-market-with-higher-trade-margins-124110300468_1.html'),
       ('V22', 'BigBasket listings: Kishlay 200 g ₹55, 400 g ₹110; Haldiram’s 200 g ₹55', 'Indexed', '2026', 'https://www.bigbasket.com'),
       ('V23', 'GST 2.0: namkeen, biscuits at 5% from 22 Sep 2025', 'Verified earlier', 'Sep 2025', 'https://cbic-gst.gov.in'),
       ('V24', 'Savoury snacks market growth 8–12% (Ken Research, Market Report Analytics, Technavio, Mordor)', 'Secondary', '2025', 'https://www.kenresearch.com'),
       ('V25', 'Heights: Indian women ~152 cm; children 6–10 years ~115–138 cm (NFHS height data; IAP growth charts)', 'Approximate', '2015–2021', 'No single link: approximate public height references'),
       ('U1', 'Compendium items not verified: Kearney discounts (MT 13–18%, QC 6–9%, GT 2–5%); Redseer QC incremental 6–8%; ICICI Sec Vishal loyalty 92% of sales; “+39% at eye level”', 'Unverified', '—', 'Shared research compendium (Modern_Trade_Research_Playbook_Northeast_India.pdf)')]
for i, row in enumerate(SRC):
    for j, v in enumerate(row):
        put(so, f'{get_column_letter(1+j)}{5+i}', v, wrap=True)

# =====================================================================================  Summary
sm = wb['Sheet']
sm.title = 'Summary'
sm.sheet_view.showGridLines = False
for i, w in enumerate([48, 13, 13, 13, 13, 13, 13, 50], 1):
    sm.column_dimensions[get_column_letter(i)].width = w
sm['A1'] = 'Kishlay: win modern trade, fix EBITDA first, then scale with the market'
sm['A1'].font = TITLE
sm['A2'] = 'Tulsi Speciality Foods (manufacturing, Amingaon) + Kishlay Foods (brands). Prepared by Chethan N. Switch the scenario in Inputs!B3.'
sm['A2'].font = SUB
put(sm, 'A4', 'Scenario', bold=True)
put(sm, 'B4', '=Inputs!C3', GRN)
header(sm, 6, ['₹ Cr unless stated', 'FY26E', 'FY27E', 'FY28P', 'FY29P', 'FY30P', 'FY31P', 'Reading'])
SUMROWS = [('Total revenue', 5, CR), ('Modern trade revenue', 14, CR2), ('Quick commerce revenue', 19, CR2), ('MT + QC share of revenue', 22, PCT),
           ('EBITDA margin', 24, PCT), ('EBITDA', 25, CR), ('MT stores selling (end of year)', 8, INT), ('Dark stores (end of year)', 16, INT),
           ('MT + QC receivables', None, CR2), ('MT volume, new chains (tonnes)', 32, CR)]
for i, (lab, srow, fmt) in enumerate(SUMROWS):
    rr = 7 + i
    put(sm, f'A{rr}', lab, bold=i in (0, 5))
    for j, yc in enumerate('CDEFGH'):
        col = get_column_letter(2 + j)
        f_ = f'=Scale!{yc}27+Scale!{yc}28' if srow is None else f'=Scale!{yc}{srow}'
        put(sm, f'{col}{rr}', f_ if not (srow is None and yc == 'C') else 0, GRN, fmt)
put(sm, 'A18', 'EBITDA “corrected” (≥ target) in', bold=True)
put(sm, 'B18', '=Corr_q', GRN, None, SAND)
put(sm, 'C18', '=Corr_m', GRN, INT, SAND)
put(sm, 'D18', 'months from Jan 2027')
put(sm, 'A19', 'Per MT store a month: MRP sales · realisation · contribution (₹)')
put(sm, 'B19', '=Store_MRP_m', GRN, RS)
put(sm, 'C19', '=Store_real_m', GRN, RS)
put(sm, 'D19', '=Store_contr_m', GRN, RS)
put(sm, 'A20', 'Contribution ₹/kg: GT ₹10 namkeen · GT 400 g · MT 400 g · MT 1 kg · QC 400 g')
put(sm, 'B20', '=UE_GT10_kg', GRN, RS)
put(sm, 'C20', '=UE_GT400_kg', GRN, RS)
put(sm, 'D20', '=UE_MT400_kg', GRN, RS)
put(sm, 'E20', '=UE_MT1kg_kg', GRN, RS)
put(sm, 'F20', '=UE_QC_kg', GRN, RS)
put(sm, 'A21', 'Pilot store payback (months) · extra contribution from proven terms (₹ lakh/yr)')
put(sm, 'B21', '=Store_PnL!B19', GRN, CR)
put(sm, 'C21', '=Store_PnL!B24', GRN, CR)
put(sm, 'A22', 'Implied Kishlay share of a Vishal Assam store’s snack shelf')
put(sm, 'B22', f'=Market!B{a0+7}', GRN, PCT)
put(sm, 'A23', 'Months to correct EBITDA: Slow · Base · Fast')
put(sm, 'B23', '=Corr_m_Slow', GRN, INT)
put(sm, 'C23', '=Corr_m_Base', GRN, INT)
put(sm, 'D23', '=Corr_m_Fast', GRN, INT)
put(sm, 'A24', 'Checks', bold=True)
put(sm, 'A25', 'Revenue split adds up (FY31)')
put(sm, 'B25', '=IF(ABS(Scale!H5-Scale!H14-Scale!H19-Scale!H21)<0.001,"OK","CHECK")')
put(sm, 'A26', 'GT and other stays positive in every year')
put(sm, 'B26', '=IF(MIN(Scale!C21:H21)>0,"OK","CHECK")')
put(sm, 'A28', 'Colour code: blue input · black formula · green link · yellow validate first. Sheets: Inputs, Scale, EBITDA, SKU_Plan, Unit_Econ, Store_PnL, Chains, Supply_Chain, Procurement, Segments, QC_Plan, Data_Capture, Primary_Research, Market, Sources.', wrap=True)
sm.merge_cells('A28:H28')
sm.row_dimensions[28].height = 44

# ---- Raw materials to buy for the MT range (links SKU_Plan tonnes × Procurement recipes)
q = PROC_BPS + 5
put(pr, f'A{q}', 'Raw materials to buy for the MT range (tonnes a year)', bold=True)
header(pr, q + 1, ['Raw material', 'FY29P', 'FY31P', '', '', '', '', '', '', 'Basis'])
t_first, t_last = v0 + 1, v0 + len(SKUS)
for k, n_ in enumerate(names_list):
    rrow = REC_FIRST + k
    rr = q + 2 + k
    put(pr, f'A{rr}', n_)
    for colY, colOut in (('J', 'B'), ('L', 'C')):
        terms = '+'.join(f'${get_column_letter(2+j)}${rrow}*SUMIF(SKU_Plan!$E${SK_FIRST}:$E${SK_LAST},"{FAM[j]}",SKU_Plan!{colY}${t_first}:{colY}${t_last})' for j in range(len(FAM)))
        put(pr, f'{colOut}{rr}', f'={terms}', BLK, CR)
rr = q + 2 + len(names_list)
put(pr, f'A{rr}', 'Total inputs (tonnes)', bold=True)
put(pr, f'B{rr}', f'=SUM(B{q+2}:B{rr-1})', BLK, CR, SAND)
put(pr, f'C{rr}', f'=SUM(C{q+2}:C{rr-1})', BLK, CR, SAND)
put(pr, f'J{q+2}', 'Tonnes of finished goods by SKU (SKU_Plan) × kg of input per kg (recipes above). Fresh potato is in fresh weight.', wrap=True)

order = ['Summary', 'Inputs', 'Scale', 'EBITDA', 'SKU_Plan', 'Unit_Econ', 'Store_PnL', 'Chains', 'Supply_Chain', 'Procurement', 'Segments', 'QC_Plan', 'Data_Capture', 'Primary_Research', 'Market', 'Sources']
wb._sheets = [wb[n_] for n_ in order]
for ws in wb.worksheets:
    ws.sheet_properties.tabColor = 'C8141C' if ws.title in ('Summary', 'Inputs', 'Scale', 'EBITDA') else '1E1712'
wb.save(OUT)
print('saved', OUT)
