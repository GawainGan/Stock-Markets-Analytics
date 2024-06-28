import pandas as pd
from trading_strategy_utils import calculate_ema, calculate_is_positive, calculate_ema_diff, calculate_signal, calculate_count, calculate_consistency, calculate_weight_and_class

# 更新 DataFrame
def update_dataframe_with_new_row(df_new, new_row, results_list, short_window=7, long_window=15, true_weight=1, high_weight=100, medium_weight=65, low_weight=30):
    new_row_df = pd.DataFrame([new_row])
    df_new = pd.concat([df_new, new_row_df], ignore_index=True)
    
    df_new = calculate_ema(df_new, short_window, long_window)
    
    # only update the calculation when the length of the DataFrame is greater than or equal to long_window
    if len(df_new) >= long_window:
        df_new = calculate_is_positive(df_new)
        df_new = calculate_signal(df_new)
        df_new = calculate_count(df_new)
        df_new = calculate_consistency(df_new)
        df_new = calculate_weight_and_class(df_new, true_weight, high_weight, medium_weight, low_weight)

        # weighted_pnl
        calculation = 0
        if len(df_new) > 1:
            calculation = df_new.iloc[-2]['weight'] * df_new.iloc[-1]['pnl']
        df_new.at[len(df_new) - 1, 'weighted_pnl'] = calculation
        
        
        # save result
        if len(df_new) > 1:
            result_entry = {
                "ts_hour": df_new.iloc[-1]['ts_hour'],
                "当前pnl": df_new.iloc[-1]['pnl'],
                "is_positive": df_new.iloc[-1]['is_positive'],
                "signal": df_new.iloc[-1]['signal'],
                "对下一个pnl施加weight": df_new.iloc[-1]['count'] != 0,
                "施加的weight": df_new.iloc[-1]['weight'],
                "calculation": df_new.iloc[-2]['weight'] * df_new.iloc[-1]['pnl'],
                # "累积pnl": df_new.iloc[-1]['accumulated_pnl'],
                "Class": df_new.iloc[-1]['class'],
                # "weight_effect": weight_effect
            }
            results_list.append(result_entry)
        else:
            result_entry = {
                "ts_hour": df_new.iloc[-1]['ts_hour'],
                "当前pnl": df_new.iloc[-1]['pnl'],
                "is_positive": df_new.iloc[-1]['is_positive'],
                "signal": df_new.iloc[-1]['signal'],
                "对下一个pnl施加weight": df_new.iloc[-1]['count'] != 0,
                "施加的weight": df_new.iloc[-1]['weight'],
                "calculation": 0,
                "Class": df_new.iloc[-1]['class'],
            }
            results_list.append(result_entry)
    # 打印信息
        # if len(df_new) > 1:
        #     print(f"{df_new.iloc[-1]['ts_hour']}: 当前pnl: {df_new.iloc[-1]['pnl']}, is positive: {df_new.iloc[-1]['is_positive']}, signal: {df_new.iloc[-1]['signal']}, 对下一个pnl施加weight: {df_new.iloc[-1]['count'] != 0}, 施加的weight: {df_new.iloc[-1]['weight']}, calculation: {df_new.iloc[-2]['weight']} * {df_new.iloc[-1]['pnl']}, Class: {df_new.iloc[-1]['class']}")
        # else:
        #     print(f"{df_new.iloc[-1]['ts_hour']}: 当前pnl: {df_new.iloc[-1]['pnl']}, is positive: {df_new.iloc[-1]['is_positive']}, signal: {df_new.iloc[-1]['signal']}, 对下一个pnl施加weight: {df_new.iloc[-1]['count'] != 0}, 施加的weight: {df_new.iloc[-1]['weight']}, calculation: 0 * {df_new.iloc[-1]['pnl']}, Class: {df_new.iloc[-1]['class']}")
    else:
        df_new.at[len(df_new) - 1, 'weight_percentage'] = 0
        df_new.at[len(df_new) - 1, 'weight'] = 0
        df_new.at[len(df_new) - 1, 'class'] = 0
        df_new.at[len(df_new) - 1, 'weighted_pnl'] = 0
            
    return df_new