-- Билеты компании за месяц
select distinct
	t.id as ticket,
	extract(month from st.sale_date) as month
from 
	sale_ticket st
join tickets t
	on t.id=st.ticket
join airlines a
	on t.airline=a.id
where extract(month from st.sale_date) = 12
	and a.name='Байкал'

-- Общая сумма продаж компании
select
	-- t.id as ticket,
	-- c.id as coupone,
	-- st.client as client,
	-- fare
	sum(fare) as sum_fare,
	a.name
from 
	sale_ticket st
join tickets t
	on t.id=st.ticket
join coupones c 
	on c.ticket=t.id
join airlines a
	on t.airline=a.id
group by a.id
select * from sale_ticket

sele


-- список клиентов компании на указанную дату
select distinct
	concat(c.first_name, ' ', c.last_name)
from 
	sale_ticket st
join tickets t
	on t.id=st.ticket
join airlines a
	on t.airline=a.id
join clients c
	on c.id=st.client
join coupones cp
	on cp.ticket=t.id
where date(cp.flight_time) = '2025-01-01'
	and a.name='Байкал'
