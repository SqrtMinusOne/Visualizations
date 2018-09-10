import queue

import numpy as np
from matplotlib import pyplot as plt


def get_series(num, q, length):
    i = 0
    series = []
    for el in q:
        if num < len(el):
            series.append(el[num])
        else:
            series.append(0)
        i = i + 1
    return series


def avrg(series, n):
    q = queue.Queue(n + 1)
    res = []
    for i in range(len(series)):
        q.put(series[i])
        if i >= n:
            t = 0
            for el in q.queue:
                t = t + el
            t = t / n
            res.append(t)
            q.get(i)
    return res


def main(file_name):
    # params
    L = 30
    W = 10
    plot_first = False
    plot_second = True
    only_final = False

    # init
    file = open(file_name, 'r')
    content = file.readlines()
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
              'Декабрь']

    name_fig = plt.figure(1)
    names_axes = name_fig.add_axes([0.25, 0.05, 0.7, 0.9])
    graph_fig = plt.figure(2)
    graph_axes = graph_fig.add_axes([0.05, 0.05, 0.9, 0.9])

    # variables
    names = []  # All names
    freq = []  # Frequency of names
    current_freq = []
    last_freqs = queue.Queue(L + 1)
    last_last_freqs = queue.Queue(L+1)
    current_day = 0
    passed_days = 0

    i = 0
    k = 0
    plot_here = True
    final = False

    # iteration
    for line in content:
        k = k + 1
        if k >= len(content) - 1:
            final = True
        if line[0].isnumeric():
            i = i + 1
            #  hour = int(line[0:2])
            #  minute = int(line[3:5])
            day = int(line[10:12])
            month = int(line[13:15])
            year = int(line[16:21])
            name = line[21:].strip()

            if current_day != day:
                plot_here = True
                passed_days = passed_days + 1
                current_day = day
                last_freqs.put(current_freq)
                last_last_freqs.put([i for i in freq])
                current_freq = [0 for i in range(len(names))]
                if passed_days >= L:
                    old_freq = last_freqs.get()
                    last_last_freqs.get()
                    for j in range(len(old_freq)):
                        freq[j] = freq[j] - old_freq[j]

            if name not in names:
                names.append(name)
                freq.append(0)
                current_freq.append(0)
            freq[names.index(name)] = freq[names.index(name)] + 1
            current_freq[names.index(name)] = current_freq[names.index(name)] + 1

            sorted_ind = sorted(range(len(freq)), key=lambda x: freq[x])
            sorted_freq = [freq[j] for j in sorted_ind]
            sorted_names = [names[j] for j in sorted_ind]
            names_range = np.arange(len(names))

            if plot_here and not only_final or only_final and final:
                plot_here = False
                total = 0
                for i in range(len(freq)):
                    total = total + freq[i]
                title = "Date: {0:2}/{1:2}/{2:2}, Total: {3:5}".format(day, month, year, total)
                if plot_first:
                    fig1 = plt.figure(1)
                    names_axes.clear()
                    names_axes.barh(names_range, sorted_freq)
                    names_axes.set_title(title)
                    plt.yticks(names_range, sorted_names)
                    plt.savefig('fig1/fig{0:5}'.format(passed_days))
                if plot_second:
                    fig2 = plt.figure(2)
                    graph_axes.clear()
                    graph_axes.set_title(title)
                    for i in range(len(names)):
                        series_here = get_series(i, last_last_freqs.queue, L)
                        graph_axes.plot(series_here, label=names[i])
                    graph_axes.legend(loc='upper left', shadow=True, fontsize='x-small')
                    plt.savefig('fig2/fig{0:5}'.format(passed_days))


main("confa1.txt")
