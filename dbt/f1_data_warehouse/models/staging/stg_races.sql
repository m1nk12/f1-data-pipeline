SELECT
    season,
    round,
    name,
    date,
    time
from {{ source('bronze', 'races') }}