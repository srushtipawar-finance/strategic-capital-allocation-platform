-- Full Investment Pipeline Overview
-- Business question: What is our complete investment pipeline worth?
SELECT
    i.id,
    i.name,
    '$' || printf('%.0f', i.cost)                               AS investment_cost,
    '$' || printf('%.0f', i.yr1+i.yr2+i.yr3+i.yr4+i.yr5)     AS total_5yr_inflows,
    '$' || printf('%.0f', (i.yr1+i.yr2+i.yr3+i.yr4+i.yr5)
                          - i.cost)                             AS gross_profit,
    i.risk_level,
    i.category
FROM investments i
ORDER BY (i.yr1+i.yr2+i.yr3+i.yr4+i.yr5) - i.cost DESC;