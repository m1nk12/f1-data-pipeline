with source as (
    select * from {{ source('bronze', "constructors") }}
),

deduplicate as (
    select * from(
        select
            *,
            row_number() over(
                partition by constructor_id
                order by time_stamp desc
            ) as rn
        from source
    ) x
    where rn = 1
)

SELECT
    constructor_id,
    name as team_name,
    nationality
from deduplicate