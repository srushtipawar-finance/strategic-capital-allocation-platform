import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ================================================================
# Script 3: Composite Risk Score Model
# Risk = 40% Volatility + 30% Capital Requirement + 30% Payback
# All scores normalised to 1-10 scale (1=safest, 10=riskiest)
# ================================================================

data = {
    'Investment':  [
        'New Store Expansion', 'E-Commerce Platform', 'New Product Line',
        'Geographic Expansion', 'Warehouse Automation', 'Customer Loyalty Prog',
        'Mobile App Investment', 'Strategic Acquisition'
    ],
    'Cost':    [1_200_000, 800_000, 600_000, 1_000_000,
                  700_000, 400_000, 500_000, 1_500_000],
    'Payback': [4.1, 3.6, 3.3, 4.8, 3.8, 2.8, 3.1, 5.2],
    'Risk_Level': ['High','Medium','Medium','High','Low','Low','Medium','Very High'],
}

df = pd.DataFrame(data)

def norm_to_10(series, ascending=True):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([5.0] * len(series), index=series.index)
    if ascending:
        return 1 + 9 * (series - mn) / (mx - mn)
    else:
        return 1 + 9 * (mx - series) / (mx - mn)

df['Capital_Score']    = norm_to_10(df['Cost'],    ascending=True)
df['Payback_Score']    = norm_to_10(df['Payback'], ascending=True)

vol_map = {'Low': 2.5, 'Medium': 5.0, 'High': 7.5, 'Very High': 10.0}
df['Vol_Raw']          = df['Risk_Level'].map(vol_map)
df['Vol_Score']        = norm_to_10(df['Vol_Raw'], ascending=True)

# Weights from Excel Assumptions tab
W_VOL = 0.40; W_CAP = 0.30; W_PAY = 0.30

df['Composite_Risk'] = (
    W_VOL * df['Vol_Score'] +
    W_CAP * df['Capital_Score'] +
    W_PAY * df['Payback_Score']
).round(2)

df['Risk_Rank'] = df['Composite_Risk'].rank(ascending=True).astype(int)
df['Risk_Cat']  = pd.cut(df['Composite_Risk'],
                         bins=[0, 3.5, 6.5, 10.1],
                         labels=['Low Risk', 'Medium Risk', 'High Risk'])

df_s = df.sort_values('Risk_Rank')
df_s.to_csv('outputs/risk_scores.csv', index=False)

print("COMPOSITE RISK SCORE RANKINGS")
print("=" * 68)
print(f"{'Rank':<5} {'Investment':<26} {'Score':>7} {'Category':>14} {'Vol':>6} {'Cap':>6} {'Pay':>6}")
print("-" * 68)
for _, row in df_s.iterrows():
    print(f"{int(row.Risk_Rank):<5} {row.Investment:<26} {row.Composite_Risk:>7.2f} "
          f"{str(row.Risk_Cat):>14} {row.Vol_Score:>6.1f} {row.Capital_Score:>6.1f} "
          f"{row.Payback_Score:>6.1f}")
print("=" * 68)
print("Risk saved: outputs/risk_scores.csv")

# Risk heatmap bar chart
fig, ax = plt.subplots(figsize=(13, 6))
norm   = mcolors.Normalize(vmin=1, vmax=10)
cmap   = plt.cm.RdYlGn_r
bcolors = [cmap(norm(s)) for s in df_s['Composite_Risk']]
bars  = ax.bar([n.replace(' ', '\n') for n in df_s['Investment']],
               df_s['Composite_Risk'], color=bcolors, edgecolor='white')
ax.axhline(3.5, color='green', lw=1.5, linestyle=':', alpha=0.8, label='Low/Medium boundary')
ax.axhline(6.5, color='red',   lw=1.5, linestyle=':', alpha=0.8, label='Medium/High boundary')
ax.set_ylim(0, 12)
ax.set_ylabel('Composite Risk Score (1 = Safest, 10 = Riskiest)', fontsize=11)
ax.set_title('Investment Risk Score Heatmap\n'
             '40% Volatility · 30% Capital Requirement · 30% Payback Period',
             fontsize=13, fontweight='bold')
ax.legend()
for bar, score in zip(bars, df_s['Composite_Risk']):
    ax.text(bar.get_x()+bar.get_width()/2, score+0.1,
            f'{score:.2f}', ha='center', fontsize=9, fontweight='bold')
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
plt.colorbar(sm, ax=ax, label='Risk Level', shrink=0.8)
plt.tight_layout()
plt.savefig('outputs/risk_score_heatmap.png', dpi=150)
plt.show()
print("Chart saved: outputs/risk_score_heatmap.png")