-- ============================================================================
--  SQL INTERVIEW SANDBOX  -  SCHEMA (DDL)
--  Dialect: PostgreSQL
--
--  This file is itself a lesson. Every constraint type you are likely to be
--  asked about appears at least once, with a comment saying what it does.
--  Read it top-to-bottom before you run a single SELECT.
-- ============================================================================

DROP TABLE IF EXISTS web_events      CASCADE;
DROP TABLE IF EXISTS staging_signups CASCADE;
DROP TABLE IF EXISTS order_items     CASCADE;
DROP TABLE IF EXISTS orders          CASCADE;
DROP TABLE IF EXISTS products        CASCADE;
DROP TABLE IF EXISTS customers       CASCADE;
DROP TABLE IF EXISTS employees       CASCADE;
DROP TABLE IF EXISTS departments     CASCADE;

-- ----------------------------------------------------------------------------
-- departments
--   Demonstrates: PRIMARY KEY, UNIQUE, NOT NULL, DEFAULT, CHECK
--   Note: two departments deliberately have NO employees, so you can practise
--   anti-joins ("find departments with nobody in them").
-- ----------------------------------------------------------------------------
CREATE TABLE departments (
    dept_id     integer     PRIMARY KEY,               -- entity identity; implies NOT NULL + UNIQUE
    dept_name   text        NOT NULL UNIQUE,           -- no two departments share a name
    location    text        NOT NULL,
    budget      numeric(12,2) NOT NULL DEFAULT 0
                            CHECK (budget >= 0)        -- row-level rule enforced on every write
);

-- ----------------------------------------------------------------------------
-- employees
--   Demonstrates: self-referencing FOREIGN KEY (manager_id -> emp_id),
--                 nullable FK (dept_id), ON DELETE SET NULL, CHECK.
--   Note: the CEO has manager_id = NULL and dept_id = NULL. That single row is
--   why "INNER JOIN departments" silently drops the CEO - a classic trap.
--   Salaries contain deliberate TIES so RANK / DENSE_RANK / ROW_NUMBER differ.
-- ----------------------------------------------------------------------------
CREATE TABLE employees (
    emp_id      integer     PRIMARY KEY,
    emp_name    text        NOT NULL,
    title       text        NOT NULL,
    dept_id     integer     REFERENCES departments(dept_id) ON DELETE SET NULL,
    manager_id  integer     REFERENCES employees(emp_id)    ON DELETE SET NULL,
    salary      numeric(10,2) NOT NULL CHECK (salary > 0),
    hire_date   date        NOT NULL,
    email       text        UNIQUE                         -- UNIQUE still allows many NULLs
);

-- ----------------------------------------------------------------------------
-- customers
--   Note: 3 customers have NO orders (LEFT JOIN / NOT EXISTS practice) and
--   2 have a NULL city (NULL-handling practice).
-- ----------------------------------------------------------------------------
CREATE TABLE customers (
    cust_id     integer     PRIMARY KEY,
    cust_name   text        NOT NULL,
    email       text        NOT NULL UNIQUE,
    city        text,                                   -- nullable ON PURPOSE
    country     text        NOT NULL,
    segment     text        NOT NULL
                            CHECK (segment IN ('SMB','Mid-Market','Enterprise')),
    signup_date date        NOT NULL
);

-- ----------------------------------------------------------------------------
-- products
--   Note: 2 products were never ordered (anti-join practice).
-- ----------------------------------------------------------------------------
CREATE TABLE products (
    product_id   integer      PRIMARY KEY,
    product_name text         NOT NULL UNIQUE,
    category     text         NOT NULL
                              CHECK (category IN ('Software','Platform','Service')),
    unit_price   numeric(10,2) NOT NULL CHECK (unit_price > 0),
    cost         numeric(10,2) NOT NULL CHECK (cost >= 0),
    launch_date  date         NOT NULL,
    CONSTRAINT price_above_cost CHECK (unit_price > cost)   -- named TABLE-level constraint
);

-- ----------------------------------------------------------------------------
-- orders  (the "header" table - one row per order)
--   Note: shipped_date is NULL for pending/cancelled orders.
--   status and channel are constrained so you can trust GROUP BY on them.
-- ----------------------------------------------------------------------------
CREATE TABLE orders (
    order_id     integer  PRIMARY KEY,
    cust_id      integer  NOT NULL REFERENCES customers(cust_id) ON DELETE CASCADE,
    order_date   date     NOT NULL,
    status       text     NOT NULL
                          CHECK (status IN ('completed','pending','cancelled','refunded')),
    channel      text     NOT NULL
                          CHECK (channel IN ('direct','partner','web')),
    shipped_date date,                                  -- NULL until it ships
    CONSTRAINT ship_after_order CHECK (shipped_date IS NULL OR shipped_date >= order_date)
);

-- ----------------------------------------------------------------------------
-- order_items  (the "line" table - MANY rows per order)
--   THIS IS THE FAN-OUT TABLE. Joining orders -> order_items multiplies the
--   order rows. Any SUM over an orders-level column after that join will be
--   DOUBLE COUNTED. This is the single most common analyst interview mistake.
--   Demonstrates: composite UNIQUE, GENERATED column, multi-column FK targets.
-- ----------------------------------------------------------------------------
CREATE TABLE order_items (
    item_id      integer  PRIMARY KEY,
    order_id     integer  NOT NULL REFERENCES orders(order_id)     ON DELETE CASCADE,
    product_id   integer  NOT NULL REFERENCES products(product_id) ON DELETE RESTRICT,
    quantity     integer  NOT NULL CHECK (quantity > 0),
    unit_price   numeric(10,2) NOT NULL CHECK (unit_price >= 0),
    discount_pct numeric(5,2) CHECK (discount_pct >= 0 AND discount_pct < 100), -- nullable
    -- A GENERATED column is computed by the database, never written by you:
    line_total   numeric(12,2)
                 GENERATED ALWAYS AS
                 (quantity * unit_price * (1 - COALESCE(discount_pct,0)/100)) STORED,
    CONSTRAINT uq_order_product UNIQUE (order_id, product_id)   -- composite UNIQUE
);

-- ----------------------------------------------------------------------------
-- web_events  (clickstream - for funnels, sessionisation, gaps-and-islands)
--   cust_id is NULLABLE: anonymous visitors exist.
-- ----------------------------------------------------------------------------
CREATE TABLE web_events (
    event_id   integer   PRIMARY KEY,
    cust_id    integer   REFERENCES customers(cust_id) ON DELETE SET NULL,  -- NULL = anonymous
    session_id text      NOT NULL,
    event_type text      NOT NULL
                         CHECK (event_type IN ('page_view','signup','add_to_cart','checkout','purchase')),
    event_at   timestamp NOT NULL
);

-- ----------------------------------------------------------------------------
-- staging_signups  (deliberately DIRTY - contains exact duplicate rows)
--   No primary key, on purpose. Use it to practise de-duplication with
--   ROW_NUMBER() and to see why a PK matters.
-- ----------------------------------------------------------------------------
CREATE TABLE staging_signups (
    raw_email   text,
    raw_name    text,
    source      text,
    loaded_at   timestamp
);

-- ----------------------------------------------------------------------------
-- Indexes: these are what make WHERE / JOIN / ORDER BY fast.
-- ----------------------------------------------------------------------------
CREATE INDEX idx_orders_cust        ON orders(cust_id);            -- FK lookups
CREATE INDEX idx_orders_date        ON orders(order_date);         -- range scans
CREATE INDEX idx_orders_cust_date   ON orders(cust_id, order_date);-- COMPOSITE: leftmost-prefix rule
CREATE INDEX idx_items_order        ON order_items(order_id);
CREATE INDEX idx_items_product      ON order_items(product_id);
CREATE INDEX idx_events_cust_time   ON web_events(cust_id, event_at);
CREATE INDEX idx_emp_mgr            ON employees(manager_id);
-- PARTIAL index: only indexes the rows you actually query. Smaller and faster.
CREATE INDEX idx_orders_open        ON orders(order_date) WHERE status = 'pending';
