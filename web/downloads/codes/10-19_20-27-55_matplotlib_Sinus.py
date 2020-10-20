def make_chart_matplotlib(model_name, options):
    ''' Fetches the data from database and makes chart figure that will be shown on the webpage '''
    ''' Get data for plotting '''
    points = make_points(model_name)

    xx = [point[0] for point in points]
    yy = [point[1] for point in points]

    print("[MAKE_CHART_MATPLOTLIB]")
    print(f"x: {xx}")
    print(f"y: {yy}")
    ''' Options for plotting '''
    kwargs = dict()

    kwargs['color']     = options.get('color', 'r')               # set color -> b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    kwargs['linewidth'] = options.get('line_width', 2)            # set witdh of the line 
    kwargs['linestyle'] = options.get('line_style', 'dashed')     # linestyle/ls:      {'-', '--', '-.', ':', ''}
    kwargs['marker']    = options.get('marker', '.')              # markers -> {'', '.', ',', '1', '2', 's', 'x', '+'}

    scatter_plot        = options.get('flag_scatter_plot', False) # dots or solid line
    show_grid           = options.get('flag_show_grid', False)    # show grid or not
    logscale_y          = options.get('flag_logscale_y', False )  # logarithmic scale
    show_legend         = options.get('flag_show_legend', False)  # show_legend
  


    ''' Get the figure object that will be returned '''
    fig = Figure(figsize=(5.0, 5.0))
    chart = fig.add_subplot(1, 1, 1)

    if logscale_y:
        chart.semilogy()  # set logscaly for  Y

    chart.grid(show_grid) 
    if show_legend:
        chart.legend()


    chart.set_xlabel('x')
    chart.set_ylabel('y')
    chart.set_title('Matplotlib')
    
    ''' Plot on the figure and return this object to embed in web page '''
    if scatter_plot:
        kwargs['s'] = 20*kwargs['linewidth'] # marker size
        chart.scatter(xx, yy, **kwargs)
    else:
        kwargs['marker'] = None 
        chart.plot(xx, yy, **kwargs)

    
    return fig
