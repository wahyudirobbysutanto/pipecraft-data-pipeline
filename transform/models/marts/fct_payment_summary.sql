WITH daily_sales AS (
    SELECT * FROM {{ ref('stg_daily_sales') }}
),
payment_category_mapping AS (
    SELECT * FROM {{ ref('payment_category_mapping') }}
)

select 
    a.payment_method,
    coalesce(b.payment_category, 'Uncategorized') as payment_category,
    sum(a.total_revenue) as grand_total_revenue,
    sum(a.total_trx) as grand_total_transactions,
    {{ safe_divide('sum(a.total_revenue)', 'sum(a.total_trx)') }} as avg_revenue_per_trx,
    {{ classify_sales_tier('sum(a.total_revenue)') }} as revenue_tier
from daily_sales a
left join payment_category_mapping b 
    on a.payment_method = b.payment_method
group by 
    a.payment_method,
    b.payment_category