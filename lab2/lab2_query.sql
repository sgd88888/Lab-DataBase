use weibo;
go

select users.uids, users.names, users.sex, users.byear, users.city
from follow, users
where follow.uidfled = users.uids and follow.uids in(
	select users.uids
	from users
	where users.names = '����'
	)
order by users.byear desc, users.uids asc

select mblog.bid, mblog.title, users.names
from mblog, users
where users.uids = mblog.uids and  mblog.bid not in
	(
		select bid from thumb
	)
order by mblog.title asc

select mblog.bid
from mblog, users, topday
where	mblog.uids = users.uids and
		topday.bid = mblog.bid and
		users.byear > 2000 and
		users.city = '�人'

select sub.uids
from sub
group by uids
having count(*) = any(select count(*) from label);

select uids, byear, city
from users
where byear not between '1970' and '2010'

select city, count(uids) '�û���'
from users
group by city

select city, byear, count(uids)
from users
group by  byear,city
order by city, byear desc;

select bid
from thumb
group by bid
having count(bid) > 10

select bid
from thumb, users
where	thumb.uids = users.uids and
		users.byear >=2000
group by bid
having count(bid) > 10

select topday.bid, count(*) as '����'
from topday
where topday.bid in (
	select bid
	from thumb, users
	where	thumb.uids = users.uids and
			users.byear >= 2000
	group by bid
	having count(bid) > 10
)
group by topday.bid

select distinct uids
from sub, label
where	sub.lid = label.lid and
		label.lname in ('��ѧ','����','��ѧ','����')

select bid, title, uids, pyear, pmonth, pday
from mblog
where	cont like '%������վ%' or
		cont like '%\_���пƼ���ѧ%'

select one.uids, two.uids
from follow one, follow two
where	one.uids = two.uidfled and
		one.uidfled = two.uids and
		one.uids > two.uids

select uids
from users
where not exists(
	select *
	from friends one
	where	one.uids='5'and
			not exists(
				select *
				from friends two
				where	two.uids = users.uids and
						one.fuid = two.fuid
			)
	)

select mblog.bid, mblog.title, b_l.lid
from topday, mblog, b_l
where	topday.bid = mblog.bid and
		mblog.bid = b_l.bid and
		pyear = '2019' and
		pmonth = '4' and
		pday = '20'

select one.uids, two.uids
from friends one, friends two
where	one.uids <> two.uids and
		one.fuid = two.fuid and
		one.uids < two.uids
group by one.uids, two.uids
having count(*) >= 3

drop view if exists topten;
go
create view topten as
select distinct topday.bid, mblog.title, users.uids, users.names, count(*) as liking
from topday, mblog, users, thumb
where topday.tyear = (select DATENAME(YYYY,GETDATE()))
	  and topday.tmonth = (select DATENAME(MM,GETDATE()))
	  and topday.tday = (select DATENAME(DAY,GETDATE()))
	  and topday.bid = mblog.bid
	  and mblog.uids = users.uids
	  and thumb.bid = mblog.bid
group by topday.bid, mblog.title, users.uids, users.names
go
