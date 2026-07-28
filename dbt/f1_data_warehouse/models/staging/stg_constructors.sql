SELECT
    constructor_id,
    name as team_name,
    nationality
from {{ source('bronze', 'constructors') }}