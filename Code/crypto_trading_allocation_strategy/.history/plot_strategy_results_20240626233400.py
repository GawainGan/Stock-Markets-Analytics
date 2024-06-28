import pandas as pd
import plotly.graph_objects as go

def plot_strategy_results(df, date_range):
    # Create the cumulative weighted PnL column
    df_copy = df.copy()
    df_copy['cumulative_weighted_pnl'] = df_copy['weighted_pnl'].cumsum()

    # Create the plot
    fig = go.Figure()

    # Add the cumulative weighted PnL line
    fig.add_trace(go.Scatter(
        x=date_range,
        y=df_copy['cumulative_weighted_pnl'],
        mode='lines',
        name='Cumulative Weighted PnL',
        line=dict(color='blue')
    ))

    # Update layout
    fig.update_layout(
        title='Cumulative Weighted PnL over Time with Annotations for Non-zero Classes',
        xaxis_title='Time',
        yaxis_title='Cumulative Weighted PnL',
        # template='plotly_white'
    )

    # Show the plot
    fig.show()

    # Define shape and color map for different classes
    class_marker_map = {
        '1': {'color': 'red', 'symbol': 'circle', 'size': 10},
        '2.1': {'color': 'blue', 'symbol': 'triangle-up', 'size': 8},
        '2.2': {'color': 'blue', 'symbol': 'triangle-up', 'size': 8},
        '2.3': {'color': 'blue', 'symbol': 'triangle-up', 'size': 8},
        '3.1': {'color': 'green', 'symbol': 'square', 'size': 6},
        '3.2': {'color': 'green', 'symbol': 'square', 'size': 6},
        '3.3': {'color': 'green', 'symbol': 'square', 'size': 6}
    }

    # Create the plot
    fig = go.Figure()

    # Add the cumulative weighted PnL line
    fig.add_trace(go.Scatter(
        x=date_range,
        y=df_copy['cumulative_weighted_pnl'],
        mode='lines',
        name='Cumulative Weighted PnL',
        line=dict(color='blue')
    ))

    # Add Class and Weight points to the plot
    for class_type in df_copy['class'].unique():
        if class_type not in class_marker_map:
            continue
        class_df = df_copy[df_copy['class'] == class_type]
        marker = class_marker_map[str(class_type)]
        fig.add_trace(go.Scatter(
            x=date_range[:len(class_df)],
            y=class_df['cumulative_weighted_pnl'],
            mode='markers',
            name=f'Class {class_type}',
            marker=dict(color=marker['color'], symbol=marker['symbol'], size=marker['size']),
            text=[f"Class: {row['class']}<br>Weight: {row['weight']:.2f}" for index, row in class_df.iterrows()],
            hoverinfo='text'
        ))

    # Update layout
    fig.update_layout(
        title='Cumulative Weighted PnL over Time with Annotations for Non-zero Classes',
        xaxis_title='Time',
        yaxis_title='Cumulative Weighted PnL',
        # template='plotly_white'
    )

    # Show the plot
    fig.show()

