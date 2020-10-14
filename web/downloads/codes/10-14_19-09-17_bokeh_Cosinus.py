def make_chart_bokeh(model_name):
    Model = str_to_class(model_name)
    points = Model.query.all()

    xx = [point.x for point in points]
    yy = [point.y for point in points]

    chart = figure(title="Bokeh plot", width=500, height=450, x_axis_label='x', y_axis_label='y')
    chart.line(xx, yy)
    

    return chart
