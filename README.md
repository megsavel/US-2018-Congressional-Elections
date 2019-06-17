# Candidate Self Presentation Project

This project uses web scraping and machine learning to analyze how candidates presented themselves and their issue stances to voters in the 2018 election. This is an ongoing project, and as such, data files are not provided.


## Web Scraping

- Using csv files created from public candidate filing records for candidates, this project scrapes every available campaign website produced for U.S. Congressional Elections in 2018.
- Those csv files are not provided, but are used by house_bios.py, house_issues.py, senate_bios.py, and senate_issues.py to scrape every campaign website.

## Keeping biographies separate from issue pages

- As "About Me" pages and "Issue" pages are quite different, their information is kept separate for this project.
- Files are named logically to reflect this separation.

## Creating DTMs from the "About Me" pages
- In order to use the scraped information in ongoing machine learning projects, Document Term Matrices (DTMs) were created to easily store the data collected.
- These DTMs are created by HouseDTM.py and SenateDTM.py.
- These DTMs are used to create structural topic models, but are not provided here due to the ongoing nature of this work.

Questions or requests for data can be made to meg.m.savel@gmail.com.

