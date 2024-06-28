import pandas as pd
from trading_strategy_utils import calculate_ema, calculate_is_positive, calculate_ema_diff, calculate_signal, calculate_count, calculate_consistency, calculate_weight_and_class

# 更新 DataFrame
def update_dataframe_with_new_row(df_new, new_row, results_list, short_window=7, long_window=15, true_weight=1, high_weight=100, medium_weight=65, low_weight=30):
    new_row_df = pd.DataFrame([new_row])
    df_new = pd.concat([df_new, new_row_df], ignore_index=True)
    
    df_new = calculate_ema(df_new, short_window, long_window)
    
    # 仅在数据点数量达到 EMA_long 所需的数值后才开始计算
    if len(df_new) >= long_window:
        df_new = calculate_is_positive(df_new)
        # df_new = calculate_ema_diff(df_new)
        df_new = calculate_signal(df_new)
        df_new = calculate_count(df_new)
        df_new = calculate_consistency(df_new)
        df_new = calculate_weight_and_class(df_new, true_weight, high_weight, medium_weight, low_weight)

        # 计算 weighted_pnl
        calculation = 0
        if len(df_new) > 1:
            calculation = df_new.iloc[-2]['weight'] * df_new.iloc[-1]['pnl']
        # df_new.at[len(df_new) - 1, 'calculation'] = calculation
        df_new.at[len(df_new) - 1, 'weighted_pnl'] = calculation
        
        # 累积 pnl
        # if len(df_new) > 1:
        #     df_new.at[len(df_new) - 1, 'accumulated_pnl'] = df_new.iloc[-2]['accumulated_pnl'] + calculation
        # else:
        #     df_new.at[len(df_new) - 1, 'accumulated_pnl'] = 0 + calculation
        
        # 判断 weight 对下一个 pnl 的影响
        # if len(df_new) > 2:
        #     next_pnl_is_positive = df_new.iloc[-1]['pnl'] > 0
        #     if df_new.iloc[-2]['weight'] > 0:
        #         weight_effect = 1 if next_pnl_is_positive else -1
        #     else:
        #         weight_effect = 0
        # else:
        #     weight_effect = 0
        
        # df_new.at[len(df_new) - 1, 'weight_effect'] = weight_effect
        
        # 保存到结果列表
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
                # "累积pnl": df_new.iloc[-1]['accumulated_pnl'],
                "Class": df_new.iloc[-1]['class'],
                # "weight_effect": weight_effect
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
        # df_new.at[len(df_new) - 1, 'calculation'] = 0
        df_new.at[len(df_new) - 1, 'weighted_pnl'] = 0
        # df_new.at[len(df_new) - 1, 'weight_effect'] = 0
        # if len(df_new) > 1:
        #     df_new.at[len(df_new) - 1, 'accumulated_pnl'] = df_new.iloc[-2]['accumulated_pnl']
        # else:
        #     df_new.at[len(df_new) - 1, 'accumulated_pnl'] = 0
            
    return df_new