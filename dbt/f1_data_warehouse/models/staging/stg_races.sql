with source as (
    select * from {{ source('bronze', "races") }}
),

deduplicate as (
    select * from(
        select
            *,
            row_number() over(
                partition by season, round
                order by time_stamp desc
            ) as rn
        from source
    ) x
    where rn = 1
)



SELECT
    season,
    round,
    name,
    date,
    time
from deduplicate