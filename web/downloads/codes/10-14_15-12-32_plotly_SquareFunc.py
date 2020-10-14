def make_chart_plotly(model_name):
    Model = str_to_class(model_name)
    points = Model.query.all()
    
    xx = [point.x for point in points]
    yy = [point.y for point in points]
    chart_props = {
        "data": [go.Line(x=xx, y=yy)],
        "layout": go.Layout(title="Plotly chart", title_x=0.5, xaxis_title="x", yaxis_title="y", width=500, height=500, margin={"l": 20, "t": 30})
        
    }
    
    chart_div_html = plotly.offline.plot(chart_props, include_plotlyjs=False, output_type='div')
    return chart_div_html
