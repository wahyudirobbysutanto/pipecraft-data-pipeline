with source as (
    select * from {{ source('staging', 'daily_sales') }}
),

renamed as (
    select
        id as sales_id,
        trx_date AS transaction_date,
        total_trx,
        total_revenue,
        lower(payment_method) as payment_method
    from source
)

select * from renamed