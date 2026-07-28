select
    driver_id,
    given_name,
    family_name,
    code,
    nationality,
    dob
from {{ source("bronze", "drivers") }}