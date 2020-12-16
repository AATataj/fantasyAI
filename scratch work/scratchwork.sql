/*
this query is going to see how well I can compile the team rosters
without the need for more web scraping.
*/

select distinct(playerID), name from boxscores where team = 'TOR' and date >'2019-10-01' and date > '2019-11-30';

select count(distinct(nbaID)) from rotoworld;


select distinct(playerID) from rotoworld

select * from rotoworld as r2
inner join 
    (select name, nbaID, playerID, min(date) as date from rotoworld group by name, nbaID, playerID) as r1
on r2.playerID = r1.playerID and r2.date = r1.date; 

