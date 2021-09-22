#  AI for societal challenges: A bibliometric analysis

## Digital transformation vs sustainability

### University of Strasbourg

### I. Presentation (by Stefano Bianchini)

   #### 1. Unlike past technological revolutions, digital transformation comes at a time of profound interdependent changes 
   including global warming, migration, an aging population, and new geopolitical tensions. 
   It will cause great stress. 
   on our economic, social and political systems, creating some preconditions for 
   sustainability, but undermining others. Sustainability can be understood as the result of a balanced 
   articulation of the three pillars – social, economic, environmental – including good governance.  
     

   #### 2. Sustainable development goals by the UN :
   ![](img/sdg.jpg)
   #### 3. AI for good?
      1. Some Pros
     Support green transition through smarter energy management
     Virtual and augmented realities empowered by AI can enable transnational communication networks, 
     thereby stimulating cultural diversity.
      2. Some Cons
      Data processing requires (massive) computing centres, which are high energy intensive and thus 
      responsible for a high carbon footprint.
      Digitally-driven configurations of the economic, social, political and cultural systems may 
      disempower individuals and amplify disparities.
   #### 4. The project 
      1. Mapping the inter-linkages between digital transformation and the Sustainable Development Goals (SDGs) 
      in research and innovation.
      2. Assessing the contribution – i.e., enabling, neutral, or inhibiting – of digital transformation on 
      the achievement of the SDGs and the targets therein. (Sentiment analysis)  
        

### II. Method  

#### 1. We do queries on Web of Science (WoS), choosing one sdg at the time. First one, is the climate action sdg (number 13)
Adapting the query found here (https://aurora-network-global.github.io/sdg-queries/query_SDG13.xml) to WoS 
(see no_code/query_climate_action.txt), we found about 470k articles related to Climate action on WoS.
What we download is not the text of the articles, but metadatas such as Authors, Abstract etc...
(see data/field_tags.csv)
It would be extremely tedious to download them manually and the API is not available therefore
we use a very simple auto-clicker (auto_clicker.py + mouse_pos.py).
Web of science refuses to download more 100k results at the time, therefore it
is necessary to downlaod the data by chunks of 100k or else results. We chose to download by 
filtering the date (2010-2013, 2014-2015, 2016-2017, 2018,2019,2020,2021).
Each folder is about or less than 100k results.  

#### 2. We use a couple of scripts (reading_cleaning.py, fixed_languages_country_year_no_dups.py) to read, clean and 
create a unique csv file containing all the data.
  - Only 8 variables are kept (Publication Type, Authors, Title, Language, Keywords, Abstract, Address, Year).
  - Many rows contain errors, and we choose to remove them rather than trying to fix them.
  - we drop every single row that is missing on of those variables. 
    ```python
    df = pd.read_csv(file_path, sep='\t', encoding='utf-8', index_col=False, error_bad_lines=False)
    # we keep only a handful of useful variables, to avoid bugs, we only keep the file if our 8 variables
    # are present.
    columns = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY']
    set_columns = set(columns)
    if set_columns.issubset(set(df.columns)):
        # making sure to only keep rows that have the proper columns
        df = df[['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY']]
    else:
        continue

    ```
  - we exclude problematic lines ```error_bad_lines=False```.
  - We only keep a handful of languages, and remove every row that does not have a correct language.
    ```python
    # Only keeping main languages to filter wrongly parsed rows
    lst_of_language = ["English", "Spanish", "Portugese", "Chinese", "French", "Russian", "German",
                       "Korean", "Turkish",
                       "Polish", "Czech", "Japanese", "Italian"]
    condition = df.LA.isin(lst_of_language)
    df = df[condition]
    ```
  - Address are transformed to country. Tweaks are necessary to standardise the country name in order to generate 
plotly maps.
    ```python
    # fixing countries
    df['C1'] = df['C1'].apply(lambda x: x.split(", ")[-1] if "USA" not in x else "United States")
    df['C1'] = df['C1'].replace(['Peoples R China'], 'China')
    ```
  - We found about 30k duplicated (6%) which are removed.
    ```python
    # Dropping duplicated
    print(df.duplicated().sum())
    df = df.drop_duplicates()
    ```
  - Some error on the year column, we need to make date is in the correct range
    ```python
    # Fixing Year of Publication
    condition_year = df.PY > 2009
    df = df[condition_year]
    ```

#### 3. Remarks about the method
We are dealing with a very large corpus with **470 928** articles related to climate action 
only. Therefore, we made to choice to be rash regarding the selection, only keeping
rows that does not countain any Errors. As a results, we have a total of 
**349 497 non-null rows** that is to say, we have lost 25.6% of the articles.
  

### III. Filtering using AI keywords
   #### 1.Two ways to filter
First way is to create a new dataframe that contains only articles related to both 
climate action and artificial intelligence. The second way is to create a new column "AI'
that reads True if it is related to AI and False if not. 
We have done both methods:  

- The filtered new dataframe is found here (data/clean_data/full_data_filtered.csv), 
it presents the advantage to be way lighter than the full dataframe.
- The full dataframe with a AI column is found here: data/clean_data/full_data_AI_col.csv
It is way bigger (1.3 GB).
  
#### 2. How to filter
- We use a list of words related to IA (available here : data/ai_keywords.csv).   
This list includes :  

_Artificial Intelligence, 
Automated reasoning, 
Backpropagation, 
Computer vision, 
Data mining, 
Data science, 
Deep learning, 
Expert system*, 
Face detection, 
Feature extraction, 
Generative adversarial network*, 
Gesture recognition, 
Image classification, 
Image recognition, 
Image segmentation, 
Information retrieval, 
Intelligent machine*, 
Kernel machine, 
Knowledge representation, 
Machine intelligence, 
Machine learning, 
Machine translation, 
Meta-learning, 
Multilayer perceptron*, 
Natural language processing, 
Neural net*, 
Object detection, 
Object identification, 
Object recognition, 
Pattern recognition, 
Pose estimation, 
Reinforcement learning, 
Semantic search, 
Semi-supervised learning,
Sentiment analysis, 
Speech recognition,
Statistical learning, 
Supervised learning, 
Text classification, 
Transfer learning, 
Transformer network*, 
Unsupervised learning, 
Voice recognition._

- To filter, we, then, create a new column aggregating all the text columns. 
(Title + Abstract + Keywords).
    ```python
    df["TXT"] = df["TI"] + " " + df["DE"] + " " + df["AB"]
    ```
- We generate a pattern of all the AI related keywords.
    ```python
        keyword_csv = pd.read_csv("data/ai_keywords.csv", sep="\t", encoding="utf-8")
        # Put these keywords in a list and create a patter
        lst_ai = []
        for keyword in keyword_csv["Artificial Intelligence"]:
            lst_ai.append(keyword)
    
        pattern = '|'.join([f'(?i){keyword}' for keyword in lst_ai])
    ```
- We can then filter using a condition:
    ```python
    condition = df.TXT.str.contains(pattern, na=False)
    ```
- Finally, creating a new database is done like this :
    ```python
        df = df[condition]
    
        columns = ['PT', 'AU', 'TI', 'LA', 'DE', 'AB', 'C1', 'PY', 'TXT']
        df.to_csv("data/clean_data/full_data_filtered.csv", columns=columns, header=True, index=False, sep='\t')
    ```
- Whereas, we add a new column "AI" True/False, using the numpy "where" keyword like this (see "create_new_col_AI.py" script:
```python
df['AI'] = numpyp.where(condition, True, False)
```

#### 3. Results
From **382 742** rows related to climate change to **5 899** rows related to both _climate action_ and Artificial Intelligence.  
**1.5%** of the corpus only is related to AI.
