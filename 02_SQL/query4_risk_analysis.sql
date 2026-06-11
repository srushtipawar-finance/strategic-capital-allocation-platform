-- Risk-Adjusted Investment Analysis
-- Business question: What is the real risk-adjusted return for each investment?
SELECT
    r.risk_rank,
    r.name,
    r.composite                                            AS risk_score,
    '$' || printf('%.0f', m.npv)                          AS npv,
    '$' || printf('%.0f', m.npv / r.composite)            AS risk_adjusted_npv,
    printf('%.3f', m.pi)                                  AS profitability_index,
    i.risk_level,
    CASE
        WHEN r.composite < 4   THEN 'Low Risk — Safe to Fund'
        WHEN r.composite < 7   THEN 'Medium Risk — Fund with Monitoring'
        WHEN r.composite < 9   THEN 'High Risk — Fund Selectively'
        ELSE                        'Very High Risk — Defer or Reject'
    END                                                    AS risk_category
FROM risk_scores r
JOIN financial_metrics m ON r.inv_id = m.inv_id
JOIN investments i ON r.inv_id = i.id
ORDER BY r.risk_rank;