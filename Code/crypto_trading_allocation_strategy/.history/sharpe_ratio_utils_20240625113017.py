import numpy as np
import pandas as pd

def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    """
    Calculate the Sharpe Ratio for a series of returns.

    Parameters:
    returns (pd.Series or np.array): Array-like object of returns.
    risk_free_rate (float): The risk-free rate. Default is 1%.

    Returns:
    float: The Sharpe Ratio.
    """
    excess_returns = returns - risk_free_rate
    mean_excess_return = np.mean(excess_returns)
    std_excess_return = np.std(excess_returns)

    sharpe_ratio = mean_excess_return / std_excess_return
    return sharpe_ratio

def calculate_true_weights(sharpe_ratios):
    """
    Calculate the true weights for a list of Sharpe Ratios.

    Parameters:
    sharpe_ratios (list of float): List of Sharpe Ratios for each asset.

    Returns:
    list of float: List of true weights corresponding to each Sharpe Ratio.
    """
    total_sharpe = sum(sharpe_ratios)
    true_weights = [sharpe_ratio / total_sharpe for sharpe_ratio in sharpe_ratios]
    return true_weights