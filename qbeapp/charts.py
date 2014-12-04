# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 2014

@author: Mahesh.Jadhav

"""
import logging

try:
    import networkx as nx
except ImportError:
    import sys
    print("NetworkX needed for graphs. Skipping")
    sys.exit(0)
try:
    import matplotlib.pyplot as plt
except ImportError:
    import sys
    print("Matplotlib needed for drawing. Skipping")
    sys.exit(0)
import numpy as np
import matplotlib.mlab as mlab

import qbeapp.errors as errs


logger = logging.getLogger('qbe.log')

def draw_graph(graph, labels=None, 
               graph_layout='shell',
               node_size=1600, 
               node_color='blue', 
               node_alpha=0.4,
               node_text_size=10,
               edge_color='grey', 
               edge_alpha=0.3, 
               edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos = nx.spring_layout(graph)
    elif graph_layout == 'spectral':
        graph_pos = nx.spectral_layout(graph)
    elif graph_layout == 'random':
        graph_pos = nx.random_layout(graph)
    else:
        graph_pos = nx.shell_layout(graph)

    # draw graph
    nx.draw_networkx_nodes(graph, graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(graph, graph_pos, width=edge_tickness,
                           alpha=edge_alpha, edge_color=edge_color)
    nx.draw_networkx_labels(graph, graph_pos, font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph.edges()))
    # dict([((u,v,),d) for u,v,d in graph.edges(data=True)])

    edge_labels = dict(zip(graph.edges(), labels))

    nx.draw_networkx_edge_labels(graph, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)

    font = {'fontname'   : 'Helvetica',
            'color'      : 'm',
            'fontweight' : 'bold',
            'fontsize'   : 14
            }
    plt.title("Database Tables Graph", font)

    font = {'fontname'   : 'Helvetica',
            'color'      : 'r',
            'fontweight' : 'bold',
            'fontsize'   : 14
            }

    plt.text(0.5, 0.97, "edge = foreign key relationship",
             horizontalalignment='center',
             transform=plt.gca().transAxes)
    plt.axis('off')
    plt.savefig("db_tbls_graph.png")
    # show graph
    plt.show()

def get_axis_from_report_data(report_data):
    x_ax = []
    y_ax = []
    try:    
        for data in report_data:
            if data['chart'] == 'X':
                x_ax.append(data['field'])
            elif data['chart'] == 'Y':
                y_ax.append(data['field'])
    except:
        raise
    if x_ax and y_ax:
        return {'X': x_ax, 'Y': y_ax}
    return None

def get_chart_data(header, results, x, y):
    x_data = [] 
    y_data = []
    try:
        for clm in header:
            if clm == x:            
                x_idx = header.index(clm)
                x_data = [x[x_idx] for x in results]
            elif clm == y:            
                y_idx = header.index(clm)
                y_data = [int(y[y_idx]) for y in results]
    except ValueError:
        raise errs.QBEError("Y axis data should have numeric values.")
    except:
        raise
    if x_data and y_data:
        return {'X': x_data, 'Y': y_data}
    return None
    
def autolabel(rects, ax):
    """
    Attaches some text labels
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, 
                '%d' % int(height),
                ha='center', va='bottom')

def dyna_chart(title, xlabel, ylabel, legend, x_data, y_data):    
    """
    Shows a bar chart with x and y axis values
    """
    N = len(y_data)
    means = y_data  # (20, 35, 30, 35, 27)
    std =   [2 for x in range(0, N)]

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects = ax.bar(ind, means, width, color='r', yerr=std)
    fig.autofmt_xdate()
    # add some text for labels, title and axes ticks
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(x_data) 

    ax.legend((rects), legend, loc='best', fancybox=True, framealpha=0.5)
    autolabel(rects, ax)

    plt.show()

def histogram(mu,                 # mean of distribution
              sigma,              # standard deviation of distribution
              records, 
              num_bins, 
              title, 
              xlabel, 
              ylabel, 
              normed=1, 
              facecolor='green', 
              alpha=0.75,
              grid=True):
    # the histogram of the data
    n, bins, patches = plt.hist(records, 50, normed=normed, 
                                facecolor=facecolor, alpha=alpha)
    # add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, y, 'r--')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title + ': $\mu='+ str(mu) +'$, $\sigma='+ str(sigma) +'$')

    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    plt.xlim([mu-150, mu+150])
    plt.grid(grid)

    plt.show()


