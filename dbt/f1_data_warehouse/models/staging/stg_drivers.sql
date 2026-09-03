with source as (
    select * from {{ source('bronze', "drivers") }}
),

deduplicate as (
    select * from(
        select
            *,
            row_number() over(
                partition by driver_id
                order by time_stamp desc
            ) as rn
        from source
    ) x
    where rn = 1
)


select
    driver_id,
    given_name,
    family_name,
    code,
    nationality,
    dob,
    CURRENT_TIME as time_stamp
from deduplicate