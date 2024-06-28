import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# EMA
def calculate_ema(df, short_window=6, long_window=12):
    """
    Calculate Exponential Moving Average (EMA) for the given DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing the pnl data.
    short_window (int): The window length for short term EMA. Default is 7.
    long_window (int): The window length for long term EMA. Default is 15.

    Returns:
    pd.DataFrame: DataFrame with additional columns for short term and long term EMA.
    """
    df['EMA_short'] = df['pnl'].ewm(span=short_window, adjust=False).mean()
    df['EMA_long'] = df['pnl'].ewm(span=long_window, adjust=False).mean()
    return df

# is_positive
def calculate_is_positive(df):
    """
    Calculate if the pnl is positive or not.

    Parameters:
    df (pd.DataFrame): DataFrame containing the pnl data.

    Returns:
    pd.DataFrame: DataFrame with an additional column 'is_positive'.
    """
    df['is_positive'] = (df['pnl'] > 0).astype(int)
    return df

# EMA_diff
def calculate_ema_diff(df):
    """
    Calculate the difference between short term EMA and long term EMA.

    Parameters:
    df (pd.DataFrame): DataFrame containing EMA_short and EMA_long columns.

    Returns:
    pd.DataFrame: DataFrame with an additional column 'EMA_diff'.
    """
    df['EMA_diff'] = df['EMA_short'] - df['EMA_long']
    return df

# signal
def calculate_signal(df):
    """
    Generate trading signals based on the crossover of short term and long term EMAs.

    Parameters:
    df (pd.DataFrame): DataFrame containing EMA_short and EMA_long columns.

    Returns:
    pd.DataFrame: DataFrame with an additional column 'signal' where
                    1 represents a golden cross,
                    -1 represents a death cross, and
                    0 represents no signal.
    """
    df['signal'] = 0
    golden_cross = (df['EMA_short'] > df['EMA_long']) & (df['EMA_short'].shift(1) <= df['EMA_long'].shift(1))
    death_cross = (df['EMA_short'] < df['EMA_long']) & (df['EMA_short'].shift(1) >= df['EMA_long'].shift(1))
    df.loc[golden_cross, 'signal'] = 1
    df.loc[death_cross, 'signal'] = -1
    return df

# count
def calculate_count(df):
    """
    Calculate the count of consecutive positive signals.

    Parameters:
    df (pd.DataFrame): DataFrame containing is_positive and signal columns.

    Returns:
    pd.DataFrame: DataFrame with an additional column 'count'.
    """
    df['count'] = 0
    for i in range(1, len(df)):
        if df.loc[i, 'is_positive'] == 1 and df.loc[i, 'signal'] in [1, -1]:
            df.loc[i, 'count'] = 1 if df.loc[i-1, 'count'] > 0 else 1
        else:
            df.loc[i, 'count'] = -1 if df.loc[i-1, 'count'] > 0 else 0
    return df

# consistency & is_continuous
def calculate_consistency(df):
    """
    Calculate the consistency and is_continuous flags for the DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing count column.

    Returns:
    pd.DataFrame: DataFrame with additional columns 'consistency' and 'is_continuous'.
    """
    consistency = np.nan
    is_continuous = 0
    if len(df) > 1:
        if df.iloc[-1]['count'] != 0:
            previous_consistency = df.iloc[-2]['consistency']
            if isinstance(previous_consistency, list):
                consistency = previous_consistency + [len(df) - 1]
            else:
                consistency = [len(df) - 2, len(df) - 1]
            if len(consistency) >= 2:
                is_continuous = 1

    df.at[len(df) - 1, 'consistency'] = consistency
    df.at[len(df) - 1, 'is_continuous'] = is_continuous
    return df

def calculate_weight_and_class(df, true_weight=1, high_weight=100, medium_weight=65, low_weight=35):
    """
    Calculate the weight and class based on given conditions.

    Parameters:
    df (pd.DataFrame): DataFrame containing is_positive, signal, and is_continuous columns.
    true_weight (float): The actual weight to be applied, ranging between 0 and 1.
    high_weight (int): Percentage for high weight. Default is 100.
    medium_weight (int): Percentage for medium weight. Default is 65.
    low_weight (int): Percentage for low weight. Default is 30.

    Returns:
    pd.DataFrame: DataFrame with additional columns 'weight', 'class', and 'weight_percentage'.
    """
    
    weight_percentage = 0
    signal = df.iloc[-1]['signal']
    is_positive = df.iloc[-1]['is_positive']
    is_continuous = df.iloc[-1]['is_continuous']
    class_type = 0

    # define the best case (weight = high_weight%)
    if is_positive == 1 and signal == 1 and is_continuous == 1:
        weight_percentage = high_weight
        class_type = '1'

    # define the second cases (weight = medium_weight% - 20%)
    elif is_positive == 1 and signal == 1:
        weight_percentage = medium_weight
        class_type = '2.1'
    elif is_positive == 1 and signal == 0 and is_continuous == 1:
        weight_percentage = medium_weight*(3/4)
        class_type = '2.2'
    elif is_positive == 1 and signal == 0 and is_continuous == 0:
        weight_percentage = medium_weight*(3/4)
        class_type = '2.3'

    # define the third cases, the weight range is low (weight = low_weight% - 10%)
    elif is_positive == 1 and signal == -1 and is_continuous == 1:
        weight_percentage = low_weight*(2/3)
        class_type = '3.1'
    elif is_positive == 1 and signal == -1 and is_continuous == 0:
        weight_percentage = low_weight
        class_type = '3.2'
    elif is_positive == 0 and signal == 1 and is_continuous == 1:
        weight_percentage = low_weight
        class_type = '3.3'

    actual_weight = true_weight * (weight_percentage / 100.0)
    df.at[len(df) - 1, 'weight_percentage'] = weight_percentage
    df.at[len(df) - 1, 'weight'] = actual_weight
    df.at[len(df) - 1, 'class'] = class_type
    
    return df
