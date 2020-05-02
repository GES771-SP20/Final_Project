-- covid19_states_view
SELECT covid.*, states.name AS state_name, states.geom
FROM tl_2019_us_state AS states
LEFT JOIN (SELECT * FROM covid19_stats) AS covid
ON covid.state = states.stusps
--WHERE covid.ymd_date BETWEEN '20200429' AND '20200501'
WHERE covid.ymd_date IN ('2020-04-03', '2020-04-10', '2020-04-17', '2020-04-24', '2020-05-01')
ORDER BY covid.state, covid.ymd_date DESC
;

/*
-- covid19_maxvalues
SELECT 
	max(positive) as max_pos,
	max(negative) as max_neg,
	max(total_tests) as max_total,
	max(hospitalized) as max_hosp,
	max(deaths) as max_deaths,
	max(infect_rate) as max_infect_rate,
	max(hosp_rate) as max_hosp_rate,
	max(death_rate) as max_death_rate
FROM covid19_stats AS covid
;
*/