# Readme
Overview: this readme aims to go through the steps that help you navigate the ethereum OSS development analysis. 

We analyze All Event by first running SQL query on Bigquery and retrieve activity data from Github Archive. We secondly analyze core users by Python. Lastly, we use R for visualization.

Side note: because of information shortage, we analyze "2013 & 2014" differently from "2015 to present".

The final output data is stored in "Data" folder.

The step-by-step procedures are listed below. 


# Ethereum Project: Data Collection Manuscript
Alina Chen, Mariia Petryk, Jiasun Li

## All Events

You will need access to [BigQuery](https://cloud.google.com/bigquery), a data warehouse created by Google to manage and analyze data, and [GH Archive](https://www.gharchive.org/), a project that records and archives the public GitHub timeline.

### 2015 to Present

On BigQuery, run [Project Ethereum - All Events Code](<Code/BigQuery/Project Ethereum - All Events Code.txt>)

This script calculates and returns the frequency of twenty-eight different events: 

```
num_activities, num_dist_commits, num_dist_commitcomments, num_actors_pushevents, num_actors_pusheventscomment, num_dist_pullreqopened, num_dist_pullreqclosed, num_dist_pullreqAll, num_dist_pullreqcomments, num_actors_pullreq, num_actors_pullreqcomment, num_actors_pullreq_opened, num_actors_pullreq_closed, num_dist_issuesopened, num_dist_issuesclosed, num_dist_issuesAll, num_dist_issuecomments, num_actors_issues, num_actors_issuescomment, num_actors_allevents, num_actors_issues_opened, num_actors_issues_closed, num_forks_event, num_actors_forks, num_watch_event, num_actors_watch, num_releases, release_payload.
```

BigQuery should return a table with entries that specify repositories, dates, actor IDs, actor logins, and the different recorded events for the year 2015.

Save the results as a local CSV file. Repeat the script for 2016, 2017, 2018, 2019, 2020, 2021, 2022, and 2023 by changing the line
```sql
FROM (SELECT * FROM `githubarchive.month.*` WHERE _TABLE_SUFFIX BETWEEN '201501' AND '201512') t1 WHERE t1.repo.name LIKE 'ethereum/%'
```
accordingly. Save each result as a CSV file.

### 2013 and 2014

GitHub Archive data has a slightly different structure before 2015. For example, only actor logins are available to identify actors, but not actor.id. Also, repository links (repo.url) and names (repo.names) has different format. Therefore, we need to slightly modify the script to retrieve the data in the same structure as 2015 and later.

To collect data from 2014 and earlier, run the BigQuery script: [https://github.com/DARLresearchlab/bigquery-data-collect/blob/4fb5d727cf4988813f7a9bc4ffffca7d235d0785/Code/BigQuery/Project%20Ethereum%20-%202013%20and%202014%20All%20Events%20Code.txt] 

BigQuery should return a table with exactly same columns with twenty-eight different events as for 2015 and on. Save the result as a local CSV file.

## Exporting data from BigQuery

Google has 10 MB limitations to export data into local .csv file.
There are two options to export data effectively.
# Option 1
Query the data within smaller time increments, e.g., couple of months at a time, and export every resulting table. 

# Option 2
After querying the data, save the resulting table into a new BigQuery table.
Query the data from a newly created table by small chunks and export every chunk.
To keep track of already exported rows and make sure all rows are exported and none are missed, you may number the rows as follows.

CREATE TABLE NewTableName AS (
  select ROW_NUMBER() OVER (ORDER BY (SELECT 1)) as RowNum, *
  from TableName
  where TRUE
  order by RowNum)

SELECT *
FROM NewTableName
where RowNum between 1 and 40000
