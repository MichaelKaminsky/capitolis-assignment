-- year uer/usd rates with min and max year rates
with usd_rate as (
	SELECT * FROM public.exchange_rates
	where currency_name = 'USD' and rate_date > now() - interval '1 year'
)
select * from usd_rate
join
(select currency_name, min(currency_rate_flt) min_year, max(currency_rate_flt) max_year from usd_rate group by 1) r
using (currency_name)
order by rate_date asc;

-- the most volatile rate within a single week in the past year.
with usd_rate as (
	SELECT * FROM public.exchange_rates
	where currency_name = 'USD' and rate_date > now() - interval '1 year'
)
SELECT week, min(currency_rate_flt), max(currency_rate_flt),
        max(currency_rate_flt) - min(currency_rate_flt) week_volatile
FROM usd_rate
group by week
order by week_volatile desc
limit 1;
