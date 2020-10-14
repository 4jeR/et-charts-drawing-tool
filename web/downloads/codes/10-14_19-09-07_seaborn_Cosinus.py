def make_chart_seaborn(model_name):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title('Seaborn')

    axis.grid(True)
    sb.set(style="darkgrid")

    Model = str_to_class(model_name)
    points = Model.query.all()
    data = [
        {model_name: point.x, model_name: point.y} for point in points
    ]
    
    df = pd.DataFrame(data=data)
    sb.lineplot(data=df, ax=axis)
    
    return fig
