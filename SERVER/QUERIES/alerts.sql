SELECT  drone_id,
        time_captured, 
        lat, 
        lon, 
        image

FROM    images

WHERE   prediction = 'FIRE'
AND     time_captured >= '{min_time}'

ORDER BY time_captured DESC