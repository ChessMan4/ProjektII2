    # tabulka
    index = index1.get()
    indexx = index2.get()

    columns = columns1.get()
    columnss = columns2.get()

    value = value1.get()

    global data
    pivot = pd.pivot_table(data, values=value, index=[index, indexx],
                           columns=[columns, columnss], aggfunc=np.sum, fill_value=0)

    # graf
    plot = pivot.plot(kind='bar', figsize=(12, 6))
    plot.tick_params(rotation=40)
    image = plot.get_figure().savefig('plot.png')

    # konecna slozka
    folname = foldname.get()

    ## html + css template
    image_tag = '<img src="plot.png">'
    heading = '<h1>Report</h1>'
    subh = '<h2>Automated report system</h2>'

    now = datetime.datetime.now()
    current_time = now.strftime("%d/ %m/ %Y  %H: %M: %S")

    header = '<div class="top">' + heading + subh +'</div>'
    footer = '<div class="bottom"> <h3>This report has been Generated\n on ' + current_time + '</h3></div>'

    content = '<div class="table"> ' + pivot.to_html() + '</div> \n <div class="chart">' + image_tag + '</div>'

    html = header + content + footer

    css = '<style> body {\n text-align:center; \n}\n table{\n margin:0px auto;\n}</style>'
    html = html + css

    ## generovani reportu v html
    with open('report.html', 'w+') as file: file.write(html)

    ## prevedeni html do pdf
    pdfkit.from_file('report.html', folname, configuration=config, options=options)
