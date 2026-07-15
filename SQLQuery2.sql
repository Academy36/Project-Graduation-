use Export_project;

/*
1-What is the global market size for Hydrogen Peroxide?*/
select sum (Value_imported_in_2024_USD_thousand) as Global_Market_size
from Importers;


/*
2-Which countries are the world’s leading importers? Top importer in usd 10 country */ 

select  top 10 
Importers,Value_imported_in_2024_USD_thousand
from Importers
order by Value_imported_in_2024_USD_thousand
desc;

/*
3-Which regions have the highest demand growth*/
select 
Region,
AVG (Annual_growth_in_value_between_2020_2024) as Avg_Growth
from Importers
group by Region
order by AVG (Annual_growth_in_value_between_2020_2024)
desc;
/*
4-conc of  supplier per region*/
select 
Region,
round(AVG (Concentration_of_supplying_countries),2) as Conc_of_supplier
from Importers
group by Region
order by AVG (Concentration_of_supplying_countries)
Asc;

-------------------------------------

select top 20
Importers , Value_imported_in_2024_USD_thousand 
from Importers
where Region in ('Middle East' ,'Africa')
order by Value_imported_in_2024_USD_thousand 
desc;

select top 20
Importers , Annual_growth_in_value_between_2020_2024
from Importers
where Region in ('Middle East' ,'Africa')
order by Annual_growth_in_value_between_2020_2024 
desc;

 
 select
 Target_Country
 from Target
  where (Egypt_Exported_to = 1)
;
----------------------

Create view TopImporteres As
select top 20
Importers , Value_imported_in_2024_USD_thousand 
from Importers
where Region in ('Middle East' ,'Africa')
order by Value_imported_in_2024_USD_thousand 
desc;

Create View MostDynamic As

select top 20
Importers , Annual_growth_in_value_between_2020_2024
from Importers
where Region in ('Middle East' ,'Africa')
order by Annual_growth_in_value_between_2020_2024 
desc;

Create View ActualMarket As 
 select
 Target_Country
 from Target
  where (Egypt_Exported_to = 1)
;

Create view All_unique_Country As

Select Importers 
from TopImporteres
union
select Importers
from MostDynamic
union
select Target_Country
from ActualMarket;

/*SELECT * FROM All_Unique_Country;*/
-------------
Select 
U.Importers,

Case when T.Importers is not null then 'Yes' else 'No' end as Top_Importer_Countries,
Case when D.Importers is not null then 'Yes' else 'No' end as Most_Dynamic_Countries,
Case when A.Target_Country is not null then 'Yes' else 'No' end as Exported_Before,

(
        CASE WHEN T.Importers IS NOT NULL THEN 1 ELSE 0 END +
        CASE WHEN D.Importers IS NOT NULL THEN 1 ELSE 0 END +
        CASE WHEN A.Target_Country IS NOT NULL THEN 1 ELSE 0 END
    ) AS Criteria_Met



from All_Unique_Country U
left join TopImporteres T
on U.Importers= T.Importers
left join MostDynamic D
on U.Importers= D.Importers
left join ActualMarket A
on U.Importers= A.Target_Country

where
  (
     Case when T.Importers is not null then 1 else 0 end +
      Case when D.Importers is not null then 1 else 0 end +
     Case when A.Target_Country is not null then 1 else 0 end 
)>=2

ORDER BY Criteria_Met DESC;
--------------------------------------------------------------
/* ph3 the most competitative countries to our target market*/

select top 20
C.Compitatores,
round(sum (M.Market_Share),2) As Total_Market_Share
from Market_share M
join Compeitaters C 
on C.CID=M.C_ID
group by C.Compitatores
order by Total_Market_Share desc;

---------------------------------------------------------------
Create View Top_10Competing_Country As
select top 10
C.Compitatores,
round(sum (M.Market_Share),2) As Total_Market_Share
from Market_share M
join Compeitaters C 
on C.CID=M.C_ID
group by C.Compitatores
order by Total_Market_Share desc;

/*select*from Top_10Competing_Country;*/
-----------------------------------------
/*ph4 Comparative Advantage Analysis*/

select
I.Unit_value_USD_unit,
I.Average_distance_of_supplying_countries_km ,
cast(I.Average_tariff_estimated_applied_by_the_country as decimal(10,2)) as tariff,
I.Importers
from Importers I
join Top_10Competing_Country 
on I.Importers=Top_10Competing_Country.Compitatores

----------------------------------
/*ph5*/
with autoscoring as(
select
T.Target_Country,
T.Market_Size,
T.Growth,
T.Logistics,
T.Tariffs,
ntile(5) over(order by T.Market_Size asc )as Size_Score,
ntile(5) over(order by T.Growth asc )as Growth_Score,
ntile(5) over (order by T.Logistics desc ) as Logistics_score,
ntile(5) over (order by T.Tariffs desc) as Tariffs_Score
From Target t
),
FinalAttractiveness As(

select
Target_Country,
Market_Size,
Growth,
Logistics,
Tariffs,
Size_Score,
Growth_Score,
Logistics_score,
Tariffs_Score,
Cast (
(Size_Score *.30)+
(Growth_Score * .30)+
(Logistics_score*.20)+
(Tariffs_Score*.20)
as decimal (10,2)) as Final_Attractive_Score
from autoscoring)
select
Target_Country,
Size_Score,
Growth_Score,
Logistics_score,
Tariffs_Score,

Case 
when Final_Attractive_Score >=4 then 'periority'
 when Final_Attractive_Score Between 2.5 and 3.9 then 'Long_Term_Opprtiunity'
Else 'Low_Interest'
End As Market_Category
from FinalAttractiveness
order by Final_Attractive_Score desc;
