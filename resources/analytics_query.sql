/*
Which age category have bought the most expensive TVs (above 1500)?
Under 30, from 30 to 40 or above 40?
*/
WITH category_buy AS (
    SELECT
        CASE
            WHEN age<30 THEN "under 30"
            WHEN age>=30 AND age<=40 THEN "from 30 to 40"
            ELSE "above 40"
        END AS age_category,
        price
    FROM `curated.customers` c
    JOIN `curated.sales` s
    ON c.first_name=s.first_name AND c.last_name=s.last_name
    WHERE price > 1500
),
buy_stat AS (
    SELECT
        age_category,
        count(price) as buy_count
    FROM category_buy
    group by age_category
)
SELECT age_category FROM buy_stat
WHERE buy_count=( SELECT max(buy_count) FROM buy_stat )
;
