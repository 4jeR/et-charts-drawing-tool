def make_chart_matplotlib(model_name):
    fig = Figure(figsize=(5.0, 5.0))
    axis = fig.add_subplot(1, 1, 1)
    axis.grid(True)
    Model = str_to_class(model_name)

    points = Model.query.all()
    xx = [point.x for point in points]
    yy = [point.y for point in points]
    axis.plot(xx, yy)
    axis.set_xlabel('x')
    axis.set_ylabel('y')
    axis.set_title('Matplotlib')
    return fig
