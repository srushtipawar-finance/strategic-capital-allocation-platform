-- NPV, IRR, and All Advanced KPIs Ranked
-- Business question: Which investments create the most value — absolutely and per dollar?
SELECT
    m.npv_rank                                             AS rank,
    m.name,
    '$' || printf('%.0f', i.cost)                         AS cost,
    '$' || printf('%.0f', m.npv)                          AS npv,
    printf('%.1f', m.irr) || '%'                          AS irr,
    printf('%.2f', m.payback)                             AS payback_yrs,
    printf('%.3f', m.pi)                                  AS profitability_index,
    printf('%.4f', m.npv_per_dollar)                      AS npv_per_dollar_invested,
    '$' || printf('%.0f', m.npv / r.composite)            AS risk_adjusted_npv,
    r.composite                                           AS risk_score,
    m.decision,
    CASE
        WHEN m.irr >= 20 THEN 'Exceptional — Strong Buy'
        WHEN m.irr >= 17 THEN 'Strong — Buy'
        WHEN m.irr >= 10 THEN 'Acceptable — Marginal Buy'
        ELSE                   'Reject — Below WACC'
    END                                                   AS irr_quality
FROM financial_metrics m
JOIN investments i ON m.inv_id = i.id
JOIN risk_scores  r ON m.inv_id = r.inv_id
ORDER BY m.npv_rank;