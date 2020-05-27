/*
this query is going to see how well I can compile the team rosters
without the need for more web scraping.
*/

select distinct(playerID), name from boxscores where team = 'TOR' and date >'2019-10-01' and date > '2019-11-30';