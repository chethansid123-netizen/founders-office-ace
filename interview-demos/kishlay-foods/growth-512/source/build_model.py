"""Build the Kishlay Group ₹512 Cr growth model (Excel, live formulas).
Usage: python3 build_model.py <out.xlsx>
Every hardcoded number is an input (blue) with its basis and source; every output is a formula.
"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter

OUT = sys.argv[1] if len(sys.argv) > 1 else 'Kishlay-512-Growth-Model.xlsx'
F = 'Arial'
BLUE = Font(name=F, size=10, color='0000FF')
BLK = Font(name=F, size=10, color='000000')
GRN = Font(name=F, size=10, color='008000')
BOLD = Font(name=F, size=10, bold=True)
HDR = Font(name=F, size=10, bold=True, color='FFFFFF')
TITLE = Font(name=F, size=14, bold=True, color='C8141C')
SUB = Font(name=F, size=10, italic=True, color='5E5147')
RED_FILL = PatternFill('solid', fgColor='C8141C')
INK_FILL = PatternFill('solid', fgColor='1E1712')
SAND = PatternFill('solid', fgColor='FBF3E6')
YEL = PatternFill('solid', fgColor='FFFF00')
GREY = PatternFill('solid', fgColor='F2EEE8')
THIN = Side(style='thin', color='D9CBB5')
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
WRAP = Alignment(wrap_text=True, vertical='top')
CR = '#,##0.0;(#,##0.0);"-"'
CR2 = '#,##0.00;(#,##0.00);"-"'
RS = '₹#,##0.00;(₹#,##0.00);"-"'
PCT = '0.0%;(0.0%);"-"'
BPS = '#,##0" bps";(#,##0" bps");"-"'
MULT = '0.00"x"'
INT = '#,##0;(#,##0);"-"'

wb = Workbook()


def sheet(name, title, subtitle, widths):
    ws = wb.create_sheet(name)
    ws['A1'] = title
    ws['A1'].font = TITLE
    ws['A2'] = subtitle
    ws['A2'].font = SUB
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.sheet_view.showGridLines = False
    return ws


def header(ws, row, labels, fill=INK_FILL):
    for i, lab in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=lab)
        c.font = HDR
        c.fill = fill
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


# ---------------------------------------------------------------- Inputs
inp = sheet('Inputs', 'Inputs and scenario levers',
            'Blue = hardcoded input · black = formula · yellow fill = key assumption to validate first. Change B3 to switch scenario (1 Bear, 2 Base, 3 Bull).',
            [10, 52, 11, 11, 11, 12, 10, 13, 90])
put(inp, 'A3', 'Scenario', bold=True)
put(inp, 'B3', 2, BLUE, fill=YEL)
inp['B3'].number_format = '0'
put(inp, 'C3', '=CHOOSE(B3,"Bear","Base","Bull")', BLK)
dv = DataValidation(type='whole', operator='between', formula1='1', formula2='3', allow_blank=False)
inp.add_data_validation(dv)
dv.add('B3')
name('Scenario', 'Inputs!$B$3')
header(inp, 5, ['ID', 'Parameter', 'Bear', 'Base', 'Bull', 'Active', 'Unit', 'Label', 'Basis and source (see Sources sheet)'])

# (id, parameter, bear, base, bull, unit, label, basis, key, fmt)
INPUTS = [
    ('A', 'Baseline (consolidated Kishlay Group: Kishlay Foods Pvt Ltd + Tulsi Speciality Foods)'),
    ('Rev_FY24', 'FY24 revenue, consolidated', 344.0, 344.0, 344.0, '₹ Cr', 'External', 'Motilal Oswal Snacks thematic (Jan 2026) ₹343.4 Cr; Dealroom ₹344.0 Cr [S07, S08]. CRISIL publishes FY23 ₹335.59 Cr as the last consolidated actual and only ₹213 Cr for Apr–Dec 2023 [S02].', True, CR),
    ('Rev_FY25', 'FY25 revenue, actual (Kishlay Foods Pvt Ltd)', 288.0, 288.0, 288.0, '₹ Cr', 'External', 'Tracxn company profile from the MCA filing: ₹288 Cr for the year to 31 Mar 2025, down 16% YoY; net loss ₹6.31 Cr [S52]. Standalone KFPL; group consolidated not public — FY19–FY23 standalone was within ~2% of CRISIL consolidated [S02, S07]. Tulsi Pvt Ltd had no FY25 revenue [S05].', True, CR),
    ('g_FY26', 'Revenue growth FY26 (after FY25’s −16%)', 0.0, 0.08, 0.15, '%', 'Hypothesis', 'FY26 not public. Tulsi headcount 512 in Feb 2026, +15% YoY, and EPFO payments up from ₹12.9 L (May 2025) to ₹14.3 L (Feb 2026) point to recovery [S53]. Bear: flat. Replace with FY26 provisional sales in week 1.', True, PCT),
    ('Share_copack', 'FY26 share of revenue: co-packing (Frito-Lay, Britannia)', 0.06, 0.06, 0.06, '%', 'Hypothesis', 'Co-packing for Frito-Lay and Britannia reported in dossier [S10]; share not disclosed. Replace with MIS.', True, PCT),
    ('Share_export', 'FY26 share of revenue: exports (Bhutan)', 0.01, 0.01, 0.01, '%', 'Hypothesis', 'Exports to Bhutan only, run by an in-house export analyst [S10]; value not disclosed.', False, PCT),
    ('Share_MT', 'FY26 share of revenue: modern trade + e-commerce', 0.02, 0.02, 0.02, '%', 'Hypothesis', 'Take-home packs listed on BigBasket [S10]; Non Stop not found in indexed Blinkit/Zepto listings (Nov 2026). Share not disclosed.', False, PCT),
    ('B', 'Engine 0: general trade core'),
    ('GT_CAGR', 'General-trade revenue growth FY27–FY29 (a year)', 0.025, 0.045, 0.06, '%', 'Hypothesis', 'Category growth 8–12% a year (Ken Research 9.2%, Technavio 10.2%) [S47]; listed peers FY26: Gopal +2.7%, Prataap +1.0%, Bikaji +14.2%, Annapurna +27% [S12–S17]. Base sits below category because tail SKUs are pruned.', True, PCT),
    ('C', 'Engine 1: quick commerce + modern-trade multipacks'),
    ('QC_stores', 'Dark stores listing Kishlay by FY29 (East + NE cities, all platforms)', 500, 1000, 1500, 'stores', 'Hypothesis', 'Blinkit 2,751 dark stores nationally (30 Sep 2026), Instamart 1,240, Flipkart Minutes ~1,200 [S21]; Blinkit in Guwahati since Jan 2025 (Zoo Road, Chandmari) [S20].', True, INT),
    ('QC_SKUs', 'Hero SKUs + multipacks per dark store', 6, 6, 6, 'SKUs', 'Hypothesis', '6 SKUs: 400 g bhujia, 200 g namkeen, party multipack of ₹10 packs, cookies, soya chunks, noodles multipack.', False, INT),
    ('QC_units', 'Units per SKU per store per day', 0.8, 1.0, 1.3, 'units', 'Hypothesis', 'Regional brand velocity, to be measured in the 8-week Guwahati pilot (KPI gate ≥1.0).', True, CR2),
    ('QC_net', 'Kishlay realisation per QC unit', 62, 62, 62, '₹/unit', 'Calculation', '≈ ₹85 average MRP less 5% GST and ~22% platform margin (see Unit_Econ column D).', False, RS),
    ('MT_stores', 'Modern-trade doors by FY29 (East + NE)', 250, 400, 600, 'stores', 'Hypothesis', 'National and regional supermarket chains; validate door list in the 10-store pilot.', False, INT),
    ('MT_sales', 'Sales per modern-trade door per month (Kishlay realisation)', 25000, 33000, 40000, '₹', 'Hypothesis', 'Pilot KPI: sales per store per week.', False, INT),
    ('Ecom_FY29', 'E-commerce (BigBasket, Amazon, Flipkart) FY29', 2, 3, 5, '₹ Cr', 'Hypothesis', 'Existing BigBasket listings [S10].', False, CR),
    ('QC_r27', 'Ramp: share of FY29 run-rate reached in FY27', 0.25, 0.25, 0.25, '%', 'Hypothesis', 'Pilot in Q1 of FY27 plan, city roll-out after.', False, PCT),
    ('QC_r28', 'Ramp: share of FY29 run-rate reached in FY28', 0.6, 0.6, 0.6, '%', 'Hypothesis', '', False, PCT),
    ('D', 'Engine 2: exports (Bhutan today; Nepal and GCC new)'),
    ('Bhutan_g', 'Bhutan export growth a year', 0.05, 0.10, 0.15, '%', 'Hypothesis', 'India–Bhutan free-trade regime, INR-pegged ngultrum [S50].', False, PCT),
    ('Nepal_trucks', 'Nepal: trucks a month (Panitanki–Kakarbhitta, then local 3P)', 4, 8, 12, 'trucks', 'Hypothesis', 'India exports to Nepal: chapter-19 cereal/bakery preparations ~$97.4M (2024), sweet biscuits ~$4.9M FY25 [S31]. Haldiram’s and Bikaji now make in Nepal [S25, S26].', True, INT),
    ('Nepal_value', 'Nepal: value per truck at Kishlay price', 12.5, 12.5, 12.5, '₹ lakh', 'Hypothesis', 'Light, bulky cargo; validate with transporter and distributor.', False, CR),
    ('GCC_cont', 'GCC: 40 ft containers a month by FY29', 2, 6, 9, 'containers', 'Hypothesis', 'PRAN (Bangladesh) exported $245M to the UAE in FY24 via one importer, Emerging World Group [S34]. Hormuz disruption since Feb 2026: route via Fujairah, Khor Fakkan, Sohar or Jeddah [S42].', True, INT),
    ('GCC_value', 'GCC: value per container at FOB', 25, 25, 25, '₹ lakh', 'Hypothesis', 'Export realisation ~2x India per pack (Export_Calc).', False, CR),
    ('Nepal_r27', 'Nepal ramp FY27', 0.3, 0.3, 0.3, '%', 'Hypothesis', '', False, PCT),
    ('Nepal_r28', 'Nepal ramp FY28', 0.6, 0.6, 0.6, '%', 'Hypothesis', '', False, PCT),
    ('GCC_r27', 'GCC ramp FY27', 0.0, 0.0, 0.1, '%', 'Hypothesis', 'Registration (Dubai Municipality FIRS) and shipping-risk gate first [S40, S42].', False, PCT),
    ('GCC_r28', 'GCC ramp FY28', 0.4, 0.4, 0.5, '%', 'Hypothesis', '', False, PCT),
    ('E', 'Engine 3: asset-light 3P and co-packing'),
    ('Copack_incr', 'Additional co-pack / 3P revenue by FY29', 8, 17, 25, '₹ Cr', 'Hypothesis', 'Spare lines (est. 50–75% utilisation) sold to brand owners; existing clients Frito-Lay, Britannia [S10]. Bikaji runs 4 exclusive + 1 non-exclusive contract units [S45].', False, CR),
    ('F', 'Engine 4: bolt-on M&A'),
    ('MA_rev', 'Bolt-on regional brand revenue (acquired in FY28)', 0, 30, 45, '₹ Cr', 'Hypothesis', 'Screen: ₹20–80 Cr regional brands in Bengal, Bihar, Odisha, NE (Partners_MA).', True, CR),
    ('MA_months', 'Months consolidated in FY28', 6, 6, 6, 'months', 'Hypothesis', '', False, INT),
    ('MA_g', 'Bolt-on growth in FY29', 0.10, 0.10, 0.10, '%', 'Hypothesis', '', False, PCT),
    ('MA_EVS', 'Bolt-on price, EV / sales', 1.0, 1.2, 1.5, 'x', 'Hypothesis', 'Britannia–Kishlay talks ₹600–700 Cr ≈ 1.7–2.0x FY24 revenue [S44]; small bolt-ons usually lower.', False, MULT),
    ('G', 'Targets from the problem statement'),
    ('Target_Rev', 'Revenue target FY29', 512, 512, 512, '₹ Cr', 'Company target (user)', 'Problem statement. No public source for ₹512 Cr; horizon FY29 is our assumption.', True, CR),
    ('Target_EBITDA', 'EBITDA margin target FY29', 0.10, 0.10, 0.10, '%', 'Company target (user)', 'Benchmarks: Bikaji 13.7% FY26, Annapurna ~11.6% FY26, Gopal 6.7% FY26 [S12–S17].', True, PCT),
    ('H', 'EBITDA bridge (basis points of revenue at FY29 run-rate)'),
    ('EBITDA_base', 'Starting EBITDA margin (FY26E)', 0.05, 0.06, 0.07, '%', 'Calculation', 'Not disclosed. CRISIL FY23 interest cover 6.40x and expected cash accrual ₹15–18 Cr a year [S02] imply mid-single digits; Gopal FY26 6.7% [S13].', True, PCT),
    ('L_mix', 'Lever: channel and pack mix (QC, MT, export, take-home)', 100, 140, 170, 'bps', 'Hypothesis', 'Contribution per kg 1.5–2.9x GT ₹10 pack (Unit_Econ).', False, BPS),
    ('L_sku', 'Lever: SKU rationalisation (cut bottom ~20% tail)', 40, 70, 90, 'bps', 'Hypothesis', '236 listed, 292+ claimed, 900+ with sizes [S09, S10]; fewer changeovers and expiries.', False, BPS),
    ('L_proc', 'Lever: procurement (palm oil, potato, laminates)', 30, 60, 80, 'bps', 'Hypothesis', 'Raw materials 70–75% of operating cost [S02]; forward contracts, re-tender packaging.', False, BPS),
    ('L_util', 'Lever: capacity utilisation and co-pack absorption', 60, 100, 130, 'bps', 'Hypothesis', 'Est. 50–75% utilisation of 2,600 MT/month installed (Rev ÷ ₹150–220/kg) [S09].', False, BPS),
    ('L_trade', 'Lever: trade-spend ROI (scheme discipline by beat)', 40, 60, 80, 'bps', 'Hypothesis', 'Super-stockist 3–5%, distributor 8–15% in snacks [S48].', False, BPS),
    ('L_freight', 'Lever: freight ₹/kg via 3P closer to demand', 20, 40, 60, 'bps', 'Hypothesis', 'Hajipur and Chhattisgarh 3P at 300 MT/month each [S09].', False, BPS),
    ('L_qcfees', 'Offset: QC platform fees and digital ads', -70, -50, -40, 'bps', 'Hypothesis', 'Blinkit 2–18% variable commission; Zepto 22–23%; Instamart 20–22%; take rates 14–18% FY25 [S19].', False, BPS),
    ('L_invest', 'Offset: people, MIS and brand investment', -40, -30, -20, 'bps', 'Hypothesis', 'Founder’s Office, data, field force analytics.', False, BPS),
    ('L_ma', 'Lever: bolt-on margin mix', 0, 10, 15, 'bps', 'Hypothesis', 'Acquire only EBITDA-positive targets (≥10%).', False, BPS),
    ('R27', 'Lever ramp FY27 (share of FY29 effect)', 0.3, 0.3, 0.3, '%', 'Hypothesis', '', False, PCT),
    ('R28', 'Lever ramp FY28', 0.65, 0.65, 0.65, '%', 'Hypothesis', '', False, PCT),
    ('R29', 'Lever ramp FY29', 1.0, 1.0, 1.0, '%', 'Hypothesis', '', False, PCT),
    ('I', 'Prices, taxes, FX and channel margins'),
    ('FX_USD', 'Rupees per US dollar (13 Nov 2026)', 94.24, 94.24, 94.24, '₹', 'External', 'Closing rate 13 Nov 2026 [S43].', False, CR2),
    ('AED_peg', 'Dirhams per US dollar (peg)', 3.6725, 3.6725, 3.6725, 'AED', 'External', 'UAE dirham peg.', False, '0.0000'),
    ('NPR_per_INR', 'Nepali rupees per Indian rupee (peg)', 1.6, 1.6, 1.6, 'NPR', 'External', 'NPR–INR peg.', False, CR2),
    ('GST', 'India GST on namkeen, biscuits, noodles', 0.05, 0.05, 0.05, '%', 'External', 'GST 2.0 from 22 Sep 2025 (namkeen 12%→5%, biscuits 18%→5%) [S23].', False, PCT),
    ('Ret_GT', 'Retailer margin, general trade (% of MRP)', 0.16, 0.16, 0.16, '%', 'Hypothesis', 'Industry-typical; validate with scheme sheets [S48].', False, PCT),
    ('Trade_GT', 'Super-stockist + distributor margin (% of MRP)', 0.07, 0.07, 0.07, '%', 'Hypothesis', 'SS 3–5% [S48]; distributor share of MRP lower than % of distributor price.', False, PCT),
    ('Ret_MT', 'Retailer margin, modern trade (% of MRP)', 0.20, 0.20, 0.20, '%', 'Hypothesis', '', False, PCT),
    ('Plat_QC', 'Quick-commerce platform margin (% of MRP)', 0.22, 0.22, 0.22, '%', 'Hypothesis', 'Zepto 22–23%, Instamart 20–22% [S19].', False, PCT),
    ('UAE_VAT', 'UAE VAT', 0.05, 0.05, 0.05, '%', 'External', 'UAE VAT 5%.', False, PCT),
    ('UAE_duty', 'UAE import duty on Indian snacks (CEPA)', 0.05, 0.0, 0.0, '%', 'Hypothesis', 'CEPA: ~80–90% of Indian exports duty-free [S41]; verify HS line. Bear assumes 5% GCC common tariff.', True, PCT),
    ('UAE_ret', 'UAE retailer margin (% of shelf)', 0.25, 0.25, 0.25, '%', 'Hypothesis', 'Validate with Lulu / Al Adil buyers.', False, PCT),
    ('UAE_imp', 'UAE importer / distributor margin (% of shelf)', 0.15, 0.15, 0.15, '%', 'Hypothesis', '', False, PCT),
    ('UAE_frt', 'Export freight, insurance, clearing to UAE (% of FOB)', 0.15, 0.12, 0.10, '%', 'Hypothesis', 'Higher while Hormuz is disrupted [S42].', False, PCT),
    ('NP_VAT', 'Nepal VAT', 0.13, 0.13, 0.13, '%', 'External', 'Nepal VAT 13% [S24].', False, PCT),
    ('NP_duty', 'Nepal customs duty on snacks from India', 0.30, 0.30, 0.20, '%', 'Hypothesis', '30% quoted for biscuits HS 1905 31 (secondary source) [S24]; namkeen HS to confirm with a Nepal customs broker.', True, PCT),
    ('NP_ret', 'Nepal retailer margin (% of shelf)', 0.15, 0.15, 0.15, '%', 'Hypothesis', '', False, PCT),
    ('NP_dist', 'Nepal distributor margin (% of shelf)', 0.10, 0.10, 0.10, '%', 'Hypothesis', '', False, PCT),
    ('NP_frt', 'Freight and clearing to Nepal border (% of value)', 0.05, 0.05, 0.05, '%', 'Hypothesis', 'Guwahati → Siliguri → Panitanki–Kakarbhitta.', False, PCT),
]
r = 6
INPUT_ROW = {}
for item in INPUTS:
    if len(item) == 2:
        c = inp.cell(row=r, column=1, value=item[0])
        c.font = BOLD
        inp.cell(row=r, column=2, value=item[1]).font = BOLD
        for col in range(1, 10):
            inp.cell(row=r, column=col).fill = GREY
        r += 1
        continue
    nid, par, bear, base, bull, unit, lab, basis, key, fmt = item
    put(inp, f'A{r}', nid)
    put(inp, f'B{r}', par, wrap=True)
    for col, v in zip('CDE', (bear, base, bull)):
        put(inp, f'{col}{r}', v, BLUE, fmt, YEL if key else None)
    put(inp, f'F{r}', f'=CHOOSE(Scenario,C{r},D{r},E{r})', BLK, fmt)
    put(inp, f'G{r}', unit)
    put(inp, f'H{r}', lab)
    put(inp, f'I{r}', basis, wrap=True)
    name(nid, f'Inputs!$F${r}')
    INPUT_ROW[nid] = r
    r += 1
# derived FX
put(inp, f'A{r}', 'FX_AED')
put(inp, f'B{r}', 'Rupees per dirham (calculated)')
put(inp, f'F{r}', '=FX_USD/AED_peg', BLK, CR2)
put(inp, f'G{r}', '₹')
put(inp, f'H{r}', 'Calculation')
put(inp, f'I{r}', 'Rupees per dollar ÷ dirham peg')
name('FX_AED', f'Inputs!$F${r}')
inp.freeze_panes = 'C6'

# ---------------------------------------------------------------- Historicals
hi = sheet('Historicals', 'Historical financials and credit profile',
           'Consolidated Kishlay Group (KFPL + Tulsi Speciality Foods) per CRISIL; revenue series per Motilal Oswal. ₹ Cr unless stated.',
           [44, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 60])
years = ['FY15', 'FY16', 'FY17', 'FY18', 'FY19', 'FY20', 'FY21', 'FY22', 'FY23', 'FY24']
header(hi, 4, ['Metric (₹ Cr)'] + years + ['Source'])
mosl = [14.1, 15.0, 15.2, 25.8, 173.1, 238.1, 294.1, 319.4, 335.3, 343.4]
crisil_rev = [None, None, None, None, 174.33, 238.79, 299.35, 319.49, 335.59, None]
pat = [None, None, None, -0.09, -7.15, -8.18, 0.82, -20.69, -11.50, None]
gearing = [None, None, None, 0.19, 0.35, 0.30, 0.32, 0.39, 0.58, None]
icr = [None, None, None, None, 7.37, 9.06, 15.00, 2.89, 6.40, None]
fcf = [None, None, None, -0.7, -97.2, 4.4, -3.8, 0.6, -12.1, -4.6]
rows = [
    ('Revenue (Motilal Oswal series)', mosl, CR, 'Motilal Oswal Snacks thematic, Jan 2026 (₹ mn ÷ 10), via dossier [S07, S10]'),
    ('Operating income (CRISIL, consolidated)', crisil_rev, CR2, 'CRISIL rationales May 2021 (FY19–20), Feb 2024 (FY22–23) [S01, S02]; FY21 per dossier citing CRISIL Aug 2022 [S10]'),
    ('Reported profit after tax (CRISIL)', pat, CR2, 'Same as above; FY18 per dossier [S10]'),
    ('Adjusted debt / adjusted net worth (x)', gearing, MULT, 'CRISIL [S01, S02]; FY18, FY21 per dossier [S10]'),
    ('Interest coverage (x)', icr, MULT, 'CRISIL [S01, S02]; FY21 per dossier [S10]'),
    ('Free cash flow (Motilal Oswal)', fcf, CR, 'Motilal Oswal via dossier [S07, S10]'),
]
rr = 5
for lab, vals, fmt, src in rows:
    put(hi, f'A{rr}', lab)
    for j, v in enumerate(vals):
        col = get_column_letter(2 + j)
        put(hi, f'{col}{rr}', v, BLUE, fmt)
    put(hi, f'L{rr}', src, wrap=True)
    rr += 1
# formulas
put(hi, f'A{rr}', 'Revenue growth (MOSL series)', bold=True)
for j in range(1, 10):
    col = get_column_letter(2 + j)
    prev = get_column_letter(1 + j)
    put(hi, f'{col}{rr}', f'=IFERROR({col}5/{prev}5-1,"")', BLK, PCT)
put(hi, f'L{rr}', 'Calculation')
rr += 1
put(hi, f'A{rr}', 'PAT margin (on CRISIL operating income)', bold=True)
for j in range(10):
    col = get_column_letter(2 + j)
    put(hi, f'{col}{rr}', f'=IF(AND(ISNUMBER({col}7),ISNUMBER({col}6)),{col}7/{col}6,"")', BLK, PCT)
put(hi, f'L{rr}', 'Calculation; CRISIL prints FY22 −6.48%, FY23 −3.43%')
rr += 1
put(hi, f'A{rr}', 'Revenue FY15 → FY24 multiple', bold=True)
put(hi, f'K{rr}', '=K5/B5', BLK, MULT)
put(hi, f'L{rr}', 'Calculation (≈24x)')
rr += 2
put(hi, f'A{rr}', 'Other CRISIL data points', bold=True)
rr += 1
header(hi, rr, ['Item', 'Value', '', '', '', '', '', '', '', '', '', 'Source'])
rr += 1
for lab, val, fmt, src in [
    ('Revenue Apr–Dec 2023 (9 months, FY24)', 213, CR, 'CRISIL Feb 2024 [S02]'),
    ('Implied Jan–Mar 2024 if FY24 = MOSL figure', '=K5-B{r}', CR, 'Calculation: flags a validation question (vs ₹71 Cr a quarter Apr–Dec)'),
    ('Management guidance, medium-term turnover (low)', 350, CR, 'CRISIL Feb 2024 [S02]'),
    ('Management guidance, medium-term turnover (high)', 400, CR, 'CRISIL Feb 2024 [S02]'),
    ('Raw materials share of operating cost (low)', 0.70, PCT, 'CRISIL Feb 2024 [S02]'),
    ('Raw materials share of operating cost (high)', 0.75, PCT, 'CRISIL Feb 2024 [S02]'),
    ('Bank-limit utilisation, 12 months to Dec 2023', 0.93, PCT, 'CRISIL Feb 2024, liquidity "Stretched" [S02]'),
    ('Bank-limit utilisation, 12 months to Apr 2021', 0.79, PCT, 'CRISIL May 2021 [S01]'),
    ('Expected net cash accrual a year (low)', 15, CR, 'CRISIL Feb 2024 [S02]'),
    ('Expected net cash accrual a year (high)', 18, CR, 'CRISIL Feb 2024 [S02]'),
    ('Term-debt repayment a year (low)', 3, CR, 'CRISIL Feb 2024 [S02]'),
    ('Term-debt repayment a year (high)', 6, CR, 'CRISIL Feb 2024 [S02]'),
    ('Net worth projected 31 Mar 2024', 56, CR, 'CRISIL Feb 2024 [S02]'),
    ('KFPL rated bank facilities (HDFC Bank)', 21.5, CR2, 'CC 9.75 + TL 2.93 + TL 5.25 + WCTL 3.19 + proposed 0.38 [S04]'),
    ('Tulsi Speciality Foods (firm) rated facilities', 28.53, CR2, 'CC 9.00 + WCTL 7.53 + proposed 12.00 (CRISIL 2 Feb 2024) [S03]'),
]:
    put(hi, f'A{rr}', lab, wrap=True)
    v = val.replace('{r}', str(rr - 1)) if isinstance(val, str) else val
    put(hi, f'B{rr}', v, BLUE if not isinstance(val, str) else BLK, fmt)
    put(hi, f'L{rr}', src, wrap=True)
    rr += 1
rr += 1
put(hi, f'A{rr}', 'CRISIL rating history (Kishlay Foods Pvt Ltd)', bold=True)
rr += 1
header(hi, rr, ['Date', 'Rating', '', '', '', '', '', '', '', '', '', 'Note'])
rr += 1
for d, rt, note in [
    ('Feb 2020', 'CRISIL BB+/Stable', 'Initial rating [S10]'),
    ('26 May 2021', 'CRISIL BBB-/Stable', 'Upgrade; investment grade [S01]'),
    ('10 Aug 2022', 'CRISIL BBB-/Negative', 'Input-cost pressure [S04 history]'),
    ('8 Nov 2023', 'CRISIL BB+/Stable (Issuer Not Cooperating)', 'Information not provided [S02]'),
    ('1 Feb 2024', 'CRISIL BB+/Stable', 'Management resumed sharing data [S02]'),
    ('30 Apr 2025', 'CRISIL BB+/Stable (Issuer Not Cooperating)', '[S04 history]'),
    ('24 Jun 2026', 'Crisil B/Stable (Issuer Not Cooperating)', 'No financial or strategic information received; monthly NDS not provided [S04]'),
]:
    put(hi, f'A{rr}', d)
    put(hi, f'B{rr}', rt)
    hi.merge_cells(f'B{rr}:K{rr}')
    put(hi, f'L{rr}', note, wrap=True)
    rr += 1
rr += 1
put(hi, f'A{rr}', 'Tulsi Speciality Foods Pvt Ltd: first filing, standalone, 7 Oct 2024 – 31 Mar 2025 (₹ Cr)', bold=True)
rr += 1
header(hi, rr, ['Line item', 'FY25', '', '', '', '', '', '', '', '', '', 'Source'])
rr += 1
t0 = rr
tulsi = [
    ('Share capital (total equity)', 5.00), ('Other current liabilities', 0.2513713),
    ('Other non-current assets', 0.1777883), ('Other current assets', 5.0684843), ('Cash and cash equivalents (₹50,987)', 0.0050987),
    ('Cash from operating activities', -4.8171130), ('Cash from investing activities', -0.1777883), ('Cash from financing activities', 5.00),
    ('Revenue, inventory, receivables, fixed assets, debt', 0),
]
for lab, v in tulsi:
    put(hi, f'A{rr}', lab)
    put(hi, f'B{rr}', v, BLUE, '#,##0.0000;(#,##0.0000);"-"')
    put(hi, f'L{rr}', 'Tracxn summary of MCA filing (export 17 Nov 2026), user-provided [S05]')
    rr += 1
put(hi, f'A{rr}', 'Check: assets − (equity + liabilities)', bold=True)
put(hi, f'B{rr}', f'=ROUND(B{t0+2}+B{t0+3}+B{t0+4}-B{t0}-B{t0+1},4)', BLK, '#,##0.000;(#,##0.000);"OK"')
put(hi, f'L{rr}', 'Should read OK (0)')
rr += 1
put(hi, f'A{rr}', 'Check: cash flows − closing cash', bold=True)
put(hi, f'B{rr}', f'=ROUND(B{t0+5}+B{t0+6}+B{t0+7}-B{t0+4},4)', BLK, '#,##0.000;(#,##0.000);"OK"')
put(hi, f'L{rr}', 'Should read OK (0). Reading: in FY25 the new company was capitalised but not yet operating; the business ran in the partnership firm and KFPL.')
HI_TCHECK = rr
rr += 2
put(hi, f'A{rr}', 'Tulsi Speciality Foods Pvt Ltd: borrowings and auditor', bold=True)
rr += 1
header(hi, rr, ['Item', 'Value', '', '', '', '', '', '', '', '', '', 'Source'])
rr += 1
put(hi, f'A{rr}', 'Open charges as a borrower (₹ Cr), as on 14 Apr 2026')
HI_TCHG = rr
put(hi, f'B{rr}', 24.5, BLUE, CR2)
put(hi, f'L{rr}', 'Tracxn company page (user screenshot, 17 Nov 2026) [S05]; dossier cites ₹26.03 Cr across five HDFC Bank charges created 2025–2026 [S10]', wrap=True)
rr += 1
put(hi, f'A{rr}', 'Closed charges as a borrower')
put(hi, f'B{rr}', 'None', BLUE)
put(hi, f'L{rr}', 'Tracxn (as on 14 Apr 2026) [S05]')
rr += 1
put(hi, f'A{rr}', 'Statutory auditor')
put(hi, f'B{rr}', 'MSKA & Associates LLP', BLUE)
hi.merge_cells(f'B{rr}:K{rr}')
put(hi, f'L{rr}', 'Tracxn [S05]; MSKA is the BDO International network firm in India (NFRA inspection report) [S51]', wrap=True)
rr += 1
put(hi, f'A{rr}', 'Reading', bold=True)
put(hi, f'B{rr}', 'FY25 filing: capitalised with ₹5 Cr, no operations. By Apr 2026: ₹24.5 Cr of secured borrowings — consistent with the operating business and assets moving into the new company during FY26.', wrap=True)
hi.merge_cells(f'B{rr}:L{rr}')
hi.row_dimensions[rr].height = 34
rr += 2
put(hi, f'A{rr}', 'Kishlay Foods Pvt Ltd (brand owner): FY25 and company data (Tracxn)', bold=True)
rr += 1
header(hi, rr, ['Item', 'Value', '', '', '', '', '', '', '', '', '', 'Source'])
KF = {}
kf_rows = [
    ('rev', 'Revenue FY25, standalone (₹ Cr)', '=Rev_FY25', CR, 'Tracxn profile from MCA filing, year to 31 Mar 2025 [S52]'),
    ('yoy', 'Change vs FY24 (₹343.4 Cr, Motilal Oswal)', None, PCT, 'Calculation; Tracxn shows −16% YoY [S52]'),
    ('pat', 'Net profit FY25 (₹ Cr)', -6.31, CR2, 'Tracxn [S52]'),
    ('npm', 'Net margin FY25', None, PCT, 'Calculation'),
    ('emp', 'Employees, Kishlay Foods Pvt Ltd (legal entity)', 85, INT, 'Tracxn [S52]'),
    ('empb', 'Employees, Kishlay Foods brand profile (31 Oct 2026; trend down)', 94, INT, 'Tracxn [S52]'),
    ('chg', 'Open charges as a borrower, KFPL (₹ Cr), as on 27 May 2026', 45.9, CR2, 'Tracxn cross-directorship table [S53]'),
    ('grp', 'Secured charges, KFPL + Tulsi Pvt Ltd (₹ Cr)', None, CR2, 'Calculation: ₹45.9 Cr + ₹24.5 Cr'),
    ('rated', 'CRISIL-rated bank facilities, Feb 2024: KFPL ₹21.5 Cr + Tulsi firm ₹28.53 Cr', '=B30+B31', CR2, 'CRISIL [S02, S03]'),
    ('inc', 'Increase in secured charges vs 2024 rated facilities (₹ Cr)', None, CR2, 'Calculation (charges are sanctioned security, not drawn debt)'),
    ('eq', 'Total equity funding, 3 rounds (US$ M)', 15.9, CR2, 'Tracxn [S52]'),
    ('sa', 'Series A, 24 Jul 2018 (US$ M) — Norwest Venture Partners, Intensive Softshare', 15.0, CR2, 'Tracxn [S52]; lead investors per dossier [S10]'),
    ('pm', 'Post-money valuation, Jul 2018 (US$ M)', 32.4, CR2, 'Tracxn [S52]'),
    ('eve', 'Listed-peer median EV/EBITDA (x)', 9.15, MULT, 'Tracxn, latest available data [S52]'),
    ('evr', 'Listed-peer median EV/Revenue (x)', 1.02, MULT, 'Tracxn, latest available data [S52]'),
]
for key, lab, v, fmt, src in kf_rows:
    rr += 1
    KF[key] = rr
    put(hi, f'A{rr}', lab)
    if v is not None:
        put(hi, f'B{rr}', v, GRN if str(v).startswith('=') else BLUE, fmt)
    put(hi, f'L{rr}', src, wrap=True)
put(hi, f'B{KF["yoy"]}', f'=B{KF["rev"]}/K5-1', BLK, PCT)
put(hi, f'B{KF["npm"]}', f'=B{KF["pat"]}/B{KF["rev"]}', BLK, PCT)
put(hi, f'B{KF["grp"]}', f'=B{KF["chg"]}+B{HI_TCHG}', BLK, CR2)
put(hi, f'B{KF["inc"]}', f'=B{KF["grp"]}-B{KF["rated"]}', BLK, CR2)
rr += 1
put(hi, f'A{rr}', 'Rank among tracked competitors')
put(hi, f'B{rr}', '12th of 521', BLUE)
put(hi, f'L{rr}', 'Tracxn [S52]')
rr += 1
put(hi, f'A{rr}', 'Other promoter entity')
put(hi, f'B{rr}', 'Shresth Investtech LLP (2023): no revenue in FY25', BLUE)
hi.merge_cells(f'B{rr}:K{rr}')
put(hi, f'L{rr}', 'Tracxn [S52]')
HI_EVE, HI_EVR = KF['eve'], KF['evr']

rr += 2
put(hi, f'A{rr}', 'Tulsi Speciality Foods Pvt Ltd: entity, people and compliance (Tracxn)', bold=True)
rr += 1
header(hi, rr, ['Item', 'Value', '', '', '', '', '', '', '', '', '', 'Source'])
tul = [
    ('Corporate identity number', 'U10790AS2024PTC027099'),
    ('Incorporated', '7 Oct 2024, RoC Guwahati; private company limited by shares'),
    ('Paid-up and authorised capital', '₹5 Cr each (14 Apr 2026)'),
    ('Owner', '99% subsidiary of Kishlay Foods Pvt Ltd (Tracxn corporate structure)'),
    ('Directors', 'Sandeep Bajaj (also Managing Director of KFPL) and Vishesh Bajaj, both from 7 Oct 2024'),
    ('Plant and registered office', 'Plot 106, Brahmaputra Industrial Park, Amingaon, Kamrup, Assam 781031'),
    ('EPFO establishment', 'Set up 6 Oct 2017 as a partnership firm, activity “confectionery”: the Tulsi firm’s workforce now files under the company'),
    ('GST filing delays, FY2025-26', '5 (Tracxn risk indicator)'),
    ('Statutory auditor FY25', 'Bineet Bagaria & Associates, Guwahati (FRN 332337E)'),
    ('Auditor appointed 4 Mar 2026', 'MSKA & Associates LLP, Kolkata (FRN 105047W; BDO International network firm)'),
    ('Last AGM', '31 Dec 2025'),
    ('Corporate tree caveat', 'Tracxn shows KFPL as 100% owned by Kishlay Sweets & Savories Pvt Ltd, which its director table lists as struck off: likely stale, verify on MCA'),
    ('Other promoter companies with charges', 'Sandeep Commercial Pvt Ltd ₹4 Cr (14 Dec 2025); Madhusoodan Milk Products ₹0.25 Cr (12 Dec 2025)'),
]
for lab, v in tul:
    rr += 1
    put(hi, f'A{rr}', lab)
    put(hi, f'B{rr}', v, BLUE, wrap=True)
    hi.merge_cells(f'B{rr}:K{rr}')
    put(hi, f'L{rr}', 'Tracxn [S53]; NFRA [S51]' if 'MSKA' in v else 'Tracxn legal-entity profile [S53]', wrap=True)
rr += 2
put(hi, f'A{rr}', 'Tulsi Speciality Foods Pvt Ltd: monthly headcount and EPFO payments (labour filings)', bold=True)
rr += 1
months = ['May-25', 'Jun-25', 'Jul-25', 'Aug-25', 'Sep-25', 'Oct-25', 'Nov-25', 'Dec-25', 'Jan-26', 'Feb-26']
header(hi, rr, ['Wage month'] + months + ['Source'])
heads = [469, 465, 450, 450, 474, 468, 480, 477, 480, 512]
pays = [12.9, 13.2, 12.9, 13.1, 13.5, 13.4, 13.7, 13.7, 13.4, 14.3]
rr += 1
put(hi, f'A{rr}', 'Employees')
for i, v in enumerate(heads):
    put(hi, f'{get_column_letter(2+i)}{rr}', v, BLUE, INT)
put(hi, f'L{rr}', 'Tracxn [S53]; Feb-26 is +15% YoY')
HI_HEAD = rr
rr += 1
put(hi, f'A{rr}', 'EPFO payment (₹ lakh)')
for i, v in enumerate(pays):
    put(hi, f'{get_column_letter(2+i)}{rr}', v, BLUE, CR2)
put(hi, f'L{rr}', 'Tracxn [S53]')
HI_PAY = rr
rr += 1
put(hi, f'A{rr}', 'Change May-25 → Feb-26: employees · EPFO payment')
put(hi, f'B{rr}', f'=K{HI_HEAD}/B{HI_HEAD}-1', BLK, PCT)
put(hi, f'C{rr}', f'=K{HI_PAY}/B{HI_PAY}-1', BLK, PCT)
put(hi, f'L{rr}', 'Calculation')
hi.freeze_panes = 'B5'

# ---------------------------------------------------------------- Peers
pe = sheet('Peers', 'Peer benchmarks: is ~10% EBITDA realistic?',
           'Listed snack peers, ₹ Cr. Margins are formulas. Kishlay EBITDA is an estimate (not disclosed).',
           [30, 9, 12, 12, 11, 11, 12, 70])
header(pe, 4, ['Company', 'Year', 'Revenue', 'EBITDA', 'EBITDA %', 'Gross margin', 'PAT', 'Source and note'])
peers = [
    ('Bikaji Foods', 'FY25', 2562.0, 268.4, None, None, 150.4, 'Revenue from operations; underlying EBITDA 10.5% (12.5% incl. PLI) — Bikaji investor presentation 15 May 2025 [S14]'),
    ('Bikaji Foods', 'FY26', 2993.9, 410.6, None, 0.351, None, 'FY26: EBITDA ₹410.6 Cr, 13.7%; gross margin 35.1% [S15]'),
    ('Gopal Snacks', 'FY25', 1468.0, 105.2, None, 0.25, 19.0, 'Rajkot fire; exceptional loss ₹47.2 Cr — earnings release May 2025 [S12]'),
    ('Gopal Snacks', 'FY26', 1508.2, 101.3, None, None, 73.65, 'PAT boosted by insurance claims [S13]'),
    ('Prataap Snacks (Yellow Diamond)', 'FY25', 1707.7, 48.7, None, None, -14.0, 'Operating EBITDA ₹48.7 Cr — earnings release [S16]'),
    ('Prataap Snacks (Yellow Diamond)', 'FY26', 1725.0, None, None, None, 97.0, 'FY26 EBITDA not confirmed; Q4 FY26 margin 4.9% [S16]'),
    ('Annapurna Swadisht (Kolkata, ₹5 model)', 'FY24', 265.7, None, None, None, None, 'Aggregator data [S17]'),
    ('Annapurna Swadisht (Kolkata, ₹5 model)', 'FY25', 408.7, 49.7, None, None, 21.5, 'FY25 EBITDA derived by aggregator, not reported [S17]'),
    ('Annapurna Swadisht (Kolkata, ₹5 model)', 'FY26', 520.08, None, 0.1159, None, 30.33, 'Consolidated; PBITDA margin 11.59% per aggregator; verify on NSE filing [S17]'),
    ('Kishlay Group (consolidated)', 'FY23', 335.59, None, None, None, -11.50, 'CRISIL [S02]; EBITDA not disclosed'),
    ('Kishlay Foods Pvt Ltd (standalone)', 'FY25', 288.0, None, None, None, -6.31, 'Tracxn profile from MCA filing: revenue −16% YoY; EBITDA not disclosed [S52]'),
    ('Kishlay Group (consolidated)', 'FY26E', '=Rev_Bridge!D16', '=Rev_Bridge!D16*EBITDA_base', None, None, None, 'Model base case: FY26E revenue × starting margin (estimate)'),
]
pr = 5
for co, yr, rev, eb, ebm, gm, pt, src in peers:
    put(pe, f'A{pr}', co)
    put(pe, f'B{pr}', yr)
    put(pe, f'C{pr}', rev, BLUE if not isinstance(rev, str) else GRN, CR)
    put(pe, f'D{pr}', eb, BLUE if not isinstance(eb, str) else GRN, CR)
    if ebm is not None:
        put(pe, f'E{pr}', ebm, BLUE, PCT)
    else:
        put(pe, f'E{pr}', f'=IF(AND(ISNUMBER(C{pr}),ISNUMBER(D{pr})),D{pr}/C{pr},"")', BLK, PCT)
    put(pe, f'F{pr}', gm, BLUE, PCT)
    put(pe, f'G{pr}', pt, BLUE, CR)
    put(pe, f'H{pr}', src, wrap=True)
    pr += 1
put(pe, f'A{pr+1}', 'Reading', bold=True)
put(pe, f'B{pr+1}', '10% EBITDA sits between Gopal (6.7%) and Annapurna (~11.6%), below Bikaji (13.7%). Annapurna — same ₹5 East-India model — grew ₹265.7 Cr → ₹520 Cr in two years.', wrap=True)
pe.merge_cells(f'B{pr+1}:H{pr+1}')
pe.row_dimensions[pr + 1].height = 32

# ---------------------------------------------------------------- Rev_Bridge
rb = sheet('Rev_Bridge', 'Revenue bridge: FY24A → FY29P (₹ Cr)',
           'Engines are built bottom-up from Inputs. FY24A and FY25A are reported; FY26 is an estimate; FY27–29 are plan years.',
           [46, 11, 11, 11, 11, 11, 11, 4, 60])
header(rb, 4, ['Line (₹ Cr)', 'FY24A', 'FY25A', 'FY26E', 'FY27P', 'FY28P', 'FY29P', '', 'How it is built'])
put(rb, 'A5', 'Top-down revenue (consolidated)', bold=True)
put(rb, 'B5', '=Rev_FY24', GRN, CR)
put(rb, 'C5', '=Rev_FY25', GRN, CR)
put(rb, 'D5', '=C5*(1+g_FY26)', BLK, CR)
put(rb, 'I5', 'FY24 and FY25 reported (FY25 −16%); FY26 grown at the assumed rate')
put(rb, 'A7', 'Engines', bold=True)
eng = [
    (8, 'Engine 0 · General trade core', '=D5*(1-Share_copack-Share_export-Share_MT)', '=D8*(1+GT_CAGR)', '=E8*(1+GT_CAGR)', '=F8*(1+GT_CAGR)', 'FY26 residual share × growth'),
    (9, 'Engine 1a · Quick commerce', 0, '=G9*QC_r27', '=G9*QC_r28', '=QC_stores*QC_SKUs*QC_units*QC_net*365/10^7', 'stores × SKUs × units/day × ₹/unit × 365'),
    (10, 'Engine 1b · Modern trade + e-commerce', '=D5*Share_MT', '=D10+(G10-D10)*QC_r27', '=D10+(G10-D10)*QC_r28', '=MT_stores*MT_sales*12/10^7+Ecom_FY29', 'doors × ₹/door/month × 12 + e-commerce'),
    (11, 'Engine 2a · Exports: Bhutan', '=D5*Share_export', '=D11*(1+Bhutan_g)', '=E11*(1+Bhutan_g)', '=F11*(1+Bhutan_g)', 'existing route'),
    (12, 'Engine 2b · Exports: Nepal', 0, '=G12*Nepal_r27', '=G12*Nepal_r28', '=Nepal_trucks*Nepal_value*12/100', 'trucks/month × ₹ lakh × 12'),
    (13, 'Engine 2c · Exports: GCC', 0, '=G13*GCC_r27', '=G13*GCC_r28', '=GCC_cont*GCC_value*12/100', 'containers/month × ₹ lakh × 12'),
    (14, 'Engine 3 · Co-packing and 3P', '=D5*Share_copack', '=D14+Copack_incr/3', '=D14+Copack_incr*2/3', '=D14+Copack_incr', 'existing co-pack + new contracts'),
    (15, 'Engine 4 · Bolt-on M&A', 0, 0, '=MA_rev*MA_months/12', '=MA_rev*(1+MA_g)', 'acquired in FY28, part-year'),
]
for row, lab, d, e, f, g, how in eng:
    put(rb, f'A{row}', lab)
    for col, v in zip('DEFG', (d, e, f, g)):
        put(rb, f'{col}{row}', v, BLUE if isinstance(v, (int, float)) else BLK, CR)
    put(rb, f'I{row}', how)
put(rb, 'A16', 'Total revenue', bold=True)
for col in 'DEFG':
    put(rb, f'{col}16', f'=SUM({col}8:{col}15)', BLK, CR, fill=SAND)
put(rb, 'B16', '=B5', BLK, CR, fill=SAND)
put(rb, 'C16', '=C5', BLK, CR, fill=SAND)
put(rb, 'A17', 'Check: FY26 engines − top-down (should be 0)')
put(rb, 'D17', '=ROUND(D16-D5,6)', BLK, '#,##0.000;(#,##0.000);"OK"')
put(rb, 'A18', 'Organic revenue (excludes M&A)')
for col in 'DEFG':
    put(rb, f'{col}18', f'={col}16-{col}15', BLK, CR)
put(rb, 'A19', 'Target FY29 (problem statement)')
put(rb, 'G19', '=Target_Rev', GRN, CR)
put(rb, 'A20', 'Gap to target (+ above, − below)')
put(rb, 'G20', '=G16-G19', BLK, CR)
put(rb, 'A21', 'Share of target reached')
put(rb, 'G21', '=G16/G19', BLK, PCT)
put(rb, 'A22', 'Growth year on year')
put(rb, 'C22', '=C16/B16-1', BLK, PCT)
for col, prev in zip('DEFG', 'CDEF'):
    put(rb, f'{col}22', f'={col}16/{prev}16-1', BLK, PCT)
put(rb, 'A23', 'CAGR FY26E → FY29P')
put(rb, 'G23', '=(G16/D16)^(1/3)-1', BLK, PCT)
put(rb, 'A24', 'CAGR FY24A → FY29P')
put(rb, 'G24', '=(G16/B16)^(1/5)-1', BLK, PCT)
put(rb, 'A26', 'Where the extra revenue comes from (FY26E → FY29P)', bold=True)
header(rb, 27, ['Engine', 'FY26E', 'FY29P', 'Increase', 'Share of increase', 'FY29 mix', '', '', 'Note'])
labels = ['General trade core', 'Quick commerce', 'Modern trade + e-commerce', 'Exports: Bhutan', 'Exports: Nepal', 'Exports: GCC', 'Co-packing and 3P', 'Bolt-on M&A']
for i, lab in enumerate(labels):
    row = 28 + i
    src = 8 + i
    put(rb, f'A{row}', lab)
    put(rb, f'B{row}', f'=D{src}', BLK, CR)
    put(rb, f'C{row}', f'=G{src}', BLK, CR)
    put(rb, f'D{row}', f'=C{row}-B{row}', BLK, CR)
    put(rb, f'E{row}', f'=IFERROR(D{row}/$D$36,0)', BLK, PCT)
    put(rb, f'F{row}', f'=IFERROR(C{row}/$C$36,0)', BLK, PCT)
put(rb, 'A36', 'Total', bold=True)
for col in 'BCD':
    put(rb, f'{col}36', f'=SUM({col}28:{col}35)', BLK, CR, fill=SAND)
put(rb, 'E36', '=SUM(E28:E35)', BLK, PCT, fill=SAND)
put(rb, 'F36', '=SUM(F28:F35)', BLK, PCT, fill=SAND)
put(rb, 'A38', 'New engines (QC, MT, Nepal, GCC, co-pack increase, M&A) as share of FY29 revenue')
put(rb, 'G38', '=(G9+(G10-D10)+G12+G13+(G14-D14)+G15)/G16', BLK, PCT)
rb.freeze_panes = 'B5'

# ---------------------------------------------------------------- EBITDA_Bridge
eb = sheet('EBITDA_Bridge', 'EBITDA bridge: from a mid-single-digit start to ~10%',
           'Each lever is in basis points of revenue at full run-rate (FY29) and ramps in. All levers are hypotheses to validate.',
           [50, 11, 11, 11, 11, 4, 66])
header(eb, 4, ['Line', 'FY26E', 'FY27P', 'FY28P', 'FY29P', '', 'Basis'])
put(eb, 'A5', 'Revenue (₹ Cr)', bold=True)
for col, src in zip('BCDE', 'DEFG'):
    put(eb, f'{col}5', f'=Rev_Bridge!{src}16', GRN, CR)
put(eb, 'A6', 'Starting EBITDA margin')
for col in 'BCDE':
    put(eb, f'{col}6', '=EBITDA_base', GRN, PCT)
levers = [('L_mix', 'Channel and pack mix'), ('L_sku', 'SKU rationalisation'), ('L_proc', 'Procurement'),
          ('L_util', 'Capacity utilisation and co-pack absorption'), ('L_trade', 'Trade-spend ROI'), ('L_freight', 'Freight via 3P closer to demand'),
          ('L_qcfees', 'Less: QC platform fees and ads'), ('L_invest', 'Less: people, MIS, brand investment'), ('L_ma', 'Bolt-on margin mix')]
for i, (nm, lab) in enumerate(levers):
    row = 8 + i
    put(eb, f'A{row}', lab)
    put(eb, f'B{row}', 0, BLUE, PCT)
    put(eb, f'C{row}', f'={nm}*R27/10000', BLK, '0.00%;(0.00%);"-"')
    put(eb, f'D{row}', f'={nm}*R28/10000', BLK, '0.00%;(0.00%);"-"')
    put(eb, f'E{row}', f'={nm}*R29/10000', BLK, '0.00%;(0.00%);"-"')
    put(eb, f'G{row}', f'=Inputs!I{INPUT_ROW[nm]}', GRN, wrap=True)
put(eb, 'A17', 'EBITDA margin', bold=True)
for col in 'BCDE':
    put(eb, f'{col}17', f'={col}6+SUM({col}8:{col}16)', BLK, PCT, fill=SAND)
put(eb, 'A18', 'EBITDA (₹ Cr)', bold=True)
for col in 'BCDE':
    put(eb, f'{col}18', f'={col}5*{col}17', BLK, CR, fill=SAND)
put(eb, 'A19', 'Target margin FY29')
put(eb, 'E19', '=Target_EBITDA', GRN, PCT)
put(eb, 'A20', 'Gap to target (bps; + above)')
put(eb, 'E20', '=(E17-E19)*10000', BLK, BPS)
put(eb, 'A21', 'Net lever effect FY29 (bps)')
put(eb, 'E21', '=SUM(E8:E16)*10000', BLK, BPS)
put(eb, 'A22', 'EBITDA increase FY26E → FY29P (₹ Cr)')
put(eb, 'E22', '=E18-B18', BLK, CR)
put(eb, 'A24', 'Benchmarks (FY26)', bold=True)
for i, (lab, ref) in enumerate([('Bikaji Foods', 'Peers!E6'), ('Annapurna Swadisht', 'Peers!E13'), ('Gopal Snacks', 'Peers!E8')]):
    put(eb, f'A{25+i}', lab)
    put(eb, f'E{25+i}', f'={ref}', GRN, PCT)

# ---------------------------------------------------------------- Unit_Econ
ue = sheet('Unit_Econ', 'Unit economics: what each channel leaves per pack and per kg',
           'Shelf price to company realisation, then direct costs. Costs per pack are hypotheses (blue) to replace with plant costing in Week 1.',
           [46, 14, 14, 14, 14, 14, 14, 50])
cases = ['GT ₹10 pack', 'MT 400 g bhujia', 'QC 400 g bhujia', 'UAE 200 g namkeen', 'Nepal 200 g (export)', 'Nepal via local 3P (royalty)']
header(ue, 4, ['Line'] + cases + ['Note'])
# rows
spec = [
    (5, 'Pack size (g)', [32, 400, 400, 200, 200, 200], INT, 'Kishlay ₹10 extruded ≈30–35 g; 400 g zipper; 200 g namkeen'),
    (6, 'Shelf price, local currency incl. tax', [10, 110, 110, 3.95, 110, 110], CR2, 'Kishlay MRPs ₹10, ₹110 [S10]; UAE AED 3.95 and Nepal NPR 110 are proposed value positions (Haldiram’s: AED 5.69, NPR 135/180 g)'),
    (7, 'FX: rupees per unit of local currency', [1, 1, 1, '=FX_AED', '=1/NPR_per_INR', '=1/NPR_per_INR'], '0.0000', 'Inputs'),
    (9, 'Indirect tax rate (GST / VAT)', ['=GST', '=GST', '=GST', '=UAE_VAT', '=NP_VAT', '=NP_VAT'], PCT, 'Inputs'),
    (11, 'Retailer margin (% of shelf)', ['=Ret_GT', '=Ret_MT', 0, '=UAE_ret', '=NP_ret', '=NP_ret'], PCT, ''),
    (13, 'Distributor / importer margin (% of shelf)', ['=Trade_GT', '=Trade_GT', 0, '=UAE_imp', '=NP_dist', '=NP_dist'], PCT, ''),
    (15, 'Platform margin (% of shelf)', [0, 0, '=Plat_QC', 0, 0, 0], PCT, ''),
    (17, 'Import duty (on landed value)', [0, 0, 0, '=UAE_duty', '=NP_duty', 0], PCT, ''),
    (18, 'Export freight, insurance, clearing', [0, 0, 0, '=UAE_frt', '=NP_frt', 0], PCT, ''),
    (21, 'Raw material + packaging (₹/pack)', [4.91, 45.0, 45.0, 24.8, 23.8, 0], RS, 'Hypothesis: ~60–68% of India realisation; UAE adds ₹1 for Arabic labels'),
    (22, 'Conversion: labour, power, overheads (₹/pack)', [0.58, 4.5, 4.5, 2.4, 2.4, 0], RS, 'Hypothesis'),
    (23, 'Freight to depot / dark store / port (₹/pack)', [0.36, 2.3, 3.2, 2.0, 1.5, 0], RS, 'Hypothesis'),
    (24, 'Trade schemes / platform ads / export compliance (₹/pack)', [0.29, 3.8, 6.4, 1.0, 0.5, 0], RS, 'Hypothesis'),
    (27, 'Royalty rate on partner net sales (3P model)', [0, 0, 0, 0, 0, 0.05], PCT, 'Hypothesis: brand licence + premix supply, like Haldiram’s (Anandam) and Bikaji (Chaudhary Group JV) in Nepal [S25, S26]'),
]
cols = 'BCDEFG'
for row, lab, vals, fmt, note in spec:
    put(ue, f'A{row}', lab)
    for col, v in zip(cols, vals):
        put(ue, f'{col}{row}', v, BLUE if isinstance(v, (int, float)) else GRN, fmt)
    put(ue, f'H{row}', note, wrap=True)
calc = [
    (8, 'Shelf price in rupees', '={c}6*{c}7', RS),
    (10, 'Indirect tax (₹)', '={c}8-{c}8/(1+{c}9)', RS),
    (12, 'Retailer margin (₹)', '={c}8*{c}11', RS),
    (14, 'Distributor / importer margin (₹)', '={c}8*{c}13', RS),
    (16, 'Platform margin (₹)', '={c}8*{c}15', RS),
    (19, 'Company realisation (₹/pack)', '=({c}8-{c}10-{c}12-{c}14-{c}16)/(1+{c}17)/(1+{c}18)', RS),
    (25, 'Contribution (₹/pack)', '={c}19-{c}21-{c}22-{c}23-{c}24', RS),
    (26, 'Contribution % of realisation', '=IFERROR({c}25/{c}19,0)', PCT),
    (29, 'Contribution per kg (₹)', '={c}25/({c}5/1000)', '₹#,##0;(₹#,##0);"-"'),
    (30, 'Index vs GT ₹10 pack (per kg)', '={c}29/$B$29', MULT),
]
for row, lab, f, fmt in calc:
    put(ue, f'A{row}', lab, bold=row in (19, 25, 29))
    for col in cols:
        put(ue, f'{col}{row}', f.format(c=col), BLK, fmt, fill=SAND if row in (19, 25, 29) else None)
# royalty special-case: contribution for G = royalty × ex-tax partner net (after retail & distributor)
put(ue, 'G19', '=(G8-G10-G12-G14)', BLK, RS, fill=SAND)
put(ue, 'G25', '=G19*G27', BLK, RS, fill=SAND)
put(ue, 'H19', 'For the 3P column, row 19 = partner net sales per pack (ex-tax, after trade); Kishlay earns the royalty in row 25 with no plant, stock or freight.', wrap=True)
put(ue, 'A32', 'Reading', bold=True)
put(ue, 'B32', 'A ₹10 GT pack leaves about ₹1 per pack (~₹34/kg). Take-home 400 g in MT/QC leaves ~1.4–1.6x more per kg; a 200 g pack sold in the UAE ~2.9x. Exporting to Nepal over a ~30% duty leaves less per kg than India GT, which is why the Nepal play should be local 3P/licensing, as Haldiram’s and Bikaji have done.', wrap=True)
ue.merge_cells('B32:H32')
ue.row_dimensions[32].height = 58

# ---------------------------------------------------------------- Export_Calc
ec = sheet('Export_Calc', 'Export landed-cost check: what competitors’ shelf prices imply at the factory gate',
           'Same structure as Unit_Econ. Reference prices are real listings; margins and duties are inputs.',
           [52, 16, 16, 16, 60])
header(ec, 4, ['Line', 'Haldiram’s 200 g, Carrefour UAE', 'Haldiram’s Khatta Meetha 180 g, Nepal', 'India MRP, same pack (200 g)', 'Source'])
rows_ec = [
    (5, 'Shelf price, local currency incl. tax', [5.69, 135, 55], CR2, 'Carrefour UAE listing (indexed, AED 5.69 incl. VAT) [S38]; Vhandar Nepal price list Nov 2026 (NPR 135) [S27]; BigBasket ₹55 for Haldiram’s Aloo Bhujia 200 g (indexed) [S49]'),
    (6, 'FX: rupees per unit', ['=FX_AED', '=1/NPR_per_INR', 1], '0.0000', 'Inputs'),
    (7, 'Shelf price (₹)', ['=B5*B6', '=C5*C6', '=D5*D6'], RS, ''),
    (8, 'Tax rate', ['=UAE_VAT', '=NP_VAT', '=GST'], PCT, ''),
    (9, 'Retailer margin %', ['=UAE_ret', '=NP_ret', '=Ret_GT'], PCT, ''),
    (10, 'Importer / distributor margin %', ['=UAE_imp', '=NP_dist', '=Trade_GT'], PCT, ''),
    (11, 'Import duty %', ['=UAE_duty', '=NP_duty', 0], PCT, ''),
    (12, 'Freight, insurance, clearing %', ['=UAE_frt', '=NP_frt', 0], PCT, ''),
    (13, 'Implied factory-gate (FOB) value per pack (₹)', ['=(B7-(B7-B7/(1+B8))-B7*B9-B7*B10)/(1+B11)/(1+B12)', '=(C7-(C7-C7/(1+C8))-C7*C9-C7*C10)/(1+C11)/(1+C12)', '=(D7-(D7-D7/(1+D8))-D7*D9-D7*D10)/(1+D11)/(1+D12)'], RS, 'Calculation'),
    (14, 'Per 100 g (₹)', ['=B13/2', '=C13/1.8', '=D13/2'], RS, 'Calculation'),
    (15, 'Index vs India realisation per 100 g', ['=B14/$D$14', '=C14/$D$14', '=D14/$D$14'], MULT, 'Calculation'),
]
for row, lab, vals, fmt, src in rows_ec:
    put(ec, f'A{row}', lab, bold=row in (13, 15))
    for col, v in zip('BCD', vals):
        put(ec, f'{col}{row}', v, BLUE if isinstance(v, (int, float)) else (GRN if str(v).startswith('=') and any(k in str(v) for k in ('FX', 'NPR', 'UAE', 'NP_', 'GST', 'Ret_', 'Trade_')) else BLK), fmt)
    put(ec, f'E{row}', src, wrap=True)
put(ec, 'A17', 'Reading', bold=True)
put(ec, 'B17', 'The same 200 g pack that sells for ₹55 in India sells for AED 5.69 (≈₹146) in Dubai. Even after retailer, importer, VAT and freight, the factory-gate value is roughly 1.9x India’s. Nepal’s shelf price is high, but duty and VAT absorb most of the premium.', wrap=True)
ec.merge_cells('B17:E17')
ec.row_dimensions[17].height = 46

# ---------------------------------------------------------------- Export_Buyers
xb = sheet('Export_Buyers', 'Export buyer long-list: real, public companies (to approach — none contacted yet)',
           'Every row has a public source. Contact details are not included: use the company website or the source link. Status column is for your outreach.',
           [4, 10, 14, 34, 18, 46, 10, 34, 54, 16, 26])
header(xb, 4, ['#', 'Country', 'City', 'Company', 'Type', 'Why it matters (fact from source)', 'Priority', 'Fit / conflict', 'Source', 'Outreach status', 'Next step'])
buyers = [
    ('UAE', 'Abu Dhabi', 'Lulu Group International', 'Retail chain + India sourcing', '280+ hypermarkets across the GCC; buys ~₹10,000–11,000 Cr a year from India through 30+ sourcing centres; MoU with NAFED (Gulfood 2025)', 'A', 'Fit: mass South Asian shoppers; sources directly from India', 'Gulf News / Khaleej Times [S35]', 'Not contacted', 'Register as supplier with Lulu India sourcing; send price list + samples'),
    ('UAE', 'Dubai', 'Al Adil Trading', 'Indian grocery chain + importer', '~50 UAE stores (2023), 9,500+ Indian products; also Bahrain, Oman, KSA', 'A', 'Fit: Indian diaspora, regional products', 'Khaleej Times; Arabian Business [S36]', 'Not contacted', 'Buyer meeting; NE regional range (Jolokia, Jhalmuri)'),
    ('UAE', 'Dubai', 'Emerging World Group', 'Importer / distributor', 'Sole Middle East importer for PRAN; PRAN shipped $245M to the UAE in FY24 through it', 'B', 'Conflict: tied to PRAN (direct competitor); use as benchmark', 'The Daily Star [S34]', 'Benchmark only', 'Study model; do not approach while PRAN-exclusive'),
    ('UAE', 'Sharjah', 'Nesto Group', 'Hypermarket chain', '152 stores worldwide; Mark & Save value format (19 GCC stores); targets lower-income shoppers', 'A', 'Fit: value price point for blue-collar South Asians', 'Gulf News [S37]', 'Not contacted', 'Pitch ₹5/₹10-equivalent value packs (AED 1–2)'),
    ('UAE', 'Dubai', 'Carrefour UAE (Majid Al Futtaim)', 'Retail chain', 'Lists Haldiram’s 200 g bhujia at AED 5.69 (indexed listing)', 'B', 'Fit: price benchmark; listing via importer', 'carrefouruae.com [S38]', 'Not contacted', 'Use as price anchor; enter via an importer'),
    ('UAE', 'Online', 'noon.com', 'E-commerce marketplace', 'Lists Bikaji Bombay Mix 200 g', 'B', 'Fit: low-cost test channel after registration', 'noon.com listing [S39]', 'Not contacted', 'Seller account after Dubai Municipality registration'),
    ('UAE', 'Dubai', 'Asian Basket', 'South Asian grocery', 'South Asian store in Oud Metha stocking Haldiram’s and other Indian snack brands', 'C', 'Fit: small; good for first pallets', 'asianbasket.ae [S38b]', 'Not contacted', 'Trial pallet partner'),
    ('Qatar', 'Doha', 'Nesto Qatar', 'Hypermarket chain', 'First Qatar hypermarket (Al Gharrafa); plan for 10 stores by 2026', 'B', 'Fit: Nepali and Indian workers in Qatar', 'Gulf News [S37]', 'Not contacted', 'Follow Nesto UAE listing'),
    ('Nepal', 'Kathmandu', 'Bhat-Bhateni Supermarket & Departmental Store', 'Retail chain', '27 stores across Nepal (company site)', 'A', 'Fit: anchor modern-trade buyer', 'bbsm.com.np [S28]', 'Not contacted', 'Buyer meeting with landed-price sheet'),
    ('Nepal', 'Kathmandu', 'United Distributors Nepal (Vishal Group)', 'FMCG distributor', 'Direct distribution to ~45,000 outlets (2020 figure)', 'A', 'Fit: national reach; check category conflicts', 'Vishal Group press release [S29]', 'Not contacted', 'Distribution proposal for Eastern Nepal first'),
    ('Nepal', 'Kathmandu', 'Nepal Overseas', 'FMCG distributor', 'Rs 1.66 bn FMCG sales in 10.5 months (reported)', 'B', 'Fit: FMCG distribution scale; verify portfolio', 'Clickmandu [S30]', 'Not contacted', 'Intro call'),
    ('Nepal', 'Kathmandu', 'Vhandar', 'Online grocery', 'Delivers across Kathmandu Valley; publishes Haldiram’s Nepal price list (Nov 2026)', 'C', 'Fit: online test; price intelligence', 'vhandar.com [S27]', 'Not contacted', 'List 6 SKUs after importer is set'),
    ('Nepal', 'Kathmandu', 'Anandam Snacks & Beverage International (DV Group)', 'Local manufacturer', 'Imported Haldiram’s for ~20 years; local production since Mar 2025 (Haldiram’s 70%); 80 dealers', 'B', 'Conflict: Haldiram’s partner; shows the local-3P model works', 'Clickmandu [S25]', 'Benchmark only', 'Benchmark for Nepal 3P economics'),
    ('Nepal', 'Kathmandu', 'Chaudhary Group (CG)', 'Conglomerate / manufacturer', '50:50 JV with Bikaji (Jul 2025) to make ethnic snacks in Nepal; owns Wai Wai', 'B', 'Conflict: Bikaji JV + Wai Wai (noodles rival)', 'just-food [S26]', 'Benchmark only', 'Avoid for snacks; note for noodles'),
    ('Nepal', 'Biratnagar / Kathmandu', 'MV Dugar Group', 'Diversified group with FMCG/F&B brand roles', 'Hiring for FMCG / food & beverage brand development (2026)', 'C', 'Fit: possible distributor or 3P partner; verify', 'kumarijob listing [S30b]', 'Not contacted', 'Intro via Biratnagar trade network'),
    ('Bhutan', 'Phuentsholing / Thimphu', 'Existing Kishlay importer(s)', 'Importer', 'Kishlay already exports to Bhutan; trade in INR under the free-trade regime', 'A', 'Fit: existing relationship', 'kishlayfoods.com; Embassy of India Thimphu [S09, S50]', 'Existing', 'Confirm volumes and margins; add Gelephu and Samdrup Jongkhar'),
]
for i, b in enumerate(buyers, 1):
    row = 4 + i
    put(xb, f'A{row}', i)
    for col, v in zip('BCDEFGHIJK', b):
        put(xb, f'{col}{row}', v, BLK if col != 'J' else BLUE, wrap=True, fill=YEL if col == 'J' else None)
dvs = DataValidation(type='list', formula1='"Not contacted,Contacted,Meeting set,Samples sent,Quote sent,Order,Benchmark only,Existing,Dropped"', allow_blank=True)
xb.add_data_validation(dvs)
dvs.add(f'J5:J{4+len(buyers)+20}')
xb.freeze_panes = 'E5'
XB_LAST = 4 + len(buyers)
put(xb, f'D{XB_LAST+2}', 'Count by country', bold=True)
for j, ctry in enumerate(['UAE', 'Qatar', 'Nepal', 'Bhutan']):
    put(xb, f'D{XB_LAST+3+j}', ctry)
    put(xb, f'E{XB_LAST+3+j}', f'=COUNTIF($B$5:$B${XB_LAST},D{XB_LAST+3+j})', BLK, INT)

# ---------------------------------------------------------------- Partners_MA
pm = sheet('Partners_MA', 'Asset-light 3P partners, co-pack clients and M&A precedents',
           'Facts are sourced. Leads marked "unverified" come from directories and must be checked (FSSAI licence, site visit).',
           [34, 18, 14, 14, 14, 50, 46])
header(pm, 4, ['Partner / lead', 'Location', 'Capacity (MT/month)', 'Relationship', 'Status', 'Note', 'Source'])
plist = [
    ('Kishlay own hub (Tulsi), Brahmaputra Industrial Park', 'North Guwahati, Assam', 2000, 'Own', 'Operating', 'Chips, extruders, puffs/balls, biscuits; ‘2,000 MT’ period not stated (read as monthly)', 'kishlayfoods.com/about [S09]'),
    ('AFP Manufacturing Co. Pvt Ltd', 'Hajipur, Bihar', 300, '3P partner', 'Operating', 'Snacks, namkeen, chips for North and East. Also sells Munchh Onn (competitor): watch conflicts', 'kishlayfoods.com/about; dossier [S09, S10]'),
    ('GUD (3P facility)', 'Chhattisgarh', 300, '3P partner', 'Operating', 'Rings, chips, fryums, extruded for Central India', 'kishlayfoods.com/about [S09]'),
    ('Foodees Group', 'India', None, 'Contract mfg partner', 'Reported', 'External contract manufacturing partnership', 'dossier; foodeesgroup.com [S10]'),
    ('Frito-Lay (PepsiCo)', 'India', None, 'Co-pack client', 'Reported', 'Kishlay co-packs for Frito-Lay', 'dossier [S10]'),
    ('Britannia Industries', 'India', None, 'Co-pack client', 'Reported', 'Co-pack client; also held acquisition talks (Sep 2024)', 'dossier; news [S10, S44]'),
    ('Dadiji Snacks', 'Patna, Bihar', None, 'Lead: contract mfg', 'Unverified', 'Founded 2020; contract and private-label savoury snacks (third-party profile)', 'potatopro [S46]'),
    ('Creative Bakers & Confectioners', 'Kolkata', None, 'Lead: chanachur maker', 'Unverified', 'Directory listing as chanachur manufacturer', 'IndiaMART [S46]'),
    ('Benchmark: Bikaji contract units', 'Rajasthan, Bihar, UP, Kolkata', None, 'Model', 'Reported', '4 exclusive + 1 non-exclusive contract manufacturing units', 'bikaji.com/infrastructure [S45]'),
]
for i, p in enumerate(plist):
    row = 5 + i
    for col, v in zip('ABCDEFG', p):
        put(pm, f'{col}{row}', v, BLUE if (col == 'C' and isinstance(v, (int, float))) else BLK, INT if col == 'C' else None, wrap=True)
put(pm, 'A15', 'Installed capacity, own + 3P (MT/month)', bold=True)
put(pm, 'C15', '=SUM(C5:C7)', BLK, INT, fill=SAND)
put(pm, 'A16', 'Estimated monthly output range (MT), from FY25 revenue ÷ ₹/kg', bold=True)
put(pm, 'B16', 'Low')
put(pm, 'C16', '=Rev_FY25*10^7/220/1000/12', BLK, INT)
put(pm, 'D16', 'High')
put(pm, 'E16', '=Rev_FY25*10^7/150/1000/12', BLK, INT)
put(pm, 'F16', 'FY25 actual revenue ÷ assumed realisation of ₹150–220/kg; implies ~40–60% utilisation', wrap=True)
put(pm, 'A17', 'Utilisation range')
put(pm, 'C17', '=C16/C15', BLK, PCT)
put(pm, 'E17', '=E16/C15', BLK, PCT)

header(pm, 20, ['Deal (precedent)', 'Date', 'Stake', 'Consideration (₹ Cr)', 'Implied 100% value (₹ Cr)', 'Note', 'Source'])
deals = [
    ('Prataap Snacks → Avadh Snacks (Gujarat)', 'Aug 2018', 0.80, 148, 'Regional namkeen brand', 'Business Standard [S44]'),
    ('Advent International → DFM Foods (Crax)', 'Sep 2019', 0.68, 851.67, '≈68% from promoters and WestBridge; open offer ₹249.50/share', 'Business Standard [S44]'),
    ('Bikaji → Ariba Foods', '2023', 0.55, 60.49, '55% stake', 'just-food [S44]'),
]
for i, d in enumerate(deals):
    row = 21 + i
    put(pm, f'A{row}', d[0], wrap=True)
    put(pm, f'B{row}', d[1])
    put(pm, f'C{row}', d[2], BLUE, PCT)
    put(pm, f'D{row}', d[3], BLUE, CR2)
    put(pm, f'E{row}', f'=D{row}/C{row}', BLK, CR)
    put(pm, f'F{row}', d[4], wrap=True)
    put(pm, f'G{row}', d[5], wrap=True)
put(pm, 'A24', 'Britannia → Kishlay (talks, not executed)', wrap=True)
put(pm, 'B24', 'Sep 2024')
put(pm, 'C24', 'Majority')
put(pm, 'D24', 'EV ₹600–700 Cr')
put(pm, 'E24', '=600/Rev_FY24', BLK, MULT)
put(pm, 'F24', '=CONCATENATE("EV/sales ",TEXT(600/Rev_FY24,"0.0"),"–",TEXT(700/Rev_FY24,"0.0"),"x FY24; reportedly stalled on valuation")', BLK, wrap=True)
put(pm, 'G24', 'IIFL, Mergers India [S44]')
put(pm, 'A26', 'Bolt-on sizing (model)', bold=True)
put(pm, 'A27', 'Bolt-on revenue (₹ Cr)')
put(pm, 'C27', '=MA_rev', GRN, CR)
put(pm, 'A28', 'Price at EV/sales (₹ Cr)')
put(pm, 'C28', '=MA_rev*MA_EVS', BLK, CR)
put(pm, 'A29', 'Screen criteria', bold=True)
put(pm, 'B29', 'Regional ethnic snack or bakery brand · ₹20–80 Cr revenue · EBITDA ≥10% · new states (Bengal, Bihar, Odisha, UP East) or new category (sweets, premium namkeen) · plant within 600 km of a Kishlay depot · clean GST and FSSAI history', wrap=True)
pm.merge_cells('B29:G29')
pm.row_dimensions[29].height = 46

# ---------------------------------------------------------------- MT_Plan
mt = sheet('MT_Plan', 'Modern trade: how to break in (chains, terms, door economics, rollout, gates)',
           'Chains and terms are public data to verify with each buyer; door economics link to Unit_Econ (MT 400 g) and Inputs. Blue = input.',
           [34, 40, 30, 16, 12, 60])
header(mt, 4, ['Chain', 'Footprint (East / Northeast)', 'Why it matters', 'Entry route', 'Order', 'Source'])
chains = [
    ('Vishal Mega Mart', '~72 stores in the Northeast, 44–60 in Assam; 800+ in India', 'FMCG ~28% of FY25 sales; ~35% of FMCG is own label (co-pack hook)', 'Regional buying team', '1', 'S54, S55'),
    ('Guwahati independents: JDDS, Prince, The Grocer, Nayantara; Nasco Retails', 'Single and small multi-store supermarkets (directory listings)', 'Fast listing, low or no fees: the pilot doors', 'Direct or MT distributor', '1', 'S60'),
    ('Spencer’s Retail (RP-Sanjiv Goenka)', '131 stores in 27+ cities; focus on East India and UP; new West Bengal stores', 'Kolkata take-home shopper; historically said it charges no listing fee', 'Kolkata category team', '2', 'S56, S59'),
    ('Reliance Smart Bazaar / Smart', 'Outlets in Siliguri, Darjeeling, Kolkata; former Big Bazaar stores', 'Scale; central buying and tougher terms', 'Reliance vendor onboarding', '3', 'S60'),
    ('More Retail', '877 supermarkets and 40 hypermarkets, incl. West Bengal and Odisha', 'Neighbourhood format suits 200–400 g packs', 'Regional office, Kolkata', '3', 'S57'),
    ('Arambagh’s Foodmart', 'Kolkata chain, early modern retailer in the East', 'Regional, Bengali taste: chanachur, jhalmuri', 'Direct', '3', 'S60'),
    ('DMart (Avenue Supermarts)', '415 stores (FY25); growth focus north and west', 'Low prices, fast payment; later stage', 'Central buying', 'Later', 'S58'),
]
for i, row in enumerate(chains):
    r = 5 + i
    for col, v in zip('ABCDEF', row):
        put(mt, f'{col}{r}', v, BLUE if col in 'BE' else None, wrap=True)
MT_CH_END = 5 + len(chains) - 1

r0 = MT_CH_END + 2
header(mt, r0, ['Terms to plan for (inputs)', 'Value', 'Unit', '', '', 'Basis'])
terms = [
    ('mt_listing', 'Listing fee per SKU', 5000, '₹', INT, 'Reported ₹2,500–5,000 per SKU (dated benchmark); some chains charge none; DMart guide cites 1.0–1.5% of invoices [S59, S58]'),
    ('mt_skus', 'SKUs listed per door', 6, 'SKUs', INT, 'Hero range: 400 g bhujia, Jolokia, Jhalmuri, 40 Aana, 200 g packs'),
    ('mt_credit', 'Credit days', 45, 'days', INT, 'Varies by chain: 7 days (DMart, good standing) to 60+ days [S58, S59]'),
    ('mt_dist', 'MT distributor margin', 0.04, '% of sales', PCT, 'Snack and biscuit trade margins ~3–5%; Reliance Consumer offered 6.5% [S59]'),
    ('mt_months', 'Months to recover listing and visibility', 6, 'months', INT, 'Planning rule'),
]
MTI = {}
for i, (key, lab, v, unit, fmt, basis) in enumerate(terms):
    r = r0 + 1 + i
    MTI[key] = r
    put(mt, f'A{r}', lab)
    put(mt, f'B{r}', v, BLUE, fmt, YEL if key in ('mt_listing', 'mt_credit') else None)
    put(mt, f'C{r}', unit)
    put(mt, f'F{r}', basis, wrap=True)
r = r0 + 1 + len(terms)
put(mt, f'A{r}', 'Retailer margin, modern trade (% of MRP)')
put(mt, f'B{r}', '=Ret_MT', GRN, PCT)
put(mt, f'F{r}', 'Inputs (illustrative ~20% for MT) [S59]')

d0 = r + 2
header(mt, d0, ['Door economics (400 g pack, ₹110 MRP)', 'Value', 'Unit', '', '', 'How'])
DE = {}
door = [
    ('real', 'Kishlay realisation per pack', '=Unit_Econ!C19', '₹', CR2, 'Unit_Econ, MT column'),
    ('contr', 'Contribution per pack', '=Unit_Econ!C25', '₹', CR2, 'Unit_Econ, MT column'),
    ('sales', 'Target sales per door a month (realisation)', '=MT_sales', '₹', INT, 'Inputs'),
    ('packs', 'Packs per door a month', None, 'packs', INT, 'Sales ÷ realisation'),
    ('perday', 'Packs per door a day', None, 'packs', CR2, '÷ 30'),
    ('rosw', 'Packs per SKU per door a week', None, 'packs', CR2, '÷ SKUs ÷ 4.33'),
    ('cdoor', 'Contribution per door a month', None, '₹', INT, 'Packs × contribution per pack'),
    ('upf', 'Pilot spend per door (listing, promoters, sampling)', None, '₹', INT, 'Pilots sheet, MT lines ÷ 10 doors'),
    ('payback', 'Payback at target sales', None, 'months', CR2, 'Spend per door ÷ contribution a month'),
    ('lst', 'Listing and visibility per door (pilot)', None, '₹', INT, 'Pilots sheet ÷ 10 doors'),
    ('be', 'Break-even sales a month to recover listing in the set months', None, '₹', INT, '(Listing ÷ months) ÷ contribution per pack × realisation'),
    ('wc', 'Receivables per door at the credit days', None, '₹', INT, 'Sales × credit days ÷ 30'),
]
for i, (key, lab, f, unit, fmt, how) in enumerate(door):
    r = d0 + 1 + i
    DE[key] = r
    put(mt, f'A{r}', lab)
    if f:
        put(mt, f'B{r}', f, GRN, fmt)
    put(mt, f'C{r}', unit)
    put(mt, f'F{r}', how)
B = lambda k: f'B{DE[k]}'
put(mt, B('packs'), f'={B("sales")}/{B("real")}', BLK, INT)
put(mt, B('perday'), f'={B("packs")}/30', BLK, CR2)
put(mt, B('rosw'), f'={B("packs")}/B{MTI["mt_skus"]}/4.33', BLK, CR2)
put(mt, B('cdoor'), f'={B("packs")}*{B("contr")}', BLK, INT, SAND)
put(mt, B('upf'), '=SUMIF(Pilots!$B$5:$B$19,"MT Guwahati (10 stores)",Pilots!$E$5:$E$19)*10^5/10', BLK, INT)
put(mt, B('payback'), f'={B("upf")}/{B("cdoor")}', BLK, CR2, SAND)
put(mt, B('lst'), '=SUMIF(Pilots!$A$5:$A$19,"Listing and visibility (10 doors)",Pilots!$E$5:$E$19)*10^5/10', BLK, INT)
put(mt, B('be'), f'=({B("lst")}/B{MTI["mt_months"]})/{B("contr")}*{B("real")}', BLK, INT)
put(mt, B('wc'), f'={B("sales")}*B{MTI["mt_credit"]}/30', BLK, INT)

o0 = d0 + len(door) + 2
header(mt, o0, ['Rollout (doors at the end of each stage)', 'Doors', 'Run-rate ₹ Cr a year', 'Receivables ₹ Cr', '', 'Where'])
stages = [
    ('Pilot, weeks 5–12', 10, 'Guwahati: Vishal + independents'),
    ('End FY27', 60, 'All Vishal Assam + Guwahati independents'),
    ('End FY28', 150, 'Kolkata: Spencer’s, More, Arambagh’s; Siliguri'),
    ('FY29', '=MT_stores', 'East + Northeast chains incl. Reliance'),
]
for i, (lab, doors, where) in enumerate(stages):
    r = o0 + 1 + i
    put(mt, f'A{r}', lab)
    put(mt, f'B{r}', doors, GRN if isinstance(doors, str) else BLUE, INT)
    put(mt, f'C{r}', f'=B{r}*MT_sales*12/10^7', BLK, CR2)
    put(mt, f'D{r}', f'=B{r}*{B("wc")}/10^7', BLK, CR2)
    put(mt, f'F{r}', where)
MT_FY29 = o0 + len(stages)
g0 = MT_FY29 + 2
header(mt, g0, ['Pilot gates (week 12)', 'Threshold', '', '', '', 'Why'])
gates = [
    ('Sales per door a month', '=MT_sales', INT, 'The FY29 plan assumes it'),
    ('Packs per SKU per door a week', f'={B("rosw")}', CR2, 'Below this, the shelf goes to someone else'),
    ('Contribution after promotions vs a ₹10 GT pack (% of realisation)', '=Unit_Econ!B26', PCT, 'Stop if promotions take MT below general trade'),
    ('Fill rate to chain orders', 0.95, PCT, 'Chains de-list unreliable suppliers'),
    ('Returns and expiry', 0.03, PCT, 'Shelf life ≥6 months, first-expiry-first-out'),
]
for i, (lab, v, fmt, why) in enumerate(gates):
    r = g0 + 1 + i
    put(mt, f'A{r}', lab)
    put(mt, f'B{r}', v, BLUE if isinstance(v, float) else GRN, fmt)
    put(mt, f'F{r}', why, wrap=True)
r = g0 + len(gates) + 2
put(mt, f'A{r}', 'Reading', bold=True)
put(mt, f'B{r}', '="A door at target sells ~"&TEXT(' + B('perday') + ',"0")&" packs a day and earns ~₹"&TEXT(' + B('cdoor') + ',"#,##0")&" of contribution a month; pilot spend pays back in ~"&TEXT(' + B('payback') + ',"0.0")&" months. 400 doors tie up ~₹"&TEXT(D' + str(MT_FY29) + ',"0.0")&" Cr of receivables at "&B' + str(MTI['mt_credit']) + '&" days, so start with chains that pay fast."', BLK, wrap=True)
mt.merge_cells(f'B{r}:F{r}')
mt.row_dimensions[r].height = 48
mt.freeze_panes = 'A5'

# ---------------------------------------------------------------- Price_Audit
pa = sheet('Price_Audit', 'Price audit: Kishlay vs competitors (fill live prices tonight)',
           'Kishlay MRPs from company/retail data; competitor prices from indexed listings (date unknown). Yellow = capture from the apps (pin code + date + screenshot).',
           [4, 30, 8, 10, 10, 30, 8, 10, 10, 10, 36, 11, 11, 11, 11, 9, 11, 16])
header(pa, 4, ['#', 'Kishlay SKU', 'Pack (g)', 'Kishlay MRP ₹', 'Kishlay ₹/100 g', 'Competitor SKU', 'Pack (g)', 'Price ₹', 'Comp ₹/100 g', 'Gap vs comp', 'Source (competitor)', 'Blinkit ₹', 'Zepto ₹', 'Instamart ₹', 'BigBasket ₹', 'Pin code', 'Date', 'Screenshot file'])
skus = [
    ('Non Stop Aloo Bhujia', 200, 55, 'Haldiram’s Aloo Bhujia', 200, 55, 'BigBasket listing ₹55 (another listing ₹63), indexed [S49]'),
    ('Non Stop Bikaneri Bhujia (zipper)', 400, 110, 'Bikaji Bikaneri Bhujia', 400, 109.8, 'BigBasket: MRP ₹122, selling ₹109.80, indexed [S49]'),
    ('Non Stop Paneer Bhujia (zipper)', 400, 110, 'Haldiram’s Aloo Bhujia', 400, 100, 'BigBasket ₹100, indexed [S49]'),
    ('Non Stop Khatta Mitha', 200, 55, 'Haldiram’s Khatta Meetha', 180, None, 'Capture India price; Nepal reference NPR 135 (Vhandar, Nov 2026) [S27]'),
    ('Non Stop Navrattan Mixture', 200, 55, 'Haldiram’s Navrattan', 200, None, 'Capture'),
    ('Non Stop Butter Cookies', 150, None, 'Britannia Good Day Butter', 150, None, 'Capture (Kishlay cookies ₹35–55 range)'),
    ('Nutri Zing Soya Chunks (box)', 180, None, 'Nutrela Soya Chunks', 200, None, 'Capture'),
    ('Non Stop Water Toy Rings', None, 5, 'Yellow Diamond Rings / Crax Rings', None, 5, 'Coin MRP ₹5 [S10]'),
    ('Non Stop Masala Noodles', None, 5, 'Wai Wai noodles', None, 5, 'Coin MRP ₹5 [S10]'),
    ('Zing potato chips', None, 10, 'Lay’s', None, 10, 'Coin MRP ₹10 (capture grams)'),
]
for i, s in enumerate(skus, 1):
    row = 4 + i
    put(pa, f'A{row}', i)
    put(pa, f'B{row}', s[0], wrap=True)
    put(pa, f'C{row}', s[1], BLUE, INT)
    put(pa, f'D{row}', s[2], BLUE, CR2, fill=None if s[2] else YEL)
    put(pa, f'E{row}', f'=IF(AND(ISNUMBER(C{row}),ISNUMBER(D{row})),D{row}/C{row}*100,"")', BLK, CR2)
    put(pa, f'F{row}', s[3], wrap=True)
    put(pa, f'G{row}', s[4], BLUE, INT)
    put(pa, f'H{row}', s[5], BLUE, CR2, fill=None if s[5] else YEL)
    put(pa, f'I{row}', f'=IF(AND(ISNUMBER(G{row}),ISNUMBER(H{row})),H{row}/G{row}*100,"")', BLK, CR2)
    put(pa, f'J{row}', f'=IF(AND(ISNUMBER(E{row}),ISNUMBER(I{row})),E{row}/I{row}-1,"")', BLK, PCT)
    put(pa, f'K{row}', s[6], wrap=True)
    for col in 'LMNOPQR':
        put(pa, f'{col}{row}', None, BLUE, fill=YEL)
put(pa, 'B16', 'How to capture (tonight, 20 minutes)', bold=True)
put(pa, 'B17', '1) Set the app location to a Guwahati pin code (e.g., 781005) and repeat for a Kolkata pin code. 2) Search each SKU on Blinkit, Zepto, Instamart and BigBasket. 3) Screenshot the product page showing price and pack size. 4) Enter price, pin code, date and screenshot file name. 5) If Non Stop is not listed, write "not listed" — that is a finding.', wrap=True)
pa.merge_cells('B17:R17')
pa.row_dimensions[17].height = 44

# ---------------------------------------------------------------- Pilots
pl = sheet('Pilots', '90-day pilots: budget, KPIs and decision rules',
           'Budgets are planning assumptions (blue) to agree with finance; inventory is recoverable working capital, not cost.',
           [38, 16, 13, 13, 13, 40, 40])
header(pl, 4, ['Pilot / line item', 'Pilot', 'Cost (₹ lakh)', 'Inventory (₹ lakh)', 'Total (₹ lakh)', 'KPI gate', 'Scale / modify / stop rule'])
pilots = [
    ('Seller onboarding, content, barcodes', 'QC Guwahati (8 weeks)', 1.0, 0, 'Live on 3 apps by week 4', ''),
    ('Launch ads and in-app visibility', 'QC Guwahati (8 weeks)', 3.0, 0, 'ROS ≥1.0 unit/SKU/store/day', 'Scale to Kolkata, Siliguri, Shillong if ROS ≥1.0 and repeat ≥25%'),
    ('Sampling and combo offers', 'QC Guwahati (8 weeks)', 1.0, 0, 'Repeat ≥25% in 30 days', 'Modify SKUs/price if ROS 0.5–1.0'),
    ('Stock in dark stores', 'QC Guwahati (8 weeks)', 0, 4.0, 'Contribution ≥15% after fees and ads', 'Stop if contribution <10% after week 8'),
    ('Listing and visibility (10 doors)', 'MT Guwahati (10 stores)', 2.0, 0, 'Sales ≥₹33k per door a month', 'Scale to 50 doors if met'),
    ('Promoters (2 × 8 weeks)', 'MT Guwahati (10 stores)', 1.6, 0, 'Margin after promo ≥ GT margin', 'Stop if promo eats margin'),
    ('Sampling', 'MT Guwahati (10 stores)', 0.8, 0, '', ''),
    ('Customs broker, labels, legal (Nepal)', 'Nepal first shipments', 1.5, 0, 'Duty and HS codes confirmed by week 3', ''),
    ('First 2 trucks via Panitanki–Kakarbhitta', 'Nepal first shipments', 0, 25.0, 'Sell-through ≥70% in 45 days', 'Scale to 4 trucks/month; open 3P/licensing talks'),
    ('Trade launch (Eastern Nepal)', 'Nepal first shipments', 2.0, 0, '', ''),
    ('Dubai Municipality registration (8 SKUs)', 'UAE trial', 2.4, 0, 'All SKUs registered', 'Ship only when route avoids Hormuz risk'),
    ('Arabic / English labels', 'UAE trial', 1.0, 0, '', ''),
    ('Trial pallet (2 importers)', 'UAE trial', 0, 6.0, 'Reorder within 60 days', 'Scale to 1 container/month on reorder'),
    ('Capacity audit + co-pack RFQs', '3P and M&A', 1.0, 0, 'Utilisation by line known', ''),
    ('M&A screen and diligence (outside advisors)', '3P and M&A', 5.0, 0, '5 targets shortlisted', 'Proceed only if EBITDA ≥10% and price ≤ model'),
]
for i, p in enumerate(pilots):
    row = 5 + i
    put(pl, f'A{row}', p[0], wrap=True)
    put(pl, f'B{row}', p[1], wrap=True)
    put(pl, f'C{row}', p[2], BLUE, CR)
    put(pl, f'D{row}', p[3], BLUE, CR)
    put(pl, f'E{row}', f'=C{row}+D{row}', BLK, CR)
    put(pl, f'F{row}', p[4], wrap=True)
    put(pl, f'G{row}', p[5], wrap=True)
last = 5 + len(pilots) - 1
put(pl, f'A{last+1}', 'Total', bold=True)
for col in 'CDE':
    put(pl, f'{col}{last+1}', f'=SUM({col}5:{col}{last})', BLK, CR, fill=SAND)
put(pl, f'A{last+3}', 'Budget by pilot (₹ lakh)', bold=True)
for j, nm in enumerate(['QC Guwahati (8 weeks)', 'MT Guwahati (10 stores)', 'Nepal first shipments', 'UAE trial', '3P and M&A']):
    put(pl, f'A{last+4+j}', nm)
    put(pl, f'C{last+4+j}', f'=SUMIF($B$5:$B${last},A{last+4+j},$C$5:$C${last})', BLK, CR)
    put(pl, f'D{last+4+j}', f'=SUMIF($B$5:$B${last},A{last+4+j},$D$5:$D${last})', BLK, CR)
    put(pl, f'E{last+4+j}', f'=C{last+4+j}+D{last+4+j}', BLK, CR)
PL_TOTAL = last + 1

# ---------------------------------------------------------------- Roadmap_RAG
rm = sheet('Roadmap_RAG', '90-day Founder’s Office roadmap and twice-weekly RAG tracker',
           'Review every Monday and Thursday (30 min). Status values: Not started, On track, At risk, Off track, Done. Owners are roles; assign names in week 1.',
           [4, 22, 52, 20, 7, 7, 34, 30, 13, 9])
header(rm, 4, ['#', 'Workstream', 'Task', 'Owner (role)', 'Start wk', 'End wk', 'Gate / output', 'KPI', 'Status', '% done'])
tasks = [
    ('QC + MT multipacks', 'Pull SKU velocity and margin cube; pick 6 hero SKUs and 2 multipacks', 'Founder’s Office + Head of Sales NE', 1, 2, 'Hero list signed by founders', 'Top 30 SKUs’ share of sales'),
    ('QC + MT multipacks', 'Onboard Blinkit, Zepto, Instamart (Guwahati): accounts, listings, content, barcodes', 'Founder’s Office + e-com executive', 2, 4, 'Live on 3 apps', 'SKUs live'),
    ('QC + MT multipacks', 'Design and cost multipacks (party pack of ₹10 packs, chai-time combo, 400 g zipper)', 'Marketing + Finance', 3, 4, 'Costed packs, MRP fixed', 'Contribution % per pack'),
    ('QC + MT multipacks', 'Run 8-week QC pilot; weekly read-out', 'Founder’s Office', 5, 12, 'Weekly dashboard', 'ROS, repeat, contribution'),
    ('QC + MT multipacks', 'Run 10-door MT pilot in Guwahati', 'Modern-trade lead', 5, 12, 'Door-level P&L', 'Sales/door/month'),
    ('QC + MT multipacks', 'Scale / modify / stop decision; next cities (Kolkata, Siliguri, Shillong)', 'Founders', 12, 13, 'Decision memo', 'Pilot vs gate'),
    ('Exports', 'Baseline Bhutan: importers, volumes, margins', 'Export analyst', 1, 2, 'Bhutan fact base', 'Revenue, margin'),
    ('Exports', 'Nepal: customs broker quote on HS codes (1905, 2106, 1902), duty, VAT, labelling', 'Export analyst', 2, 3, 'Landed-cost sheet', 'Duty % confirmed'),
    ('Exports', 'Meet Bhat-Bhateni, United Distributors, Nepal Overseas, MV Dugar', 'Founder’s Office + Export analyst', 3, 6, '3 term sheets', 'Meetings held'),
    ('Exports', 'First 2 trucks to Eastern Nepal via Panitanki–Kakarbhitta', 'Export analyst + Logistics', 6, 10, 'Shipment + sell-through data', 'Sell-through ≥70% in 45 days'),
    ('Exports', 'Nepal local 3P / licensing option paper (vs export)', 'Founder’s Office', 8, 12, 'Board paper', 'Royalty vs export contribution'),
    ('Exports', 'UAE: Dubai Municipality registration for 8 SKUs; Arabic labels; halal check', 'Export analyst + QA', 2, 8, 'SKUs registered', 'Registrations'),
    ('Exports', 'GCC outreach: Lulu sourcing, Al Adil, Nesto; samples; FOB/CIF price list', 'Founder’s Office', 4, 10, 'Buyer feedback, price acceptance', 'Samples sent, quotes'),
    ('Exports', 'Shipping-risk gate: route via Fujairah / Khor Fakkan / Jeddah; trial pallet decision', 'Founders', 10, 13, 'Go / no-go', 'Freight quote, transit days'),
    ('3P and M&A', 'Capacity and utilisation audit by line (own, AFP, GUD, Foodees); cost per kg own vs 3P', 'GM Supply Chain + Founder’s Office', 1, 3, 'Utilisation by line', 'Utilisation %'),
    ('3P and M&A', 'Co-pack pipeline: renew Frito-Lay / Britannia; 2 new RFQs', 'Founders + Sales', 3, 8, 'Signed renewals / LOIs', '₹ Cr pipeline'),
    ('3P and M&A', 'Screen 20 regional brands against criteria; score', 'Founder’s Office', 4, 8, 'Long-list scored', '20 screened'),
    ('3P and M&A', 'Shortlist 5; management meetings; indicative value vs precedents', 'Founders + advisors', 8, 12, 'Shortlist memo', '5 meetings'),
    ('Board, investor, lender reporting', 'Monthly MIS v1: revenue by channel/SKU/state, GM, contribution, working capital, bank-limit use', 'Founder’s Office + Finance', 1, 2, 'MIS v1', 'MIS on day 5 of month'),
    ('Board, investor, lender reporting', 'CRISIL: resume monthly No Default Statements; share FY25–FY26 data; clear Tulsi GST filing delays (5 in FY26)', 'Finance + Founders', 1, 4, 'NDS filed monthly', 'Remove "Issuer Not Cooperating"'),
    ('Board, investor, lender reporting', 'Board pack template for promoters and NVP nominee; KPI tree to ₹512 Cr / 10%', 'Founder’s Office', 3, 4, 'Template approved', ''),
    ('Board, investor, lender reporting', 'First monthly board / investor update', 'Founder’s Office', 6, 6, 'Update sent', 'On time'),
    ('Board, investor, lender reporting', 'FY27–FY29 plan and budget for board approval', 'Founders + Finance', 12, 13, 'Approved plan', ''),
    ('Operating velocity', 'Set twice-weekly RAG review; every initiative has an owner and a date', 'Founder’s Office', 1, 1, 'Tracker live', '% tasks with owner'),
    ('Operating velocity', 'Decision log and 48-hour escalation rule', 'Founder’s Office', 2, 4, 'Log live', 'Median unblock time'),
    ('Operating velocity', 'Track % of tasks on time; target ≥85% by week 13', 'Founder’s Office', 1, 13, 'Weekly score', '% on time'),
]
for i, t in enumerate(tasks, 1):
    row = 4 + i
    put(rm, f'A{row}', i)
    put(rm, f'B{row}', t[0], wrap=True)
    put(rm, f'C{row}', t[1], wrap=True)
    put(rm, f'D{row}', t[2], wrap=True)
    put(rm, f'E{row}', t[3], BLUE, INT)
    put(rm, f'F{row}', t[4], BLUE, INT)
    put(rm, f'G{row}', t[5], wrap=True)
    put(rm, f'H{row}', t[6], wrap=True)
    put(rm, f'I{row}', 'Not started', BLUE, fill=YEL)
    put(rm, f'J{row}', 0, BLUE, '0%')
RM_LAST = 4 + len(tasks)
dvr = DataValidation(type='list', formula1='"Not started,On track,At risk,Off track,Done"', allow_blank=False)
rm.add_data_validation(dvr)
dvr.add(f'I5:I{RM_LAST}')
for status, color in [('On track', 'C6EFCE'), ('Done', 'A9D08E'), ('At risk', 'FFEB9C'), ('Off track', 'FFC7CE')]:
    rm.conditional_formatting.add(f'I5:I{RM_LAST}', CellIsRule(operator='equal', formula=[f'"{status}"'], fill=PatternFill('solid', fgColor=color)))
s0 = RM_LAST + 2
put(rm, f'C{s0}', 'Summary', bold=True)
for j, st in enumerate(['Not started', 'On track', 'At risk', 'Off track', 'Done']):
    put(rm, f'C{s0+1+j}', st)
    put(rm, f'D{s0+1+j}', f'=COUNTIF($I$5:$I${RM_LAST},C{s0+1+j})', BLK, INT)
put(rm, f'C{s0+6}', 'Share on track or done (of started tasks)', bold=True)
put(rm, f'D{s0+6}', f'=IFERROR((D{s0+2}+D{s0+5})/(COUNTA($I$5:$I${RM_LAST})-D{s0+1}),0)', BLK, PCT)
put(rm, f'C{s0+7}', 'Average % done')
put(rm, f'D{s0+7}', f'=AVERAGE($J$5:$J${RM_LAST})', BLK, PCT)
rm.freeze_panes = 'D5'

# ---------------------------------------------------------------- Board_MIS
bm = sheet('Board_MIS', 'Monthly MIS and board / investor / lender pack (template)',
           'One page the founders, the NVP nominee director and HDFC Bank can all read. Fill monthly; targets are from the model.',
           [34, 40, 14, 14, 14, 16, 24])
header(bm, 4, ['KPI', 'Definition', 'Target', 'This month', 'Last month', 'Owner', 'Source system'])
kpis = [
    ('Revenue (₹ Cr)', 'Net sales by channel: GT, MT, QC, e-com, exports, co-pack', '=Rev_Bridge!E16/12', 'Finance', 'ERP / Tally'),
    ('Volume (MT)', 'Dispatched tonnes by plant (own, AFP, GUD)', None, 'Supply chain', 'Plant MIS'),
    ('Gross margin %', '(Net sales − RM − packaging) ÷ net sales', None, 'Finance', 'ERP'),
    ('Contribution margin %', 'Gross margin − freight − trade schemes − platform fees', None, 'Finance', 'ERP + scheme sheets'),
    ('EBITDA margin %', 'Operating EBITDA ÷ net sales', '=EBITDA_Bridge!C17', 'Finance', 'ERP'),
    ('Capacity utilisation %', 'Output ÷ installed capacity, by line', None, 'Supply chain', 'Plant MIS'),
    ('Active outlets', 'Outlets billed in the month', None, 'Sales', 'DMS'),
    ('Sales per active outlet (₹)', 'GT revenue ÷ active outlets', None, 'Sales', 'DMS'),
    ('QC rate of sale', 'Units per SKU per dark store per day', '=QC_units', 'Founder’s Office', 'Platform dashboards'),
    ('Export orders (₹ lakh)', 'Orders by market: Bhutan, Nepal, GCC', None, 'Export analyst', 'Export register'),
    ('Working capital days', 'DSO + DIO − DPO', None, 'Finance', 'ERP'),
    ('Bank-limit utilisation %', 'Average fund-based utilisation (was ~93% in 2023)', 0.80, 'Finance', 'Bank statements'),
    ('Net cash accrual (₹ Cr, annualised)', 'PAT + depreciation', 15, 'Finance', 'ERP'),
    ('CRISIL NDS and GST returns on time', 'Monthly NDS submitted; GST returns filed on time (5 delays in FY26) (Y/N)', 'Y', 'Finance', 'CRISIL portal, GST portal'),
    ('Initiatives on time %', 'From Roadmap_RAG', 0.85, 'Founder’s Office', 'Roadmap_RAG'),
]
for i, k in enumerate(kpis):
    row = 5 + i
    put(bm, f'A{row}', k[0], wrap=True)
    put(bm, f'B{row}', k[1], wrap=True)
    v = k[2]
    fmt = PCT if (isinstance(v, float) and v < 1) or (isinstance(v, str) and ('C17' in v)) else (CR2 if k[0].startswith('QC') else CR)
    put(bm, f'C{row}', v, BLUE if isinstance(v, (int, float)) or v == 'Y' else GRN, fmt)
    put(bm, f'D{row}', None, BLUE, fill=YEL)
    put(bm, f'E{row}', None, BLUE, fill=YEL)
    put(bm, f'F{row}', k[3])
    put(bm, f'G{row}', k[4])
put(bm, 'A22', 'Example row format: Revenue · Target 32.0 · This month 30.4 · Last month 29.8 (₹ Cr).', SUB)

# ---------------------------------------------------------------- Assumptions register
ar = sheet('Assumptions', 'Assumptions register: what is assumed, why, and how to validate',
           'Values link to Inputs (active scenario). Sensitivity = effect on FY29 revenue or margin if wrong.',
           [6, 16, 46, 12, 11, 52, 46, 12])
header(ar, 4, ['#', 'ID', 'Assumption', 'Value', 'Label', 'Why this value', 'How to validate (owner, when)', 'Sensitivity'])
reg = [
    ('g_FY26', 'Recovery after FY25’s −16%; Tulsi headcount +15% YoY', 'FY26 provisional sales by month from finance (week 1)', 'High'),
    ('Rev_FY25', 'MCA filing via Tracxn; group ≈ KFPL standalone', 'Audited consolidated FY25 incl. Tulsi firm (week 1)', 'High'),
    ('Share_copack', 'Co-packing exists (Frito-Lay, Britannia) but share unknown', 'MIS by customer (week 1)', 'Medium'),
    ('GT_CAGR', 'Below category growth because tail SKUs are pruned', 'Secondary sales trend by state (week 2)', 'High'),
    ('QC_stores', 'Coverage of East + NE dark stores by FY29 across 4 platforms', 'Platform city plans; pilot learnings (week 12)', 'Medium'),
    ('QC_units', 'Regional brand rate of sale', '8-week Guwahati pilot (weeks 5–12)', 'High'),
    ('Nepal_trucks', 'Eastern Nepal first, then local 3P', 'Broker quote (week 3) + first 2 trucks (week 10)', 'Medium'),
    ('NP_duty', 'Biscuit HS 1905 31 at 30%; namkeen line unconfirmed', 'Nepal customs broker (week 3)', 'High'),
    ('GCC_cont', 'Depends on registration and shipping risk', 'Registrations (week 8); route gate (week 13)', 'High'),
    ('UAE_duty', 'CEPA makes most Indian goods duty-free', 'Check HS line under CEPA schedule (week 2)', 'Medium'),
    ('Copack_incr', 'Spare lines exist (est. 50–75% utilisation)', 'Capacity audit by line (week 3)', 'Medium'),
    ('MA_rev', 'One bolt-on in FY28', 'Screen and shortlist (weeks 4–12)', 'High'),
    ('EBITDA_base', 'Mid-single digits implied by CRISIL ratios', 'Audited FY25/FY26 P&L (week 1)', 'High'),
    ('L_mix', 'Higher contribution per kg in QC, MT, export', 'Pilot P&Ls; plant costing', 'High'),
    ('L_util', 'Fixed cost absorption from more volume', 'Capacity audit + co-pack pipeline', 'Medium'),
    ('Ret_GT', 'Industry-typical retailer margin for ₹10 packs', 'Scheme sheets and distributor claims (week 2)', 'Medium'),
    ('Plat_QC', 'Platform margin within published 20–23% range', 'Signed platform terms (week 4)', 'Medium'),
]
for i, (nid, why, how, sens) in enumerate(reg, 1):
    row = 4 + i
    put(ar, f'A{row}', i)
    put(ar, f'B{row}', nid)
    put(ar, f'C{row}', f'=Inputs!B{INPUT_ROW[nid]}', GRN, wrap=True)
    fmt = inp[f'F{INPUT_ROW[nid]}'].number_format
    put(ar, f'D{row}', f'={nid}', GRN, fmt)
    put(ar, f'E{row}', f'=Inputs!H{INPUT_ROW[nid]}', GRN)
    put(ar, f'F{row}', why, wrap=True)
    put(ar, f'G{row}', how, wrap=True)
    put(ar, f'H{row}', sens)

# ---------------------------------------------------------------- Sources
so = sheet('Sources', 'Sources register', 'Accessed 17 Nov 2026 unless stated. "Indexed" = price seen in a search-engine snapshot; verify live.',
           [7, 52, 22, 16, 80])
header(so, 4, ['ID', 'Source', 'Type', 'Date', 'Link / location'])
SRC = [
    ('S01', 'CRISIL Ratings — Kishlay Foods Pvt Ltd rating rationale', 'Rating agency', '26 May 2021', 'crisilratings.com (Rating Rationale, Kishlay Foods Private Limited)'),
    ('S02', 'CRISIL Ratings — Kishlay Foods Pvt Ltd rating rationale (consolidated KFPL + TSF)', 'Rating agency', '1 Feb 2024', 'crisilratings.com (Rating Rationale, Kishlay Foods Private Limited)'),
    ('S03', 'CRISIL Ratings — Tulsi Speciality Foods rating rationale', 'Rating agency', '2 Feb 2024', 'crisilratings.com (Rating Rationale, Tulsi Speciality Foods)'),
    ('S04', 'Crisil Ratings — Kishlay Foods Pvt Ltd, Issuer Not Cooperating, B/Stable', 'Rating agency', '24 Jun 2026', 'crisilratings.com (Rating Rationale, Kishlay Foods Private Limited)'),
    ('S05', 'Tracxn — Tulsi Speciality Foods Pvt Ltd financial statements FY2024-25 (summary of MCA filing)', 'Data provider (user-provided export)', '17 Nov 2026', 'Tracxn export; CIN U10790AS2024PTC027099'),
    ('S06', 'Falcon eBiz — Tulsi Speciality Foods Pvt Ltd company record', 'Company registry data', '2026', 'https://www.falconebiz.com/company/TULSI-SPECIALITY-FOODS-PRIVATE-LIMITED-U10790AS2024PTC027099'),
    ('S07', 'Motilal Oswal — Snacks thematic (Kishlay revenue series FY15–FY24)', 'Broker research (via dossier)', 'Jan 2026', 'Cited in user dossier'),
    ('S08', 'Dealroom — Kishlay Foods profile', 'Data provider (via dossier)', '2026', 'https://dealroom.co/companies/kishlay-foods/'),
    ('S09', 'Kishlay Foods website — home, about, products (236 items, 18 categories)', 'Company', '17 Nov 2026', 'https://kishlayfoods.com/'),
    ('S10', 'Comprehensive Corporate, Strategic and Marketing Dossier: Kishlay Foods', 'User-provided research', '2026', 'Kishlay_Foods_Comprehensive_Business_Analysis.pdf'),
    ('S11', 'Kishlay Foods: Strategic Business, Consumer Behaviour & GTM Decoding', 'User-provided research', '2026', 'Kishlay_Foods_Strategic_Decoding_Report.pdf'),
    ('S12', 'Gopal Snacks — FY25 earnings release', 'Company filing', 'May 2025', 'https://files.tijorifinance.com/insight/india/57717/Earnings%20Release/ER-May25.pdf'),
    ('S13', 'Gopal Snacks — FY26 results coverage', 'News / aggregator', 'May 2026', 'https://www.multibagg.ai/market-pulse/articles/gopal-fy26-93790'),
    ('S14', 'Bikaji Foods — Investor presentation Q4 & FY25', 'Company filing', '15 May 2025', 'https://www.bikaji.com/pub/media/Investor-Presentation-15-05-2025.pdf'),
    ('S15', 'Bikaji Foods — FY26 results (Restaurant India)', 'News', 'May 2026', 'https://www.restaurantindia.in/news/restaurant-india-news-bikaji-q4-profit-surges-398-percent-on-strong-ethnic-snacks-demand.n16181'),
    ('S16', 'Prataap Snacks — FY25 earnings release; FY26 results', 'Company filing / news', '2025–2026', 'https://financialreports.eu/filings/prataap-snacks-limited/earnings-release/2025/42383256/ ; https://scanx.trade/stock-market-news/companies/prataap-snacks-limited-schedules-board-meeting-on-april-27-2026-for-q4fy26-results/38398348'),
    ('S17', 'Annapurna Swadisht — FY26 results; FY25 growth', 'News / aggregator', 'May 2026', 'https://scanx.trade/stock-market-news/companies/annapurna-swadisht-reports-fy26-net-profit-of-3-033-lakh/41705645 ; NSE filing ASL_29052026194150 (not opened)'),
    ('S18', 'CareEdge — India’s Q-commerce market (GOV ₹64,000 Cr FY25 → ₹2 lakh Cr FY28)', 'Rating agency research', 'Jul 2025', 'https://www.careratings.com/uploads/newsfiles/1752146049_India%E2%80%99s%20Q-commerce%20Market%20-%20CareEdge%20Advisory%20Report.pdf'),
    ('S19', 'Quick-commerce commissions (Blinkit variable 2–18%; Zepto 22–23%; Instamart 20–22%)', 'News', 'Mar 2025', 'https://inc42.com/?p=503754 ; https://www.newsbytesapp.com/news/business/blinkit-zepto-adjust-commission-structures-to-enhance-profitability/story'),
    ('S20', 'Blinkit launched in Guwahati, Jan 2025 (Zoo Road, Chandmari warehouses)', 'News', '2025', 'https://nenow.in/north-east-news/assam/quick-commerce-boom-in-guwahati-a-double-edged-sword-for-local-businesses.html'),
    ('S21', 'Dark-store counts (Blinkit 2,751; Instamart 1,240; Flipkart Minutes ~1,200 — Sep 2026)', 'Compilation', 'Sep 2026', 'https://www.clickpost.ai/blog/quick-commerce-statistics-india'),
    ('S23', 'GST 2.0 — namkeen, biscuits, noodles to 5% from 22 Sep 2025', 'News / tax guide', 'Sep 2025', 'https://www.business-standard.com/economy/news/fmcg-sector-benefits-from-gst-as-shampoo-noodles-move-to-5-percent-slab-125090301741_1.html ; https://cleartax.in/s/gst-on-namkeen-savouries'),
    ('S24', 'Nepal import duty (biscuits 30%) and 13% VAT; US Commercial Guide', 'Trade data / government', '2025–2026', 'https://ximpex.in/hs-codes/190531/nepal ; https://www.trade.gov/country-commercial-guides/nepal-import-tariffs'),
    ('S25', 'Haldiram’s Nepal venture (Anandam Snacks & Beverage, DV Group)', 'News', 'Jul 2025', 'https://english.clickmandu.com/2025/07/848/'),
    ('S26', 'Bikaji–Chaudhary Group 50:50 JV in Nepal', 'News', 'Jul 2025', 'https://www.just-food.com/news/bikaji-foods-forms-joint-venture-with-chaudhary-group-for-nepal-expansion/'),
    ('S27', 'Vhandar — Haldiram’s price list in Nepal (Nov 2026)', 'Retailer website', 'Nov 2026', 'https://www.vhandar.com/brand/haldiram-s'),
    ('S28', 'Bhat-Bhateni Supermarket — about (27 stores)', 'Company', '2026', 'https://bbsm.com.np/pages/about'),
    ('S29', 'Vishal Group — United Distributors Nepal (45,000 outlets)', 'Company press release', 'Mar 2026', 'https://fortune.com/press-releases/vishal-group-global-brand-partnerships-distribution-emerging-markets-2026-03-23/'),
    ('S30', 'Nepal Overseas FMCG sales; MV Dugar FMCG roles', 'News / job listing', '2025–2026', 'https://english.clickmandu.com/?p=681 ; https://www.kumarijob.com/mv-dugar-auto-division/76259-brand-business-development-manager-fmcg-food-beverage'),
    ('S31', 'India–Nepal trade (Embassy brief; chapter-19 exports)', 'Government / trade data', '2024–2026', 'https://indembkathmandu.gov.in/commerce-wing-brief ; https://ximpex.in/hs-codes/chapter/19/nepal'),
    ('S32', 'Nepali migrant workers (714,165 in 8 months FY2025/26; ILO ~4.5M)', 'News / ILO', '2026', 'https://en.himalpress.com/?p=82373 ; https://www.ilo.org/resource/news/ilo-supports-safer-migration-nepali-workers-gcc-countries-advancing-social'),
    ('S33', 'Indians in GCC (UAE 43.26 lakh, KSA 27.48 lakh — MEA)', 'Government', '2026', 'https://www.mea.gov.in/Images/CPV/4407-01-english-2026.pdf'),
    ('S34', 'PRAN in the UAE ($245M FY24 via Emerging World Group); Gulf orders hit by war; Gulfood 2026 orders', 'News', '2025–2026', 'https://www.thedailystar.net/business/news/prans-journey-the-uae-3828901 ; https://online91.thedailystar.net/business/economy/news/food-exports-the-gulf-feel-war-shock-4138631'),
    ('S35', 'Lulu Group India sourcing network', 'News', '2025–2026', 'https://www.khaleejtimes.com/supplements/lulu-continues-to-strengthen-india-gcc-trade-links-through-expanded-sourcing-network ; https://gulfnews.com/business/retail/how-uaes-lulu-group-plans-to-keep-food-prices-in-check-across-the-gulf-1.500422511'),
    ('S36', 'Al Adil Trading store network', 'News', '2021–2023', 'https://www.khaleejtimes.com/kt-network/al-adil-trading-extends-reach-with-new-outlets-in-jlt-and-dip-it ; https://www.arabianbusiness.com/retail/422197-dubais-king-of-spices-aiming-to-expand-into-europe'),
    ('S37', 'Nesto Group expansion (152 stores; Qatar)', 'News', 'Oct 2024', 'https://gulfnews.com/business/corporate-news/nesto-group-expands-into-qatar-with-new-hypermarket-and-plans-for-10-stores-by-2026-1.1730109242983'),
    ('S38', 'Carrefour UAE — Haldiram’s Alu Bhujia 200 g, AED 5.69 (indexed)', 'Retail listing', 'Indexed', 'https://www.carrefouruae.com/mafuae/en/indian-food/haldiram-s-alu-bhujia-snacks-200g/p/6873'),
    ('S38b', 'Asian Basket Dubai — Indian snacks', 'Retailer website', '2026', 'https://www.asianbasket.ae/shop/category/snacks-and-sweets-17'),
    ('S39', 'noon UAE — Bikaji Bombay Mix 200 g', 'Retail listing', '2026', 'https://www.noon.com/uae-en/bikaji-bombay-mix-namkeen-200g-indian-snack/Z1EBF49D474359F82F4EEZ/p/'),
    ('S40', 'UAE food labelling and import approvals', 'Legal / free-zone guide', '—', 'https://www.tamimi.com/law-update/march-10/articles/labeling-of-foodstuff-in-dubai/ ; https://www.meydanfz.ae/relocation-dubai-india/food-import-approvals-uae-supermarkets'),
    ('S41', 'India–UAE CEPA and trade ($100.06B FY25)', 'News', '2025', 'https://knnindia.co.in/news/newsdetails/global/india-uae-review-cepa-progress-as-bilateral-trade-tops-usd-100-billion'),
    ('S42', '2026 Iran war: Hormuz shipping disruption and Gulf food imports', 'News / FAO', '2026', 'https://www.thenationalnews.com/news/mena/2026/11/06/ukraine-grain-storage-gulf-food-security-middle-east/ ; https://en.wikipedia.org/wiki/Economic_impact_of_the_2026_Iran_war'),
    ('S43', 'Rupee at 94.24 per US dollar (13 Nov 2026)', 'News', 'Nov 2026', 'https://hdfcsky.com/news/rupee-slides-0-3percent-to-94-24-as-hawkish-fed-and-oil-spike-erase-six-month-high-rally'),
    ('S44', 'M&A precedents: Prataap–Avadh; Advent–DFM; Bikaji–Ariba; Britannia–Kishlay talks', 'News', '2018–2024', 'https://business-standard.com/article/companies/prataap-snacks-to-acquire-80-stake-in-avadh-snacks-for-rs-1-48-billion-118082201037_1.html ; https://www.business-standard.com/article/companies/advent-international-to-buy-indian-snacks-maker-dfm-foods-for-rs-1-178-cr-119090901192_1.html ; https://www.indiainfoline.com/news/companies/britannia-eyes-kishlay-foods-acquisition ; https://mnacritique.mergersindia.com/news/britannia-in-talks-to-buy-northeasts-kishlay-foods/'),
    ('S45', 'Bikaji infrastructure — contract manufacturing units', 'Company', '—', 'https://bikaji.com/infrastructure'),
    ('S46', 'East-India co-packer leads (Dadiji Snacks; Creative Bakers)', 'Directories', '—', 'https://www.potatopro.com/node/173133 ; https://m.indiamart.com/creativebakersconfectioners'),
    ('S47', 'Namkeen / savoury snacks market size and growth', 'Market research', '2025', 'https://www.kenresearch.com/india-savory-snacks-market ; https://www.technavio.com/report/namkeen-market-industry-in-india-analysis'),
    ('S48', 'Trade margins in snacks (super-stockist 3–5%; distributors 8–15%)', 'News / guide', '2024–2026', 'https://www.business-standard.com/article/opinion/fmcg-distribution-system-in-a-flux-122011101572_1.html ; https://www.tradologie.com/blogs/top-most-profitable-fmcg-food-distributorships-in-india/'),
    ('S49', 'BigBasket listings (indexed): Haldiram’s 200 g ₹55; Haldiram’s 400 g ₹100; Bikaji 400 g MRP ₹122 / ₹109.80', 'Retail listing', 'Indexed', 'https://bigbasket.com/pd/40128317/haldiram-bhujiawala-namkeen-aloo-bhujia-200-g ; https://bigbasket.com/pd/264454/haldirams-namkeen-aloo-bhujia-400-g-pouch ; https://bigbasket.com/pd/30011828/bikaji-namkeen-bikaneri-bhujia-400-g-pouch'),
    ('S50', 'India–Bhutan trade framework; FSSAI workshops in Bhutan', 'Government', '2024', 'https://www.indembthimphu.gov.in/pages/MzI, ; https://mohfw.gov.in/press-info/7473'),
    ('S51', 'NFRA inspection report: MSKA & Associates LLP, network firm of BDO International', 'Regulator', '2026', 'https://caalley.com/ca/nfra/nfra_20260316866297865.pdf'),
    ('S52', 'Tracxn — Kishlay Foods company profile (FY25 revenue ₹288 Cr, −16% YoY; net loss ₹6.31 Cr; funding; listed-peer multiples; legal entities)', 'Data provider (user-provided PDF)', '17 Nov 2026', 'Tracxn platform (subscription); PDF supplied by the user — not redistributed'),
    ('S53', 'Tracxn — Tulsi Speciality Foods Pvt Ltd legal-entity profile (EPFO headcount, charges, auditors, GST filing delays, directors, corporate structure)', 'Data provider (user-provided PDF)', '17 Nov 2026', 'Tracxn platform (subscription); PDF supplied by the user — not redistributed'),
    ('S54', 'Vishal Mega Mart in the Northeast: 72 NE stores, 44 in Assam (trade report); “nearly 60 in Assam”, 800+ in India (ThePrint)', 'News', '2025', 'https://apparelresources.com/business-news/retail/indian-retailer-vishal-mega-mart-expands-retail-footprint-north-east/ ; https://theprint.in/feature/assams-vishal-mega-mart-sales-jobs-hundreds-applications/3059013/'),
    ('S55', 'Vishal Mega Mart FY25 mix: apparel 44%, general merchandise 28%, FMCG 28%; own brands 73%; ~35% own label in FMCG (HDFC Securities est.)', 'Broker research / news', '2025–2026', 'https://wealthy.in/invest/news/stock/1595376 ; HDFC Securities (HSIE) Vishal Mega Mart update, Sep 2026'),
    ('S56', 'Spencer’s Retail: 131 stores in 27+ cities (Aug 2026 filing); focus on East India and UP; 8–10 new stores in West Bengal and UP', 'Company filing / news', '2025–2026', 'https://nsearchives.nseindia.com/corporate/SPENCERS_13082026155615_IP.pdf ; https://informistmedia.com/EquityWire/39680/Expansion-Plans-Spencer-s-Retail-plans-to-open-8-10-stores-in-Bengal-Uttar-Pradesh-in-FY26 ; https://www.rpsg.in/business/spencers'),
    ('S57', 'More Retail: 877 supermarkets and 40 hypermarkets incl. West Bengal and Odisha (company LinkedIn via trade press)', 'News', '—', 'https://www.indiaretailing.com/?p=170497 ; https://www.indiaretailing.com/?p=171261'),
    ('S58', 'DMart: 415 stores at FY25 end, FY26 focus north; vendor guide: 7-day settlement, listing fee 1.0–1.5% of invoices (unverified)', 'News / vendor guide', '2025', 'https://www.magzter.com/hi/stories/newspaper/Financial-Express-Lucknow/AVENUE-SUPERMARTS-TO-DOUBLE-DOWN-ON-STORE-EXPANSION ; https://www.terra-insight.com/insights/dmart-fmcg-settlement-reconciliation/'),
    ('S59', 'Modern-trade terms: listing fees ₹2,500–5,000 per SKU, Spencer’s no listing fee (2009); MT margin ~20% (illustration); snack trade margins 3–5%, Reliance Consumer 6.5%', 'News / guides', '2009–2024', 'https://www.business-standard.com/article/companies/retailers-extract-higher-margins-from-fmcg-firms-109110600071_1.html ; https://echai.ventures/d2c/d2c-offline-retail/general-trade-vs-modern-trade-start-margins ; https://echai.ventures/d2c/d2c-offline-retail/real-cost-getting-into-modern-trade ; https://business-standard.com/companies/news/reliance-consumer-targets-chips-biscuits-market-with-higher-trade-margins-124110300468_1.html'),
    ('S60', 'Store directories: Guwahati supermarkets (JDDS, Prince, The Grocer, Nayantara, Nasco); Reliance Smart Bazaar in Siliguri, Darjeeling, Kolkata; Arambagh’s Foodmart', 'Directories / trade press', '2022–2026', 'https://threebestrated.in/supermarkets-in-guwahati-as ; https://khatabook.com/blog/top-wholesale-markets-in-guwahati ; https://www.franchiseindia.com/business-opportunities/grocery-stores-in-assam/ssc-188/loc-3 ; https://yappe.in/west-bengal/siliguri/reliance-smart-bazaar/2383293 ; https://www.magzter.com/article/Business/Images-Retail/Arambagh-Foodmart-Pioneer-of-Modern-Retail-in-East-India'),
]
for i, s in enumerate(SRC):
    row = 5 + i
    for col, v in zip('ABCDE', s):
        put(so, f'{col}{row}', v, wrap=True)

# ---------------------------------------------------------------- Target_Check
tcs = sheet('Target_Check', 'Is ₹512 Cr the right target? Tests, scenarios and options',
            'No public source states ₹512 Cr (the only public "512" is Tulsi’s headcount, Feb 2026). FY25 revenue fell 16% to ₹288 Cr, so the tests start from the FY25 actual.',
            [60, 13, 13, 13, 13, 13, 64])
header(tcs, 4, ['Test 1 · Growth a year needed to reach the target', 'FY27', 'FY28', 'FY29', 'FY30', 'FY31', 'Reading'])
put(tcs, 'A5', 'Years from FY25A')
for col, n in zip('BCDEF', (2, 3, 4, 5, 6)):
    put(tcs, f'{col}5', n, BLUE, INT)
put(tcs, 'A6', 'From FY25A (₹288 Cr, latest actual)', bold=True)
for col in 'BCDEF':
    put(tcs, f'{col}6', f'=(Target_Rev/Rev_FY25)^(1/{col}5)-1', BLK, PCT, fill=SAND)
put(tcs, 'G6', 'FY29 needs ~15.5% a year from the FY25 actual; FY31 ~10%, the category’s pace.', wrap=True)
put(tcs, 'A7', 'From FY26E (model, active scenario)')
for col in 'BCDEF':
    put(tcs, f'{col}7', f'=(Target_Rev/Rev_Bridge!$D$16)^(1/({col}5-1))-1', BLK, PCT)
put(tcs, 'A8', 'From FY24A (₹344 Cr), for reference')
for col in 'BCDEF':
    put(tcs, f'{col}8', f'=(Target_Rev/Rev_FY24)^(1/({col}5+1))-1', BLK, PCT)

header(tcs, 10, ['Test 2 · Track record and guidance', 'Value', '', '', '', '', 'Source'])
t2 = [
    ('Kishlay growth FY21 → FY24, a year', '=(Historicals!K5/Historicals!H5)^(1/3)-1', PCT, 'Motilal Oswal series [S07]'),
    ('Kishlay growth FY24', '=Historicals!K5/Historicals!J5-1', PCT, 'Motilal Oswal series [S07]'),
    ('Kishlay growth FY25 (actual)', '=Rev_FY25/Historicals!K5-1', PCT, 'Tracxn, MCA filing [S52]'),
    ('Category growth, low (namkeen / savoury snacks)', 0.08, PCT, 'Ken Research, Market Report Analytics [S47]'),
    ('Category growth, high', 0.12, PCT, 'Technavio, Mordor [S47]'),
    ('Management’s own medium-term guidance, low (₹ Cr)', '=Historicals!B19', CR, 'CRISIL Feb 2024 [S02]'),
    ('Management’s own medium-term guidance, high (₹ Cr)', '=Historicals!B20', CR, 'CRISIL Feb 2024 [S02]'),
    ('₹512 Cr vs guidance high', '=Target_Rev/B17-1', PCT, 'Calculation'),
    ('₹512 Cr vs guidance low', '=Target_Rev/B16-1', PCT, 'Calculation'),
]
for i, (lab, v, fmt, src) in enumerate(t2):
    row = 11 + i
    put(tcs, f'A{row}', lab)
    put(tcs, f'B{row}', v, BLUE if isinstance(v, (int, float)) else (GRN if 'Historicals' in str(v) else BLK), fmt)
    put(tcs, f'G{row}', src)

header(tcs, 21, ['Test 3 · Capacity: tonnes ₹512 Cr needs', '₹150/kg', '₹185/kg', '₹220/kg', '₹250/kg', '', 'Reading'])
put(tcs, 'A22', 'Realisation per kg (₹)')
for col, v in zip('BCDE', (150, 185, 220, 250)):
    put(tcs, f'{col}22', v, BLUE, INT)
put(tcs, 'A23', 'Tonnes a year at ₹512 Cr')
for col in 'BCDE':
    put(tcs, f'{col}23', f'=Target_Rev*10^7/{col}22/1000', BLK, INT)
put(tcs, 'A24', 'Tonnes a month')
for col in 'BCDE':
    put(tcs, f'{col}24', f'={col}23/12', BLK, INT)
put(tcs, 'A25', 'Share of installed capacity (own + 3P, 2,600 t a month)', bold=True)
for col in 'BCDE':
    put(tcs, f'{col}25', f'={col}24/Partners_MA!$C$15', BLK, PCT, fill=SAND)
put(tcs, 'A26', 'FY25 output at the same ₹/kg, share of capacity')
for col in 'BCDE':
    put(tcs, f'{col}26', f'=Rev_FY25*10^7/{col}22/1000/12/Partners_MA!$C$15', BLK, PCT)
put(tcs, 'G25', 'At ₹150–220/kg, ₹512 Cr fills 75–109% of capacity: it needs more ₹ per kilo (mix) or more 3P.', wrap=True)

header(tcs, 28, ['Test 4 · Market room', 'Low', 'High', '', '', '', 'Source'])
put(tcs, 'A29', 'Savoury snacks / namkeen market, 2025 (US$ bn)')
put(tcs, 'B29', 6.5, BLUE, CR)
put(tcs, 'C29', 6.8, BLUE, CR)
put(tcs, 'G29', 'Ken Research $6.5B; Market Report Analytics $6.78B [S47]')
put(tcs, 'A30', 'Market in ₹ Cr')
put(tcs, 'B30', '=B29*FX_USD*100', BLK, INT)
put(tcs, 'C30', '=C29*FX_USD*100', BLK, INT)
put(tcs, 'A31', 'Kishlay share at FY25A (₹288 Cr)')
put(tcs, 'B31', '=Rev_FY25/C30', BLK, '0.00%')
put(tcs, 'C31', '=Rev_FY25/B30', BLK, '0.00%')
put(tcs, 'A32', 'Kishlay share at ₹512 Cr (today’s market size)')
put(tcs, 'B32', '=Target_Rev/C30', BLK, '0.00%')
put(tcs, 'C32', '=Target_Rev/B30', BLK, '0.00%')
put(tcs, 'G32', 'Under 1% of the market even at ₹512 Cr: demand is not the constraint.', wrap=True)

header(tcs, 34, ['Test 5 · Profit', 'Value', '', '', '', '', 'Reading'])
put(tcs, 'A35', 'EBITDA at ₹512 Cr × 10% (₹ Cr)')
put(tcs, 'B35', '=Target_Rev*Target_EBITDA', BLK, CR)
put(tcs, 'A36', 'Estimated EBITDA, FY26E (₹ Cr)')
put(tcs, 'B36', '=EBITDA_Bridge!B18', GRN, CR)
put(tcs, 'A37', 'Multiple of FY26E EBITDA')
put(tcs, 'B37', '=B35/B36', BLK, MULT)
put(tcs, 'A38', 'Peer at that size: Annapurna Swadisht FY26 revenue (₹ Cr) · EBITDA %')
put(tcs, 'B38', '=Peers!C13', GRN, CR)
put(tcs, 'C38', '=Peers!E13', GRN, PCT)

# live scenario columns: every engine recomputed from the Bear / Base / Bull input columns
header(tcs, 40, ['Scenarios, FY29 (live: recomputed from each Inputs column)', 'Bear', 'Base', 'Bull', '', '', 'Reading'])
def v(nid, ic):
    return f'Inputs!${ic}${INPUT_ROW[nid]}'
lines = [
    (41, 'FY26E revenue', lambda X, ic: f'=Rev_FY25*(1+{v("g_FY26", ic)})'),
    (42, 'General trade core', lambda X, ic: f'={X}41*(1-{v("Share_copack", ic)}-{v("Share_export", ic)}-{v("Share_MT", ic)})*(1+{v("GT_CAGR", ic)})^3'),
    (43, 'Quick commerce', lambda X, ic: f'={v("QC_stores", ic)}*{v("QC_SKUs", ic)}*{v("QC_units", ic)}*{v("QC_net", ic)}*365/10^7'),
    (44, 'Modern trade + e-commerce', lambda X, ic: f'={v("MT_stores", ic)}*{v("MT_sales", ic)}*12/10^7+{v("Ecom_FY29", ic)}'),
    (45, 'Exports: Bhutan', lambda X, ic: f'={X}41*{v("Share_export", ic)}*(1+{v("Bhutan_g", ic)})^3'),
    (46, 'Exports: Nepal', lambda X, ic: f'={v("Nepal_trucks", ic)}*{v("Nepal_value", ic)}*12/100'),
    (47, 'Exports: GCC', lambda X, ic: f'={v("GCC_cont", ic)}*{v("GCC_value", ic)}*12/100'),
    (48, 'Co-packing and 3P', lambda X, ic: f'={X}41*{v("Share_copack", ic)}+{v("Copack_incr", ic)}'),
    (49, 'Bolt-on M&A', lambda X, ic: f'={v("MA_rev", ic)}*(1+{v("MA_g", ic)})'),
    (50, 'Total FY29 revenue (₹ Cr)', lambda X, ic: f'=SUM({X}42:{X}49)'),
    (51, 'Organic FY29 revenue (excl. M&A)', lambda X, ic: f'={X}50-{X}49'),
    (52, 'Gap to ₹512 Cr (+ above, − short)', lambda X, ic: f'={X}50-Target_Rev'),
    (53, 'EBITDA margin FY29', lambda X, ic: f'={v("EBITDA_base", ic)}+({v("L_mix", ic)}+{v("L_sku", ic)}+{v("L_proc", ic)}+{v("L_util", ic)}+{v("L_trade", ic)}+{v("L_freight", ic)}+{v("L_qcfees", ic)}+{v("L_invest", ic)}+{v("L_ma", ic)})*{v("R29", ic)}/10000'),
    (54, 'EBITDA FY29 (₹ Cr)', lambda X, ic: f'={X}50*{X}53'),
    (56, 'Years after FY29 to reach ₹512 Cr at the growth rate in B55', lambda X, ic: f'=IF({X}50>=Target_Rev,0,LN(Target_Rev/{X}50)/LN(1+$B$55))'),
    (57, 'Year ₹512 Cr is reached', lambda X, ic: f'="FY"&(29+ROUNDUP({X}56,0))'),
]
for row, lab, f in lines:
    put(tcs, f'A{row}', lab, bold=row in (50, 54, 57))
    for X, ic in zip('BCD', 'CDE'):
        fmt = PCT if row == 53 else ('0.0' if row == 56 else (None if row == 57 else CR))
        put(tcs, f'{X}{row}', f(X, ic), BLK, fmt, SAND if row in (50, 54) else None)
put(tcs, 'A55', 'Growth a year after FY29 (category mid-point)')
put(tcs, 'B55', 0.10, BLUE, PCT, YEL)
put(tcs, 'A58', 'Check: active scenario column ties to Rev_Bridge and EBITDA_Bridge')
put(tcs, 'B58', '=IF(AND(ABS(INDEX(B50:D50,1,Scenario)-Rev_Bridge!G16)<0.01,ABS(INDEX(B53:D53,1,Scenario)-EBITDA_Bridge!E17)<0.00001),"OK","CHECK")', BLK)
put(tcs, 'G50', 'Base misses ₹512 Cr in FY29 after FY25’s fall; bull clears it.', wrap=True)

header(tcs, 60, ['What closes the FY29 gap (active scenario)', 'Value', '', '', '', '', 'Reading'])
put(tcs, 'A61', 'Shortfall to ₹512 Cr in FY29 (₹ Cr)')
put(tcs, 'B61', '=MAX(0,Target_Rev-Rev_Bridge!G16)', BLK, CR, SAND)
put(tcs, 'A62', 'Option 1 · general-trade growth a year needed (vs GT_CAGR)')
put(tcs, 'B62', '=((Rev_Bridge!G8+B61)/Rev_Bridge!D8)^(1/3)-1', BLK, PCT)
put(tcs, 'C62', '=GT_CAGR', GRN, PCT)
put(tcs, 'G62', 'Doubling GT growth after a −16% year is not a plan.', wrap=True)
put(tcs, 'A63', 'Option 2 · acquired revenue needed at purchase (₹ Cr)')
put(tcs, 'B63', '=(Rev_Bridge!G15+B61)/(1+MA_g)', BLK, CR)
put(tcs, 'A64', '… price at the base EV/sales multiple (₹ Cr)')
put(tcs, 'B64', '=B63*MA_EVS', BLK, CR)
put(tcs, 'G64', 'Too big for a balance sheet with bank limits near 93%.', wrap=True)
put(tcs, 'A65', 'Option 3 · extra dark stores at base rate of sale')
put(tcs, 'B65', '=B61/(QC_SKUs*QC_units*QC_net*365/10^7)', BLK, INT)
put(tcs, 'A66', 'Option 4 · one more year: FY30 revenue at B55 growth (₹ Cr)')
put(tcs, 'B66', '=Rev_Bridge!G16*(1+B55)', BLK, CR)

header(tcs, 68, ['Value lens: why steer by EBITDA', 'Value', '', '', '', '', 'Source'])
put(tcs, 'A69', 'Listed-peer median EV/EBITDA (x)')
put(tcs, 'B69', f'=Historicals!B{HI_EVE}', GRN, MULT)
put(tcs, 'G69', 'Tracxn [S52]')
put(tcs, 'A70', 'Listed-peer median EV/Revenue (x)')
put(tcs, 'B70', f'=Historicals!B{HI_EVR}', GRN, MULT)
put(tcs, 'G70', 'Tracxn [S52]')
put(tcs, 'A71', 'Indicative value at FY26E EBITDA (₹ Cr)')
put(tcs, 'B71', '=EBITDA_Bridge!B18*B69', BLK, CR)
put(tcs, 'A72', 'Indicative value at FY29 EBITDA, active scenario (₹ Cr)')
put(tcs, 'B72', '=EBITDA_Bridge!E18*B69', BLK, CR)
put(tcs, 'A73', 'Value added FY26E → FY29 (₹ Cr)')
put(tcs, 'B73', '=B72-B71', BLK, CR, SAND)
put(tcs, 'G73', 'Each ₹1 Cr of EBITDA ≈ ₹9 Cr of value; ₹1 Cr of revenue ≈ ₹1 Cr. Indicative only.', wrap=True)

header(tcs, 75, ['Ways to set the target', 'FY29 revenue (₹ Cr)', 'EBITDA %', 'EBITDA (₹ Cr)', '', '', 'When to use it'])
alts = [
    ('A · FY29 organic only (no acquisition)', '=Rev_Bridge!G18', '=EBITDA_Bridge!E17-L_ma*R29/10000', 'If no bolt-on clears the screen'),
    ('B · FY29 base with one bolt-on (recommended commitment)', '=Rev_Bridge!G16', '=EBITDA_Bridge!E17', 'Budget and board commitment'),
    ('C · FY29 bull case (₹512 Cr as the stretch)', '=D50', '=D53', 'Upside if every engine and the bolt-on land'),
    ('D · ₹512 Cr dated to the base-case year (see C57)', '=Target_Rev', '=Target_EBITDA', 'Keep the number, move the date'),
    ('E · Profit-first: ₹50 Cr EBITDA at 11%', '=50/0.11', 0.11, 'If the board prefers profit to scale'),
]
for i, (lab, rev, m, use) in enumerate(alts):
    row = 76 + i
    put(tcs, f'A{row}', lab)
    put(tcs, f'B{row}', rev, GRN if ('!' in str(rev) or 'Target' in str(rev)) else BLK, CR)
    put(tcs, f'C{row}', m, BLUE if isinstance(m, float) else GRN, PCT)
    put(tcs, f'D{row}', f'=B{row}*C{row}', BLK, CR)
    put(tcs, f'G{row}', use, wrap=True)
put(tcs, 'A82', 'Verdict (updates with the model)', bold=True)
put(tcs, 'B82', '="FY25 actual ₹"&TEXT(Rev_FY25,"0")&" Cr ("&TEXT(B13,"0%")&") resets the path. Base reaches ₹"&TEXT(C50,"0")&" Cr in FY29 at "&TEXT(C53,"0.0%")&" EBITDA (₹"&TEXT(C54,"0")&" Cr); ₹512 Cr arrives in "&C57&". Bull reaches ₹"&TEXT(D50,"0")&" Cr. Commit to ~₹"&TEXT(ROUND(C50/10,0)*10,"0")&" Cr and ~₹"&TEXT(ROUND(C54,0),"0")&" Cr EBITDA for FY29; keep ₹512 Cr as the stretch; FY27 is not credible."', BLK, wrap=True)
tcs.merge_cells('B82:G82')
tcs.row_dimensions[82].height = 80

# ---------------------------------------------------------------- Summary (first sheet)
sm = wb['Sheet']
sm.title = 'Summary'
sm.sheet_view.showGridLines = False
for i, w in enumerate([46, 14, 14, 14, 14, 50], 1):
    sm.column_dimensions[get_column_letter(i)].width = w
sm['A1'] = 'Kishlay Group: path to ₹512 Cr at ~10% EBITDA'
sm['A1'].font = TITLE
sm['A2'] = 'Kishlay Foods Pvt Ltd (brands) + Tulsi Speciality Foods Pvt Ltd (manufacturing). Prepared by Chethan N. Model for discussion; every input is labelled and sourced.'
sm['A2'].font = SUB
put(sm, 'A4', 'Active scenario', bold=True)
put(sm, 'B4', '=Inputs!C3', GRN)
put(sm, 'C4', '← change in Inputs!B3 (1 Bear, 2 Base, 3 Bull)')
header(sm, 6, ['Output', 'FY25A', 'FY26E', 'FY29P', 'Target', 'Reading'])
put(sm, 'A7', 'Revenue (₹ Cr)')
put(sm, 'B7', '=Rev_Bridge!C16', GRN, CR)
put(sm, 'C7', '=Rev_Bridge!D16', GRN, CR)
put(sm, 'D7', '=Rev_Bridge!G16', GRN, CR, fill=SAND)
put(sm, 'E7', '=Target_Rev', GRN, CR)
put(sm, 'F7', '=IF(D7>=E7,"Target met","Short by ₹"&TEXT(E7-D7,"0.0")&" Cr")', BLK)
put(sm, 'A8', 'EBITDA margin')
put(sm, 'C8', '=EBITDA_Bridge!B17', GRN, PCT)
put(sm, 'D8', '=EBITDA_Bridge!E17', GRN, PCT, fill=SAND)
put(sm, 'E8', '=Target_EBITDA', GRN, PCT)
put(sm, 'F8', '=IF(D8>=E8-0.0005,"Target met","Short by "&TEXT((E8-D8)*10000,"0")&" bps")', BLK)
put(sm, 'A9', 'EBITDA (₹ Cr)')
put(sm, 'C9', '=EBITDA_Bridge!B18', GRN, CR)
put(sm, 'D9', '=EBITDA_Bridge!E18', GRN, CR, fill=SAND)
put(sm, 'E9', '=E7*E8', BLK, CR)
put(sm, 'A10', 'Revenue CAGR FY26E → FY29P')
put(sm, 'D10', '=Rev_Bridge!G23', GRN, PCT)
put(sm, 'A11', 'Share of FY29 revenue from new engines')
put(sm, 'D11', '=Rev_Bridge!G38', GRN, PCT)
put(sm, 'A12', 'Organic FY29 revenue (excludes M&A)')
put(sm, 'D12', '=Rev_Bridge!G18', GRN, CR)
put(sm, 'A13', '90-day pilot budget (₹ lakh, cost + recoverable stock)')
put(sm, 'D13', f'=Pilots!E{PL_TOTAL}', GRN, CR)
header(sm, 15, ['FY29 revenue by engine (₹ Cr)', 'FY26E', 'FY29P', 'Increase', 'Share of increase', ''])
for i in range(8):
    row = 16 + i
    put(sm, f'A{row}', f'=Rev_Bridge!A{28+i}', GRN)
    put(sm, f'B{row}', f'=Rev_Bridge!B{28+i}', GRN, CR)
    put(sm, f'C{row}', f'=Rev_Bridge!C{28+i}', GRN, CR)
    put(sm, f'D{row}', f'=Rev_Bridge!D{28+i}', GRN, CR)
    put(sm, f'E{row}', f'=Rev_Bridge!E{28+i}', GRN, PCT)
header(sm, 25, ['Contribution per kg by channel (₹)', 'Per kg', 'Index vs GT', '', '', ''])
for i, (lab, col) in enumerate([('GT ₹10 pack', 'B'), ('MT 400 g bhujia', 'C'), ('QC 400 g bhujia', 'D'), ('UAE 200 g namkeen', 'E'), ('Nepal 200 g (export over duty)', 'F'), ('Nepal via local 3P (royalty)', 'G')]):
    row = 26 + i
    put(sm, f'A{row}', lab)
    put(sm, f'B{row}', f'=Unit_Econ!{col}29', GRN, '₹#,##0;(₹#,##0);"-"')
    put(sm, f'C{row}', f'=Unit_Econ!{col}30', GRN, MULT)
header(sm, 33, ['Integrity checks', 'Result', '', '', '', ''])
put(sm, 'A34', 'FY26 engines tie to top-down revenue')
put(sm, 'B34', '=IF(Rev_Bridge!D17=0,"OK","CHECK")', BLK)
put(sm, 'A35', 'Tulsi FY25 balance sheet balances')
put(sm, 'B35', f'=IF(Historicals!B{HI_TCHECK-1}=0,"OK","CHECK")', BLK)
put(sm, 'A36', 'Tulsi FY25 cash flows tie to closing cash')
put(sm, 'B36', f'=IF(Historicals!B{HI_TCHECK}=0,"OK","CHECK")', BLK)
put(sm, 'A37', 'Required growth FY26E → FY29 for ₹512 Cr (Target_Check)')
put(sm, 'B37', '=Target_Check!D7', GRN, PCT)
put(sm, 'A38', 'Scenario columns tie to the bridges (Target_Check)')
put(sm, 'B38', '=Target_Check!B58', GRN)
header(sm, 40, ['Scenarios (live)', 'Bear', 'Base', 'Bull', '', ''])
put(sm, 'A41', 'FY29 revenue (₹ Cr)')
put(sm, 'A42', 'FY29 EBITDA margin')
put(sm, 'A43', 'FY29 EBITDA (₹ Cr)')
put(sm, 'A44', 'Year ₹512 Cr is reached (10% a year after FY29)')
for X in 'BCD':
    put(sm, f'{X}41', f'=Target_Check!{X}50', GRN, CR)
    put(sm, f'{X}42', f'=Target_Check!{X}53', GRN, PCT)
    put(sm, f'{X}43', f'=Target_Check!{X}54', GRN, CR)
    put(sm, f'{X}44', f'=Target_Check!{X}57', GRN)
put(sm, 'A46', 'Colour code', bold=True)
put(sm, 'A47', 'Blue text = input (hardcoded)', BLUE)
put(sm, 'A48', 'Black text = formula')
put(sm, 'A49', 'Green text = link to another sheet', GRN)
put(sm, 'A50', 'Yellow fill = key assumption or a cell to fill in', fill=YEL)
put(sm, 'A52', 'Data labels', bold=True)
put(sm, 'A53', 'Company = reported by Kishlay · External = third party (CRISIL, Tracxn, news) · Historical = past period · Calculation = derived here · Hypothesis = to test')
sm.merge_cells('A53:F53')

# README
rd = sheet('README', 'How to use this workbook', 'Read me first.', [110])
lines = [
    '1. Summary — headline outputs and integrity checks. Change the scenario in Inputs!B3.',
    '1b. Target_Check — is ₹512 Cr credible after FY25’s −16%? Five tests, live Bear/Base/Bull columns, what closes the gap, a value lens and ways to set the target.',
    '1c. MT_Plan — modern trade: target chains, terms, door economics, rollout to 400 doors, pilot gates.',
    '2. Inputs — every assumption with Bear / Base / Bull values, label and source ID. Yellow = validate first.',
    '3. Historicals — CRISIL and Motilal Oswal history, rating history, bank facilities, Tulsi Pvt Ltd FY25 first filing (with checks).',
    '4. Peers — Bikaji, Gopal, Prataap, Annapurna: is ~10% EBITDA realistic?',
    '5. Rev_Bridge — FY24A → FY29P revenue by engine; gap to ₹512 Cr.',
    '6. EBITDA_Bridge — starting margin plus levers to ~10%.',
    '7. Unit_Econ — what each channel leaves per pack and per kg (GT, MT, QC, UAE, Nepal export, Nepal 3P).',
    '8. Export_Calc — what Haldiram’s UAE and Nepal shelf prices imply at the factory gate.',
    '9. Export_Buyers — real GCC, Nepal and Bhutan buyers with sources; track outreach status.',
    '10. Partners_MA — 3P partners, capacity, utilisation, M&A precedents and screen.',
    '11. Price_Audit — Kishlay vs competitor prices; yellow cells to capture live from the apps.',
    '12. Pilots — 90-day pilot budgets, KPI gates and stop rules.',
    '13. Roadmap_RAG — 26 tasks across 5 workstreams; twice-weekly RAG status and summary.',
    '14. Board_MIS — monthly MIS / board / lender pack template.',
    '15. Assumptions — what is assumed, why, how to validate, sensitivity.',
    '16. Sources — every source with link and date.',
    '',
    'Entity note: CRISIL rates the consolidated Kishlay Group (Kishlay Foods Pvt Ltd + Tulsi Speciality Foods). Tulsi Speciality Foods Pvt Ltd was incorporated on 7 Oct 2024; its first filing (FY25) shows ₹5 Cr equity and no operations, so group revenue and losses must not be attributed to the new company alone.',
    'No internal company data was used. Every number is public (labelled External / Company), a calculation, or a hypothesis to test in the first 90 days.',
]
for i, l in enumerate(lines):
    c = rd.cell(row=4 + i, column=1, value=l)
    c.font = BLK
    c.alignment = WRAP

order = ['Summary', 'README', 'Target_Check', 'Inputs', 'Historicals', 'Peers', 'Rev_Bridge', 'EBITDA_Bridge', 'Unit_Econ', 'MT_Plan', 'Export_Calc', 'Export_Buyers', 'Partners_MA', 'Price_Audit', 'Pilots', 'Roadmap_RAG', 'Board_MIS', 'Assumptions', 'Sources']
wb._sheets = [wb[n] for n in order]
for ws in wb.worksheets:
    ws.sheet_properties.tabColor = 'C8141C' if ws.title in ('Summary', 'Target_Check', 'Inputs', 'Rev_Bridge', 'EBITDA_Bridge') else 'F2B21B'
wb.save(OUT)
print('saved', OUT)
