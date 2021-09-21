# projet_transdisciplinaire
##Digital transformation vs sustainability


    
1. Web of Science query related to SDG 13 : Climate action
    As exhaustive as possible,about 470k results between 2010 and 2022
    More info on the quesry can be found here :  
    https://aurora-network-global.github.io/sdg-queries/query_SDG13.xml
    The query looks like this : 
```
(

TS =  ( ( "climat*" NEAR/3 "anthropogenic*" ) OR ( "climat*" NEAR/3 "action*" ) OR ( "climat*" NEAR/3 "adapt*" ) OR
 ( "climat*" NEAR/3 "biodiversity" ) OR ( "climat*" NEAR/3 "carbon*" ) OR 
( "climat*" NEAR/3 "change*" ) OR ( "climat*" NEAR/3 "crisis" ) OR ( "climat*" NEAR/3 "deforestati*" ) 
OR ( "climat*" NEAR/3 "desertificati*" ) OR ( "climat*" NEAR/3 "ecolog*" ) OR 
( "climat*" NEAR/3 "environment*" ) OR ( "climat*" NEAR/3 "GHG" ) OR ( "climat*" NEAR/3 "global change" ) OR
 ( "climat*" NEAR/3 "greenhouse gas*" ) OR 
( "climat*" NEAR/3 "hazard*" ) OR ( "climat*" NEAR/3 "reforestati*" ) OR ( "climat*" NEAR/3 "variabilit*" ) OR
 ( "climat*" NEAR/3 "warming" ) OR ( "climat*" NEAR/3 "water stress" ) OR 
( ( "climate" ) AND ( ( "Paris" ) NEAR/3 ( "agreement" OR "COP21" ) ) ) OR ( ( "climate" ) AND
 ( ( "Kyoto" ) NEAR/3 ( "protocol" ) ) ) OR ( "climate action*" ) OR ( "Climate Effect*" ) OR
( "Climate Model*" ) OR 
( "Climate Variability" ) OR ( "Climate Variation*" ) OR ( "climate-driven" ) OR ( "Climatology" ) OR
 ( "eco-innovation*" ) OR ( "environmental change*" ) OR ( "Environmental Impact" ) OR ( "Global Climate" ) OR 
( "global warming" ) OR ( "Greenhouse Effect*" ) OR ( "Green-house Effect*" ) OR ( "Greenhouse Gas*" ) OR
 ( "Green-house Gas*" ) OR ( ( "sea level*") AND ( "chang*" OR "rising" ) ) )
OR

TS =  ( (( "climat*" OR "natural disaster*") NEAR/3 "resilien*" ) ) OR

TS =  ( ( "reduc*" ) NEAR/3 ( "disaster*" ) NEAR/3 ( "risk*" ) ) OR

TS =  ( ( "disaster*" ) NEAR/3 ( ( "number" NEAR/3 ( "death*" OR "people" ) ) OR ( "missing person*" ) OR ( "human loss*" ) ) )
OR

TS =  ( ( ( "climat*" ) NEAR/3 ( "polic*" OR "strateg*" OR "plan" OR "plans" OR "planning" ) ) )
OR

TS =  ( ( "climate" ) NEAR/3 ( "information" OR "awareness" OR "educat*" OR "teach*" OR "learn*" ) )
OR

TS =  ( ( "climate" ) NEAR/3 ( "fund" OR "funds" OR "funding" OR "money" OR "dollar*" OR "commitment" OR "capitali*") ) OR

TS =  ( ( "UNFCC" OR "United Nations Framework Convention for Climate Change" ) )
OR

TS =  ( ( "climate" ) AND ( ( "assist*" OR "support*" OR "aid" OR "program*" OR "development*" OR 
"capacity*" ) NEAR/3 ( "develop* countr*" OR "least developed countr*" OR "small island*" ) ) )
)


``` 

2.  Method
- It would be extremely tedious to download everything by hand so
we made a very simple auto-clicker (auto_clicker.py).
- Web of science refuses to download more 100k results at the time, therefore it
is necessary to downlaod by chunks. We chose to download by 
filtering the date (2010-2013, 2014-2015, 2016-2017, 2018,2019,2020,2021)
Each folder is about or less than 100k results.
- We use a script (reading_cleaning.py) to read, clean and create a unique csv file with all the data
regarding climate action.
  - Cleaning process is as follow, we only 8 variables that interest us.
  - we drop every single row (= scientific paper) that is missing on of those
variables.
  - we exclude problematic lines ```error_bad_lines=False```.
  - Finally, we concatenate all dataframes into a big one that we save as a csv.

3. Remarks about the method
We are dealing with a very large corpus with **470 928** articles related to climate action 
only. Therefore, we made to choice to be rash regarding the selection, only keeping
rows that does not countain any Nan values. As a results, we have a total of 
**384 361 non-null rows** that is to say, we have skimmed 18% of the articles.


1. Basic information about the corpus
   1. Language
    ```python
    df.groupby("LA").sum()
    ```