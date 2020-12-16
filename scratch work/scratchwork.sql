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
select most recent article title/content before game date
*/

select title, content, date, availData2.home, availData2.away, availData2.gameDate 
from rotoworld
inner join availData2
on rotoworld.nbaID = availData2.nbaID
where rotoworld.date < availData2.gameDate
group by title, content, date, gameDate, rotoworld.nbaID, availData2.home, availData2.away
having max(rotoworld.date)
limit 1;
