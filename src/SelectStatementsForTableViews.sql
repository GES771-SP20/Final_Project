SELECT covid.*, states.name AS state_name, states.geom
FROM tl_2019_us_state AS states
LEFT JOIN (SELECT * FROM covid19_stats) AS covid
ON covid.state = states.stusps
WHERE covid.ymd_date BETWEEN '20200411' AND '20200414'
ORDER BY covid.state
;