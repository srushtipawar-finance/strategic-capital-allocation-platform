import numpy as np
import numpy_financial as npf
import pandas as pd
import matplotlib.pyplot as plt

# ================================================================
# Script 2: Monte Carlo Simulation — All 8 Investments
# 5,000 simulations per investment = 40,000 total
# Each simulation randomly varies cashflows based on each
# investment's specific volatility profile
# ================================================================

np.random.seed(42)     # ensures results are reproducible
NUM_SIMS = 5000        # 5,000 simulations per investment
WACC     = 0.10

BASE_CASHFLOWS = {
    'New Store Expansion':    [-1_200_000, 180_000, 250_000, 320_000, 380_000, 420_000],
    'E-Commerce Platform':    [  -800_000, 160_000, 200_000, 240_000, 280_000, 310_000],
    'New Product Line':       [  -600_000, 110_000, 150_000, 190_000, 220_000, 250_000],
    'Geographic Expansion':   [-1_000_000,  80_000, 160_000, 260_000, 360_000, 440_000],
    'Warehouse Automation':   [  -700_000, 150_000, 180_000, 210_000, 230_000, 250_000],
    'Customer Loyalty Prog':  [  -400_000,  90_000, 120_000, 150_000, 170_000, 190_000],
    'Mobile App Investment':  [  -500_000, 100_000, 140_000, 175_000, 200_000, 220_000],
    'Strategic Acquisition':  [-1_500_000, 120_000, 250_000, 400_000, 550_000, 700_000],
}

# Each investment has its own volatility based on real risk profile
# Low risk investments have narrow distributions (±10%)
# High risk investments have wide distributions (±30%)
VOLATILITY = {
    'New Store Expansion':    0.22,
    'E-Commerce Platform':    0.18,
    'New Product Line':       0.15,
    'Geographic Expansion':   0.25,
    'Warehouse Automation':   0.12,
    'Customer Loyalty Prog':  0.10,
    'Mobile App Investment':  0.18,
    'Strategic Acquisition':  0.30,
}

summary  = []
all_npvs = {}

print(f"Running {NUM_SIMS:,} simulations per investment ({NUM_SIMS*8:,} total)")
print("=" * 78)
print(f"{'Investment':<26} {'Mean NPV':>11} {'Median NPV':>11} {'Std Dev':>10} {'P(+NPV)':>9} {'5th Pct':>11}")
print("-" * 78)

for name, cfs in BASE_CASHFLOWS.items():
    vol    = VOLATILITY[name]
    cost   = cfs[0]         # Year 0 cost — does NOT vary (it is a signed contract)
    base   = cfs[1:]        # Years 1-5 cashflows vary randomly

    npv_list = []
    for _ in range(NUM_SIMS):
        # Draw a random multiplier from normal distribution
        # mean=1.0: average outcome = base case
        # std=vol: spread determined by investment risk
        multipliers  = np.random.normal(1.0, vol, len(base))
        sim_cfs      = [cost] + [b * m for b, m in zip(base, multipliers)]
        npv_list.append(npf.npv(WACC, sim_cfs))

    arr           = np.array(npv_list)
    mean_npv      = np.mean(arr)
    median_npv    = np.median(arr)
    std_npv       = np.std(arr)
    prob_positive = (arr > 0).mean() * 100
    p5            = np.percentile(arr, 5)    # worst 5% of outcomes
    p95           = np.percentile(arr, 95)   # best 5% of outcomes

    all_npvs[name] = arr
    summary.append({
        'Investment':       name,
        'Mean_NPV':         round(mean_npv, 0),
        'Median_NPV':       round(median_npv, 0),
        'Std_Dev':          round(std_npv, 0),
        'Prob_Positive_Pct':round(prob_positive, 1),
        'P5_NPV':           round(p5, 0),
        'P95_NPV':          round(p95, 0),
        'Volatility_Used':  vol,
    })
    print(f"{name:<26} ${mean_npv:>10,.0f} ${median_npv:>10,.0f} ${std_npv:>9,.0f} "
          f"{prob_positive:>8.1f}% ${p5:>10,.0f}")

print("=" * 78)

df_mc = pd.DataFrame(summary)
df_mc['MC_Rank'] = df_mc['Prob_Positive_Pct'].rank(ascending=False).astype(int)
df_mc = df_mc.sort_values('MC_Rank')

print("\nMONTE CARLO RISK RANKING (by Probability of Positive NPV):")
for _, row in df_mc.iterrows():
    print(f"  #{int(row.MC_Rank)} {row.Investment:<26}  P(NPV>0): {row.Prob_Positive_Pct:.1f}%  "
          f"Mean: ${row.Mean_NPV:,.0f}  StdDev: ${row.Std_Dev:,.0f}")

df_mc.to_csv('outputs/monte_carlo_results.csv', index=False)
print("\nFull results saved: outputs/monte_carlo_results.csv")

# ----------------------------------------------------------------
# CHART 1: 4-panel histogram grid (top 4 investments)
# ----------------------------------------------------------------
top4   = list(BASE_CASHFLOWS.keys())[:4]
colors = ['#1D4ED8','#16A34A','#B45309','#7C3AED']

fig1, axes = plt.subplots(2, 2, figsize=(14, 10))
fig1.suptitle(f'Monte Carlo NPV Distributions — {NUM_SIMS:,} Simulations Each\n'
              f'RetailCo Strategic Finance | 40,000 Total Simulations',
              fontsize=13, fontweight='bold')

for ax, name, color in zip(axes.flat, top4, colors):
    arr      = all_npvs[name]
    mean_npv = np.mean(arr)
    prob_pos = (arr > 0).mean() * 100
    p5       = np.percentile(arr, 5)

    ax.hist(arr, bins=80, color=color, edgecolor='white', alpha=0.8)
    ax.axvline(mean_npv, color='red',    lw=2, linestyle='--',
               label=f'Mean: ${mean_npv:,.0f}')
    ax.axvline(0,        color='black',  lw=1.5, label='Break-even (NPV=0)')
    ax.axvline(p5,       color='orange', lw=1.5, linestyle=':',
               label=f'5th Pct: ${p5:,.0f}')
    ax.set_title(f'{name}\nP(NPV > 0) = {prob_pos:.1f}%',
                 fontsize=10, fontweight='bold')
    ax.set_xlabel('NPV ($)'); ax.set_ylabel('Frequency')
    ax.legend(fontsize=8); ax.set_facecolor('#F8FAFC')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('outputs/monte_carlo_histograms.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: outputs/monte_carlo_histograms.png")

# ----------------------------------------------------------------
# CHART 2: Probability of positive NPV — all 8 investments
# ----------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(12, 6))
names_short = [n.replace(' ', '\n') for n in df_mc['Investment']]
bar_colors = ['#16A34A' if p >= 80 else '#B45309' if p >= 60 else '#DC2626'
              for p in df_mc['Prob_Positive_Pct']]
bars = ax2.bar(names_short, df_mc['Prob_Positive_Pct'], color=bar_colors)
ax2.axhline(80, color='green', lw=1.5, linestyle='--', label='80% threshold (strong)')
ax2.axhline(60, color='orange', lw=1.5, linestyle='--', label='60% threshold (acceptable)')
ax2.set_ylim(0, 110)
ax2.set_ylabel('Probability of Positive NPV (%)')
ax2.set_title(f'Monte Carlo Risk Analysis — Probability of Positive NPV\n'
              f'{NUM_SIMS:,} Simulations per Investment', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
for bar, val in zip(bars, df_mc['Prob_Positive_Pct']):
    ax2.text(bar.get_x()+bar.get_width()/2, val+0.5,
             f'{val:.1f}%', ha='center', fontsize=9, fontweight='bold')
ax2.set_facecolor('#F8FAFC')
plt.tight_layout()
plt.savefig('outputs/monte_carlo_probability_chart.png', dpi=150)
plt.show()
print("Chart saved: outputs/monte_carlo_probability_chart.png")