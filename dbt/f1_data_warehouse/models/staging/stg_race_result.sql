with source as (
    select * from {{ source('bronze', "race_result") }}
),

deduplicate as (
    select * from(
        select
            *,
            row_number() over(
                partition by season, round, driver_id
                order by time_stamp desc
            ) as rn
        from source
    ) x
    where rn = 1
)


select 
    season,
    round,
    race_name,
    driver_id,
    driver_number,
    constructor_id,
    grid,
    position,
    points,
    laps,
    status,
    race_time,
    fastest_lap_rank,
    fastest_lap_number,
    fastest_lap_time
from deduplicate
order by position