import pandas as pd 

def extract (filepath, filename):
    file = filepath+'/'+filename
    df = pd.read_csv(file)
    return df

def transform(df):
    #split kolom discount_price jadi currency(string), discount_price(float) --> demikian juga untuk actual_price
    df['currency']= df['discount_price'].str[0:1]
    df['discount_price'] = df['discount_price'].str.extract(r'([0-9.]+)') #discount_price ada koma
    df['actual_price'] = df['actual_price'].str.extract(r'([0-9.]+)') #actual_price ada koma

    df['discount_price'] = df['discount_price'].astype(float)
    df['actual_price'] = df['actual_price'].astype(float)

    # ubah rating dan no_of_ratings jadi float (yang bukan angka diisi nan atau 0)
    df['no_of_ratings'] = df['no_of_ratings'].str.extract(r'([0-9.]+)') #no of ratings ada koma
    df['no_of_ratings'] = pd.to_numeric(df['no_of_ratings'], errors='coerce')
    df['no_of_ratings'] = df['no_of_ratings'].fillna(0)

    df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce')

    df['no_of_ratings'] = df['no_of_ratings'].astype(int)
    df['ratings'] = df['ratings'].astype(float)

    df['name']= df['name'].astype(str)
    
    return df

def data_demographics(df):
    print('----------------------head:----------------------')
    print(df.head())

    print('----------------------info:----------------------')
    print(df.info())

    print('----------------------null sum:----------------------')
    print(df.isnull().sum())



folder_source = 'source'
filename = 'All Grocery and Gourmet Foods.csv'
df = extract(folder_source, filename)

print('----------------------before transform----------------------')
data_demographics(df)

# print('----------------------distinct data:----------------------')
# ratings = df['ratings'].unique()
# print("ratings:")
# print(ratings)


transformed_df = transform(df)

print('----------------------after transform----------------------')
data_demographics(transformed_df)

#transformed_df.to_csv(folder_source+'/data_requirements_cleaned.csv', index=False)