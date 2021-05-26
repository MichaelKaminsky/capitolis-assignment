# capitolis-assignment
## Database
For purpose resolving this test I used PostgreSQL DB, 
its credentials I put in separately attached `.env` file.

## Part 1
For the first (sql) part of the assignmet have been created tables named
`organization`, `trades`, `trades_1` and `organization_1` 
with the input data as described in the assignment.

This part's solution I put in `capitolis_test_part_1.sql` file.

## Part 2
You should replace `.env` file with the attached `.env` file's content.

To run the code from the local first create conda environment with

`conda env create -f environment.yml`

and set up the created `capitolis-assignment` conda environment 
as the active interpreter.

Then run `python data_pipeline.py`.

The code has been configured to run at Mon-Fri every week 
at 16:00 UTC that use to be one hour after the site should make 
the daily update. It writes the fetched data into `exchange_rates` table.

If you want to run the code on demand without of the scheduler
run `daily_exchange_rates_etl()` function from `data_pipeline.py`

The asked for this part quiries I put into `capitolis_test_part_2.sql` file.

Also I created and tested `Dockerfile` for running in Docker.