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