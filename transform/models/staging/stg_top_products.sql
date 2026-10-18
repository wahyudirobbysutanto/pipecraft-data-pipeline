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
)

SELECT * FROM renamed