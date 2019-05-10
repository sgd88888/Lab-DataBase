use weibo;
go
drop table if exists fans_3;
create table fans_3(
	uids int primary key,
	names char(30) not null,
	sex char(2) not null,
	byear int not null,
	city char(30) not null
);
insert into fans_3
(uids, names, sex, byear, city)
select users.uids, users.names, users.sex, users.byear, users.city
from users, follow
where users.uids = follow.uids and follow.uidfled = 3