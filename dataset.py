import pandas as pd
import numpy as np
import os

__author__ = "Romayne Whyte"
__license__ = "MIT"
__version__ = "2018_12"

def pull_jse_prices(folder):
    """
    Pull the stock prices from the CSV files
    returns: dataframe 
        List of all the stock prices pulled from JSE CSV
    """
    slist = []    
    filelist = os.listdir('c:/'+folder+'/stockcsv/')
    for filename in filelist:
        slist.append(pd.read_csv('c:/'+folder+'/stockcsv/'+filename))
    
    #clean up
    frame = pd.concat(slist, axis = 0, ignore_index = True)
    frame = frame.sort_values(by='Date')
    frame = frame.rename(columns={'Close Price': 'Close'})
    
    frame = frame.drop(['52 Week High','52 Week Low','Current Year Div','Today High','Today Low','Last Traded','Price Change','Closing Bid','Closing Ask','Previous Year Div','Volume (non block)'],axis=1)
    frame['Date'] = pd.to_datetime(frame['Date'])

    validstock = pull_valid_stocklist(folder)
    
    #Remove invalid stocks
    frame = frame[frame["Symbol"].isin(validstock["Symbol"].tolist())]

    frame['split'] = 1.0#np.nan
    frame['dividend'] = 0.00 #np.nan

    #Remove Duplicated stock price
    frame = frame.drop_duplicates(subset = ["Symbol","Date"], keep=False)
        
    return frame

def pull_valid_stocklist(folder):
    #Pull the list of delisted to remove from stock frame
    framevalid = pd.read_csv('c:/'+folder+'/stockdelist/stockvalid.csv')
    
    # clean up
    framevalid = framevalid.rename(columns={'Instrument Code': 'Symbol'})
    framevalid = framevalid[framevalid.Type == "ORDINARY"]
    
    return framevalid

def pull_corporate_action(folder):
    slist = []
    slist.append(pd.read_csv('c:/'+folder+'/stocksplit/corporate-actions (1).csv'))
    slist.append(pd.read_csv('c:/'+folder+'/stocksplit/corporate-actions (2).csv'))
    slist.append(pd.read_csv('c:/'+folder+'/stocksplit/corporate-actions (3).csv'))
    slist.append(pd.read_csv('c:/'+folder+'/stocksplit/corporate-actions (4).csv'))
    df_info = pd.concat(slist, axis = 0, ignore_index = True)

    #Extract the Split Information from the Info dataframe
    df_info["Action"] = df_info["Action"].str.strip()
    df_split = df_info[df_info["Action"]=='Stock Split']
    df_split = df_split.drop(['Record Date','Action','Payment Date'],axis=1)
    df_split['Ex-Date'] = pd.to_datetime(df_split['Ex-Date'])
    df_split = df_split.dropna(axis=0,how='any')
    df_split

    #Extract the Dividend from the Info Dataframe
    df_info["Action"] = df_info["Action"].str.strip()
    df_div = df_info[df_info["Action"]!='Stock Split']
    df_div = df_info.drop(['Action','Record Date','Payment Date'],axis=1)
    df_div['Ex-Date'] = pd.to_datetime(df_div['Ex-Date'])
    df_div = df_div.dropna(axis=0,how='any')

    return [df_split, df_div]


def pull_indices(folder):
    #Pull the valid stock Indicies
    slist = []
    filelist = os.listdir('c:/'+folder+'/stockindicies/')
    for filename in filelist:
        slist.append(pd.read_csv('c:/'+folder+'/stockindicies/'+filename))
    
    stkindices_frame = pd.concat(slist, axis = 0, ignore_index = True)
    stkindices_frame = stkindices_frame.dropna(axis=0)
    
    #Clean up data
    stkindices_frame = stkindices_frame.drop(['Change ($)','Change (%)','Volume Traded'],axis=1)
    stkindices_frame['Date'] = pd.to_datetime(stkindices_frame['Date'])
    
    #split the indicies by index
    gp_index = stkindices_frame.groupby("Index")
    stk_indicies_list = [gp_index.get_group(x) for x in gp_index.groups]

    df_ind_data = pd.DataFrame()
    for idx, index in enumerate(stk_indicies_list):
        stk_indicies_list[idx] = stk_indicies_list[idx].set_index('Date')
        df_ind_data[index['Index'].iloc[0]] = stk_indicies_list[idx]['Value']

    df_ind_data = df_ind_data.sort_index(axis=0)
        
    return df_ind_data

# https://joshschertz.com/2016/08/27/Vectorizing-Adjusted-Close-with-Python/
def calculate_adjusted_prices(df, column):
    """ Vectorized approach for calculating the adjusted prices for the
    specified column in the provided DataFrame. This creates a new column
    called 'adj_<column name>' with the adjusted prices. This function requires
    that the DataFrame have columns with dividend and split_ratio values.

    :param df: DataFrame with raw prices along with dividend and split_ratio
        values
    :param column: String of which price column should have adjusted prices
        created for it
    :return: DataFrame with the addition of the adjusted price column
    """
    adj_column = 'adj_' + column + '_Check'

    # Reverse the DataFrame order, sorting by date in descending order
    df.sort_index(ascending=False, inplace=True)

    price_col = df[column].values
    split_col = df['split'].values
    dividend_col = df['dividend'].values
    adj_price_col = np.zeros(len(df.index))
    adj_price_col[0] = price_col[0]
          
    for i in range(1, len(price_col)):
        adj_price_col[i] = round((adj_price_col[i - 1] + adj_price_col[i - 1] *
                   (((price_col[i] * (1/split_col[i - 1])) -
                     price_col[i - 1]) / price_col[i - 1])), 4)

    df[adj_column] = adj_price_col

    # Change the DataFrame order back to dates ascending
    df.sort_index(ascending=True, inplace=True)

    return df


def generate_stock_dataframe(folder):
    frame = pull_jse_prices(folder)
    df_infos = pull_corporate_action(folder)    
    df_split = df_infos[0]
    df_div = df_infos[1]

    gp = frame.groupby("Symbol")
    
    stklist = [gp.get_group(x) for x in gp.groups]

    # swap CAR with 138SL
    temp = stklist[0]
    stklist[0] = stklist[10]
    stklist[10] = temp   

    for idx, stk in enumerate(stklist):    
        stklist[idx] = stklist[idx].set_index('Date')
    
    for idx, stk in enumerate(stklist):            
        symbol = stk['Symbol'].iloc[0]
        
        #Assign the split values per symbol and date from split dataframe to the stock dataframe
        if not df_split[(df_split.Symbol == symbol)].empty:
            split_s = df_split[(df_split.Symbol == symbol)]        
            stk.at[split_s['Ex-Date'].iloc[0],'split'] = split_s['Dividend Amount'].iloc[0]
            #print(stk[stk.index.isin(split_s['Ex-Date'].tolist())])
            stklist[idx] = stk    
    
        #Assign the dividend values per symbol and date from info dataframe to the stock dataframe
        if not df_div[(df_div.Symbol == symbol)].empty:
            div_s = df_div[(df_div.Symbol == symbol)]
            for ds in div_s.values:            
                stk.at[ds[2],'dividend'] = ds[1]                
            stklist[idx] = stk  
    
    #Generate adjusted Price
    for idx, stk in enumerate(stklist):        
        stklist[idx] = calculate_adjusted_prices(stklist[idx],'Close')
    
    stkframe = pd.DataFrame()
    for stk in stklist:
        stkframe[stk['Symbol'][0]] = stk['adj_Close_Check']

    divframe = pd.DataFrame()
    for div in stklist:
        divframe[div['Symbol'][0]] = div['dividend']

    return (stkframe,divframe)
