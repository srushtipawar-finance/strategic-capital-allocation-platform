-- Executive Summary — One query for the CFO
-- Business question: What is the headline summary of this analysis?
SELECT '8'                                                  AS investments_analysed
UNION ALL SELECT COUNT(*) || ' of 8'                        FROM financial_metrics WHERE decision='INVEST'
UNION ALL SELECT '$' || printf('%.0f', MAX(npv))            FROM financial_metrics
UNION ALL SELECT printf('%.1f', MAX(irr)) || '%'            FROM financial_metrics
UNION ALL SELECT printf('%.3f', MAX(pi))                    FROM financial_metrics
UNION ALL SELECT printf('%.0f', MIN(composite))             FROM risk_scores
UNION ALL SELECT printf('%.0f', MAX(composite))             FROM risk_scores
UNION ALL SELECT '$5,000,000';