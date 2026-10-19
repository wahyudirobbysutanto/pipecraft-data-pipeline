{% macro classify_sales_tier(amount_column) %}
    CASE
        WHEN {{ amount_column }} >= 1000000 THEN 'High Revenue'
        WHEN {{ amount_column }} >= 500000 THEN 'Medium Revenue'
        ELSE 'Low Revenue'
    END
{% endmacro %}
