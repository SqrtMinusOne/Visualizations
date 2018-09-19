import math

from matplotlib import pyplot as plt
from random import uniform


def get_color():
    if random_colors:
        return [uniform(0, 255) / 255, uniform(0, 255) / 255, uniform(0, 255) / 255]
    else:
        return [0, 0, 0]


def plot_p(axes, m_t, n_t, p_t, t_t):
    pl_t = 0
    for i in range(m_t):  # Plotting
        col = get_color()
        for k in range(0, t_t[i] * n_t, t_t[i]):
            axes.plot([k + pl_t, k + pl_t + t_t[i]], [i, i], color=col, **line_params)
        pl_t = pl_t + t_t[i] * n_t
        if i != m_t - 1:
            axes.arrow(pl_t, i, 0, 1, **arrow_params)
    return pl_t


def plot_pm(axes, m_t, n_t, p_t, t_t):
    pl_t = 0
    major_i, major_t = 0, 0
    col = [get_color() for i in range(m_t)]
    for i in range(m_t):  # Getting the major operation
        if t_t[i] > major_t:
            major_t = t_t[i]
            #  major_i = i
    for k in range(int(n_t / p_t)):  # Plotting
        pl_t = k * major_t * p_t
        for i in range(m_t):
            axes.plot([pl_t, pl_t + t_t[i] * p_t], [i, i], color=col[i])
            pl_t = pl_t + t_t[i] * p_t
            if i != m_t - 1:
                axes.arrow(pl_t, i, 0, 1, **arrow_params)
    return pl_t


def plot_pp(axes, m_t, n_t, p_t, t_t):
    pl_t = 0
    draw_next_arrows = False
    for i in range(m_t):
        col = get_color()
        draw_arrow = False
        if i != m_t - 1:
            if t_t[i] < t_t[i + 1]:
                draw_arrow = True
        for k in range(0, t_t[i] * n_t, t_t[i]):
            axes.plot([k + pl_t, k + pl_t + t_t[i]], [i, i], color=col, **line_params)
        if i != m_t -1:
            if t_t[i] < t_t[i + 1]:
                pl_t = pl_t + t_t[i] * p_t
                arrow_start = pl_t + (n_t - p_t) * t_t[i]
            else:
                pl_t = pl_t + (t_t[i] * n_t) - (n_t - p_t) * t_t[i + 1]
                arrow_start = pl_t + (n_t - p_t) * t_t[i + 1]
            axes.arrow(pl_t, i, 0, 1, **arrow_params)
            axes.arrow(arrow_start, i, 0, 1, **arrow_params)
            x = [pl_t, pl_t, arrow_start, arrow_start]
            y = [i, i+1, i+1, i]
            axes.fill(x, y, color=get_color(), fill=False, hatch='\\')
        else:
            pl_t = pl_t + t_t[i] * n_t

    return pl_t


def enhance(axes, pl_t):  # Post-plotting enhancement
    y_min, y_max = axes.get_ylim()
    axes.set_ylim(y_max + 2, y_min)
    ticks_max = int(math.ceil((pl_t + 1)/5))*5 + 1
    major_ticks_spacing = int(ticks_max / 20)
    axes.set_xticks(range(ticks_max), minor=True)
    axes.set_xticks(range(0, ticks_max, major_ticks_spacing))
    axes.grid(which='minor', alpha=0.2)
    axes.grid(which='major', alpha=0.5)
    plt.annotate('', xy=(0, m), xytext=(pl_t, m), arrowprops=dict(arrowstyle='<->', linewidth=2))
    plt.text(int(pl_t / 2), m - 0.1, '$T_c$', fontsize=15)


def init():  # initialization
    figure = plt.figure()
    axes = figure.add_axes([0.08, 0.1, 0.87, 0.8])
    plt.yticks(range(m))
    axes.set_xlabel("t,мин", position=(1, 0), size=15)
    axes.set_ylabel("i", position=(0, 1), rotation='horizontal', size=15)
    plt.grid(True)
    return figure, axes


def draw(m, n, p, t, mode):
    fig, main_axes = init()
    pl = 0
    if mode == 'p':
        pl = plot_p(main_axes, m, n, p, t)
    elif mode == 'pm':
        pl = plot_pm(main_axes, m, n, p, t)
    else:
        pl = plot_pp(main_axes, m, n, p, t)
    enhance(main_axes, pl)


# parameters
m = 5  # Number of operations
n = 10  # Size of a batch
p = 1  # Size of a transfer batch
t = [2, 6, 5, 3, 4]  # Time of execution of a operation
random_colors = False


line_params = dict(marker='|', markersize=10, linewidth=2)  # Line parameters
arrow_params = dict(width=0.02, head_width=0.2, head_length=0.1, length_includes_head=True, color='black')
fig_n = 0

draw(m, n, p, t, 'p')
draw(m, n, p, t, 'pm')
draw(m, n, p, t, 'pp')

plt.show()
