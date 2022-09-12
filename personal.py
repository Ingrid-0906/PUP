# -*- coding: utf-8 -*-
"""personal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gkmsWjvXEUEpCqFbd58VOjqOAP_izUTO
"""

import pandas as pd

url_personal = 'https://media.githubusercontent.com/media/Ingrid-0906/Obiwan_2022/main/CSVFiles/meta_Health_and_Personal_Care.csv?token=AWDSUEQZ64TBJZ7BCU7B5DTDD7HJQ'
df = pd.read_csv(url_personal)
df = df.loc[:,['title','categories']]

url_feed = 'https://media.githubusercontent.com/media/Ingrid-0906/Obiwan_2022/main/CSVFiles/metadata_Feeding_PERSONAL_CARE.csv?token=AWDSUERHNUMCFVEGCO5IZF3DD7HTM'
feed = pd.read_csv(url_feed)

"""# Original data"""

# Splititng the categories into columns
def get_columns(categ):
  try:
    return ' -> '.join(eval(categ)[0])
  except IndexError: # Error if the outer list is empty
    return 'no_category'
  except TypeError: # Error if the outer list is missing
    return 'no_category'

# Create column for category path
df['category_path'] = df['categories'].apply(get_columns)

# Exclude data where title or category is missing
df_0 = df[df['category_path'] != 'no_category']

# Splitting into columns
df_1 = pd.DataFrame(df_0['category_path'].str.split(' -> ').values.tolist())

df_1['title'] = df_0['title']

# Dropping the products with les classes -CHANGE HERE AFTER THE SCARPPING!!!
df_1 = df_1.dropna(subset=['title'], axis=0)

df_1 = df_1[df_1[1].isin(['Health Care','Vitamins & Dietary Supplements','Personal Care','Baby & Child Care','Sexual Wellness'])]
df_1 = df_1.loc[:,['title',1,2]]

"""# Feeding data"""

# Splititng the categories into columns
def get_columns_feed(categ):
  try:
    return ' -> '.join(eval(categ))
  except IndexError: # Error if the outer list is empty
    return 'no_category'
  except TypeError: # Error if the outer list is missing
    return 'no_category'

# Create column for category path
feed['category_path'] = feed['category'].apply(get_columns_feed)

# Exclude data where title or category is missing
feed_0 = feed[feed['category_path'] != 'no_category']

# Splitting into columns
feed_1 = pd.DataFrame(feed_0['category_path'].str.split(' -> ').values.tolist())

feed_1['title'] = feed_0['title']

# Dropping the products with les classes -CHANGE HERE AFTER THE SCARPPING!!!
feed_1 = feed_1.dropna(subset=['title'], axis=0)

feed_1 = feed_1.loc[:,['title',0,1]]
feed_1 = feed_1.rename(columns={0:1, 1:2})
feed_1[:2]

# Linking both datas
df_1 = pd.concat([df_1,feed_1])

# Clear null values
data_personal = df_1[~df_1[2].isnull()]

