/*
this query is going to see how well I can compile the team rosters
without the need for more web scraping.
*/

select distinct(playerID), name from boxscores where team = 'TOR' and date >'2019-10-01' and date > '2019-11-30';

/*
return the first entry for all players with an entry in rotoworld
*/

select * from rotoworld as r2
inner join 
    (select name, nbaID, playerID, min(date) as date from rotoworld group by name, nbaID, playerID) as r1
on r2.playerID = r1.playerID and r2.date = r1.date; 

/*
all traded players this season and date of 1st game on a new team
*/

select b1.nbaID, b1.name as n, min(b2.date) as d2, b1.team
from boxscores as b1
inner join boxscores as b2
on b1.nbaID = b2.nbaID 
and b1.team != b2.team
and b1.date > '2019-10-01'
where  b1.date < b2.date
group by b1.name, b1.team, b1.nbaID

select b1.nbaID, b1.name as n, min(b2.date) as d2, b1.posTeam
from rotoworld as b1
inner join rotoworld as b2
on b1.nbaID = b2.nbaID 
and b1.posTeam != b2.posteam
where  b1.date < b2.date
group by b1.name, b1.posTeam, b1.nbaID

/*
set played column in availData
*/

update availData as A
inner join boxscores 
on A.nbaID=boxscores.nbaID and A.gameDate = boxscores.date
set A.played = 1



