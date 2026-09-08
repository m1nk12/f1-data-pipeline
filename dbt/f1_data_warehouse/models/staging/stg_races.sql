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
    name as race_name,
    date,
    time,
    CURRENT_TIME as time_stamp
from deduplicate