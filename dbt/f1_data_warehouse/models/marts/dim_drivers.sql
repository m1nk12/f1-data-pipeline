select * from {{ref('stg_drivers')}}
where dob is not null