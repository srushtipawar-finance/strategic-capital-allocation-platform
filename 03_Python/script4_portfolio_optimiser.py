import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

# ================================================================
# Script 4: TRUE Brute-Force Portfolio Optimiser
#
# GREEDY METHOD (what naive analysts do):
#   Sort investments by NPV. Keep adding until budget runs out.
#   PROBLEM: This is often WRONG. A large high-NPV project can
#   crowd out several smaller projects whose combined NPV is higher.
#
# BRUTE-FORCE METHOD (what this script does):
#   Test EVERY possible combination (255 total for 8 investments).
#   Calculate total cost and total NPV for each.
#   Find the combination within $5M with the HIGHEST total NPV.
#   This is GUARANTEED to find the true mathematical optimum.
# ================================================================

BUDGET = 5_000_000

# Use your actual NPV values from Script 1 output
investments = [
    {'name': 'New Store Expansion',   'cost': 1_200_000, 'npv': 134_820, 'irr': 18.2, 'risk': 7.74},
    {'name': 'E-Commerce Platform',   'cost':   800_000, 'npv': 122_440, 'irr': 20.8, 'risk': 5.28},
    {'name': 'New Product Line',      'cost':   600_000, 'npv':  95_310, 'irr': 19.4, 'risk': 4.57},
    {'name': 'Geographic Expansion',  'cost': 1_000_000, 'npv': 141_260, 'irr': 17.1, 'risk': 7.68},
    {'name': 'Warehouse Automation',  'cost':   700_000, 'npv':  93_640, 'irr': 17.6, 'risk': 4.30},
    {'name': 'Customer Loyalty Prog', 'cost':   400_000, 'npv':  88_950, 'irr': 22.1, 'risk': 2.72},
    {'name': 'Mobile App Investment', 'cost':   500_000, 'npv':  82_780, 'irr': 19.9, 'risk': 4.13},
    {'name': 'Strategic Acquisition', 'cost': 1_500_000, 'npv': 197_350, 'irr': 16.8, 'risk': 10.0},
]

n = len(investments)

# ----------------------------------------------------------------
# STEP 1: Brute-force search — test all 255 combinations
# ----------------------------------------------------------------
best_npv   = -np.inf
best_combo = None
all_valid  = []

for r in range(1, n + 1):
    for combo in combinations(investments, r):
        total_cost = sum(inv['cost'] for inv in combo)
        total_npv  = sum(inv['npv']  for inv in combo)
        avg_irr    = np.mean([inv['irr']  for inv in combo])
        avg_risk   = np.mean([inv['risk'] for inv in combo])

        if total_cost <= BUDGET:
            all_valid.append({
                'Num_Projects':    len(combo),
                'Project_Names':   ' | '.join(inv['name'] for inv in combo),
                'Total_Cost':      total_cost,
                'Total_NPV':       total_npv,
                'Avg_IRR_Pct':     round(avg_irr, 2),
                'Avg_Risk_Score':  round(avg_risk, 2),
                'Budget_Util_Pct': round(total_cost / BUDGET * 100, 1),
            })
            if total_npv > best_npv:
                best_npv   = total_npv
                best_combo = combo

total_combos = 2**n - 1
total_valid  = len(all_valid)
opt_cost     = sum(inv['cost'] for inv in best_combo)
opt_irr      = np.mean([inv['irr']  for inv in best_combo])
opt_risk     = np.mean([inv['risk'] for inv in best_combo])

# ----------------------------------------------------------------
# STEP 2: Greedy comparison
# ----------------------------------------------------------------
sorted_by_npv = sorted(investments, key=lambda x: x['npv'], reverse=True)
greedy_combo, greedy_cost = [], 0
for inv in sorted_by_npv:
    if greedy_cost + inv['cost'] <= BUDGET:
        greedy_combo.append(inv)
        greedy_cost += inv['cost']
greedy_npv = sum(inv['npv'] for inv in greedy_combo)
npv_gain   = best_npv - greedy_npv

# ----------------------------------------------------------------
# STEP 3: Print results
# ----------------------------------------------------------------
print("=" * 68)
print("RETAILCO — PORTFOLIO OPTIMISATION RESULTS")
print(f"Method: Brute-Force | {total_combos} combinations tested | {total_valid} within budget")
print("=" * 68)

print("\nOPTIMAL PORTFOLIO (Brute-Force):")
print("-" * 68)
for inv in sorted(best_combo, key=lambda x: x['npv'], reverse=True):
    print(f"  INCLUDE: {inv['name']:<26} Cost: ${inv['cost']:>9,.0f}  NPV: ${inv['npv']:>8,.0f}")
print("-" * 68)
print(f"  TOTAL                             Cost: ${opt_cost:>9,.0f}  NPV: ${best_npv:>8,.0f}")
print(f"\n  Budget Remaining:  ${BUDGET - opt_cost:,.0f}")
print(f"  Budget Utilisation: {opt_cost/BUDGET*100:.1f}%")
print(f"  Average IRR:        {opt_irr:.1f}%")
print(f"  Average Risk Score: {opt_risk:.2f} / 10")

included_names = {inv['name'] for inv in best_combo}
excluded = [inv for inv in investments if inv['name'] not in included_names]
if excluded:
    print("\nEXCLUDED FROM OPTIMAL PORTFOLIO:")
    for inv in excluded:
        print(f"  EXCLUDE: {inv['name']:<26} Cost: ${inv['cost']:>9,.0f}  NPV: ${inv['npv']:>8,.0f}")
    print("  Reason: Including excluded investments would reduce total NPV")
    print("  or push total cost above the $5,000,000 budget constraint.")

print(f"\nGREEDY vs BRUTE-FORCE COMPARISON:")
print(f"  Greedy Selection NPV:  ${greedy_npv:>10,.0f}")
print(f"  Brute-Force NPV:       ${best_npv:>10,.0f}")
print(f"  Improvement:           ${npv_gain:>10,.0f}  ({npv_gain/greedy_npv*100:+.1f}%)")

# Save results
df_all = pd.DataFrame(all_valid).sort_values('Total_NPV', ascending=False)
df_all.head(20).to_csv('outputs/optimal_portfolio.csv', index=False)
print(f"\nTop 20 portfolios saved: outputs/optimal_portfolio.csv")

# ----------------------------------------------------------------
# STEP 4: Charts
# ----------------------------------------------------------------
colors_opt = ['#1D4ED8','#16A34A','#B45309','#7C3AED','#0891B2','#DC2626','#059669']
opt_names  = [inv['name'] for inv in best_combo]
opt_costs  = [inv['cost'] for inv in best_combo]
opt_npvs   = [inv['npv']  for inv in best_combo]

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle(f'Optimal Portfolio — Total NPV: ${best_npv:,.0f} | '
             f'Budget Used: {opt_cost/BUDGET*100:.1f}%',
             fontsize=13, fontweight='bold')

# Budget pie
axes[0].pie(opt_costs, labels=[n.replace(' ', '\n') for n in opt_names],
            colors=colors_opt[:len(opt_names)], autopct='%1.1f%%', startangle=90)
axes[0].set_title('Budget Allocation\nOptimal Portfolio', fontweight='bold')

# NPV contribution
bars_npv = axes[1].barh([n.replace(' ', '\n') for n in opt_names],
                          opt_npvs, color=colors_opt[:len(opt_names)])
axes[1].set_xlabel('NPV ($)')
axes[1].set_title('NPV Contribution\nby Project', fontweight='bold')
axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars_npv, opt_npvs):
    axes[1].text(val + 100, bar.get_y()+bar.get_height()/2,
                 f'${val:,.0f}', va='center', fontsize=8)

# Greedy vs Optimal
cats  = ['Greedy\nSelection', 'Brute-Force\nOptimal']
vals  = [greedy_npv, best_npv]
bcs   = ['#E24B4A', '#16A34A']
bars3 = axes[2].bar(cats, vals, color=bcs, width=0.5)
axes[2].set_ylabel('Total Portfolio NPV ($)')
axes[2].set_title('Greedy vs True Optimal\nNPV Comparison', fontweight='bold')
axes[2].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars3, vals):
    axes[2].text(bar.get_x()+bar.get_width()/2, val + 200,
                 f'${val:,.0f}', ha='center', fontsize=11, fontweight='bold')
axes[2].set_facecolor('#F8FAFC')

plt.tight_layout()
plt.savefig('outputs/optimal_portfolio_chart.png', dpi=150, bbox_inches='tight')
plt.show()
print("Charts saved: outputs/optimal_portfolio_chart.png")