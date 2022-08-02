import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objs as go
import os
"""
sudo pip install plotly
sudo pip install plotly.express
sudo pip install -U kaleido
"""

def plotly_plot(df_,x_axis,y_axis):
    """
    plots graph with axis names
    """
    fig = px.line(df_, x=x_axis, y=y_axis,title=f"{y_axis} by {x_axis}")
    
    fig.update_layout(
        title=f"{y_axis} by {x_axis}",
        title_x=0.3,
        xaxis_title=f"{x_axis}",
        yaxis_title=f"{y_axis} (%)",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="Black"
        )
    )    
    fig.show()
    if not os.path.exists("plots"):
        os.mkdir("plots")
    plotly.offline.plot(fig, image_filename=f"plots/{y_axis}_by_{x_axis}.png", image='png')
    #fig.write_image(f"plots/{y_axis}_by_{x_axis}.png")

def process_df(df):
    """
    reindex for date to be reversed and rename col to correct axis   
    """
    df = df.reindex(index=df.index[::-1])
    df.rename(columns={'Date (DD/MM/YY)': 'Date (MM/DD/YY)'},
          inplace=True, errors='raise')
    return df

def main():
    df = pd.read_csv('full_df.csv')
    print(df.columns[3:5])
    df = process_df(df)

    plotly_plot(df,'Date (MM/DD/YY)','Battery')
    plotly_plot(df,'Date (MM/DD/YY)','Capacity')

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date (MM/DD/YY)'], y=df['Battery'],
                        mode='lines',
                        name='Battery'))
    fig.add_trace(go.Scatter(x=df['Date (MM/DD/YY)'], y=df['Capacity'],
                        mode='lines+markers',
                        name='Capacity'))

    fig.update_layout(
        title="Capacity and Battery by Date",
        title_x=0.5,
        xaxis_title="Date (MM/DD/YY)",
        yaxis_title="Capacity and Battery (%)",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="Black"
        )
    )

    fig.show()
    plotly.offline.plot(fig, image_filename=f"plots/Capacity+and_Battery_by_Time.png", image='png')
    
    print(df)



if __name__ == '__main__':
    main()
