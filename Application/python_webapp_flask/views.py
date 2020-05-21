"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from python_webapp_flask import app

from flask import Flask, render_template,request
import plotly
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import numpy as np
import json

from programs import gran_postgres


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

def create_line_chart(df, x_axis, y_axis, text_axis, group_axis):

    fig = go.Figure()

    # columns: date, close_price, symbol, simple_name

    data = []
    count = 0
    for group in df[group_axis].unique():

        df_sub = df[df[group_axis] == group]

        # cut clutter by only displaying four items at start
        if count < 4:
            visible = True
        else:
            visible = 'legendonly'

        data.append(go.Scatter(
            x = df_sub[x_axis],
            y = df_sub[y_axis],
            visible=visible,
            mode = 'lines',
            name = group,

        ))
        count += 1


    layout = go.Layout(
        title = 'Robinhood lineplot',
        showlegend = True,
        yaxis = {'title': y_axis},
        xaxis = {'title': x_axis},
        template='plotly_dark'
    )

    fig = dict(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/visualise')
def visualise():
    """Renders the visualize page."""

    # get df of stocks
    artifact = gran_postgres.StockConn()
    S2 = artifact.get_stocks_df()
    columns = S2.columns

    # create table
    #table = create_table(S2, columns)

    # create line graph
    x_axis, y_axis, group_axis = 'date', 'close_price', 'symbol'
    linechart = create_line_chart(S2, x_axis, y_axis, y_axis, group_axis)

    return render_template(
        'visualise.html',
        linechart=linechart,
        #table=table,
        title='Visualise',
        year=datetime.now().year,
        message='Visualize digested data using plotly'
    )
