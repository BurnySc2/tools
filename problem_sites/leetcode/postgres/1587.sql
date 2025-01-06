-- Write your PostgreSQL query statement below
SELECT u.name AS NAME, SUM(t.amount) AS BALANCE
FROM Users u
LEFT JOIN Transactions t
ON u.account = t.account
GROUP BY u.name, u.account
HAVING SUM(t.amount) > 10000
