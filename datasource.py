# Libraries and Settings
import re
import sys
import warnings
import pandas as pd
import numpy as np
import unicodedata
import html

# Stopwords package
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# Split and vectorize them
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Opening data and taking the columns i need to proceed
df = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/Original_grocery_280k.csv")
df = df.loc[:,['title','category']]

# Opening feeding data
feed = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/metadata_Feeding_GROCERIES.csv")
feed[:2]

"""# Working with categories - Cleaning phase"""

# Splititng the categories into columns
def get_columns(categ):
  try:
    return ' -> '.join(eval(categ))
  except IndexError: # Error if the outer list is empty
    return 'no_category'
  except TypeError: # Error if the outer list is missing
    return 'no_category'

"""## Original data"""

# Create column for category path
df['category_path'] = df['category'].apply(get_columns)

# Exclude data where title or category is missing
df_0 = df[df['category_path'] != 'no_category']

# Splitting into columns
df_1 = pd.DataFrame(df_0['category_path'].str.split(' -> ').values.tolist())

df_1['title'] = df_0['title']

# Dropping the products with les classes -CHANGE HERE AFTER THE SCARPPING!!!
df_1 = df_1.dropna(subset=['title'], axis=0)

# Removing categories that actually does not exists
df_1[2] = df_1[2].replace({"20 easy prefilled Easter eggs with 3 candy assortments including Brach's Jellybeans and Chewy Lemonheads":"Candy & Chocolate Gifts",
                           "-Butlers -Creamy Toffees -Contains Milk & Soya & May Contain Traces of Nuts -Bagged, 125g":"Candy & Chocolate Bars",
                           "-The Connemara Kitchen -Coffee Fudge -Tin Package -160g":"Candy & Chocolate"})

# Changing the names accordingly to current year: 2022
df_1[2] = df_1[2].replace({'Coffee, Tea & Cocoa': df_1[3].values})
df_1[2] = df_1[2].replace({'Cocoa': 'Hot Chocolate & Malted Drinks'})
df_1[2] = df_1[2].replace({'Ice Cream & Novelties':'Ice Cream & Frozen Novelties'})

# Filling the child category if there is not a class
df_1[2] = df_1[2].fillna(df_1[1])

# Removing categories less than 10 products
counts = df_1[2].value_counts()
df_1 = df_1[~df_1[2].isin(counts[counts < 11].index)]

# Reseting index for all dataframe
df_1 = df_1.reset_index()
df_1 = df_1.loc[:,['title',1,2]]
df_1.head(2)

"""## Feeding data"""

# Create column for category path
feed['category_path'] = feed['category'].apply(get_columns)

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

# Changing column 1 / the mother
df_1[1] = df_1[1].replace({'Breakfast':'Breakfast Foods','Jams, Jellies & Preserves':'Jams, Jellies & Sweet Spreads'})

# Changing column 1 / the child
df_1[2] = df_1[2].replace({'Jams, Jellies & Sweet Spreads':'Jams, Jellies & Preserves',
                           'Beans':'Beans & Peas',
                           'Peas':'Beans & Peas',
                           'Bubble Tea Kits':'Bubble Tea Tapioca Pearls',
                           'Cheeses':'Cheese',
                           'Cheese Assortments & Samplers':'Cheese',
                           'Dairy & Plant-Based Yogurt':'Yogurt',
                           'Desserts & Bakery':'Desserts',
                           'Baking Syrups, Sugars & Sweeteners':'Syrups, Sugars & Sweeteners',
                           'Beverage Syrups & Concentrates':'Syrups, Sugars & Sweeteners',
                           'Cream Cheeses':'Cream Cheese',
                           'Coconut Milk & Cream':'Milk & Cream'})

# Changing col two
df_1[2] = df_1[2].replace({'Milks & Cream':'Milk & Cream',
                           'Butter, Margarine & Plant-Based Alternatives':'Butter & Margarine',
                           'Dried Beans, Grains & Rice':'Grains & Rice',
                           'Dried Grains & Rice':'Grains & Rice',
                           'Dried Beans':'Grains & Rice',
                           'Dried Lentils':'Grains & Rice',
                           'Dried Peas':'Grains & Rice',
                           'Packaged Cured & Deli Meats':'Deli',
                           'Dried Fruit & Raisins':'Dried Fruits & Vegetables',
                           'Fruit Compotes':'Fruit & Compotes',
                           'Fruits':'Fruit & Compotes',
                           'Hard Candy':'Hard Candy & Lollipops',
                           'Herb, Spice & Seasoning Gifts':'Herbs, Spices & Seasonings',
                           'Hot Dogs, Links & Sausages':'Hot Dogs & Franks',
                           'Ice Creams & Frozen Novelties':'Ice Cream & Frozen Novelties',
                           'Jelly Beans':'Jelly Beans & Gummy Candy'})

# Changing col two
df_1[2] = df_1[2].replace({'Juices':'Juice',
                           'Meat Substitute':'Meat Substitutes',
                           'Meatballs, Chunks & Crumbles':'Meats',
                           'Noodle Soups':'Pasta & Noodles',
                           'Asian Noodle Soup':'Pasta & Noddles',
                           'Pork':'Pork Meat',
                           'Sandwich Spreads':'Sandwiches & Wraps',
                           'Frozen Seafood':'Seafood',
                           'Sour Cream':'Sour Creams',
                           'Wasabi Peas':'Wasabi',
                           'Wild Game & Fowl':'Wild Game & Fowl Meat',
                           'Meat, Poultry & Seafood':'Meats',
                           'Meat & Seafood':'Meats',
                           'Sauce, Gravy & Marinade Gifts':'Sauces',
                           'Soda Soft Drinks':'Soft Drinks',
                           'Tea Beverages':'Tea',
                           'Suckers & Lollipops':'Hard Candy & Lollipops',
                           'Soups, Stews & Chili':'Soups',
                           'Soups, Stocks & Broths':'Soups',
                           'Baking Chips':'Baking Chocolates, Carob & Cocoa',
                           'Fresh Baked Cookies':'Grocery Cookies'})


# Removing gifts_1
df_1 = df_1[~df_1[2].isin(['Fresh Cut Flowers','Meat & Seafood Gifts','Assortments & Variety Gifts','Food & Beverage Gifts',
                           'Fresh Flowers & Live Indoor Plants','Candy & Chocolate Assortments','Candy & Chocolate Gifts'])]

# Removing gifts_2
df_1 = df_1[~df_1[2].isin(['Jam, Jelly & Sweet Spread Gifts','Fruit & Nut Gifts','Fruit & Vegetable Trays',
                          'Fresh Flowers & Live Indoor Plants','Bakery & Dessert Gifts','Coffee & Tea Gifts'])]

df_1[df_1[2]=='Grocery Cookies']

"""# Working with titles - cleaning phase"""

# Function to encode string
def encode_string(title):
  """(str) -> str
    Returns a string that is encoded as ascii
    :param title:
    :return:
  """
  try:
    encoded_title = unicodedata.normalize('NFKD', str(title)).encode('ascii', 'ignore')
    encoded_title = html.unescape(encoded_title.decode('ascii','ignore')).lower()
  except TypeError:  # if title is missing and a float
    encoded_title = 'NA'
    
  return encoded_title

# Tokenizing the title taking out the fancy thgs
def tokenize_title_string(title, excluded="‘.%/)("):
  """(str) -> list(str)
  Returns a list of string tokens given a string.
  It will exclude the following characters from the tokenization: - / . %
  :param title:
  :return:
  """
  striper = re.sub(r'[\b\d]+[a-z]+','',title)
  bag =  re.split("[^" + excluded + "\w]+", striper)
  #striper = re.sub(r'[\b\d]+[a-z]+','',bag)
  return [x for x in bag if x.strip()]

# Remove stopwords from string
def remove_words_list(sentence, words_to_remove):
  """ (list(str), set) -> list(str)
  Returns a list of tokens where the stopwords/spam words/colours have been removed
  :param title:
  :param words_to_remove:
  :return:
  >>> remove_words_list(['python', 'is', 'the', 'best'], set(stopwords.words('english')))
  ['python', 'best']
  """
  return [token for token in sentence if token not in words_to_remove]

# Remove words that are fully numeric
def remove_numeric_list(sentence):
  """ (list(str)) -> list(str)
  Remove words which are fully numeric
  :param title:
  :return:
  >>> remove_numeric_list(['A', 'B2', '1', '123', 'C'])
  ['A', 'B2', 'C']
  >>> remove_numeric_list(['1', '2', '3', '123'])
  []
  """
  return [token for token in sentence if not token.isdigit()]

# Remove common words from a sentence
stemmer = SnowballStemmer("english")
def stemming(sentence):
  """ (list(str)) -> list(str)
  Returns a list of str without stopwords.
  :parm title:
  :return:
  >>> stemming(['And','delicious'])
  ['delicious']
  """
  steem = [stemmer.stem(x) for x in sentence]
  return list(dict.fromkeys(steem))

# Remove words with character count below threshold from string
def remove_chars(sentence, word_len=2):
  """ (list(str), int) -> list(str)
  Returns a list of str (tokenized titles) where tokens of character length =< word_len is removed.     
  :param title:     
  :param word_len:     
  :return:     
  >>> remove_chars(['what', 'remains', 'of', 'a', 'word', '!', ''], 1)
  ['what', 'remains', 'of', 'word']
  """
  return [token for token in sentence if len(token) > word_len]

# Applying enconde function
low = [encode_string(x) for x in df_1['title']]

# Applying token function
clean = [tokenize_title_string(x,'') for x in low]

# Applying stopwords function / delayed 49s
words = [remove_words_list(x,set(stopwords.words('english'))) for x in clean]

# Applying no-numeric function
nums = [remove_numeric_list(x) for x in words]

# Applying stemm function / Delayed 34s
stemm = [stemming(x) for x in nums]

# Applying no-short words function
chars = [remove_chars(x) for x in stemm]

# Replacing in the whole datafra some characters that mess data
df_1['title'] = [' '.join(x) for x in chars]

# Getting just the first hierarchical position after mother
cat_0 = df_1[1].str.strip().unique()
cat_1 = df_1[2].str.strip().unique()

df_2 = np.concatenate([cat_0,cat_1])
df_2 = list(dict.fromkeys(df_2))
df_2 = [x for x in df_2 if x is not None]
len(df_2)

# Concating to create the matrix / delayed 27s and boosted
dxf = df_1.loc[:,[1,2]].copy()
df_3 = pd.concat([dxf, pd.DataFrame(columns=list(df_2))]).reset_index()
df_3.fillna(0, inplace=True)

# Creating a copy to compare after
df_4 = df_3.copy()

# loc is label-based, which means that you have to specify rows and columns based on their row and column labels / delayed 17m 44s
for i in range(1,3):
  row = 0
  for category in df_4[i]:
    if category!=0:
      df_4.loc[row,category] = 1
      # loc is label-based, which means that you have to specify rows and columns based on their row and column labels.
    row = row + 1

# Reseting index
df_1 = df_1.reset_index()

# creating new dataframe which contains name of product,description and categories it belong to
dataframe = pd.concat([df_1['title'], df_4.iloc[:,3:]],axis=1)

"""# Splitting data"""

# Splitting into samples to train & test
X_train, X_test, y_train, y_test = train_test_split(dataframe['title'], 
                                                   dataframe[dataframe.columns[1:]], 
                                                    test_size=0.3, 
                                                    random_state=0, 
                                                    shuffle=True)

# Using a tf-idf weighting scheme rather than normal boolean weights for better performance
vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2') 
vectorizer.fit(X_train)
X_train_Vector = vectorizer.transform(X_train)
X_test_Vector = vectorizer.transform(X_test)

# Shape of samples
print("X_train shape : ", X_train_Vector.shape)
print("X_test shape : ", X_test_Vector.shape)
