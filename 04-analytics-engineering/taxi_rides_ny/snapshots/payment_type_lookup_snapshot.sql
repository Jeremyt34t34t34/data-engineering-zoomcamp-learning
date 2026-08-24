{% snapshot payment_type_lookup_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='payment_type',
      strategy='check',
      check_cols=['description']
    )
}}

select
    payment_type,
    description
from {{ ref('payment_type_lookup') }}

{% endsnapshot %}
