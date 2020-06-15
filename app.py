import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import glob, os
import plotly.express as px
from dash.dependencies import Input, Output, State
import base64
import datetime
import io
import numpy as np
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(html.Header(children='Framework SCA', style={
        'padding': ' 60px',
        'text-align': 'left',
        'background': '#0b095c',
        'color': 'white',
        'font-size': '30px'
    })),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Atacar', value='tab-1'),
        dcc.Tab(label='Plot', value='tab-2'),
        dcc.Tab(label='Capturar', value='tab-3'),
    ]),
    html.Div(id='tabs-content')

])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([

            html.P(html.H5(
                'En que carpeta quieres que se guarde tu ataque')),
            dcc.Input(id="input-carpeta", type="text", value="/home/jaimeb/Documentos/Framework/ataques/",
                      style={'width': '50%'}),
            html.P(html.H5(
                'Escribe el número de trazas que quieres utilizar en el ataque')),
            dcc.Input(id="input-trazas", type="text", value="Máximo 64000", style={'width': '50%'}),
            html.P(html.H5(
                'Si quieres que sea un ataque gradual, escribe como quieres que sean los intervalos')),
            dcc.Input(id="input-intervalos", type="text", value="0", style={'width': '50%'}),
            html.P(html.H5(
                'Elige el directorio que contenga las muestras de ataque')),

            dcc.Dropdown(id='input-dir',
                         options=[{'label': file, 'value': file} for file in
                                  glob.glob("/home/jaimeb/Documentos/Framework/muestras*")], style={'width': '50%'}

                         ),
            dcc.Dropdown(id='dropdown-algo',
                         options=[{'label': 'CPA', 'value': 'cpa'},
                                  {'label': 'DPA', 'value': 'dpa'},
                                  {'label': 'CDPA', 'value': 'cdpa'}], style={'width': '50%'}

                         ),
            html.Button(id='submit-button-ataque', n_clicks=0, children='Submit'),
            html.Div(id='output-state-ataque'),
            html.Div(id='output-status')

        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Tabs(id="tabs-plot", value='tab-plot-1', children=[
                dcc.Tab(label='plot', value='tab-plot-1'),
                dcc.Tab(label='gradual plot', value='tab-plot-2')]),
            html.Div(id='tabs-content-plot')

        ])
    elif tab == 'tab-3':
        return html.Div([
            html.P(html.H5(
                'Elige el nombre de la carpeta en la que se guardarán tus muestras')),
            dcc.Input(id="input-carpeta-muestreo", type="text", value="--",
                      style={'width': '50%'}),
            html.P(html.H5(
                'Escribe el nombre del fichero de datos que quieras utilizar')),
            dcc.Input(id="input-ficherodatos", type="text", value="--", style={'width': '50%'}),
            html.P(html.H5(
                'Escribe el número de trazas que quieras capturar')),
            dcc.Input(id="input-nmuestras", type="text", value="0", style={'width': '50%'}),
            html.Button(id='submit-button-muestreo', n_clicks=0, children='Submit'),
            html.Div(id='output-muestreo')
        ])


@app.callback(Output('tabs-content-plot', 'children'),
              [Input('tabs-plot', 'value')])
def render_content_plot(tab):
    if tab == 'tab-plot-2':
        return html.Div([

            html.P(html.H5(
                'Elige la carpeta que quieres visualizar')),
            dcc.Dropdown(id='input-ncarpeta',
                         options=[{'label': file, 'value': file} for file in
                                  glob.glob("/home/jaimeb/Documentos/Framework/ataques/*")], style={'width': '50%'}),

            # AQUI TE FALTA PONER PESTAÑITA
            html.Div(id='output-state-key'),
            html.Button(id='submit-button-gradual', n_clicks=0, children='Submit'),

            html.Div(id='output-state-gradual')

        ])
    elif tab == 'tab-plot-1':
        return html.Div([
            html.P(html.H6(
                'Elige la carpeta y el debug que quieras visualizar')),

            dcc.Dropdown(id='input-dd',
                         options=[{'label': file, 'value': file} for file in
                                  glob.glob("/home/jaimeb/Documentos/Framework/ataques/*")], style={'width': '50%'}),
            html.Div(id='dropdown-intervalos'),
            html.Div(id='output-state-dropdown'),
            html.Div(id='output-state')
        ])


@app.callback(Output('output-state-gradual', 'children'),
              [Input('submit-button-gradual', 'n_clicks')],
              [State('input-ncarpeta', 'value'),
               State('input-key', 'value')]
              )
def update_output(n_clicks, inputcarpeta, inputkey):
    data2 = pd.DataFrame()
    intervalos = []
    for path in glob.glob(str(inputcarpeta) + "/*"):
        if os.path.isdir(path):
            intervalos.append(int(os.path.basename(path)))
    intervalos.sort()

    for i in intervalos:
        for path in glob.glob(str(inputcarpeta) + "/" + str(i) + "/paa.dat.progress*"):
            if os.path.isfile(path):
                data = pd.read_csv(path,
                                   names=['key', 'correlaciones con ' + str(i)], index_col='key', skiprows=16)
                data2 = pd.concat([data2, data], axis=1)

    fig = px.line(data2, x=intervalos, y=data2.loc[str(inputkey), :])

    for i in data2.index.values.tolist():
        fig.add_scatter(x=intervalos, y=data2.loc[i, :], name=i, opacity=0.1)
    data3 = data2.reset_index()
    return html.Div([

        dcc.Graph(id='graphplot2',
                  figure=fig
                  ), dash_table.DataTable(
            id='tabla-datos',
            columns=[{"name": i, "id": i} for i in data3.columns],
            data=data3.to_dict('records'),
        )

    ])


@app.callback(Output('output-state-key', 'children'),
              [Input('input-ncarpeta', 'value')],
              [State('input-ncarpeta', 'value')]
              )
def update_output(n_clicks, inputcarpeta):
    data2 = pd.DataFrame()
    intervalos = []
    for path in glob.glob(str(inputcarpeta) + "/*"):
        if os.path.isdir(path):
            intervalos.append(int(os.path.basename(path)))

    intervalos.sort()
    print(intervalos)
    for i in intervalos:
        for path in glob.glob(str(inputcarpeta) + "/" + str(i) + "/paa.dat.progress*"):
            if os.path.isfile(path):
                data = pd.read_csv(path,
                                   names=['key', 'correlaciones con ' + str(i)], index_col='key', skiprows=16)
                data2 = pd.concat([data2, data], axis=1)
                break
    data3 = data2.reset_index()
    return html.Div([

        dcc.Dropdown(id='input-key',
                     options=[{'label': col1, 'value': col1} for col1 in data3['index']], style={'width': '50%'}),

    ])


@app.callback(Output('dropdown-intervalos', 'children'),
              [Input('input-dd', 'value')],
              [State('input-dd', 'value')]
              )
def update_output(n_clicks, input1):
    b = []

    os.chdir(str(input1))
    for file in glob.glob(str(input1) + "/*"):
        b.append(file)
    os.chdir("/home/jaimeb/PycharmProjects/untitled1")
    return html.Div([

        dcc.Dropdown(id='dropdown-inter',
                     options=[{'label': col, 'value': col} for col in b], style={'width': '50%'}
                     )
    ])


@app.callback(Output('output-state-dropdown', 'children'),
              [Input('dropdown-inter', 'value')],
              [State('dropdown-inter', 'value')]
              )
def update_output(n_clicks, input1):
    b = []
    os.chdir(str(input1))
    for file in glob.glob(str(input1) + "/debug.*"):
        b.append(file)
    os.chdir("/home/jaimeb/PycharmProjects/untitled1")
    return html.Div([

        dcc.Dropdown(id='dropdown',
                     options=[{'label': col, 'value': col} for col in b],
                     multi=True
                     )
    ])


@app.callback(Output('output-state', 'children'),
              [Input('dropdown', 'value')],
              [State('dropdown', 'value')]
              )
def update_output_plot(n_clicks, inputplot):
    data2 = pd.read_csv(inputplot[0], names=[str(inputplot[0])])
    fig = px.line(data2, x=data2.index, y=data2[inputplot[0]])
    for i in range(1, len(inputplot)):
        data = pd.read_csv(inputplot[i], names=[str(inputplot[i])])
        data2 = pd.concat([data2, data], axis=1)
        fig.add_scatter(x=data2.index, y=data[inputplot[i]])
    return html.Div([

        dcc.Graph(id='graphplot',
                  figure=fig
                  )
    ])


@app.callback(Output('output-state-ataque', 'children'),
              [Input('submit-button-ataque', 'n_clicks')],
              [State('input-carpeta', 'value'),
               State('input-trazas', 'value'),
               State('input-intervalos', 'value'),
               State('input-dir', 'value'),
               State('dropdown-algo', 'value')])
def update_attack(n_clicks, inputcarpeta, inputtrazas, inputintervalos, inputdir, algo):
    inputtrazas = int(inputtrazas)
    inputintervalos = int(inputintervalos)
    if (inputintervalos == 0):
        n = 1
        os.system("byobu new -d -s server1")
        os.system("byobu send-keys -t server1.0 \" cd /home/jaimeb/Documentos/Framework/\" ENTER")
        os.system("byobu send-keys -t server1.0 \"./gradual.sh " + str(n) + " " + str(inputtrazas) + " " + str(
            inputcarpeta) + " " + str(inputdir) + " " + str(algo) + "\" ENTER")

        os.system("byobu send-keys -t server1.0 \"+{F6}\" ENTER")
    else:
        n = (inputtrazas / inputintervalos) - ((inputtrazas % inputintervalos) / inputintervalos)
        os.system("byobu new -d -s server1")
        os.system("byobu send-keys -t server1.0 \" cd /home/jaimeb/Documentos/Framework/\" ENTER")
        os.system("byobu send-keys -t server1.0 \"./gradual.sh " + str(int(n)) + " " + str(inputintervalos) + " " + str(
            inputcarpeta) + " " + str(inputdir) + " " + str(algo) + "\" ENTER")

        os.system("byobu send-keys -t server1.0 \"+{F6}\" ENTER")
    os.chdir("/home/jaimeb/PycharmProjects/untitled1")
    return html.Div([
        html.Div("El ataque ha sido lanzado con éxito, puede comprobar el progreso con el botón Check Status"),
        html.Button('Check Status', id='submit-status', n_clicks=0)]
    )


@app.callback(Output('output-status', 'children'),
              [Input('submit-status', 'n_clicks')],
              [State('input-carpeta', 'value'),
               State('input-trazas', 'value'),
               State('input-intervalos', 'value'),
               ]
              )
def update_attack(n_clicks, inputcarpeta, inputtrazas, inputintervalos):
    inputtrazas = int(inputtrazas)
    inputintervalos = int(inputintervalos)
    intervalos = []
    if (inputintervalos == 0):

        ataques = inputtrazas
    else:
        n = (inputtrazas / inputintervalos) - ((inputtrazas % inputintervalos) / inputintervalos)
        ataques = range(inputintervalos, (inputintervalos * int(n) + 1), inputintervalos)

    for path in glob.glob(str(inputcarpeta) + "/*"):
        if os.path.isdir(path):
            intervalos.append(int(os.path.basename(path)))
    return html.Div([
        html.Div("Han finalizados los  " + str(len(intervalos)) + " primeros ataques, faltan  " + str(
            len(ataques) - len(intervalos)))
    ]
    )


@app.callback(Output('output-muestreo', 'children'),
              [Input('submit-button-muestreo', 'n_clicks')],
              [State('input-carpeta-muestreo', 'value'),
               State('input-ficherodatos', 'value'),
               State('input-nmuestras', 'value')]
              )
def update_output(n_clicks, input1, input2, input3):
    if (n_clicks >= 1):
        x = "\"cd Space AEST\""

        os.system("sshpass -p 'adam' ssh -o StrictHostKeyChecking=no adam@192.168.1.70 byobu new -d -s server1")
        os.system(
            "sshpass -p 'adam' ssh -o StrictHostKeyChecking=no adam@192.168.1.70 byobu send-keys -t server1.0 " + x + " ENTER")
        os.system("sshpass -p 'adam' ssh -o StrictHostKeyChecking=no adam@192.168.1.70 byobu send-keys -t server1.0 "
                  "\"sudo Space ./server\" ENTER")
        os.system("sshpass -p 'adam' ssh -o StrictHostKeyChecking=no adam@192.168.1.70 byobu send-keys -t server1.0 "
                  "\"adam\" ENTER")
        os.system(
            "sshpass -p 'adam' ssh -o StrictHostKeyChecking=no adam@192.168.1.70 byobu send-keys -t server1.0 \"+{"
            "F6}\" ""ENTER")
        os.system("sshpass -p 'adam' ssh -o StrictHostKeyChecking=no adam@192.168.1.70 exit")
        os.system("sshpass -p 'adam' ssh -o StrictHostKeyChecking=no adam@192.168.1.56 byobu new -d -s loop")
        os.system("sshpass -p 'adam' ssh -o StrictHostKeyChecking=no adam@192.168.1.56 byobu send-keys -t loop.0 "
                  "\"sudo Space ./Mloop.sh Space " + input1 + " Space " + input2 + " Space " + input3 + "\" ENTER")
        os.system(
            "sshpass -p 'adam' ssh -o StrictHostKeyChecking=no adam@192.168.1.56 byobu send-keys -t loop.0 \"adam\" "
            "ENTER")
        os.system(
            "sshpass -p 'adam' ssh -o StrictHostKeyChecking=no adam@192.168.1.56 byobu send-keys -t loop.0 \"+{F6}\" "
            "ENTER")

        return html.Div([

            'Ya se ha lanzado el proceso de captura'

        ])
    return html.Div([

        'Pulsa submit para empezar a capturar'

    ])


if __name__ == "__main__":
    app.run_server()
