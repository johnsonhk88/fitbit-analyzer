import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats as scipystats

from stats import sleepStats, hbStats

NAMES={'sleep_inefficiency':'Sleep Inefficiency (%)',
        'sleep_efficiency':'Sleep Efficiency (%)',
           'restless':'Restless (minutes)',
           'awake':'Awake (minutes)',
           'total_minutes':'Total Minutes',
           'sleep_hours':'Hours of Sleep',
           'first_min_asleep':'First Minute Asleep'}

def plotPreliminaryStats(stats):
    """
    Plot measures distribution using histograms
    :param stats: data to plot
    """
    columns = ['sleep_efficiency', 'restless', 'awake', 'total_minutes', 'sleep_hours',
               'first_min_asleep']
    plotStats = stats[columns]
    plotStats = plotStats.rename(columns=NAMES)
    plotStats.hist()
    sns.plt.show()

def plotWeekdayStatsSleep(stats):
    columns = ['sleep_efficiency', 'restless', 'sleep_hours',
               'first_min_asleep', 'awake', 'total_minutes']
    _plotWeekdayStats(stats, columns)

def plotWeekdayStatsHb(stats):
    columns = ['count', 'max', 'min', 'std']
    _plotWeekdayStats(stats, columns)

def _plotWeekdayStats(stats, columns):
    dayOfWeek = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thur', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    order = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    # Group by weekday and change stats from columns to row attribute
    dataToPlot = stats.groupby(stats['date'].dt.weekday).mean()
    dataToPlot = pd.melt(dataToPlot.reset_index(), id_vars=['date'], value_vars=columns,
                         var_name='stats', value_name='val')
    # Rename stats and weekdays
    dataToPlot['stats'].replace(NAMES, inplace=True)
    dataToPlot['date'].replace(dayOfWeek, inplace=True)
    # Plot
    g = sns.factorplot(data=dataToPlot, x="date", y="val", col="stats",
                       order=order, kind="point", sharey=False, col_wrap=3)
    g.set_xticklabels(rotation=45)
    g.set(xlabel='')
    sns.plt.show()

def plotWeekdayStatsByMonthSleep(stats):
    stat_name = 'sleep_efficiency'
    _plotWeekdayByMonthStats(stats, stat_name)

def _plotWeekdayByMonthStats(stats, stat_name):
    dayOfWeek = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thur', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    order = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    # Add day and month columns, and groupby
    stats['day'] = stats['date'].dt.weekday
    stats['month'] = stats['date'].dt.month
    dataToPlot = stats.groupby([stats['day'], stats['month']])[stat_name].mean()

    dataToPlot = dataToPlot.reset_index()
    dataToPlot['day'].replace(dayOfWeek, inplace=True)
    # Plot
    g = sns.pointplot(data=dataToPlot, x="day", y="sleep_efficiency", hue="month", order=order)
    g.set(xlabel='')
    g.set_ylabel(NAMES[stat_name])
    sns.plt.show()

# def plotWeekdayStats(stats, columns):
#     """
#     Plot aggregated (mean) stats by dayOfWeek
#     :param stats: data to plot
#     :param columns: columns from stats to plot
#     """
#     MEASURE_NAME = 'weekday'
#     dayOfWeek={0:'Mon', 1:'Tue', 2:'Wed', 3:'Thur', 4:'Fri', 5:'Sat', 6:'Sun'}
#     order = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']
#     stats[MEASURE_NAME] = stats[MEASURE_NAME].map(dayOfWeek)
#
#     f, axes = getAxes(2,2)
#     for i, c in enumerate(columns):
#         if c in NAMES:
#             c = NAMES[c]
#         g = sns.barplot(x=MEASURE_NAME, y=c, data=stats, order=order, ax=axes[i])
#         g.set_xlabel('')
#     sns.plt.show()
#     #plot(stats, columns, MEASURE_NAME, 2, 3, order=order)

def plotMonthlyStatsSleep(stats):
    columns = ['sleep_inefficiency', 'restless', 'sleep_hours',
               'first_min_asleep']
    _plotMonthlyStats(stats, columns)

def plotMonthlyStatsHb(stats):
    columns = ['count', 'max', 'min', 'std']
    _plotMonthlyStats(stats, columns)
    #plot(stats, columns, MEASURE_NAME, 4, 1, order=order)

def _plotMonthlyStats(stats, columns):
    months={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug',
            9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    # Group by month and change stats from columns to row attribute
    dataToPlot = stats.groupby(stats['date'].dt.month).mean()
    dataToPlot = pd.melt(dataToPlot.reset_index(), id_vars=['date'], value_vars=columns,
                         var_name='stats', value_name='val')
    # Rename stats and weekdays
    dataToPlot['stats'].replace(NAMES, inplace=True)
    dataToPlot['date'].replace(months, inplace=True)
    order = [m for m in order if m in dataToPlot['date'].unique()]
    # Plot
    g = sns.factorplot(data=dataToPlot, x="date", y="val", col="stats", order=order, kind="bar", sharey=False)
    g.set_xticklabels(rotation=45)
    g.set(xlabel='')
    sns.plt.show()

# def _plotMonthlyStats(stats, columns):
#     """
#     Plot aggregated (mean) stats by month
#     :param stats: data to plot
#     :param columns: columns from stats to plot
#     """
#     MEASURE_NAME = 'month'
#     months={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug',
#             9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
#     order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#     stats[MEASURE_NAME] = stats[MEASURE_NAME].map(months)
#
#     order = [m for m in order if m in stats[MEASURE_NAME].unique()]
#
#     f, axes = getAxes(2,2)
#     for i, c in enumerate(columns):
#         if c in NAMES:
#             c = NAMES[c]
#         g = sns.barplot(x=MEASURE_NAME, y=c, data=stats, order=order, ax=axes[i])
#         g.set_xlabel('')
#     sns.plt.show()

def plotYearAndMonthStatsSleep(stats):
    """
    Plot aggregated (mean) stats by year and month.
    :param stats: data to plot
    """
    columns = ['sleep_efficiency', 'sleep_hours']
    _plotYearAndMonthStats(stats, columns)

def _plotYearAndMonthStats(stats, columns):
    # Group by month and change stats from columns to row attribute
    dataToPlot = stats.groupby(stats['date'].dt.to_period("M")).mean()
    dataToPlot = pd.melt(dataToPlot.reset_index(), id_vars=['date'], value_vars=columns,
                         var_name='stats', value_name='val')
    # Rename stats
    dataToPlot['stats'].replace(NAMES, inplace=True)
    # Plot
    g = sns.factorplot(data=dataToPlot, x="date", y="val", row="stats", kind="point", sharey=False)
    g.set_xticklabels(rotation=45)
    for ax in g.axes.flat:
        ax.grid(b=True)
    sns.plt.show()

def plotDailyStatsSleep(data):
    """
    Plot daily stats. Fill all data range, and put NaN for days without measures
    :param data: data to plot
    """
    MEASURE_NAME = 'date'
    columns = ['sleep_inefficiency', 'sleep_hours']
    stats = data.rename(columns=NAMES)

    dates = pd.date_range(start=stats.date.iloc[0].date(), end=stats.date.iloc[-1].date())
    stats.set_index(['date'], inplace=True)
    stats = stats.reindex(dates)
    stats.reset_index(inplace=True)
    stats.rename(columns={'index':'date'}, inplace=True)

    f, axes = getAxes(2,1)
    xTicksDiv = min(10, len(stats))
    #xticks = [(x-pd.DateOffset(years=1, day=2)).date() for x in stats.date]
    xticks = [x.date() for x in stats.date]
    keptticks = xticks[::int(len(xticks)/xTicksDiv)]
    xticks = ['' for _ in xticks]
    xticks[::int(len(xticks)/xTicksDiv)] = keptticks
    for i, c in enumerate(columns):
        g =sns.pointplot(x=MEASURE_NAME, y=NAMES[c], data=stats, ax=axes[i])
        g.set_xticklabels([])
        g.set_xlabel('')
    g.set_xticklabels(xticks, rotation=45)
    sns.plt.show()

def plotDailyStatsHb(data):
    data.groupby(data[hbStats.NAME_DT_COL].dt.date).mean().plot()
    sns.plt.show()

def plotYearMonthStatsHb(data):
    #pd.groupby(b,by=[b.index.month,b.index.year])
    data.groupby(pd.TimeGrouper(freq='M')).mean().plot()
    sns.plt.show()

def plotSleepValueHeatmap(intradayStats, sleepValue=1):
    sns.set_context("poster")
    sns.set_style("darkgrid")

    xTicksDiv = 20
    #stepSize = int(len(xticks)/xTicksDiv)
    stepSize = 60
    xticks = [x for x in intradayStats.columns.values]
    keptticks = xticks[::stepSize]
    xticks = ['' for _ in xticks]
    xticks[::stepSize] = keptticks
    plt.figure(figsize=(16, 4.2))
    g = sns.heatmap(intradayStats.loc[sleepValue].reshape(1,-1))
    g.set_xticklabels(xticks, rotation=45)
    g.set_yticklabels([])
    g.set_ylabel(sleepStats.SLEEP_VALUES[sleepValue])
    plt.tight_layout()
    sns.plt.show()

def plotCorrelation(stats):
    #columnsToDrop = ['sleep_interval_max_len', 'sleep_interval_min_len',
    #                 'sleep_interval_avg_len', 'sleep_inefficiency',
    #                 'sleep_hours', 'total_hours']

    #stats = stats.drop(columnsToDrop, axis=1)

    g = sns.PairGrid(stats)
    def corrfunc(x, y, **kws):
        r, p = scipystats.pearsonr(x, y)
        ax = plt.gca()
        ax.annotate("r = {:.2f}".format(r),xy=(.1, .9), xycoords=ax.transAxes)
        ax.annotate("p = {:.2f}".format(p),xy=(.2, .8), xycoords=ax.transAxes)
        if p>0.04:
            ax.patch.set_alpha(0.1)

    g.map_upper(plt.scatter)
    g.map_diag(plt.hist)
    g.map_lower(sns.kdeplot, cmap="Blues_d")
    g.map_upper(corrfunc)
    sns.plt.show()

def getAxes(nrows, ncols):
    f, axes = plt.subplots(nrows=nrows, ncols=ncols)
    axes = axes.reshape(-1)
    return f, axes

def plot(data, columns, measureName, nrows, ncols, order=None):
    f, axes = plt.subplots(nrows=nrows, ncols=ncols)
    axes = axes.reshape(-1)
    for i, c in enumerate(columns):
        sns.barplot(x=measureName, y=c, data=data, order=order, ax=axes[i])
    sns.plt.show()