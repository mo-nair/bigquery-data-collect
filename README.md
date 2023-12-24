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

Due to information shortages, we will begin to work locally on BigQuery, instead of relying on GitHub Archive. Prior to 2015, only actor logins were used to identify actors. Actor IDs had not been assigned to users. This resulted in slightly different changes in the scripts we used.

*mariia explain how you retrieved the individual data files for each month of 2013 and 2014*

On any IDE, run the following Python script:
[Project Ethereum - 2013 and 2014 Merge Code](<Code/Project Ethereum - 2013 and 2014 Merge Code.py>)

This script combines each CSV file into one called AllData20132014.csv.

*mariia used her own SQL script to generate another merged file maybe have that instead*

On BigQuery, click add to upload a local file. Select AllData20132014.csv and a dataset to create the table. Then, run the following script:[Project Ethereum - 2013 and 2014 All Events Code](<Code/BigQuery/Project Ethereum - 2013 and 2014 All Events Code.txt>) 

Replace this line, `from ethereum-project-383415.Data.Data20132014Merged`, with your project and dataset name. My project is named `ethereum-project-383415` and my dataset is named Data. This can vary, depending on user preferences.

This should generate twenty-eight different events for the years 2013 and 2014. Save the result as a CSV file.

## Core Users

### 2015 to Present

To test our first hypothesis, run the following Python script using an IDE: [Project Ethereum - Core Users](<Code/Project Ethereum - Core Users.py>)

Change the following lines: `df = pd.read_csv('Data2015.csv', low_memory = False), merged_df[columns_to_display].to_csv('Data2015CoreUser.csv', index = False)` to match the corresponding year. Repeat the script for 2016, 2017, 2018, 2019, 2020, 2021, 2022, and 2023. A file containing the results for each year should be generated in the chosen directory.

### 2013 and 2014

In the CSV file that contains all the events for 2013 and 2014, create an empty column called actor_id to the right of date1 and to the left of actor_login.

Now, run the following Python script using an IDE: [Project Ethereum - 2013 and 2014 Core Users](<Code/Project Ethereum - 2013 and 2014 Core Users.py>)

actor_login is used as the unique identifier instead of actor_id.

## Shiny Visualization

The website can be found at the following URL: https://alinachen.shinyapps.io/App-1/. The code for the application can be found in [Project Ethereum - Visualization.R](<Code/Project Ethereum - Visualization.R>). 

The website allows the user to choose how they want the data to be aggregated (days, weeks, months, and years). The user can also select a custom date range and the variable the user wants to compare time to. If the custom date range selected cannot be aggregated, for example trying to aggregate five days monthly, no data will be displayed.

The website also allows the user to customize the graph, giving them an option to change the color of the line and whether it is solid or dashed. You can also choose to filter out bots from the displayed results by clicking the checkmark next to “Exclude bots?”.

For a working website, you must define the user interface and the server.  When writing the script for the website, remember that the CSV file must be read outside of the definitions for the user interface and the server. The Shiny tutorial found at https://shiny.posit.co/r/getstarted/shiny-basics/lesson1/index.html can be completed for assistance. Website details can be found within the script.

The CSV file is kept locally, so the user does not need to upload a file themselves. The CSV should be kept in the same directory as your R script. It can be found under the name Data_AllYears_Merged.csv.

Please email alinachen2028@gmail.com if you encounter any issues.
