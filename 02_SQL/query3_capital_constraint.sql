-- Capital Constraint Analysis
-- Business question: Which investments fit within $5M if selected greedily by NPV?
WITH ranked AS (
    SELECT
        m.name,
        i.cost,
        m.npv,
        m.irr,
        SUM(i.cost) OVER (ORDER BY m.npv DESC
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
    FROM financial_metrics m
    JOIN investments i ON m.inv_id = i.id
)
SELECT
    name,
    '$' || printf('%.0f', cost)          AS cost,
    '$' || printf('%.0f', npv)           AS npv,
    printf('%.1f', irr) || '%'           AS irr,
    '$' || printf('%.0f', running_total) AS running_budget_total,
    CASE
        WHEN running_total <= 5000000 THEN 'FITS IN BUDGET'
        ELSE                               'EXCEEDS $5M BUDGET'
    END                                  AS budget_status
FROM ranked
ORDER BY npv DESC;