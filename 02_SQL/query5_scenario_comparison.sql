-- Scenario NPV Comparison: Bear / Base / Bull
-- Business question: Which investments remain profitable even in worst case?
SELECT
    m.name,
    '$' || printf('%.0f', m.npv * 0.70)  AS bear_npv_70pct_revenue,
    '$' || printf('%.0f', m.npv)         AS base_npv,
    '$' || printf('%.0f', m.npv * 1.30)  AS bull_npv_130pct_revenue,
    CASE
        WHEN m.npv * 0.70 > 0 THEN 'Positive in ALL scenarios — Very Robust'
        WHEN m.npv > 0        THEN 'Positive in Base + Bull only'
        ELSE                       'Negative even in Base — Reject'
    END                              AS scenario_verdict
FROM financial_metrics m
ORDER BY m.npv DESC;