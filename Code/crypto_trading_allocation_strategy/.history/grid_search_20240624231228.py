import pandas as pd
from update_dataframe import update_dataframe_with_new_row

def grid_search_2_params(btc_df, short_window_range, long_window_range, true_weight=1, high_weight=100, medium_weight=65, low_weight=30):
    """
    Perform a grid search over short_window and long_window parameters to find the best combination for maximizing accumulated pnl.

    Parameters:
    btc_df (pd.DataFrame): DataFrame containing the btc data.
    short_window_range (range): Range of values for the short window EMA.
    long_window_range (range): Range of values for the long window EMA.

    Returns:
    pd.DataFrame: DataFrame containing the results of the grid search, including short_window, long_window, and total_accumulated_pnl.
    """
    results = []

    for short_window in short_window_range:
        for long_window in long_window_range:

            # new DataFrame for each combination of short_window and long_window
            # df_new_2 = pd.DataFrame(columns=['ts_hour', 'pnl', 'EMA_short', 'EMA_long', 'is_positive',  'signal', 'count', 'consistency', 'is_continuous', 'class', 'weight_percentage', 'weight', 'calculation', 'weighted_pnl', 'accumulated_pnl'])
            df_new_2 = pd.DataFrame(columns=['ts_hour', 'pnl', 'EMA_short', 'EMA_long', 'is_positive', 'signal', 'count', 'consistency', 'is_continuous', 'class', 'weight_percentage', 'weight', 'weighted_pnl'])

            results_list = []

            # iter row and update in DataFrame
            for _, row in btc_df.iterrows():
                df_new_2 = update_dataframe_with_new_row(df_new_2, row, results_list, short_window, long_window, true_weight=true_weight, high_weight=high_weight, medium_weight=medium_weight, low_weight=low_weight)

            # save result
            total_weighted_pnl = df_new_2['weighted_pnl'].sum()
                
            results.append({
                'short_window': short_window,
                'long_window': long_window,
                'total_weighted_pnl': total_weighted_pnl
                })
            print(f"short_window: {short_window}, long_window: {long_window}, total_weighted_pnl: {total_weighted_pnl}")

    print("Grid search finished.")
    return pd.DataFrame(results)