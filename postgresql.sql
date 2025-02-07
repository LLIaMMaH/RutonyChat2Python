select event_type, count(event_type) as cnt_et from events
group by event_type
order by cnt_et desc

select * from events
where event_type = 'music'
order by id