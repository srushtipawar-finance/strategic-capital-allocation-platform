import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf

# ================================================================
# RETAILCO — STRATEGIC CAPITAL ALLOCATION PLATFORM
# Script 1: Core Financial Calculations + Advanced KPIs
# Covers: DCF, NPV, IRR, Payback, ROI, PI, NPV/$, Risk-Adj NPV
# ================================================================

WACC   = 0.10        # Minimum required return (hurdle rate)
BUDGET = 5_000_000   # Capital constraint

# ----------------------------------------------------------------
# Investment cashflows: [Year0, Year1, Year2, Year3, Year4, Year5]
# Year0 is NEGATIVE (money going OUT). Years 1-5 are POSITIVE.
# ----------------------------------------------------------------
investments = {
    'New Store Expansion':    [-1_200_000, 180_000, 250_000, 320_000, 380_000, 420_000],
    'E-Commerce Platform':    [  -800_000, 160_000, 200_000, 240_000, 280_000, 310_000],
    'New Product Line':       [  -600_000, 110_000, 150_000, 190_000, 220_000, 250_000],
    'Geographic Expansion':   [-1_000_000,  80_000, 160_000, 260_000, 360_000, 440_000],
    'Warehouse Automation':   [  -700_000, 150_000, 180_000, 210_000, 230_000, 250_000],
    'Customer Loyalty Prog':  [  -400_000,  90_000, 120_000, 150_000, 170_000, 190_000],
    'Mobile App Investment':  [  -500_000, 100_000, 140_000, 175_000, 200_000, 220_000],
    'Strategic Acquisition':  [-1_500_000, 120_000, 250_000, 400_000, 550_000, 700_000],
}

# Risk scores from Script 3 output (composite scores)
risk_scores = {
    'New Store Expansion':   7.74,
    'E-Commerce Platform':   5.28,
    'New Product Line':      4.57,
    'Geographic Expansion':  7.68,
    'Warehouse Automation':  4.30,
    'Customer Loyalty Prog': 2.72,
    'Mobile App Investment': 4.13,
    'Strategic Acquisition': 10.00,
}

# ----------------------------------------------------------------
# CALCULATION FUNCTIONS
# Each function takes cashflows and returns one metric
# ----------------------------------------------------------------

def calc_npv(cfs, rate=WACC):
    # npf.npv = Net Present Value
    # Discounts all cashflows (including Year 0) to today's value
    return round(npf.npv(rate, cfs), 2)

def calc_irr(cfs):
    # npf.irr = Internal Rate of Return
    # Finds the % return that makes NPV = 0
    try:
        return round(npf.irr(cfs) * 100, 2)
    except:
        return None

def calc_payback(cfs):
    # Finds the exact year + fraction when cumulative cashflow crosses 0
    cumulative = 0
    for yr, cf in enumerate(cfs):
        cumulative += cf
        if cumulative >= 0 and yr > 0:
            prev = cumulative - cf
            return round(yr - 1 + (-prev / cf), 2)
    return 99.0   # investment never pays back in 5 years

def calc_roi(cfs):
    # ROI = (Total inflows - Cost) / Cost * 100
    cost    = abs(cfs[0])
    inflows = sum(cfs[1:])
    return round((inflows - cost) / cost * 100, 1)

def calc_pi(cfs, rate=WACC):
    # Profitability Index = PV of future inflows / Initial cost
    # PV of inflows = NPV of cashflows with Year0 replaced by 0
    pv_inflows = npf.npv(rate, [0] + list(cfs[1:]))
    cost = abs(cfs[0])
    return round(pv_inflows / cost, 4)

def calc_npv_per_dollar(cfs, rate=WACC):
    # NPV per dollar invested = NPV / Cost
    # Shows capital efficiency — how much net value per dollar deployed
    return round(calc_npv(cfs, rate) / abs(cfs[0]), 4)

def calc_risk_adj_npv(npv, risk_score):
    # Risk-Adjusted NPV = NPV / Composite Risk Score
    # Higher score = better risk-adjusted return
    return round(npv / risk_score, 2)

# ----------------------------------------------------------------
# RUN CALCULATIONS FOR ALL 8 INVESTMENTS
# ----------------------------------------------------------------
results = []
print("=" * 80)
print("RETAILCO — STRATEGIC CAPITAL ALLOCATION ANALYSIS")
print(f"WACC: {WACC*100:.0f}% | Budget: ${BUDGET:,.0f} | 8 Investments")
print("=" * 80)
print(f"{'Investment':<26} {'NPV':>10} {'IRR':>7} {'Payback':>9} {'ROI':>7} {'PI':>7} {'NPV/$':>8} {'R-Adj':>10}")
print("-" * 80)

for name, cfs in investments.items():
    npv          = calc_npv(cfs)
    irr          = calc_irr(cfs)
    payback      = calc_payback(cfs)
    roi          = calc_roi(cfs)
    pi           = calc_pi(cfs)
    npv_per_dol  = calc_npv_per_dollar(cfs)
    risk_adj     = calc_risk_adj_npv(npv, risk_scores[name])
    decision     = "INVEST" if (npv > 0 and irr and irr > WACC * 100) else "REJECT"

    results.append({
        'Investment':      name,
        'Cost':            abs(cfs[0]),
        'NPV':             npv,
        'IRR':             irr,
        'Payback':         payback,
        'ROI':             roi,
        'PI':              pi,
        'NPV_per_Dollar':  npv_per_dol,
        'Risk_Score':      risk_scores[name],
        'Risk_Adj_NPV':    risk_adj,
        'Decision':        decision,
    })
    print(f"{name:<26} ${npv:>9,.0f} {irr:>6.1f}% {payback:>8.2f}y {roi:>6.1f}% "
          f"{pi:>7.3f} {npv_per_dol:>8.4f} ${risk_adj:>9,.0f}")

print("=" * 80)

df = pd.DataFrame(results)
df['NPV_Rank']     = df['NPV'].rank(ascending=False).astype(int)
df['PI_Rank']      = df['PI'].rank(ascending=False).astype(int)
df['RiskAdj_Rank'] = df['Risk_Adj_NPV'].rank(ascending=False).astype(int)
df_sorted = df.sort_values('NPV_Rank')

print("\nFINAL RANKED RESULTS:")
print(df_sorted[['NPV_Rank','Investment','NPV','IRR','PI','Risk_Adj_NPV','Decision']].to_string(index=False))

df_sorted.to_csv('outputs/investment_results.csv', index=False)
print("\nResults saved: outputs/investment_results.csv")

# ----------------------------------------------------------------
# CHART SET 1: NPV and IRR Comparison
# ----------------------------------------------------------------
colors = ['#1D4ED8','#16A34A','#B45309','#7C3AED','#0891B2','#DC2626','#059669','#D97706']
names_short = [n.replace(' ', '\n') for n in df_sorted['Investment']]

fig1, axes1 = plt.subplots(1, 2, figsize=(14, 6))
fig1.suptitle('RetailCo — DCF Analysis: NPV & IRR Comparison', fontsize=14, fontweight='bold')

ax = axes1[0]
bars = ax.bar(names_short, df_sorted['NPV'], color=colors)
ax.axhline(0, color='black', lw=1)
ax.set_title('Net Present Value (NPV)', fontweight='bold', fontsize=12)
ax.set_ylabel('NPV ($)')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars, df_sorted['NPV']):
    ax.text(bar.get_x() + bar.get_width()/2, val + 300,
            f'${val:,.0f}', ha='center', fontsize=7.5, fontweight='bold')
ax.set_facecolor('#F8FAFC')

ax2 = axes1[1]
bars2 = ax2.bar(names_short, df_sorted['IRR'], color=colors)
ax2.axhline(WACC * 100, color='red', lw=2, linestyle='--', label=f'WACC ({WACC*100:.0f}%)')
ax2.set_title('IRR vs WACC Hurdle Rate', fontweight='bold', fontsize=12)
ax2.set_ylabel('IRR (%)')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))
ax2.legend(fontsize=10)
for bar, val in zip(bars2, df_sorted['IRR']):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.1,
             f'{val}%', ha='center', fontsize=7.5, fontweight='bold')
ax2.set_facecolor('#F8FAFC')

plt.tight_layout()
plt.savefig('outputs/dcf_comparison_charts.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: outputs/dcf_comparison_charts.png")

# ----------------------------------------------------------------
# CHART SET 2: Advanced KPIs
# ----------------------------------------------------------------
df_pi  = df_sorted.sort_values('PI', ascending=False)
df_npd = df_sorted.sort_values('NPV_per_Dollar', ascending=False)
df_rad = df_sorted.sort_values('Risk_Adj_NPV', ascending=False)

fig2, axes2 = plt.subplots(1, 3, figsize=(17, 6))
fig2.suptitle('RetailCo — Advanced Capital Allocation KPIs', fontsize=14, fontweight='bold')

ax3 = axes2[0]
bars3 = ax3.bar([n.replace(' ', '\n') for n in df_pi['Investment']], df_pi['PI'], color=colors)
ax3.axhline(1.0, color='red', lw=2, linestyle='--', label='PI = 1.0 (break-even)')
ax3.set_title('Profitability Index\n(PV of Inflows / Cost)', fontweight='bold')
ax3.set_ylabel('PI'); ax3.legend(fontsize=9); ax3.set_facecolor('#F8FAFC')
for bar, val in zip(bars3, df_pi['PI']):
    ax3.text(bar.get_x()+bar.get_width()/2, val+0.002, f'{val:.3f}', ha='center', fontsize=8)

ax4 = axes2[1]
bars4 = ax4.bar([n.replace(' ', '\n') for n in df_npd['Investment']], df_npd['NPV_per_Dollar'], color=colors)
ax4.set_title('NPV per $1 Invested\n(NPV / Cost)', fontweight='bold')
ax4.set_ylabel('$ NPV per $ Cost'); ax4.set_facecolor('#F8FAFC')
for bar, val in zip(bars4, df_npd['NPV_per_Dollar']):
    ax4.text(bar.get_x()+bar.get_width()/2, val+0.001, f'${val:.3f}', ha='center', fontsize=8)

ax5 = axes2[2]
bars5 = ax5.bar([n.replace(' ', '\n') for n in df_rad['Investment']], df_rad['Risk_Adj_NPV'], color=colors)
ax5.set_title('Risk-Adjusted NPV\n(NPV / Risk Score)', fontweight='bold')
ax5.set_ylabel('Risk-Adjusted NPV ($)')
ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax5.set_facecolor('#F8FAFC')
for bar, val in zip(bars5, df_rad['Risk_Adj_NPV']):
    ax5.text(bar.get_x()+bar.get_width()/2, val+50, f'${val:,.0f}', ha='center', fontsize=8)

plt.tight_layout()
plt.savefig('outputs/advanced_kpi_charts.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: outputs/advanced_kpi_charts.png")