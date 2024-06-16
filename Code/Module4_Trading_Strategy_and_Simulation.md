# 1.Find the new global best CAGR with Random Forest tuning

### 1.1 df_score plot,find highest precision and recall for the best model
<img src='https://github.com/GawainGan/Stock-Markets-Analytics/blob/main/Src/Module4_Pic/Module1_1.png' style="width: 70%;">

### 1.2 New column `predxx_rf_best_rule_yy` to cover the interval >= [0.51, 0.60)
<img src='https://github.com/GawainGan/Stock-Markets-Analytics/blob/main/Src/Module4_Pic/Module1_2.png' style="width: 60%;">

### 1.3 Return the best simuation result (best CAGR)
<img src='https://github.com/GawainGan/Stock-Markets-Analytics/blob/main/Src/Module4_Pic/Module1_3.png' style="width: 90%;">

# 2.Less Ferature is More
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">

# 2.2 Hyper Tuning
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">
<img src='' style="width: 60%;">

# 3. Predicting Strong Future Growth
### 3.1 New column `is_strong_positive_growth_5d_future`
<img src='https://github.com/GawainGan/Stock-Markets-Analytics/blob/main/Src/Module4_Pic/Module3_1.png' style="width: 60%;">

### 3.2 Set `is_strong_positive_growth_5d_future` as target to train the model
<img src='https://github.com/GawainGan/Stock-Markets-Analytics/blob/main/Src/Module4_Pic/Module3_2.png' style="width: 70%;">

### 3.3 Return the best simuation result (best CAGR)
<img src='https://github.com/GawainGan/Stock-Markets-Analytics/blob/main/Src/Module4_Pic/Module3_3.png' style="width: 80%;">

# 4. Expand the Strategy
In the trading simulation mentioned above, we can implement at least two detailed improvements without requiring extensive financial knowledge:

**1.	Enhanced Prediction Utilization:**
For the models we use, instead of outputting only binary 0/1 results, we can output probability scores (applicable to both decision and random forest classifiers). 
By utilizing probability scores, we can adjust our investment amounts based on the confidence level of the predictions. 
This approach allows for more nuanced capital allocation, rather than using a uniform investment amount for each prediction, similar to the “grid trading” or “turtle trading” methods.

**2.	Stop Loss Implementation:**
It appears that the current model environment does not have a clear stop loss rule. 
Without a stop loss, significant downturns could lead to severe losses. 
Therefore, we should establish a clear exit mechanism. 
For instance, we could implement a rule such as “exit the trade if the value decreases by 5%-10% from the entry point.” 
This would help mitigate potential losses and protect the trading capital.

By incorporating these strategies, we can better optimize our trading approach, efficiently utilize our capital, and manage risks more effectively.








