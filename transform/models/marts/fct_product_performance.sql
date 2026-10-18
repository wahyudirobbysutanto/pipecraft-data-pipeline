WITH product_performance AS (
    SELECT * FROM {{ ref('stg_top_products') }}
)

SELECT
    product_name, SUM(subtotal) AS total_revenue_generated, SUM(qty_sold) AS total_units_sold
FROM product_performance
GROUP BY product_name