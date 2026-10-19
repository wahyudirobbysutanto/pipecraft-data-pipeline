{% macro safe_divide(numerator, denominator) %}
    CASE 
        WHEN {{denominator}} = 0 OR {{denominator}} IS NULL THEN 0
        ELSE ROUND( ({{numerator}}::NUMERIC / {{denominator}} ), 2)
    END
{% endmacro %}
