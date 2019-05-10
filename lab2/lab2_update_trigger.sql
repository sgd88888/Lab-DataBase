use weibo;
go
drop trigger if exists refuse_self_thumb
go
create trigger refuse_self_thumb
on thumb
instead of insert, update
as
begin
	if exists (
		-- find blog which has thumb.bid = uid in blog table
		-- from thumb table and blog table
		select *
		from inserted, mblog
		where inserted.bid = mblog.bid
		and inserted.uids = mblog.uids
	)
	begin
		-- print error
		-- print 'error, you cannot give the thumbs to blogs which belongs to yourself'
		print 'error, 不能给自己点赞'
	end
	else
	begin
		-- insert
		insert into thumb
		(uids, bid)
		select uids, bid
		from inserted
	end
end
go