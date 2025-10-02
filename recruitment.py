import pandas as pd 

def extract (filepath, filename):
    file = filepath+'/'+filename
    df = pd.read_csv(file)
    return df

def transform(df):
    #ubah nama kolom Unnamed: 0 jadi id
    df = df.rename(columns={'Unnamed: 0': 'id'})

    #ubah column type id jadi int
    df['id'] = df['id'].astype(int)

    #kolom company ada 2 baris, ambil baris ke 0 (nama company) -> karena sepertinya baris ke 1 adalah rating yang salah penempatan
    df['company'] = df['company'].str.split('\n').str[0]

    #split kolom salary_estimate jadi salary_currency(string), salary(float), rate_per (string, year or hour)
    df['salary_currency']= df['salary_estimate'].str[0:1]
    df['salary'] = df['salary_estimate'].str.extract(r'([0-9,.]+)')
    df['rate_per'] = df['salary_estimate'].str.split('/').str[1].str.replace('(est.)','').str.strip()
    df['rate_per']= df['rate_per'].replace({'yr':'year','hr':'hour'})
    
    # #ubah column type salary jadi float (yang nan diisi 0)
    df['salary'] = df['salary'].str.replace(',','').astype(float)
    df['salary'] = df['salary'].fillna(0.00)

    #ubah column type company_rating jadi float (yang nan diisi 0)
    df['company_rating'] = df['company_rating'].astype(float)
    df['company_rating'] = df['company_rating'].fillna(0.00)
    
    
    #buat column baru date_jakarta_timezone (datetime) dari column dates
    df['date_jakarta_timezone'] = pd.to_datetime(df['dates'], utc=True)
    df['date_jakarta_timezone']  = df['date_jakarta_timezone'].dt.tz_convert('Asia/jakarta')
    #.tz_convert('Jakarta/Asia')

    #fill all null/blank with 'UNKNOWN' -- khusus untuk kolom string (selain float dan datetime)
    # Identify string columns
    string_cols = df.select_dtypes(include='object').columns

    # Fill NaN values in identified string columns with a specific string
    df[string_cols] = df[string_cols].fillna('UNKNOWN')
    df[string_cols] = df[string_cols].astype(str)

    return df


def data_demographics(df):
    print('----------------------head:----------------------')
    print(df.head())

    print('----------------------info:----------------------')
    print(df.info())

    # print('----------------------distinct data:----------------------')
    # unique_Unnamed = df['Unnamed: 0'].unique()
    # print("Unique Unnamed:")
    # print(unique_Unnamed)

    # cek kemungkinan pengisian data di kolom salary_estimate 
    # uq_salary_estimate = df['salary_estimate'].unique()
    # print("Unique salary_estimate:")
    # print(uq_salary_estimate)

    #cek ada berapa jenis currency di kolom salary_estimate --> hanya ada 1 jenis currency yaitu $
    # uq_salary_estimate_currency = df['salary_estimate'].str[0:1].unique()
    # print("Unique salary currency:")
    # print(uq_salary_estimate_currency)

    # print('----------------------describe:----------------------')
    # print(df.describe())

    print('----------------------null sum:----------------------')
    print(df.isnull().sum())

    # print('----------------------duplicated:----------------------')
    # print(df.duplicated().sum())

    # print('----------------------nunique:----------------------')
    # print(df.nunique())

    # print('----------------------columns----------------------')
    # print(df.columns)

    print('----------------------dtypes----------------------') 
    print(df.dtypes)

    # print('----------------------shape----------------------')
    # print(df.shape)

    # print('val count' + df.value_counts())
    
folder_source = 'source'
filename_recruitment = 'data_requirements.csv'
df = extract(folder_source, filename_recruitment)

print('----------------------before transform----------------------')
data_demographics(df)

transformed_df = transform(df)

print('----------------------after transform----------------------')
data_demographics(transformed_df)

transformed_df.to_csv(folder_source+'/data_requirements_cleaned.csv', index=False)