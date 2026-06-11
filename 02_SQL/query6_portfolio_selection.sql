-- True Portfolio Optimisation Result
-- Business question: Which combination of investments maximises NPV within $5M?
-- NOTE: This shows the result from the Python brute-force optimiser.
-- Replace YES/NO values with actual Python output after running Script 4.
SELECT
    m.name,
    '$' || printf('%.0f', i.cost)   AS cost,
    '$' || printf('%.0f', m.npv)    AS npv,
    printf('%.1f', m.irr) || '%'    AS irr,
    m.pi                             AS profitability_index,
    r.composite                      AS risk_score,
    CASE m.inv_id
        WHEN 1 THEN '[YES or NO — fill from Python]'
        WHEN 2 THEN '[YES or NO — fill from Python]'
        WHEN 3 THEN '[YES or NO — fill from Python]'
        WHEN 4 THEN '[YES or NO — fill from Python]'
        WHEN 5 THEN '[YES or NO — fill from Python]'
        WHEN 6 THEN '[YES or NO — fill from Python]'
        WHEN 7 THEN '[YES or NO — fill from Python]'
        WHEN 8 THEN '[YES or NO — fill from Python]'
    END AS optimal_portfolio
FROM financial_metrics m
JOIN investments i ON m.inv_id = i.id
JOIN risk_scores r ON m.inv_id = r.inv_id
ORDER BY m.npv DESC;