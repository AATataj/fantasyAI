scratch queries for formatting key tables to propert datatypes

creating playerHashes :
create table playerHashes2 (name varchar(100), dob date, playerID int NOT NULL AUTO_INCREMENT, PRIMARY KEY (playerID));

crreating boxscores:
create table boxscores3 (name varchar(100), age varchar(8), position varchar(5), date varchar(11), team varchar(6), homeAway varchar(2), opponent varchar(6), result varchar(2), started varchar(1), minutes varchar(3), fgm varchar(3), fga varchar(3), fgPer varchar(10), 2fgm varchar(3), 2fga varchar(3), 2fgPer varchar(10), 3fgm varchar(3), 3fga varchar(3), 3fgPer varchar(10), ftm varchar(3), fta varchar(3), ftPer varchar(10), orb varchar(3), drb varchar(3), trb varchar(3), ast varchar(3), stl varchar(3), blk varchar(3), tov varchar(3), pf varchar(3), pts varchar(3), gmsc varchar(10), playerID int)


create table boxscores2 (name varchar(100), age varchar(8), position varchar(5), date date, team varchar(6), homeAway varchar(2), opponent varchar(6), result varchar(2), started varchar(1), minutes int(11), fgm int(11), fga int(11), fgPer decimal(4,3), 2fgm int(11), 2fga int(11), 2fgPer decimal(4,3), 3fgm int(11), 3fga int(11), 3fgPer decimal(4,3), ftm int(11), fta int(11), ftPer decimal(4,3), orb int(11), drb int(11), trb int(11), ast int(11), stl int(11), blk int(11), tov int(11), pf int(11), pts int(11), gmsc decimal(4,3), playerID int(11))

insert into boxscores2 (name, age, position, date, team, homeAway, opponent, result, started, minutes, fgm, fga, fgPer, 2fgm, 2fga, 2fgPer, 3fgm, 3fga, 3fgPer, ftm, fta, ftPer, orb, drb, trb, ast, stl, blk, tov, pf, pts, gmsc) select name, age, position, STR_TO_DATE(date, '%Y-%m-%d'),
team, homeAway, opponent, result, started, CAST(minutes as signed int),CAST(fgm as signed int),CAST(fga as signed int),if (fgPer ='', NULL, CAST(fgPer as decimal(4,3))),CAST(2fgm as signed int),CAST(2fga as signed int),if (2fgPer ='', NULL, CAST(2fgPer as decimal(4,3))),CAST(3fgm as signed int),CAST(3fga as signed int),if (3fgPer = '', NULL, CAST(3fgPer as decimal(4,3))),CAST(ftm as signed int),CAST(fta as signed int),if (ftPer = '', NULL, CAST(ftPer as decimal(4,3))),CAST(orb as signed int),CAST(drb as signed int),CAST(trb as signed int),CAST(ast as signed int),CAST(stl as signed int), CAST(blk as signed int),CAST(tov as signed int),CAST(pf as signed int),CAST(pts as signed int),if (gmsc='', NULL, CAST(gmsc as decimal(4,3))) from boxscores3;

load data local infile "/var/lib/mysql-files/bballref.csv" into table boxscores3 fields terminated by ',' lines terminated by '\n' ignore 0 rows;

/home/slick/Documents/side\ coding/web\ scraping/MASTER.csv

insert into boxscores3 (name, age, position, date, team, homeAway, opponent, result, started, minutes, fgm, fga, 2fgm, 2fga, 3fgm, 3fga, ftm, fta, orb, drb, trb, ast, blk, tov, pf, pts) select name, age, position, STR_TO_DATE(date, '%d-%b-%Y'), team, homeAway, opponent, result, started, minutes, fgm, fga, 2fgm, 2fga, 3fgm, 3fga, ftm, fta, orb, drb, trb, ast, blk, tov, pf, pts from boxscores2;

select substr(age, 1,2) as years, substr(age, 4,3) as days from boxscores3 limit 2;

select name, cast(substr(age, 1,2) as signed) as years, cast(substr(age, 4,3) as signed) as days, date, makedate(year(date)-cast(substr(age, 1,2) as signed), day(date)-cast(substr(age, 4,3) as signed)) as dob from boxscores3 group by name, dob; 

date_sub(date_sub(date, interval (cast(substr(age, 1,2) as signed) year), interval (cast(substr(age, 4,3) as signed))) day

select name, cast(substr(age, 1,2) as signed) as years, cast(substr(age, 4,3) as signed) as days, date, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day) as dob from boxscores3 group by name, dob;

create table playerHashes (name varchar(100), dob date, playerID int auto_increment, primary key (playerID));

insert into playerHashes2 (name, dob) 
select distinct name, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day) as dob from boxscores2 group by name, dob;


insert into playerHashes2 (name, dob) 
select name, count(name) from playerHashes group by name having count(name)>1;


insert into playerHashes2 (name, dob) 
select name, max(dob) from playerHashes group by name having count(name)=4;

select * from playerHashes group by name having count(name)>3;

insert into playerHashes2 (name, dob)
select name, dob from playerHashes where playerID in (458,461, 711, 713, 716, 724, 727, 729, 788, 791,  853, 1675, 1678, 1899, 1902, 1921, 1924, 1948, 1951, 3073, 3076, 3309, 3312, 3337, 3340, 3559, 3562, 4063, 4065,  4708, 4711, 4983, 5103, 5106);

update boxscores 
inner join playerHashes on name=playerHashes.name 
and 
	(datesub(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as 		signed) year), interval cast(substr(age, 4,3) as signed) day)) = 1
   or 
	datesub(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as 		signed) year), interval cast(substr(age, 4,3) as signed) day)) = -1 
   or 
	playerHashes.dob = date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) 		year), interval cast(substr(age, 4,3) as signed) day));
set playerID = playerHashes.playerID;

update boxscores4 inner join playerHashes on name=playerHashes.name and (datesub(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) = 1 or datesub(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) = -1 or playerHashes.dob = date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day));
set boxscores.playerID = playerHashes.playerID;


update boxscores
select boxscores.name, playerHashes.playerID from boxscores
update boxscores
inner join playerHashes
on playerHashes.name = boxscores.name and (
datediff(playerHashes., date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =0 or
datediff(boxscores.date, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =1 or
datediff(boxscores.date, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =-1
)
limit 4;

select boxscores4.name, playerHashes.playerID from boxscores4
inner join playerHashes
on playerHashes.name = boxscores4.name and (
datediff(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =0) limit 10;


update boxscores,
set boxscores.playerID = playerHashes.playerID
inner join playerHashes
on playerHashes.name = boxscores.name 
and (
datediff(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =0 or
datediff(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =1 or
datediff(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =-1
)
;

update boxscores4, playerHashes 
set boxscores4.playerID = playerHashes.playerID
where playerHashes.name = boxscores4.name
and (
datediff(playerHashes.dob, date_sub(date_sub(boxscores4.date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =0 or
datediff(playerHashes.dob, date_sub(date_sub(boxscores4.date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =1 or
datediff(playerHashes.dob, date_sub(dshowate_sub(boxscores4.date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =-1
);


update boxscores2
inner join playerHashes2
on playerHashes2.name = boxscores2.name 
set boxscores2.playerID = playerHashes2.playerID
where 
datediff(playerHashes2.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =0 or
datediff(playerHashes2.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =1 or
datediff(playerHashes2.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =-1
;


select distinct playerHashes.playerID, playerHashes.name 
from playerHashes
inner join boxscores
on playerHashes.playerID = boxscores.playerID
and (boxscores.date between '2012-10-30' and '2013-04-17');

insert into boxscores (stl) select if (stl ='', 0, CAST(stl as signed int)) from boxscores2;

select count(distinct(b1.date)) from boxscores as b1
inner join boxscores as b2 on
b1.team = b2.team and
b2.playerID = 2958 and
b1.date < '2018-01-18' and
b1.date >= '2017-10-01'

select count(distinct(date)) from boxscores
where 

-- All values with name is unique
select name, dob, playerID from playerHashes where name in (select name from playerHashes group by name having count(name)=1);
-- update based on straight name match out of the list of unique names
update nbaHashes t2
inner join (select name, dob, playerID from playerHashes where name in 
(select name from playerHashes group by name having count(name)=1)) as t1
on t2.name = t1.name
set t2.dob = t1.dob, t2.playerID = t1.playerID

-- find all sr's and jr's
-- not currently correct
select t1.name, dob, playerID
from (select name, dob, playerID 
	from playerHashes 
	where name in (select name from playerHashes group by name having count(name)=2)
) as t1
inner join 
(select name, college, nbaID from nbaHashes where name like '%Jr.') as t2
on t1.name = replace(t2.name, 'Jr.', '');