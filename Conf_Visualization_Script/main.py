import queue

import numpy as np
from matplotlib import pyplot as plt


def main(file_name):
    # params
    L = 30
    plot_first = True
    plot_second = True
    only_final = True

    # init
    file = open(file_name, 'r')
    content = file.readlines()
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    name_fig = plt.figure(1)
    names_axes = name_fig.add_axes([0.25, 0.05, 0.7, 0.9])
    time_fig = plt.figure(2)
    last_axes = time_fig.add_axes([0.61, 0.05, 0.33, 0.39])
    month_axes = time_fig.add_axes([0.15, 0.5, 0.8, 0.4])
    hours_axes = time_fig.add_axes([0.15, 0.05, 0.4, 0.39])

    # variables
    names = []  # All names
    freq = []  # Frequency of names
    months_count = [0] * 12  # Messages per month
    hours_count = [0] * 24  # Messages per hours
    last_ones = queue.Queue(L + 1)  # Last L days message count

    prev_day = 0
    this_day = 0
    i = 0
    k = 0
    plot_here = True
    final = False

    month_range = np.arange(len(months))
    hours_range = np.arange(len(hours_count))

    # iteration
    for line in content:
        k = k + 1
        if k >= len(content) - 1:
            final = True
        if line[0].isnumeric():
            i = i + 1
            hour = int(line[0:2])
            #  minute = int(line[3:5])
            day = int(line[10:12])
            month = int(line[13:15])
            year = int(line[16:21])
            name = line[21:].strip()

            if name not in names:
                names.append(name)
                freq.append(0)
            freq[names.index(name)] = freq[names.index(name)] + 1
            sorted_ind = sorted(range(len(freq)), key=lambda x: freq[x])
            freq = [freq[i] for i in sorted_ind]
            names = [names[i] for i in sorted_ind]
            names_range = np.arange(len(names))

            months_count[month - 1] = months_count[month - 1] + 1
            hours_count[hour] = hours_count[hour] + 1

            if last_ones.full():
                last_ones.get()
            if prev_day != day:
                last_ones.put(this_day)
                this_day = 0
                prev_day = day
                plot_here = True
            this_day = this_day + 1

            if plot_here and not only_final or only_final and final:
                plot_here = False
                title = "Date: {0:2}/{1:2}/{2:2}, Total: {3:5}".format(day, month, year, i)
                if plot_first:
                    fig1 = plt.figure(1)
                    names_axes.clear()
                    names_axes.barh(names_range, freq)
                    names_axes.set_title(title)
                    plt.yticks(names_range, names)
                    plt.savefig('fig1/fig{0:5}'.format(i))
                if plot_second:
                    fig2 = plt.figure(2)
                    month_axes.clear()
                    month_axes.set_title(title)
                    month_axes.barh(month_range, months_count, color='green')
                    month_axes.set_yticks(month_range)
                    month_axes.set_yticklabels(months)

                    hours_axes.clear()
                    hours_axes.bar(hours_range, hours_count, color='red')

                    last_axes.clear()
                    last_axes.plot(range(len(last_ones.queue)), last_ones.queue)

                    plt.savefig('fig2/fig{0:5}'.format(i))
    plt.show()

main("confa3.txt")