###############################################################################
# @authors          Alan Ramponi (151369), Davide Martintoni (171076)
# @courses          Data Mining / Big Data and Social Networks
# @description      A user-based collaborative filtering algorithm
#
# A script that allows to plot the results of k-fold cross validation
###############################################################################

import plotly.plotly as py
from plotly.graph_objs import *


knn = [20, 40, 60, 80, 100] # steps of testing (number of nearest neighbors)

# TESTING RESULTS ON K-FOLD FIRST ITERATION (TEST DATA 1)
adj_test1 = [1.02970841215, 1.02049859808, 1.01601177216, 1.02067868222, 1.01853249221]
cos_test1 = [0.956728569853, 0.980459574778, 1.00061412067, 1.0063500672, 1.00368598711]
pea_test1 = [1.17292194685, 1.10870893399, 1.10745332092, 1.05605953579, 1.05271694168]
man_test1 = [1.16577264911, 1.09265387443, 1.07783771666, 1.06818141405, 1.05896089094]
euc_test1 = [1.16881154052, 1.09380104619, 1.07877248154, 1.06868522802, 1.05847046802]

# TESTING RESULTS ON K-FOLD SECOND ITERATION (TEST DATA 2)
adj_test2 = [0.97241687452, 0.97928494619, 0.976312371581, 0.987931007341, 0.998798821303]
cos_test2 = [0.93672405926, 0.944281903065, 0.958541826338, 0.956929820468, 0.957279298248]
pea_test2 = [1.06052331949, 1.10261578094, 1.16536827957, 1.1847413016, 1.19437669481]
man_test2 = [1.13209612603, 1.05651378036, 1.0528977389, 1.05988521712, 1.04714173134]
euc_test2 = [1.13313786072, 1.05799508455, 1.05328269526, 1.06029515822, 1.04748181971]

# TESTING RESULTS ON K-FOLD THIRD ITERATION (TEST DATA 3)
adj_test3 = [0.96839992109, 0.950039201889, 0.924190488290, 0.956482001875, 0.96804227589]
cos_test3 = [0.945016110219, 0.929026439653, 0.919093068649, 0.945728443874, 0.967439144331]
pea_test3 = [1.18170088193, 1.11237246276, 1.2018901863, 1.1777536543, 1.16803353548]
man_test3 = [1.10122235007, 1.05480577767, 1.0457727711, 1.0352164105, 1.03939401762]
euc_test3 = [1.09993516074, 1.05643994126, 1.04512193143, 1.03539266286, 1.03944412974]

# TESTING RESULTS ON K-FOLD FOURTH ITERATION (TEST DATA 4)
adj_test4 = [0.96001948700, 0.948229010057, 0.9819001849559, 0.995386889308, 1.0000208739907]
cos_test4 = [0.939390678514, 0.920866126679, 0.966719204855, 0.994477936545, 0.994133328353]
pea_test4 = [1.0477589084, 0.99394907391, 1.09544473141, 1.03743088593, 1.03488547681]
man_test4 = [1.11207539068, 1.10068375898, 1.09135315104, 1.07955470137, 1.080822605]
euc_test4 = [1.11149808862, 1.09929098077, 1.09070225091, 1.07953799148, 1.08070097228]

# TESTING RESULTS ON K-FOLD FIFTH ITERATION (TEST DATA 5)
adj_test5 = [0.959372910078, 0.984628666381, 0.984781848906, 0.989771197746, 0.990278647826]
cos_test5 = [0.928359049427, 0.952605388389, 0.957559731381, 0.986070607533, 0.989462432555]
pea_test5 = [1.1347157958, 1.03034861895, 1.0739454512, 1.150489385, 1.16479099989]
man_test5 = [1.16618413239, 1.1021184107, 1.09173532208, 1.08032914117, 1.06547577612]
euc_test5 = [1.16025590993, 1.10242620771, 1.09262546192, 1.08096273475, 1.0657339066]

# AVERAGE OF TESTING RESULTS
adj_avg = []
cos_avg = []
pea_avg = []
man_avg = []
euc_avg = []

# Calculate the average of testing results
for i in range(0,5):
    adj_avg.append((adj_test1[i] + adj_test2[i] + adj_test3[i] + adj_test4[i] + adj_test5[i]) / 5)
    cos_avg.append((cos_test1[i] + cos_test2[i] + cos_test3[i] + cos_test4[i] + cos_test5[i]) / 5)
    pea_avg.append((pea_test1[i] + pea_test2[i] + pea_test3[i] + pea_test4[i] + pea_test5[i]) / 5)
    man_avg.append((man_test1[i] + man_test2[i] + man_test3[i] + man_test4[i] + man_test5[i]) / 5)
    euc_avg.append((euc_test1[i] + euc_test2[i] + euc_test3[i] + euc_test4[i] + euc_test5[i]) / 5)

print "Average Adj cos:"
print adj_avg # print the Adjusted cosine vector
print "\n"

print "Average Cos:"
print cos_avg # print the Cosine vector
print "\n"

print "Average Pea:"
print pea_avg # print the Pearson vector
print "\n"

print "Average Man:"
print man_avg # print the Manhattan vector
print "\n"

print "Average Euc:"
print euc_avg # print the Euclidean vector
print "\n"


# Initialize Adjusted cosine similarity data
trace0 = Scatter(
    x=knn,
    y=adj_avg,
    mode='lines+markers',
    name='Adjusted cosine   ',
    line=Line(
        dash='solid'
    )
)

# Initialize Cosine similarity data
trace1 = Scatter(
    x=knn,
    y=cos_avg,
    mode='lines+markers',
    name='Cosine',
    line=Line(
        color='rgb(156, 165, 196)',
        dash='solid'
    )
)

# Initialize Pearson correlation coefficient data
trace2 = Scatter(
    x=knn,
    y=pea_avg,
    mode='lines+markers',
    name='Pearson',
    line=Line(
        dash='solid'
    )
)

# Initialize Manhattan distance data
trace3 = Scatter(
    x=knn,
    y=man_avg,
    mode='lines+markers',
    name='Manhattan',
    line=Line(
        dash='solid'
    )
)

# Initialize Euclidean distance data
trace4 = Scatter(
    x=knn,
    y=euc_avg,
    mode='lines+markers',
    name='Euclidean',
    line=Line(
        dash='solid'
    )
)

data = Data([trace0, trace1, trace2, trace3, trace4])
layout = Layout(
    # title='Comparison of distance measures: experiment #5',
    title='Comparison of distance measures: final results',
    font=Font(
        family='Helvetica',
        size=12,
        color='#000000'
    ),
    autosize=False,
    width=700,
    height=450,
    margin=Margin(
        l=120,
        r=120,
        b=100,
        t=100,
        pad=0
    ),
    xaxis=XAxis(
        title='K (number of nearest neighbors)',
        titlefont=Font(
            family='Helvetica',
            size=16,
            color='#000000'
        ),
        range=[20, 100],
        showgrid=True,
        zeroline=True,
        showline=True,
        zerolinecolor='#969696',
        zerolinewidth=4,
        ticks='outside',
        ticklen=10,
        autotick=False,
        dtick=20
    ),
    yaxis=YAxis(
        title='RMSE (root-mean-squar error)',
        titlefont=Font(
            family='Helvetica',
            size=16,
            color='#000000'
        ),
        range=[0.9, 1.25],
        showgrid=True,
        zeroline=True,
        showline=True,
        zerolinecolor='#969696',
        zerolinewidth=4,
        ticks='outside',
        ticklen=10,
        autotick=False,
        dtick=0.05
    ),
    legend=Legend(
        y=1,
        traceorder='reversed',
        font=Font(
            size=14
        ),
        bordercolor='#969696',
        borderwidth=1,
        yref='paper'
    )
)

fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='line-dash')

py.image.save_as({'data': data}, 'experiment_results.png')
