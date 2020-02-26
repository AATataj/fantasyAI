create table rotoworld (name varchar(100), posTeam varchar(100), title varchar(1000), content varchar(5000), date varchar(30), playerID int(11))

load data local infile "/var/lib/mysql-files/rotoworldTemp.csv" into table rotoworld 
fields optionally enclosed by '"' 
terminated by ',' 
lines terminated by '\n'

create table rotoworld2 (name varchar(100), posTeam varchar(100), title varchar(1000), content varchar(5000), date datetime, playerID int(11))

insert into rotoworld2 (name, posTeam, title, content, date, playerID)
select name, posTeam, title, content, STR_TO_DATE(date, '%b %d, %Y, %h:%i %p ET"'), playerID
from rotoworld

update rotoworld 
inner join playerHashes on lower(rotoworld.name) = lower(playerHashes.name)
set rotoworld.playerID = playerHashes.playerID

select max(date) from rotoworld

update rotoworld
inner join 
(select name, dob, playerID
from playerHashes
    inner join  
    (select name as named, max(dob) as Dateob, count(name) 
    from playerHashes 
    group by name 
    having max(dob)) 
    as list 
on list.named = playerHashes.name and list.Dateob = playerHashes.dob) as joined
on joined.name = rotoworld.name
set rotoworld.playerID = joined.playerID
where rotoworld.playerID is null


update rotoworld
set name = REPLACE(name, 'JR.', '')

update rotoworld 
set name = CASE WHEN name <> 'JOEL EMBIID' THEN REPLACE(name, 'II', '') ELSE 'JOEL EMBIID' END

update rotoworld 
set playerID = 1919 
where name = 'LUKA DONCIC'

insert into playerHashes (name, dob)
select distinct (name), date_sub(date_sub(date, interval cast(substr(age, 1, 2) as signed) year), interval cast(substr(age, 4, 3) as signed) day) as dob
from boxscores2
where playerID is null
group by name, dob

ALTER TABLE playerHashes ADD PRIMARY KEY (playerID)
ALTER TABLE playerHashes MODIFY COLUMN playerID INT auto_increment

