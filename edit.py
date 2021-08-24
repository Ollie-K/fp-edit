#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 15:17:26 2021

@author: ollie
"""


from rdflib import Graph
import pandas as pd


import os
import json
import numpy as np
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import Levenshtein as lev

import dash_cytoscape as cyto

g = Graph()
g.parse("13-8-inference.ttl", format="ttl")
node_lex = pd.read_csv('13-8-nodes.csv')

def sim_score(a, b):
    a = a.lower()
    b = b.lower()
    denom = len(b)
    if len(a) > len(b):
        denom = len(a)
    c = (lev.distance(a, b) / denom)
    return c




asset_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'assets'
)

app = dash.Dash(__name__, assets_folder=asset_path)
server = app.server
cyto.load_extra_layouts()

    
with open('onto-positions.json') as f:
    onto_elements = json.loads(f.read())

with open('map_pos.json') as f:
    map_elements = json.loads(f.read())

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(0.45*(20vh)',
        'border': 'thin lightgrey solid',
    },
    'tab': {'height': 'calc(20vh-100px)'}
}
dd_style=[
                {
            'selector': '.Academic',
            'style': {
               'display': 'none'
            }
        }, 
                  
                   {
            'selector': '.Article',
            'style': {
               'display': 'none'
            }
        }, 
                    
            {
                'selector': '.Method',
                'style':{
                    'display': 'none',

                    }
                },
            
        {
            'selector': '.Publication',
            'style': {
                'display': 'none',

            }
        }, 
        ]    

all_style = [
                {
                'selector': 'edge',
                'style': {'width':'4',
                    'content': 'data(label)',
                    'text-rotation':'autorotate',
                    'opacity': '0.7',
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'vee',
                    'arrow-scale': 2
                }},
                {
                'selector': 'edge[label="equivalentClass"]',
                'style': {
                    'visibility': 'hidden'
                }},
                
                                {
                'selector': 'node[label="Thing"]',
                'style': {
                    'display': 'none'
                }},
                                
                                                {
                'selector': 'node[label="Nothing"]',
                'style': {
                    'display': 'none'
                }},
                {
            'selector': '.Actor',
            'style': {
                'background-color': '#fb8072',
                'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2',
            }
        }, 
                  {
            'selector': '.Action',
            'style': {
                'background-color': '#b3de69',
                'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2',
            }
        }, 
                    {
            'selector': '.Issue',
            'style': {
                'background-color': '#80b1d3',
                'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2',
            }
        }, 
            {
                'selector': '.Method',
                'style':{
                    'background-color': '#ffffb3',
                    'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2'
                    }
                },
            {
            'selector': '.Place',
            'style': {
                'background-color': '#fdb462',
                    'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2'
            }
        }, 
        {
            'selector': '.Publication',
            'style': {
                'background-color': '#8dd3c7',
                    'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2'
            }
        }, 
            {
            'selector': '.Literal',
            'style': {
                'background-color': '#d9d9d9',
                    'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2'
            }
        }, 
            
            {
            'selector': ':selected',
            'style': {
                'background-color': '#bc80bd',
                    'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2'
            }
        },
        ]
with open('positions.json') as f:
    full_data = json.loads(f.read())



app.layout = html.Div([
    html.Div(className='eight columns', children=[
        
        

          cyto.Cytoscape(
            id='food-pol-net',
            boxSelectionEnabled= True,

            elements=full_data,
            layout={
                'name': 'preset','spacingFactor':'4'
            },
            style={
                'height': '74vh',
                'width': '100%'
            },
            stylesheet=all_style + dd_style
        ),
        
        html.Div(className='four columns', children=[
        dcc.Tabs(id='tabs', children=[
            dcc.Tab(label='Legend', children=[
                html.Div(style=styles['tab'], children=[
                    html.P(children=['Classes:',
                    html.Div(),
                    html.Button('Actor', style={'background-color': '#fb8072', 'fontSize': 13}),
                    html.Button('Action', style={'background-color': '#b3de69', 'fontSize': 13}),
                    html.Button('Issue', style={'background-color': '#80b1d3', 'fontSize': 13}),
                    html.Button('Method', style={'background-color': '#ffffb3', 'fontSize': 13}),
                    html.Button('Place', style={'background-color': '#fdb462', 'fontSize': 13}),
                    html.Button('Publication', style={'background-color': '#8dd3c7', 'fontSize': 13}),
                    html.Button('Literal/Descriptive', style={'background-color': '#d9d9d9', 'fontSize': 13}),
                    ]),
                    html.P(children=['On Selection:',
                    html.Div(),
                    html.Button('Selected Node/Edge(s)', style={'background-color': '#bc80bd', 'fontSize': 13}),
                    html.Div(),
                    html.Button('Edges To Selected Node', style={'background-color': '#fccde5', 'fontSize': 13}),
                    html.Button('Edges From Selected Node', style={'background-color': '#bebada', 'fontSize': 13}),
                    ])])
                ]),
            
            dcc.Tab(label='Selected Node Info', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Selected Node Data'),
                    html.Pre(
                        id='tap-node-data',
                        style=styles['json-output']
                    ),                    
                   
                        ])
                    ]),  
            
            
            dcc.Tab(label='Navigation', children=[
                html.Div(style=styles['tab'], children=[
                    html.P(children=['Search:',
                    dcc.Input(id='search-box', type='text', placeholder='Search Term e.g. NFPOs'),
                    html.Button("Search", id='search-button')]),
                    
                    html.P(children=['Explore:',
                    html.Button("Focus On Selected Node(s)", id='focus-button'),       
                    html.Button("Expand Selected Node(s)", id='expand-button')]),

                    html.P(children=['Load Interaction Pathways:',
                    html.Button("Show Actor-Action-Issue Paths", id='path-button'),
                    html.Button("Show Actor-Action-Actor Paths", id='aapath-button')]),
                    html.P(children=['Load Overviews',
                    html.Button("Load Entire Dataset", id='full-button'),
                    html.Button("Load Class Hierarchy", id='onto-button'),
                    html.Button("Load Class Schema", id='map-button')]),
                    
                    ])
                ]),
            
             dcc.Tab(label='Display Options', children=[
                html.Div(style=styles['tab'], children=[

                    
                    html.P('Node Display Options:'),
                    dcc.RadioItems(
                    id='display-radio',
                    options=[{'label': 'Hide Academics, Articles, Methods & Publications', 'value': 'dummy-button'}, 
                             {'label': 'Show All Data', 'value': 'all-button'}], value='dummy-button'),
                    dcc.Checklist(
                        id="nodes-checklist",
                        options=[
                        {"label": "Actor", "value": "Actor"},
                         {"label": "Action", "value": "Action"},
                         {"label": "Issue", "value": "Issue"},
                         {"label": "Place", "value": "Place"},
                         {"label": "Publication", "value": "Publication"},
                         {"label": "Method", "value": "Method"},
                         {"label": "Descriptive Info", "value": "Literal"},

                        ],
                        value=['Actor', 'Action', 'Issue'],),
                    html.P('Hidden Edges:'),
                    dcc.Checklist(
                        id="edges-checklist",
                        options=[
                        {"label": "actionImpacts", "value": "actionImpacts"},
                        {"label": "activeIn", "value": "activeIn"},
                        {"label": "concernsPlace", "value": "concernsPlace"},
                        {"label": "interactWith", "value": "interactWith"},
                        {"label": "issueIn", "value": "issueIn"},
                        {"label": "locatedIn", "value": "locatedIn"},
                        {"label": "publishedIn", "value": "publishedIn"},
                        {"label": "relatesTo", "value": "relatesTo"},
                        {"label": "takeAction", "value": "takeAction"},
                        {"label": "usesMethod", "value": "usesMethod"},
                        {"label": "workingOn", "value": "workingOn"},
                        {"label": "wrote", "value": "wrote"},
                        {"label": "subClassOf", "value": "subClassOf"},
                        {"label": "type", "value": "type"},
                        
                        
                        
                        

                        
                        ],
                        value=[],
                        labelStyle={"display": "inline-block"},
                    )

                
                    ])
                ]),
             
             dcc.Tab(label='Editing Toolkit', children=[
                html.Div(style=styles['tab'], children=[
                    
                    html.P(children=['Add Node:', dcc.Input(id='node-name', type='text', placeholder='Name (e.g. Trussell Trust)'),
                    dcc.Input(id='node-class', type='text', placeholder='Classes (e.g. Actor, Charity, Group)'),
                    html.Button("Add Node", id='node-button')]),


                    html.P(children=['Connect Selected Nodes:', dcc.Input(id='edge-name', type='text', placeholder='Edge Label (e.g. worksFor)'), html.Button("Connect Nodes", id='edge-button')]),
                    
           
                    html.P(children=['Remove Selected Node(s)/Edge(s):',html.Button("Remove Selected", id='remove-button')]),
                    
                    
                    ])
                ]),
             
            
        ]),
    ]),
        
       
  
    
    
])
])


@app.callback((Output('food-pol-net', 'elements'),
                Output('food-pol-net', 'layout'),
                Output('food-pol-net', 'stylesheet')),
              [Input('food-pol-net', 'tapNode'),
               Input('food-pol-net', 'selectedEdgeData'),
               Input('full-button', 'n_clicks'),
               Input('node-name', 'value'),
                Input('node-class', 'value'),
                Input('node-button', 'n_clicks'),
                Input('edge-name', 'value'),
                Input('edge-button', 'n_clicks'),
                Input('onto-button', 'n_clicks'),
                Input('path-button', 'n_clicks'),
                Input('map-button', 'n_clicks'),
                Input('aapath-button', 'n_clicks'),
                Input('display-radio', 'value'),
                Input("nodes-checklist", "value"),
                Input("edges-checklist", "value"),
                Input('search-button', 'n_clicks'),
                Input('remove-button', 'n_clicks'),
                Input('expand-button', 'n_clicks'),
                Input('focus-button', 'n_clicks'),

                ],
              [State('food-pol-net', 'elements'),
                State('food-pol-net', 'layout'),
                State('food-pol-net', 'stylesheet'),
                State('search-box', 'value'),
                State('food-pol-net', 'selectedNodeData'),
                State('food-pol-net', 'selectedEdgeData')]
              )
def function(tapnode, tapedge, full_button, nname, nclass, ngen, ename, egen, onto_button, path_button, map_button, aa_path, display, nodes, edges, search_button, remove_button, expand_button, focus, elements, layout, stylesheet, search_term, data_n, data_e):
    dd_style=[
                {
            'selector': '.Academic',
            'style': {
               'display': 'none'
            }
        }, 
                  
                   {
            'selector': '.Article',
            'style': {
               'display': 'none'
            }
        }, 
                    
            {
                'selector': '.Method',
                'style':{
                    'display': 'none',

                    }
                },
            
        {
            'selector': '.Publication',
            'style': {
                'display': 'none',

            }
        }, 
        ]    

    all_style = [
                {
                'selector': 'edge',
                'style': {'width':'4',
                    'content': 'data(label)',
                    'text-rotation':'autorotate',
                    'opacity': '0.7',
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'vee',
                    'arrow-scale': 2
                }},
                {
                'selector': 'edge[label="equivalentClass"]',
                'style': {
                    'visibility': 'hidden'
                }},
                
                                {
                'selector': 'node[label="Thing"]',
                'style': {
                    'display': 'none'
                }},
                                
                                                {
                'selector': 'node[label="Nothing"]',
                'style': {
                    'display': 'none'
                }},
                {
            'selector': '.Actor',
            'style': {
                'background-color': '#fb8072',
                'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2',
            }
        }, 
                  {
            'selector': '.Action',
            'style': {
                'background-color': '#b3de69',
                'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2',
            }
        }, 
                    {
            'selector': '.Issue',
            'style': {
                'background-color': '#80b1d3',
                'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2',
            }
        }, 
            {
                'selector': '.Method',
                'style':{
                    'background-color': '#ffffb3',
                    'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2'
                    }
                },
            {
            'selector': '.Place',
            'style': {
                'background-color': '#fdb462',
                    'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2'
            }
        }, 
        {
            'selector': '.Publication',
            'style': {
                'background-color': '#8dd3c7',
                    'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2'
            }
        }, 
            {
            'selector': '.Literal',
            'style': {
                'background-color': '#d9d9d9',
                    'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2'
            }
        }, 
            
            {
            'selector': ':selected',
            'style': {
                'background-color': '#bc80bd',
                    'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2'
            }
        },
        ]
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    nodes_list = ['Actor', 'Action', 'Issue', 'Place', 'Publication', 'Method', 'Literal']
    if (button_id == 'full-button'):
        elements = full_data
        return (elements, {'name': 'preset', 'spacingFactor':'2'},  stylesheet)
    if (button_id == 'onto-button'):
        elements = onto_elements
        return (elements, {'name': 'preset'},  stylesheet)
    if (button_id == 'map-button'):
        elements = map_elements
        return (elements, {'name': 'preset'},  stylesheet)          
    
    if (button_id == 'path-button'):
        qres = g.query(
        """
        SELECT ?actor1 ?gen ?action ?rel ?issue 
        WHERE{
        
       ?action fp:relatesTo ?issue .
       ?action ?rel ?issue .

       ?actor1 fp:takeAction ?action .
       ?actor1 ?gen ?action .
        }
        """ )



        df = pd.DataFrame(columns=['source','interaction','target'])
        for row in qres:
               df= df.append({'source': row.action, 'interaction': row.rel, 'target': row.issue}, ignore_index=True)
               df= df.append({'source': row.actor1, 'interaction': row.gen, 'target': row.action}, ignore_index=True)
            
        df_out = df.drop_duplicates()
        df_out = df_out[~(df_out['interaction'].str.contains('rdf'))]
        df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
        df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
        df_out = df_out.drop_duplicates()
        df_out.replace("", float("NaN"), inplace=True)
        df_out.dropna(how='any', inplace=True)
        data = df_out
        
        new_node_table = pd.concat([data['source'], data['target']], axis=0)
        new_node_table = new_node_table.drop_duplicates() 
        
        node_types = pd.DataFrame(columns=['node', 'class'])
        for node in new_node_table:
            node = str(node).replace(' ', '_')
            qres = g.query(
                """
                SELECT  ?node_class 
                WHERE{
              <http://wrenand.co.uk/fpn/%s> rdf:type ?node_class . 
            } 
                """ % node)
            type_list = list()
    
            for row in qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
            if len(type_list) == 0:
                    type_list.append('Literal')
            node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
        type_dict = {}
        for index,row in node_types.iterrows():
            type_dict[row[0]] = row[1]
            
        new_nodes = list()
        for node in new_node_table:
            new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
    
        new_edges = [
            {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
            for index, row in data.iterrows()
        ]
        new_elements = new_nodes + new_edges
            
        return (new_elements, {'name': 'cose', 'spacingFactor':'4'}, stylesheet)
        
    if (button_id == 'aapath-button'):
        qres = g.query(
        """
        SELECT ?actor1 ?gen ?action ?imp ?actor2 
        WHERE{
       ?actor1 fp:takeAction ?action .
        ?actor1 ?gen ?action .
       ?action fp:actionImpacts ?actor2 .
       ?action ?imp ?actor2 .
       

        }
        """ )



        df = pd.DataFrame(columns=['source','interaction','target'])
        for row in qres:
               df= df.append({'source': row.action, 'interaction': row.imp, 'target': row.actor2}, ignore_index=True)
               df= df.append({'source': row.actor1, 'interaction': row.gen, 'target': row.action}, ignore_index=True)
            
        df_out = df.drop_duplicates()
        df_out = df_out[~(df_out['interaction'].str.contains('rdf'))]
        df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
        df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
        df_out = df_out.drop_duplicates()
        df_out.replace("", float("NaN"), inplace=True)
        df_out.dropna(how='any', inplace=True)
        data = df_out
        
        new_node_table = pd.concat([data['source'], data['target']], axis=0)
        new_node_table = new_node_table.drop_duplicates() 
        
        node_types = pd.DataFrame(columns=['node', 'class'])
        for node in new_node_table:
            node = str(node).replace(' ', '_')
            qres = g.query(
                """
                SELECT  ?node_class 
                WHERE{
              <http://wrenand.co.uk/fpn/%s> rdf:type ?node_class . 
            } 
                """ % node)
            type_list = list()
    
            for row in qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
            if len(type_list) == 0:
                    type_list.append('Literal')
            node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
        type_dict = {}
        for index,row in node_types.iterrows():
            type_dict[row[0]] = row[1]
            
        new_nodes = list()
        for node in new_node_table:
            new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
    
        new_edges = [
            {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
            for index, row in data.iterrows()
        ]
        new_elements = new_nodes + new_edges
            
        return (new_elements, {'name': 'dagre', 'spacingFactor':'4'}, stylesheet) 
    
    if (button_id == 'search-button') and search_term:
        
        node_lex['scores'] = np.vectorize(sim_score)(node_lex['node'], search_term)
        max_sim = node_lex['node'][node_lex['scores'].idxmin()]
        search_term = max_sim
        
        search_term = search_term.replace(' ', '_')
        qres = g.query(
        """
        SELECT ?p ?o
        WHERE{
        <http://wrenand.co.uk/fpn/%s> ?p ?o . 


        }
        """ % search_term)
        bqres = g.query(
            """
            SELECT ?s ?p 
            WHERE{
            ?s ?p <http://wrenand.co.uk/fpn/%s> . 

    
        }
        """ % search_term)
        
        df = pd.DataFrame(columns=['source', 'interaction', 'target'])

        for row in qres:
            df = df.append(
                {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
    
        for row in bqres:
            df = df.append({'source': row.s, 'interaction': row.p,
                            'target': search_term}, ignore_index=True)


        df_out = df.drop_duplicates()
        df_out = df_out[~(df_out['interaction'].str.contains('rdf'))]
        df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
        df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
        df_out = df_out.drop_duplicates()
        df_out.replace("", float("NaN"), inplace=True)
        df_out.dropna(how='any', inplace=True)
        data = df_out
        
        new_node_table = pd.concat([data['source'], data['target']], axis=0)
        new_node_table = new_node_table.drop_duplicates()
        if new_node_table.empty:
            new_node_table = [search_term]

        
        node_types = pd.DataFrame(columns=['node', 'class'])
        for node in new_node_table:
            node = str(node).replace(' ', '_')
            qres = g.query(
                """
                SELECT  ?node_class 
                WHERE{
              <http://wrenand.co.uk/fpn/%s> rdf:type ?node_class . 
            } 
                """ % node)
            type_list = list()
    
            for row in qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
            if len(type_list) == 0:
                    type_list.append('Literal')
            node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
        type_dict = {}
        for index,row in node_types.iterrows():
            type_dict[row[0]] = row[1]
            
        new_nodes = list()
        for node in new_node_table:
            new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})

        new_edges = [
            {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
            for index, row in data.iterrows()
        ]
        new_elements = new_nodes + new_edges
        stylesheet = all_style
        if (display == 'dummy-button'):
           stylesheet = stylesheet + dd_style

        for node in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
        for edge in edges:
            stylesheet.append({
            'selector': 'edge[label="%s"]' % edge,
            'style': {
                'display': 'none'
            }}) 
        stylesheet = stylesheet + [{
                'selector': 'node[id="%s"]' % search_term,
                'style': {
                    'display': 'element'
                }}]
       
        return (new_elements, {'name': 'dagre', 'spacingFactor':'2.5'}, stylesheet)
    
    if (button_id =='remove-button') and elements and data_n and data_e:
            nodes_to_remove = {ele_data['id'] for ele_data in data_n}
            edges_to_remove = {ele_data['id'] for ele_data in data_e}
            intermediate_elements = [ele for ele in elements if ele['data']['id'] not in nodes_to_remove]
            new_elements = [ele for ele in intermediate_elements if ele['data']['id'] not in edges_to_remove]
            return (new_elements, {'name': 'dagre', 'spacingFactor':'2.5'}, stylesheet)
        
    if (button_id =='remove-button') and elements and data_n:
            nodes_to_remove = {ele_data['id'] for ele_data in data_n}
            new_elements = [ele for ele in elements if ele['data']['id'] not in nodes_to_remove]
            return (new_elements, {'name': 'dagre', 'spacingFactor':'2.5'}, stylesheet)

    if (button_id =='remove-button') and elements and data_e:
            edges_to_remove = {ele_data['id'] for ele_data in data_e}
            new_elements = [ele for ele in elements if ele['data']['id'] not in edges_to_remove]
            return (new_elements, {'name': 'dagre', 'spacingFactor':'2.5'}, stylesheet)
    
    if (button_id =='expand-button') and elements and data_n:
        df = pd.DataFrame(columns=['source', 'interaction', 'target'])
        for ele in elements:
            if 'source' in ele['data']:
                df = df.append({'source':ele['data']['source'], 'interaction': ele['data']['label'], 'target':ele['data']['target']}, ignore_index=True)

        node_to_expand = {ele_data['id'] for ele_data in data_n}
        for node in node_to_expand:
            search_term = node
            qres = g.query(
            """
            SELECT ?p ?o
            WHERE{
            <http://wrenand.co.uk/fpn/%s> ?p ?o . 
            }"""% search_term)
            
            bqres = g.query(
                """
            SELECT ?s ?p
            WHERE{
          ?s ?p <http://wrenand.co.uk/fpn/%s> .
          } 

    
            """ % search_term)
            
            class_qres = g.query(
            """
            SELECT ?s
            WHERE{
            ?s a <http://wrenand.co.uk/fpn/%s> .
            }
            """ % search_term)
            
        
            if len(qres) > 0:
                for row in qres:
                    df = df.append(
                        {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
            if len(bqres) > 0:
                for row in bqres:
                    df = df.append({'source': row.s, 'interaction': row.p,
                                'target': search_term}, ignore_index=True)
            if len(class_qres) > 0:
                for row in class_qres:
                    df = df.append({'source': row.s, 'interaction': 'Type',
                                'target': search_term}, ignore_index=True)
            
            # df_out = df[~(df['interaction'].str.contains('rdf'))]
            
            # df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
            df_out = df.replace('http://wrenand.co.uk/fpn/', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2002/07/owl#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2000/01/rdf-schema#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2001/XMLSchema#', '', regex=True)
            df_out = df_out[(df_out['source'] != df_out['target'])]
            df_out = df_out[df_out['target'] != 'Class']
            df_out = df_out.drop_duplicates()
            df_out.replace("", float("NaN"), inplace=True)
            df_out.dropna(how='any', inplace=True)
            data = df_out
            
            new_node_table = pd.concat([data['source'], data['target']], axis=0)
            new_node_table = new_node_table.drop_duplicates()

            node_types = pd.DataFrame(columns=['node', 'class'])
            for node in new_node_table:
                node = str(node).replace(' ', '_')
                qres = g.query(
                    """
                    SELECT  ?node_class 
                    WHERE{
                  <http://wrenand.co.uk/fpn/%s> rdf:type ?node_class . 
                } 
                    """ % node)
                class_qres = g.query(
                    """
                    SELECT  ?node_class 
                    WHERE{
                  <http://wrenand.co.uk/fpn/%s> rdfs:subClassOf ?node_class . 
                } 
                    """ % node)    
                
                type_list = list()
    
                for row in qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
                for row in class_qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
                if len(type_list) == 0:
                    type_list.append('Literal')
                node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
            type_dict = {}
            for index,row in node_types.iterrows():
                type_dict[row[0]] = row[1]
                
                
                
            new_nodes = list()
            for node in new_node_table:
                new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
    
            new_edges = [
                {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
                for index, row in data.iterrows()
            ]
            
            elements = new_nodes + new_edges
            if len(elements) < 250:
                layout = {'name': 'dagre', 'spacingFactor':'5'}
            else:
                layout = {'name': 'cose', 'spacingFactor':'2.5'}
        return (elements, layout, stylesheet)
    if (button_id =='focus-button') and data_n:
        df = pd.DataFrame(columns=['source', 'interaction', 'target'])
        node_to_focus = {ele_data['id'] for ele_data in data_n}
        for node in node_to_focus:
            search_term = node
            qres = g.query(
            """
            SELECT ?p ?o
            WHERE{
            <http://wrenand.co.uk/fpn/%s> ?p ?o . 
            }"""% search_term)
            
            bqres = g.query(
                """
            SELECT ?s ?p
            WHERE{
          ?s ?p <http://wrenand.co.uk/fpn/%s> .
          } 

    
            """ % search_term)
            
            class_qres = g.query(
            """
            SELECT ?s
            WHERE{
            ?s a <http://wrenand.co.uk/fpn/%s> .
            }
            """ % search_term)
            
        
            if len(qres) > 0:
                for row in qres:
                    df = df.append(
                        {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
            if len(bqres) > 0:
                for row in bqres:
                    df = df.append({'source': row.s, 'interaction': row.p,
                                'target': search_term}, ignore_index=True)
            if len(class_qres) > 0:
                for row in class_qres:
                    df = df.append({'source': row.s, 'interaction': 'Type',
                                'target': search_term}, ignore_index=True)
            

            df_out = df.replace('http://wrenand.co.uk/fpn/', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2002/07/owl#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2000/01/rdf-schema#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2001/XMLSchema#', '', regex=True)
            df_out = df_out[(df_out['source'] != df_out['target'])]
            df_out = df_out[df_out['target'] != 'Class']
            df_out = df_out.drop_duplicates()
            df_out.replace("", float("NaN"), inplace=True)
            df_out.dropna(how='any', inplace=True)
            data = df_out
            
            new_node_table = pd.concat([data['source'], data['target']], axis=0)
            new_node_table = new_node_table.drop_duplicates()

            node_types = pd.DataFrame(columns=['node', 'class'])
            for node in new_node_table:
                node = str(node).replace(' ', '_')
                qres = g.query(
                    """
                    SELECT  ?node_class 
                    WHERE{
                  <http://wrenand.co.uk/fpn/%s> rdf:type ?node_class . 
                } 
                    """ % node)
                class_qres = g.query(
                    """
                    SELECT  ?node_class 
                    WHERE{
                  <http://wrenand.co.uk/fpn/%s> rdfs:subClassOf ?node_class . 
                } 
                    """ % node)    
                
                type_list = list()
    
                for row in qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
                for row in class_qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
                if len(type_list) == 0:
                    type_list.append('Literal')
                node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
            type_dict = {}
            for index,row in node_types.iterrows():
                type_dict[row[0]] = row[1]
                
                
                
            new_nodes = list()
            for node in new_node_table:
                new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
    
            new_edges = [
                {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
                for index, row in data.iterrows()
            ]
            
            elements = new_nodes + new_edges
            if len(elements) < 250:
                layout = {'name': 'dagre', 'spacingFactor':'5'}
            else:
                layout = {'name': 'cose', 'spacingFactor':'2.5'}
        return (elements, layout, stylesheet)
    if (button_id == 'nodes-checklist'):
        stylesheet = all_style
        if (display == 'dummy-button'):
            stylesheet = dd_style + stylesheet
        for edge in edges:
            stylesheet.append({
            'selector': 'edge[label="%s"]' % edge,
            'style': {
                'display': 'none'
            }})
        for node in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
        return(elements, layout, stylesheet)
    if (button_id == 'edges-checklist'):
        stylesheet = all_style
        if (display == 'dummy-button'):
           stylesheet = stylesheet + dd_style
        for node in nodes_list:
            if node not in nodes:
              
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
        for edge in edges:
            stylesheet.append({
            'selector': 'edge[label="%s"]' % edge,
            'style': {
                'display': 'none'
            }})
        
        return (elements, layout, stylesheet)
    
    if (button_id == 'node-button') and nname and nclass:
        new_id = nname.replace(' ', '_') + 'foo'
        new_label = nname
        new_classes = [nclass]
        new_node = {'data': {'id': new_id, 'label': new_label}, 'classes': new_classes}
        elements += [new_node]
        return (elements, layout, stylesheet)
    
    if (button_id == 'edge-button') and len(data_n)==2 and ename:
        source = data_n[0]['id']
        target = data_n[1]['id']
        label = ename
        new_edge = [
                {'data': {'source': source, 'target': target, 'label': label}}]
        elements += new_edge
        return (elements, layout, stylesheet)

    
    if (display == 'dummy-button'):
        stylesheet = all_style + dd_style
        for node  in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
                 
        for edge in edges:
                stylesheet.append({
                'selector': 'edge[label="%s"]' % edge,
                'style': {
                    'display': 'none'
                }})


    if (display == 'all-button'):    
        stylesheet = all_style
        for node in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
        for edge in edges:
                stylesheet.append({
                'selector': 'edge[label="%s"]' % edge,
                'style': {
                    'display': 'none'
                }})
    if tapnode:
        stylesheet = all_style
        if (display == 'dummy-button'):
            stylesheet += dd_style
        for node in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
        for edge in edges:
                stylesheet.append({
                'selector': 'edge[label="%s"]' % edge,
                'style': {
                    'display': 'none'
                }})
        for edge in tapnode['edgesData']:
            if edge['source'] == tapnode['data']['id']: 
                stylesheet.append({"selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {"line-color": '#bebada',
                          'target-arrow-color':'#bebada',
                          'width':'7'}})
            if edge['target'] == tapnode['data']['id']: 
                stylesheet.append({"selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {"line-color": '#fccde5',
                          'target-arrow-color':'#fccde5',
                          'width':'7'}})
    if data_e:
        for edge in data_e:
                stylesheet.append({"selector": 'edge[id= "{}"]'.format(edge['id']), "style": {"line-color": '#bc80bd',
                          'target-arrow-color':'#bc80bd',
                          'width':'7'}})
        return (elements, layout, stylesheet)
    return (elements, layout, stylesheet)




@app.callback(Output('tap-node-data', 'children'),
              Input('food-pol-net', 'tapNode'))
def display_tap_node(data):
    if data:
        name = data['data']['label']
        node_classes = data['classes'].replace(' ', ', ')
        return 'Selected Node:\n' + name + '\nClasses:\n' + node_classes
    return 'nothing selected'




if __name__ == '__main__':
    app.run_server(debug=False)