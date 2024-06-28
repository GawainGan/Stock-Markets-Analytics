# Capital Allocation Strategy Based on Trend Calculations

## Overview

The capital allocation strategy uses trend-following techniques to determine the optimal allocation of capital across four cryptocurrencies: Bitcoin (BTC), Ethereum (ETH), Cardano (ADA), and Dogecoin (DOGE). The strategy aims to maximize returns by dynamically adjusting the weights assigned to each asset based on their performance metrics, including Exponential Moving Averages (EMA) and Sharpe Ratios.

## Files and Functions

The strategy consists of the following Python scripts and their respective functions:

1. **`update_dataframe.py`**
2. **`sharpe_ratio_utils.py`**
3. **`grid_search.py`**
4. **`trading_strategy_utils.py`**

Each script contains functions that are critical to the implementation of the strategy. Here’s a detailed breakdown:

### 1. `trading_strategy_utils.py`

**Key Functions:**

- **`calculate_ema(df, short_window=6, long_window=12)`**
- **`calculate_is_positive(df)`**
- **`calculate_ema_diff(df)`**
- **`calculate_signal(df)`**
- **`calculate_count(df)`**
- **`calculate_consistency(df)`**
- **`calculate_weight_and_class(df, true_weight=1, high_weight=100, medium_weight=65, low_weight=30)`**

This script contains utility functions to calculate EMAs, signals, and other financial indicators.

The primary idea behind using dual EMAs is that our PnL typically fluctuates. We aim to capture these fluctuations through EMA calculations to identify trends.

Given that we need to allocate a portion [0 - 1], it's crucial to focus on identifying positive trend signals amidst these fluctuations. The `calculate_signal` function helps us recognize the Golden Cross (signal == 1). Combined with other conditions, this function determines whether the next PnL data should be assigned weight from the allocation.

- **calculate_signal**: Helps identify Golden Cross signals (signal == 1) to decide on allocating weight from the allocation.

The `calculate_count` function tracks consecutive occurrences of positive signals in the trading data. This strategy identifies the frequency of successive positive signals, aiding in determining the strength and reliability of a trend.

- **calculate_count**: Tracks the consecutive occurrences of positive signals to assess trend strength and reliability.

The `calculate_consistency` function evaluates the consistency of signals over time and identifies continuous patterns. Consistent PnL can maximize profits by increasing allocation in stable trends until a reversal signal (loss of consistency) appears. This strategy assesses the reliability and sustainability of signals over multiple periods.

- **calculate_consistency**: Evaluates signal consistency to ensure stable trends for maximizing profits and assesses signal reliability over time.

The `calculate_weight_and_class` function is designed to dynamically adjust weights and classify signals based on specific conditions. This strategy helps to fine-tune the weight applied to signals, taking into account their positivity, signal direction, and continuity.

Reason I choose this strategy:
1.	**Dynamic Weight Adjustment**: Adjusts weights based on real-time signal conditions, allowing for more responsive and adaptive trading decisions.
2.	**Detailed Signal Classification**: Provides a clear classification of signals, helping to differentiate between strong, moderate, and weak signals.
3.	**Enhanced Decision-Making**: By considering factors like signal positivity, direction, and continuity, the strategy supports more informed and nuanced trading decisions.
4.	**Ease of Implementation**: The function is simple to implement and integrate into existing trading systems.
5.	**Scalability**: Can be easily scaled and adapted for different trading assets or markets by adjusting the parameters and conditions.

However, the strategy may have limitations in certain market conditions, such as high volatility or sudden price changes, which could impact the effectiveness of the signal classification and weight adjustment process. Additionally, the strategy may require frequent monitoring and adjustment to optimize performance and adapt to changing market conditions.

### 2. `update_dataframe.py`

This script contains functions to update the DataFrame with new rows and compute the necessary financial indicators.

**Key Functions:**

- **`update_dataframe_with_new_row(df_new, new_row, results_list, short_window=7, long_window=15, true_weight=1, high_weight=100, medium_weight=65, low_weight=30)`**

    Updates the DataFrame with a new row and calculates EMA, signal, and weight.

### 3. `sharpe_ratio_utils.py`

This script contains functions to calculate the Sharpe Ratio and allocate weights based on Sharpe Ratios.

For any asset, the return is a random variable. We use the Sharpe Ratio to measure the relationship between the expected value and variance of this random variable, aiming to find an optimal asset allocation. Therefore, beyond understanding the weight percentage each crypto can individually bear, the overall allocation needs to be adjusted based on the Sharpe Ratio generated from the PnL.

**Key Functions:**

- **`calculate_sharpe_ratio(returns, risk_free_rate=0.01)`**

    Calculates the Sharpe Ratio for a series of returns.

- **`calculate_true_weights(sharpe_ratios)`**

    Allocates true weights to each cryptocurrency based on their Sharpe Ratios.

### 4. `grid_search.py`

This script contains functions for performing grid search to optimize parameters.

**Key Functions:**

- **`grid_search_2_params(btc_df, short_window_range, long_window_range)`**

    Performs grid search to find the best parameters for short and long EMAs.


## Explanation of Strategy Updates

In the revised strategy, I implemented several changes to enhance the accuracy and tracking of our capital allocation model. The primary reasons for these updates are to enable detailed result tracking for follow-up analysis and to ensure that allocations are only influenced by scenarios expected to yield positive returns. Here are the key differences and their purposes:

#### Tracking Generated Results
- **Reason:** To verify the effectiveness of the strategy and enable detailed analysis for follow-up adjustments.
- **Rationale:** Detailed tracking is essential to understand each component's contribution to the final result and ensure transparency.
  
#### Handling Only Positive Returns in Allocation
- **Reason:** To focus allocations on scenarios where the model predicts a gain, reducing the risk of allocating capital based on negative or neutral predictions.
- **Rationale:** Prioritizing positive returns optimizes performance and minimizes risk, a common practice in trading strategies.

#### PnL as Model Prediction Result
- **Reason:** Assumes that PnL values are predictions for the next hour’s performance, allowing informed decision-making based on anticipated market movements.
- **Rationale:** Using predictive models to guide allocation decisions aligns with standard financial strategy practices.

### Key Updates

- **Granular Tracking:**
  - Implemented `cumulative_return_list` for each cryptocurrency.
  - **Purpose:** To provide a detailed log for each asset, allowing better performance analysis and strategy refinement.

- **Positive Return Consideration:**
  - Added conditional checks to ensure only positive `next_hour_pnl_list` values influence allocation.
  - **Purpose:** To ensure that allocations are based on scenarios expected to yield positive returns, aligning with risk-averse investment principles.

- **Parameterized Windows:**
  - Used specific window parameters for different cryptocurrencies.
  - **Purpose:** Different assets may respond better to different moving average windows, enhancing the strategy's adaptability and effectiveness.

### Conclusion

The modifications made to the strategy aim to improve its robustness and reliability. By focusing on detailed result tracking and ensuring allocations are based on positive PnL predictions, we align our approach with best practices in financial modeling and strategy development.