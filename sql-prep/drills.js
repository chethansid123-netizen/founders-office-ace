/* 60 graded SQL drills. `sol` is the model solution, verified to run against the seeded database.
   `ordered:true` means row ORDER is part of the correct answer. */
window.DRILLS = [
/* ---------- SELECT / WHERE / ORDER / LIMIT ---------- */
{id:1,lvl:'e',t:'SELECT',q:'List every customer name and their country.',
 h:'Two columns, no filter.',sol:`SELECT cust_name, country FROM customers;`},
{id:2,lvl:'e',t:'WHERE',q:'Show all customers from India.',
 h:"String literals use single quotes.",sol:`SELECT * FROM customers WHERE country = 'India';`},
{id:3,lvl:'e',t:'WHERE',q:'List employees earning more than 120000, highest first.',
 h:'WHERE then ORDER BY … DESC.',ordered:true,
 sol:`SELECT emp_name, salary FROM employees WHERE salary > 120000 ORDER BY salary DESC;`},
{id:4,lvl:'e',t:'DISTINCT',q:'What distinct countries do customers come from? Sort alphabetically.',
 h:'DISTINCT removes duplicate rows.',ordered:true,
 sol:`SELECT DISTINCT country FROM customers ORDER BY country;`},
{id:5,lvl:'e',t:'LIMIT',q:'Show the 5 most expensive products (name and price).',
 h:'ORDER BY … DESC LIMIT 5.',ordered:true,
 sol:`SELECT product_name, unit_price FROM products ORDER BY unit_price DESC LIMIT 5;`},
{id:6,lvl:'e',t:'BETWEEN',q:'Find employees hired between 2019-01-01 and 2020-12-31.',
 h:'BETWEEN is inclusive at both ends.',
 sol:`SELECT emp_name, hire_date FROM employees WHERE hire_date BETWEEN DATE '2019-01-01' AND DATE '2020-12-31';`},
{id:7,lvl:'e',t:'IN',q:'List products in the Software or Platform categories.',
 h:'IN takes a bracketed list.',
 sol:`SELECT product_name, category FROM products WHERE category IN ('Software','Platform');`},
{id:8,lvl:'e',t:'LIKE',q:'Find customers whose name contains the letters "an" (case-insensitive).',
 h:'ILIKE with % on both sides.',
 sol:`SELECT cust_name FROM customers WHERE cust_name ILIKE '%an%';`},
{id:9,lvl:'e',t:'OFFSET',q:'Show employees ranked 4th to 6th by salary (highest first). Break ties by emp_id.',
 h:'LIMIT 3 OFFSET 3.',ordered:true,
 sol:`SELECT emp_name, salary FROM employees ORDER BY salary DESC, emp_id LIMIT 3 OFFSET 3;`},
/* ---------- NULL ---------- */
{id:10,lvl:'e',t:'NULL',q:'Which customers have no city recorded?',
 h:'IS NULL, never = NULL.',sol:`SELECT cust_name, country FROM customers WHERE city IS NULL;`},
{id:11,lvl:'e',t:'NULL',q:'List every customer with their city, showing "(unknown)" where the city is missing.',
 h:'COALESCE.',sol:`SELECT cust_name, COALESCE(city,'(unknown)') AS city FROM customers;`},
{id:12,lvl:'m',t:'NULL',q:'For order_items, show the count of all rows, the count of non-null discount_pct, and how many rows have a NULL discount.',
 h:'COUNT(*) vs COUNT(col).',
 sol:`SELECT COUNT(*) AS all_rows, COUNT(discount_pct) AS with_discount,
        COUNT(*) - COUNT(discount_pct) AS null_discount FROM order_items;`},
{id:13,lvl:'m',t:'NULL',q:'Find departments that have no employees. Your answer must be correct despite the NULL dept_id in employees.',
 h:'NOT EXISTS, not NOT IN.',
 sol:`SELECT d.dept_name FROM departments d
      WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.dept_id);`},
/* ---------- CASE ---------- */
{id:14,lvl:'m',t:'CASE',q:'Label each product Premium (>=1500), Standard (>=500) or Budget, with its price.',
 h:'Searched CASE, conditions in order.',
 sol:`SELECT product_name, unit_price,
        CASE WHEN unit_price >= 1500 THEN 'Premium'
             WHEN unit_price >= 500  THEN 'Standard'
             ELSE 'Budget' END AS tier
      FROM products;`},
{id:15,lvl:'m',t:'CASE',q:'Count orders by status in a single row, one column per status (completed, pending, cancelled, refunded).',
 h:'Conditional aggregation — SUM(CASE …) or COUNT(*) FILTER.',
 sol:`SELECT COUNT(*) FILTER (WHERE status='completed') AS completed,
             COUNT(*) FILTER (WHERE status='pending')   AS pending,
             COUNT(*) FILTER (WHERE status='cancelled') AS cancelled,
             COUNT(*) FILTER (WHERE status='refunded')  AS refunded
      FROM orders;`},
/* ---------- AGGREGATES / GROUP BY / HAVING ---------- */
{id:16,lvl:'e',t:'AGG',q:'How many customers are there in total?',
 h:'COUNT(*) with no GROUP BY.',sol:`SELECT COUNT(*) AS total_customers FROM customers;`},
{id:17,lvl:'e',t:'GROUP BY',q:'Count customers per country, busiest first.',
 h:'GROUP BY country.',ordered:true,
 sol:`SELECT country, COUNT(*) AS customers FROM customers GROUP BY country ORDER BY customers DESC, country;`},
{id:18,lvl:'e',t:'GROUP BY',q:'For each product category show the number of products and the average unit price rounded to 2dp.',
 h:'ROUND(AVG(x),2) — AVG of numeric is fine here.',
 sol:`SELECT category, COUNT(*) AS products, ROUND(AVG(unit_price),2) AS avg_price
      FROM products GROUP BY category;`},
{id:19,lvl:'m',t:'GROUP BY',q:'Per department (by name) show headcount and total payroll. Exclude employees with no department.',
 h:'JOIN then GROUP BY the department name.',
 sol:`SELECT d.dept_name, COUNT(*) AS headcount, SUM(e.salary) AS payroll
      FROM employees e JOIN departments d ON d.dept_id = e.dept_id
      GROUP BY d.dept_name;`},
{id:20,lvl:'m',t:'HAVING',q:'Which countries have more than 1 customer?',
 h:'HAVING filters groups.',
 sol:`SELECT country, COUNT(*) AS customers FROM customers GROUP BY country HAVING COUNT(*) > 1;`},
{id:21,lvl:'m',t:'HAVING',q:'Which product categories have an average unit price above 800? Show the average rounded to 2dp.',
 h:'HAVING can use the aggregate directly.',
 sol:`SELECT category, ROUND(AVG(unit_price),2) AS avg_price
      FROM products GROUP BY category HAVING AVG(unit_price) > 800;`},
{id:22,lvl:'m',t:'WHERE+HAVING',q:'Among completed orders only, find customers (by cust_id) who placed 3 or more orders.',
 h:'WHERE filters rows first, HAVING filters groups after.',
 sol:`SELECT cust_id, COUNT(*) AS orders FROM orders
      WHERE status='completed' GROUP BY cust_id HAVING COUNT(*) >= 3;`},
{id:23,lvl:'m',t:'AGG',q:'Show the min, max, average (0dp) and median salary across all employees.',
 h:'PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary).',
 sol:`SELECT MIN(salary) AS lowest, MAX(salary) AS highest,
             ROUND(AVG(salary),0) AS mean,
             PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median
      FROM employees;`},
{id:24,lvl:'m',t:'STRING_AGG',q:'For each department name, list its employees as one comma-separated string, alphabetically.',
 h:'STRING_AGG(x, ", " ORDER BY x).',
 sol:`SELECT d.dept_name, STRING_AGG(e.emp_name, ', ' ORDER BY e.emp_name) AS team
      FROM employees e JOIN departments d ON d.dept_id=e.dept_id GROUP BY d.dept_name;`},
/* ---------- JOINS ---------- */
{id:25,lvl:'e',t:'JOIN',q:'List each order id with the customer name that placed it.',
 h:'INNER JOIN on cust_id.',
 sol:`SELECT o.order_id, c.cust_name FROM orders o JOIN customers c ON c.cust_id = o.cust_id;`},
{id:26,lvl:'m',t:'LEFT JOIN',q:'List every customer with their number of orders — including customers who have never ordered (show 0).',
 h:'LEFT JOIN, and COUNT the order column (not *) so no-order customers give 0.',
 sol:`SELECT c.cust_name, COUNT(o.order_id) AS orders
      FROM customers c LEFT JOIN orders o ON o.cust_id = c.cust_id
      GROUP BY c.cust_id, c.cust_name;`},
{id:27,lvl:'m',t:'ANTI-JOIN',q:'Which customers have never placed an order?',
 h:'NOT EXISTS, or LEFT JOIN … IS NULL.',
 sol:`SELECT c.cust_name FROM customers c
      WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.cust_id);`},
{id:28,lvl:'m',t:'ANTI-JOIN',q:'Which products have never been ordered?',
 h:'Same anti-join shape against order_items.',
 sol:`SELECT p.product_name FROM products p
      WHERE NOT EXISTS (SELECT 1 FROM order_items i WHERE i.product_id = p.product_id);`},
{id:29,lvl:'m',t:'SELF JOIN',q:'List each employee alongside their manager name. Include the CEO, whose manager is NULL.',
 h:'LEFT JOIN employees to itself on manager_id.',
 sol:`SELECT e.emp_name AS employee, m.emp_name AS manager
      FROM employees e LEFT JOIN employees m ON m.emp_id = e.manager_id;`},
{id:30,lvl:'m',t:'SELF JOIN',q:'Find employees who earn more than their own manager. Show both salaries.',
 h:'INNER self-join, then compare.',
 sol:`SELECT e.emp_name AS employee, e.salary, m.emp_name AS manager, m.salary AS manager_salary
      FROM employees e JOIN employees m ON m.emp_id = e.manager_id
      WHERE e.salary > m.salary;`},
{id:31,lvl:'m',t:'JOIN',q:'Total completed revenue per country, highest first. Use order_items.line_total.',
 h:'Three-table join, filter status, GROUP BY country.',ordered:true,
 sol:`SELECT c.country, ROUND(SUM(oi.line_total),2) AS revenue
      FROM orders o
      JOIN customers c ON c.cust_id = o.cust_id
      JOIN order_items oi ON oi.order_id = o.order_id
      WHERE o.status='completed'
      GROUP BY c.country ORDER BY revenue DESC;`},
{id:32,lvl:'h',t:'GRAIN',q:'Per customer, show the number of DISTINCT completed orders and total revenue. Beware the fan-out.',
 h:'COUNT(DISTINCT o.order_id) — COUNT(*) counts line items, not orders.',
 sol:`SELECT c.cust_name, COUNT(DISTINCT o.order_id) AS orders, ROUND(SUM(oi.line_total),2) AS revenue
      FROM customers c
      JOIN orders o ON o.cust_id=c.cust_id AND o.status='completed'
      JOIN order_items oi ON oi.order_id=o.order_id
      GROUP BY c.cust_id, c.cust_name;`},
{id:33,lvl:'h',t:'ON vs WHERE',q:'Show every customer with their count of COMPLETED orders, keeping customers who have none (0). The status filter must not drop them.',
 h:'Put the status condition in ON, not WHERE.',
 sol:`SELECT c.cust_name, COUNT(o.order_id) AS completed_orders
      FROM customers c LEFT JOIN orders o
        ON o.cust_id = c.cust_id AND o.status = 'completed'
      GROUP BY c.cust_id, c.cust_name;`},
{id:34,lvl:'m',t:'JOIN',q:'Which employees work in a department located in Bengaluru?',
 h:'Join employees to departments and filter on location.',
 sol:`SELECT e.emp_name, d.dept_name FROM employees e
      JOIN departments d ON d.dept_id=e.dept_id WHERE d.location='Bengaluru';`},
/* ---------- SET OPS ---------- */
{id:35,lvl:'m',t:'UNION',q:'Produce one list of all names: customer names labelled "customer" and employee names labelled "employee".',
 h:'UNION ALL with a literal label column.',
 sol:`SELECT cust_name AS name, 'customer' AS kind FROM customers
      UNION ALL
      SELECT emp_name, 'employee' FROM employees;`},
{id:36,lvl:'m',t:'EXCEPT',q:'Which customer cities are NOT also a department location? Ignore NULL cities.',
 h:'EXCEPT compares whole rows.',ordered:true,
 sol:`SELECT city FROM customers WHERE city IS NOT NULL
      EXCEPT SELECT location FROM departments ORDER BY city;`},
{id:37,lvl:'m',t:'INTERSECT',q:'Which cities appear both as a customer city and as a department location?',
 h:'INTERSECT.',
 sol:`SELECT city FROM customers WHERE city IS NOT NULL INTERSECT SELECT location FROM departments;`},
/* ---------- SUBQUERIES ---------- */
{id:38,lvl:'m',t:'SUBQUERY',q:'List employees earning above the overall company average salary.',
 h:'Scalar subquery in WHERE.',
 sol:`SELECT emp_name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);`},
{id:39,lvl:'h',t:'CORRELATED',q:'List employees earning above the average salary OF THEIR OWN DEPARTMENT.',
 h:'The subquery must reference the outer row: WHERE e2.dept_id = e.dept_id.',
 sol:`SELECT e.emp_name, e.dept_id, e.salary FROM employees e
      WHERE e.salary > (SELECT AVG(e2.salary) FROM employees e2 WHERE e2.dept_id = e.dept_id);`},
{id:40,lvl:'h',t:'CORRELATED',q:'For each customer show their most recent order date (NULL if they never ordered).',
 h:'Correlated scalar subquery in SELECT, or a LEFT JOIN with MAX.',
 sol:`SELECT c.cust_name,
             (SELECT MAX(o.order_date) FROM orders o WHERE o.cust_id=c.cust_id) AS last_order
      FROM customers c;`},
{id:41,lvl:'m',t:'DERIVED',q:'Using a subquery in FROM, show each department id and its headcount, only for departments with 2 or more people.',
 h:'A derived table needs an alias.',
 sol:`SELECT t.dept_id, t.headcount FROM
      (SELECT dept_id, COUNT(*) AS headcount FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id) t
      WHERE t.headcount >= 2;`},
{id:42,lvl:'h',t:'EXISTS',q:'Find customers who have at least one order that was cancelled.',
 h:'EXISTS with a correlated condition.',
 sol:`SELECT DISTINCT c.cust_name FROM customers c
      WHERE EXISTS (SELECT 1 FROM orders o WHERE o.cust_id=c.cust_id AND o.status='cancelled');`},
{id:43,lvl:'h',t:'ALL',q:'Find employees whose salary is greater than every salary in department 3.',
 h:'> ALL (subquery).',
 sol:`SELECT emp_name, salary FROM employees
      WHERE salary > ALL (SELECT salary FROM employees WHERE dept_id=3);`},
/* ---------- CTEs ---------- */
{id:44,lvl:'m',t:'CTE',q:'Using a CTE named "completed", compute total revenue per customer id for completed orders only.',
 h:'WITH completed AS (…) SELECT … FROM completed.',
 sol:`WITH completed AS (SELECT order_id, cust_id FROM orders WHERE status='completed')
      SELECT c.cust_id, ROUND(SUM(oi.line_total),2) AS revenue
      FROM completed c JOIN order_items oi ON oi.order_id=c.order_id
      GROUP BY c.cust_id;`},
{id:45,lvl:'h',t:'RECURSIVE',q:'Build the full org chart: every employee with their depth level (CEO = 1).',
 h:'WITH RECURSIVE, anchor = manager_id IS NULL.',
 sol:`WITH RECURSIVE org AS (
        SELECT emp_id, emp_name, manager_id, 1 AS level FROM employees WHERE manager_id IS NULL
        UNION ALL
        SELECT e.emp_id, e.emp_name, e.manager_id, o.level+1
        FROM employees e JOIN org o ON e.manager_id = o.emp_id)
      SELECT emp_id, emp_name, level FROM org;`},
{id:46,lvl:'h',t:'RECURSIVE',q:'List everyone who reports (directly or indirectly) to Priya Nair.',
 h:'Anchor on Priya, then walk down.',
 sol:`WITH RECURSIVE sub AS (
        SELECT emp_id, emp_name FROM employees WHERE emp_name='Priya Nair'
        UNION ALL
        SELECT e.emp_id, e.emp_name FROM employees e JOIN sub s ON e.manager_id = s.emp_id)
      SELECT emp_name FROM sub WHERE emp_name <> 'Priya Nair';`},
{id:47,lvl:'m',t:'CTE',q:'Generate the six months of 2024 H1 as dates (2024-01-01 to 2024-06-01).',
 h:'generate_series with an INTERVAL step.',ordered:true,
 sol:`SELECT g::date AS month
      FROM generate_series(DATE '2024-01-01', DATE '2024-06-01', INTERVAL '1 month') g
      ORDER BY month;`},
/* ---------- WINDOWS ---------- */
{id:48,lvl:'m',t:'WINDOW',q:'Show every employee with the average salary of their department alongside (0dp), without collapsing rows.',
 h:'AVG(salary) OVER (PARTITION BY dept_id).',
 sol:`SELECT emp_name, dept_id, salary,
             ROUND(AVG(salary) OVER (PARTITION BY dept_id),0) AS dept_avg
      FROM employees;`},
{id:49,lvl:'m',t:'RANKING',q:'Rank all employees by salary descending using ROW_NUMBER, RANK and DENSE_RANK side by side.',
 h:'Three window functions, same OVER clause.',ordered:true,
 sol:`SELECT emp_name, salary,
             ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,
             RANK()       OVER (ORDER BY salary DESC) AS rnk,
             DENSE_RANK() OVER (ORDER BY salary DESC) AS drnk
      FROM employees ORDER BY salary DESC, emp_name;`},
{id:50,lvl:'h',t:'TOP-N',q:'Find the top 2 earners in each department (exclude the NULL department). Use RANK so ties both count.',
 h:'Rank in a CTE, filter r <= 2 outside.',
 sol:`WITH r AS (SELECT emp_name, dept_id, salary,
                    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
             FROM employees WHERE dept_id IS NOT NULL)
      SELECT dept_id, emp_name, salary, rk FROM r WHERE rk <= 2;`},
{id:51,lvl:'h',t:'LAG',q:'Monthly completed revenue with the previous month alongside and the absolute change.',
 h:'Aggregate to month in a CTE, then LAG.',ordered:true,
 sol:`WITH m AS (SELECT DATE_TRUNC('month',o.order_date)::date AS month, SUM(oi.line_total) AS rev
             FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
             WHERE o.status='completed' GROUP BY 1)
      SELECT month, ROUND(rev,2) AS revenue,
             ROUND(LAG(rev) OVER (ORDER BY month),2) AS prev_month,
             ROUND(rev - LAG(rev) OVER (ORDER BY month),2) AS change
      FROM m ORDER BY month;`},
{id:52,lvl:'h',t:'RUNNING',q:'Monthly completed revenue with a running cumulative total.',
 h:'SUM(rev) OVER (ORDER BY month) is cumulative by default.',ordered:true,
 sol:`WITH m AS (SELECT DATE_TRUNC('month',o.order_date)::date AS month, SUM(oi.line_total) AS rev
             FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
             WHERE o.status='completed' GROUP BY 1)
      SELECT month, ROUND(rev,2) AS revenue,
             ROUND(SUM(rev) OVER (ORDER BY month),2) AS cumulative
      FROM m ORDER BY month;`},
{id:53,lvl:'h',t:'NTILE',q:'Split employees into 4 salary quartiles (1 = lowest) and show each employee’s quartile.',
 h:'NTILE(4) OVER (ORDER BY salary).',
 sol:`SELECT emp_name, salary, NTILE(4) OVER (ORDER BY salary) AS quartile FROM employees;`},
{id:54,lvl:'h',t:'DEDUP',q:'From staging_signups keep only the most recent row per email (case-insensitive). Return email, name and loaded_at.',
 h:'ROW_NUMBER() OVER (PARTITION BY LOWER(raw_email) ORDER BY loaded_at DESC), keep rn = 1.',
 sol:`WITH r AS (SELECT raw_email, raw_name, loaded_at,
                    ROW_NUMBER() OVER (PARTITION BY LOWER(raw_email) ORDER BY loaded_at DESC) AS rn
             FROM staging_signups)
      SELECT raw_email, raw_name, loaded_at FROM r WHERE rn=1;`},
{id:55,lvl:'h',t:'SHARE',q:'Revenue per country for completed orders, plus each country’s percentage of total revenue (1dp).',
 h:'SUM(...) OVER () gives the grand total alongside grouped rows.',ordered:true,
 sol:`SELECT c.country, ROUND(SUM(oi.line_total),2) AS revenue,
             ROUND(100.0*SUM(oi.line_total)/SUM(SUM(oi.line_total)) OVER (),1) AS pct_of_total
      FROM orders o JOIN customers c ON c.cust_id=o.cust_id
      JOIN order_items oi ON oi.order_id=o.order_id
      WHERE o.status='completed'
      GROUP BY c.country ORDER BY revenue DESC;`},
{id:56,lvl:'h',t:'NTH',q:'Find the 3rd highest DISTINCT salary among employees.',
 h:'DENSE_RANK = 3, or DISTINCT with OFFSET 2 LIMIT 1.',
 sol:`WITH r AS (SELECT DISTINCT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rk FROM employees)
      SELECT salary FROM r WHERE rk = 3;`},
/* ---------- PATTERNS ---------- */
{id:57,lvl:'h',t:'GAPS',q:'For customer 1’s page_view events, find each run of consecutive days: start date, end date and length.',
 h:'date - ROW_NUMBER() is constant within a run. Group by it.',ordered:true,
 sol:`WITH d AS (SELECT DISTINCT event_at::date AS dt FROM web_events
             WHERE cust_id=1 AND event_type='page_view'),
      g AS (SELECT dt, dt - (ROW_NUMBER() OVER (ORDER BY dt))::int AS island FROM d)
      SELECT MIN(dt) AS run_start, MAX(dt) AS run_end, COUNT(*) AS days
      FROM g GROUP BY island ORDER BY run_start;`},
{id:58,lvl:'h',t:'PIVOT',q:'For each country, one row with counts of completed, pending, cancelled and refunded orders.',
 h:'COUNT(*) FILTER (WHERE …) per status.',
 sol:`SELECT c.country,
             COUNT(*) FILTER (WHERE o.status='completed') AS completed,
             COUNT(*) FILTER (WHERE o.status='pending')   AS pending,
             COUNT(*) FILTER (WHERE o.status='cancelled') AS cancelled,
             COUNT(*) FILTER (WHERE o.status='refunded')  AS refunded
      FROM orders o JOIN customers c ON c.cust_id=o.cust_id
      GROUP BY c.country;`},
{id:59,lvl:'h',t:'SPINE',q:'Show completed revenue for every month of 2024 H1, including months with zero partner-channel revenue. Filter channel = partner.',
 h:'generate_series spine LEFT JOINed to the aggregate.',ordered:true,
 sol:`WITH spine AS (SELECT g::date AS month FROM generate_series(DATE '2024-01-01', DATE '2024-06-01', INTERVAL '1 month') g),
      a AS (SELECT DATE_TRUNC('month',o.order_date)::date AS month, SUM(oi.line_total) AS rev
            FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
            WHERE o.status='completed' AND o.channel='partner' GROUP BY 1)
      SELECT s.month, COALESCE(ROUND(a.rev,2),0) AS partner_revenue
      FROM spine s LEFT JOIN a ON a.month=s.month ORDER BY s.month;`},
{id:60,lvl:'h',t:'FUNNEL',q:'Across all web_events, count distinct sessions at each funnel stage (page_view, add_to_cart, checkout, purchase) and the overall view-to-purchase conversion percentage (1dp).',
 h:'COUNT(DISTINCT session_id) FILTER per stage, guard the division with NULLIF.',
 sol:`WITH f AS (SELECT COUNT(DISTINCT session_id) FILTER (WHERE event_type='page_view')   AS viewed,
                    COUNT(DISTINCT session_id) FILTER (WHERE event_type='add_to_cart') AS carted,
                    COUNT(DISTINCT session_id) FILTER (WHERE event_type='checkout')    AS checked_out,
                    COUNT(DISTINCT session_id) FILTER (WHERE event_type='purchase')    AS purchased
             FROM web_events)
      SELECT viewed, carted, checked_out, purchased,
             ROUND(100.0*purchased/NULLIF(viewed,0),1) AS overall_pct FROM f;`},
];
