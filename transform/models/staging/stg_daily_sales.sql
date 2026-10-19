{{ 
    config(
        materialized='incremental',
        unique_key='sales_id'
    )
}}

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
    {% if is_incremental() %}
        -- Hanya ambil data yang tanggalnya lebih baru dari data terakhir di dbt
        where trx_date > (select max(transaction_date) from {{ this }})
    {% endif %}
)

select * from renamed