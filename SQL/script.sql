-- 1) --
SELECT uid FROM wifi_session
WHERE 1=1
	  AND (start_station in (50, 161) or stop_station in (50, 161))
	  AND stop_dttm >= NOW() - INTERVAL '3' MONTH
GROUP BY uid
HAVING COUNT(*) > 50

-- 2) --
SELECT uid, start_dttm, stop_dttm, start_station, stop_station FROM (
SELECT *,
	   LEAD(start_dttm) OVER (PARTITION BY uid ORDER BY start_dttm) as next_session_start_dttm
FROM wifi_session
) t
WHERE next_session_start_dttm < stop_dttm

-- 3) --
SELECT station FROM (
	SELECT station,
		   dense_rank() OVER (ORDER BY attendance DESC) as dr
	FROM (
		SELECT station, COUNT(station) as attendance
		FROM (
				SELECT start_station as station FROM wifi_session
				UNION ALL
				SELECT stop_station as station FROM wifi_session
			 ) t
		GROUP BY station
		 ) q
) s
WHERE dr >= 10

-- 4) --
WITH buf as (
SELECT * FROM (
SELECT *,
	   ROW_NUMBER() OVER (PARTITION BY uid, DATE_TRUNC('day', stop_dttm) ORDER BY stop_dttm DESC) as rn
FROM wifi_session
) t
WHERE rn = 1
)
, buf_2 AS (
SELECT uid, stop_station, COUNT(stop_station) as cnt FROM buf
GROUP BY uid, stop_station
)
SELECT t_1.uid, t_1.stop_station FROM buf_2 t_1
LEFT JOIN buf_2 t_2
ON t_1.uid = t_2.uid AND  t_1.cnt < t_2.cnt
WHERE t_2.cnt IS NULL