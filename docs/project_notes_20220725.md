# Project Notes
2022-07-25

This is where random musings, thoughts and ideas will live. This is where I do my thinking. 

---

I was getting caught up with trying to figure out how I was going to pull all the data from the API endpoints. Then I reminded myself, hold on buddy, one (business) requirement at a time. You're not doing yourself a favour by taking on too many things at once. On top of that, I'm thinking about pulling in data whose purpose I'm not really clear on at all! This is an issue in terms of data quality, governance and efficiency. Why would I bother to design and develop a system if I'm not even sure what the purpose of it is?

This is just a long way of saying let me focus on the transfers data pulls and then see what sort of ancillary questions I ask related to the data and then think about pulling that data as well! 

I finished reading Kimball's Data Warehouse Toolkit. Well at least the information bits, but not the case studies I think I should make a habit of looking at one case study a week or something like that. I'm still exploring the space, so I shouldn't pigeon-hole myself into an area of interest.

In any case, think about the requirement of pulling transfers data, perhaps even streaming for funsies in the future. Is going to be the requirement I work on...

I will work on making sure I can pull the data and write to a database, from there I will write cron (sp?) jobs to schedule data pulls at regular intervals.

Possible business questions:
- Most basic question I'd like to answer is what are the trends in net transfer for each PL player over a given time frame?

More Advanced Questions
- How much value is a player providing? What is there points to price ratio?
- How about effective ownership over time?
- Can I introduce new KPIs to help FPL players make decisions?
- Maybe I need to jump into Jupyter Notebook to run some analysis on historical data...

Other thoughts:
- I need to figure out the logic behind the cron jobs
- How do I design the system so that it pulls the newest file and writes to the database? 
	- I'm thinking something like have the program read whether or not the file has been pulled before...
	- If not then pull it
	- Example, if filename in list of filenames pulled, then dont' pull, else pull
	- The only issue with it is that the list is going to get larger and larger, which will make the search take longer and longer
	- However, maybe what I can do is save the time of the last pull, and if the timestamp of the filename name is later than the timestamp of the last pull then write to the database...