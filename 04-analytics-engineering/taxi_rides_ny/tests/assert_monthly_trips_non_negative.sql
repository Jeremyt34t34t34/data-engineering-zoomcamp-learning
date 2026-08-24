select *
from {{ ref('fct_monthly_zone_revenue') }}
where total_monthly_trips < 0
