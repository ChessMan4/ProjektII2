import tkinter as tk
from tkinter import filedialog
from tkinter import *
import pandas as pd
import datetime
import pdfkit
import numpy as np

# nastaveni
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
options = {"enable-local-file-access": None}

win = tk.Tk()

win.title("AGR")
win.geometry("640x360")

# funkce pro nacteni souboru
def browse_button():
    global folder_path
    filename = filedialog.askopenfilename(filetypes =(("CSV Files","*.csv"),))
    folder_path.set(filename)
    pd.set_option('display.max_columns', None)
    pd.set_option("display.max_rows", None)
    global data
    data = pd.read_csv(filename)

# konec
def quit():
    win.destroy()

# zpracovani nacteneho souboru
def DoTheJob():
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

# tlacitka, labely
text = Label(master=win, text="This is automated report system", font=("TkDefaultFont 16 bold"))
text.place(relx=0.5, y=25, anchor=CENTER)

text = Label(master=win, text="Please select folder with data", font=("TkDefaultFont 12"))
text.place(relx=0.5, y=60, anchor=CENTER)

folder_path = StringVar()
foldpath = Label(master=win, textvariable=folder_path)
foldpath.place(y = 80, anchor = NW)

browse = tk.Button(text="Choose file", command=browse_button)
browse.place(x=560, y=80)

index = Label(master=win, text="Indicators we want to include in table ")
index.place(y = 130, anchor = NW)

index1 = tk.Entry(master=win )
index1.insert(0, "index1")
index1.place(x=340, y=140, anchor=CENTER)

index2 = tk.Entry(master=win )
index2.insert(0, "index2")
index2 .place(x=490, y=140, anchor=CENTER)

columns = Label(master=win, text="Columns we want to include in table ")
columns.place(y = 170, anchor = NW)

columns1 = tk.Entry(master=win )
columns1.insert(0, "columns1")
columns1.place(x=340, y=180, anchor=CENTER)

columns2 = tk.Entry(master=win )
columns2.insert(0, "columns2")
columns2.place(x=490, y=180, anchor=CENTER)

value = Label(master=win, text="Column with number of rows")
value.place(y = 210, anchor = NW)

value1 = tk.Entry(master=win )
value1.insert(0, "value")
value1.place(x=340, y=220, anchor=CENTER)

foldnametext = Label(master=win, text="Name of PDF file")
foldnametext.place(y = 250, anchor = NW)

foldname = tk.Entry(master=win )
foldname.insert(0, "report.pdf")
foldname.place(x=340, y=260, anchor=CENTER)

proceed= Button(text="Proceed", command=DoTheJob)
proceed.place(x=220, y = 320)

cancel = Button(text="Cancel", command=quit)
cancel.place(x=420, y = 320)

win.mainloop()
