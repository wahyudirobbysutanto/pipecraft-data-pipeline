{{
    config(
        materialized = 'incremental',
        unique_key = 'product_id'
    )
}}

WITH source AS (
    SELECT * FROM {{ source('staging', 'top_products') }}
),

renamed AS (
    SELECT
        id AS product_id,
        trx_date AS transaction_date, 
        lower(product_name) AS product_name, 
        qty_sold, 
        subtotal
    FROM source

    {% if is_incremental() %}
        -- Only take data that is newer than the last date in dbt
        WHERE trx_date > (SELECT MAX(transaction_date) FROM {{ this }})
    {% endif %}

)

SELECT * FROM renamed