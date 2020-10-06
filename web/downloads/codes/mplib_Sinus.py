def make_chart_mplib(model_name):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.grid(True)

    #points = str_to_class(model_name).query.all()
    points = str_to_class(model_name).query.all()
    xx = [point.x for point in points]
    yy = [point.y for point in points]
    axis.plot(xx, yy)
    axis.set_xlabel('x')
    axis.set_ylabel('y')
    axis.set_title('Matplotlib')

    return fig
