# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""The utility functions for plotting and data manipulation."""
__author__ = "HMY"
__date__ = "2025-Aug-23"

import pickle
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import display, HTML
import matplotlib.ticker as mticker
from matplotlib import ticker
import numpy as np
import math


def KeyValStoPlot(
    ax,
    keys: list,
    vals: list,
    label: str,
    qutile: list[float, float] = [0.25, 0.75],
    linestyle="-",
    marker="",
    method="shadow",
    capsize=3,
    marker_size=3,
    color=False,
    errmethod="percentile",
    mm="mean",
    cut=False,
    alpha=0.5,
):
    """_summary_

    Args:
        ax (_type_): _description_
        keys (list): _description_
        vals (list): _description_
        label (str): _description_
        qutile (list[float, float], optional): _description_. Defaults to [0.25, 0.75].
        linestyle (str, optional): _description_. Defaults to "-".
        marker (str, optional): _description_. Defaults to "".
        method (str, optional): _description_. Defaults to "shadow".
        capsize (int, optional): _description_. Defaults to 3.
        marker_size (int, optional): _description_. Defaults to 3.
        color (bool, optional): _description_. Defaults to False.
        errmethod (bool, optional): Error methods. Defaults to False.
        mm (str, optional): _description_. Defaults to "mean".
        cut (bool, optional): _description_. Defaults to False.
        alpha (float, optional): _description_. Defaults to 0.5.

    Returns:
        _type_: _description_
    """
    x = keys

    if mm == "mean":
        y = [np.mean(vals[i]) for i in range(len(vals))]
    elif mm == "median":
        y = [np.median(vals[i]) for i in range(len(vals))]
    if cut:
        for i in range(len(y)):
            if y[i] <= cut:
                y[i] = cut

    if errmethod == "percentile":
        err1 = [np.quantile(vals[i], qutile[0]) for i in range(len(vals))]
        err2 = [np.quantile(vals[i], qutile[1]) for i in range(len(vals))]
        err_bar_1 = [y[i] - err1[i] for i in range(len(vals))]
        err_bar_2 = [err2[i] - y[i] for i in range(len(vals))]
    elif errmethod == "std":
        std_devs = [np.std(vals[i]) for i in range(len(vals))]
        err1 = [y[i] - std_devs[i] for i in range(len(vals))]
        err2 = [y[i] + std_devs[i] for i in range(len(vals))]
        err_bar_1 = std_devs
        err_bar_2 = std_devs
    elif errmethod == "stderr":
        std_derr = [np.std(vals[i]) / np.sqrt(len(vals[i])) for i in range(len(vals))]
        err1 = [y[i] - std_derr[i] for i in range(len(vals))]
        err2 = [y[i] + std_derr[i] for i in range(len(vals))]
        err_bar_1 = std_derr
        err_bar_2 = std_derr

    if color:
        lines = ax.plot(
            x,
            y,
            label=label,
            marker=marker,
            markersize=marker_size,
            linestyle=linestyle,
            color=color,
        )

    else:
        lines = ax.plot(
            x,
            y,
            label=label,
            marker=marker,
            markersize=marker_size,
            linestyle=linestyle,
        )
    if method == "shadow":
        shadow = ax.fill_between(
            x,
            err1,
            err2,
            alpha=alpha,
            color=lines[0]._color,
            edgecolor="none",  # transparancy
        )

        return ax, lines, shadow
    elif method == "error bar":
        err_bar = ax.errorbar(
            keys,
            y,
            yerr=[err_bar_1, err_bar_2],
            # xlolims=xlolims, xuplims=xuplims,
            # uplims=uplims, lolims=lolims,
            capsize=capsize,
            color=lines[0]._color,
            linestyle="none",
        )
        return ax, lines, err_bar
    elif method == "":
        # not plot any error bar
        return ax, lines


def KeyValStoPlotDots(
    ax,
    keys: list,
    vals: list,
    label: str,
    qutile: list[float, float] = [0.0, 1.0],
    linestyle="-",
    marker="",
    errmethod="percentile",
    methods="mean",
    markersize=3,
    alpha=0.5,
):
    if methods == "mean":
        means = [np.mean(vals[i]) for i in range(len(vals))]
    elif methods == "median":
        means = [np.median(vals[i]) for i in range(len(vals))]
    lines = ax.plot(
        keys,
        means,
        label=label,
        marker=marker,
        linestyle=linestyle,
    )
    if errmethod == "std":
        variances = [np.std(vals[i]) for i in range(len(vals))]
        std_devs = [np.sqrt(var) for var in variances]
        shadow = ax.fill_between(
            keys,
            [means[i] - std_devs[i] for i in range(len(means))],
            [means[i] + std_devs[i] for i in range(len(means))],
            alpha=alpha,  # transparency
        )
    elif errmethod == "stderr":
        stderr = [np.std(vals[i]) / np.sqrt(len(vals[i])) for i in range(len(vals))]
        shadow = ax.fill_between(
            keys,
            [means[i] - stderr[i] for i in range(len(means))],
            [means[i] + stderr[i] for i in range(len(means))],
            alpha=alpha,  # transparency
        )
    elif errmethod == "percentile":
        shadow = ax.fill_between(
            keys,
            [np.quantile(vals[i], qutile[0]) for i in range(len(vals))],
            [np.quantile(vals[i], qutile[1]) for i in range(len(vals))],
            alpha=0.5,  # transparancy
        )

    return ax, lines, shadow


class final_plot(object):

    def __init__(self) -> None:
        pass

    def cback(self, ax, ns: list, ls: list, markersize: int = 9):
        """This is used for plotting the classical backgrounds

        ax: ax is axis of plotting
        x_axis: if 0, fix n, and x axis is the growth of l
                else if 1, fix l, and x axis is the growth of n

        """
        if len(ns) != 1 and len(ls) != 1:
            raise Exception(
                "Both ns list and ls list are two dimensional, can not plot! Please check it!"
            )
        elif len(ns) == 1:
            x_axis = 0
            x_label = "$l$"
        elif len(ls) == 1:
            x_axis = 1
            x_label = "$n$"

        m = SoluSpace()
        lines = []
        labs = []
        y1, y2 = m.get_list(ns=ns, ls=ls)
        _x = [ls, ns][x_axis % 2]
        _y1 = [j for i in y1 for j in i]
        _y2 = [j for i in y2 for j in i]

        line = ax.plot(
            _x,
            _y1,
            linestyle="--",
            marker="o",
            markersize=markersize,
            label="Unconstrainted Brute Force",
            color="grey",
        )
        lines.append(line[0])
        labs.append(line[0].get_label())
        line = ax.plot(
            _x,
            _y2,
            linestyle="--",
            marker="o",
            markersize=markersize,
            label="Constrainted Brute Force",
            color="b",
        )
        lines.append(line[0])
        labs.append(line[0].get_label())

        ax.set_xticks(_x)
        ax.set_yscale("log")
        # ax.set_yticks()
        ax.set_ylabel("feasible region size")
        ax.set_xlabel(x_label)

        return lines, labs

    def prb(
        self,
        ax,
        data,
        plist: list,
        x_axis: list,
        y_label: str,
        x_label: str,
        perct: bool = False,
    ):
        labs = []
        lines = []
        for j in plist:
            y0 = [data[i][j] for i in range(len(data))]

            for i in range(len(y0)):
                if y0[i] <= 1e-7:
                    y0[i] = 1e-8

            line = ax.plot(x_axis, y0, label="p=" + str(j + 1), marker=".")
            lines.append(line[0])
            labs.append(line[0].get_label())

        max_record = np.max(data)
        min_record = np.min(data)
        if min_record <= 1e-7:
            # positive_data = np.array(data).flatten()
            # positive_data = positive_data[positive_data > 0]
            # min_record = np.min(positive_data)
            min_record = 1e-7
            current_bottom, current_top = ax.get_ylim()
            ax.set_ylim(min_record, current_top * 3)

        gaps = (max_record - min_record) / 5
        c = np.geomspace(min_record, max_record, num=5)
        # c = np.arange(min_record, max_record+gaps, gaps)

        ax.set_yscale("log")

        ax.minorticks_off()
        ax.get_yaxis().set_major_formatter(ticker.ScalarFormatter())
        ax.set_yticks(c)

        vals = ax.get_yticks()
        if perct:
            ax.set_yticklabels(["{:,.2%}".format(x) for x in vals])
        else:
            ax.set_yticklabels(["{:,.2}".format(x) for x in vals])

        formatter = mticker.ScalarFormatter(useMathText=True)
        formatter.set_powerlimits((0, 1))
        ax.yaxis.set_major_formatter(formatter)

        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)

        ax.set_xticks(x_axis)
        # ax2.set_xlim([2,3])

        return lines, labs

    def prm(
        self,
        ax,
        data,
        plist: list,
        x_axis: list,
        y_label: str,
        x_label: str,
        markersize: list = [12],
        marker: list = ["."],
        linestyle: list = ["-"],
        perct: bool = False,
        color=False,
        qutile=[0.5, 0.5],
        method=None,
        capsize=3,
        fixcap: list = None,
        x_posc: list = None,
        mm="mean",
        errmethod="percentile",
    ):
        """_summary_

        Args:
            ax (_type_): _description_
            data (_type_): _description_
            plist (list): _description_
            x_axis (list): _description_
            y_label (str): _description_
            x_label (str): _description_
            markersize (list, optional): _description_. Defaults to [12].
            marker (list, optional): _description_. Defaults to ["."].
            linestyle (list, optional): _description_. Defaults to ["-"].
            perct (bool, optional): _description_. Defaults to False.
            color (bool, optional): _description_. Defaults to False.
            qutile (list, optional): _description_. Defaults to [0.5, 0.5].
            method (_type_, optional): _description_. Defaults to None.
            capsize (int, optional): _description_. Defaults to 3.
            data_str (_type_, optional): Data structures. Defaults to None. If raw then change the data below
            x_posc (_type_, optional): Change the position of the error bar slightly. Defaults to None.

        Returns:
            _type_: _description_
        """

        labs = []
        lines = []
        if not fixcap:
            max_record = np.max(data)
            min_record = np.min(data)
            if min_record <= 1e-7:
                min_record = 1e-7
                current_bottom, current_top = ax.get_ylim()
                ax.set_ylim(min_record, current_top * 3)
            gaps = (max_record - min_record) / 5

            c = np.geomspace(min_record, max_record, num=5)
        else:
            c = np.geomspace(fixcap[0], fixcap[1], num=5)

        flag = 0
        for j in plist:
            dataT = [data[i][j] for i in range(len(data))]
            if mm == "mean":
                y0 = [np.mean(dataT[i]) for i in range(len(dataT))]
            elif mm == "median":
                y0 = [np.median(dataT[i]) for i in range(len(dataT))]

            if errmethod == "percentile":
                err1 = [np.quantile(dataT[i], qutile[0]) for i in range(len(dataT))]
                err2 = [np.quantile(dataT[i], qutile[1]) for i in range(len(dataT))]
            elif errmethod == "stderr":
                std_derr = [
                    np.std(dataT[i]) / np.sqrt(len(dataT[i])) for i in range(len(dataT))
                ]
                err1 = [y0[i] - std_derr[i] for i in range(len(dataT))]
                err2 = [y0[i] + std_derr[i] for i in range(len(dataT))]

            # for i in range(len(y0)):
            #     if y0[i] <= 1e-7:
            #         y0[i] = 1e-8
            if method == None:
                if color:
                    line = ax.plot(
                        x_axis,
                        y0,
                        label="p=" + str(j + 1),
                        marker=marker[flag],
                        linestyle=linestyle[flag],
                        markersize=markersize[flag],
                        color=color,
                    )
                else:
                    line = ax.plot(
                        x_axis,
                        y0,
                        label="p=" + str(j + 1),
                        marker=marker[flag],
                        linestyle=linestyle[flag],
                        markersize=markersize[flag],
                    )

            if method == "shadow":
                if color:
                    line = ax.plot(
                        x_axis,
                        y0,
                        label="p=" + str(j + 1),
                        marker=marker[flag],
                        linestyle=linestyle[flag],
                        markersize=markersize[flag],
                        color=color,
                    )
                    ax.fill_between(
                        x_axis,
                        err1,
                        err2,
                        alpha=0.5,
                        color=color,
                        edgecolor="none",  # transparancy
                    )
                else:
                    line = ax.plot(
                        x_axis,
                        y0,
                        label="p=" + str(j + 1),
                        marker=marker[flag],
                        linestyle=linestyle[flag],
                        markersize=markersize[flag],
                    )
                    ax.fill_between(
                        x_axis,
                        err1,
                        err2,
                        alpha=0.5,
                        edgecolor="none",  # transparancy
                    )
            elif method == "error bar":
                err_bar_1 = [y0[i] - err1[i] for i in range(len(y0))]
                err_bar_2 = [err2[i] - y0[i] for i in range(len(y0))]
                if x_posc:
                    x_axis_n = [
                        x_axis[i] + x_posc[flag][i] for i in range(len(x_posc[flag]))
                    ]
                else:
                    x_axis_n = x_axis
                line = ax.errorbar(
                    x_axis_n,
                    y0,
                    yerr=[err_bar_1, err_bar_2],
                    capsize=capsize,
                    color=color,
                    linestyle=linestyle[flag],
                    fmt=marker[flag],
                    markersize=markersize[flag],
                )
                line[-1][0].set_linestyle(linestyle[flag])

            lines.append(line[0])
            labs.append(line[0].get_label())

            flag += 1

        ax.minorticks_off()
        ax.get_yaxis().set_major_formatter(ticker.ScalarFormatter())
        ax.set_yticks(c)

        vals = ax.get_yticks()
        if perct:
            ax.set_yticklabels(["{:,.2%}".format(x) for x in vals])
        else:
            ax.set_yticklabels(["{:,.2}".format(x) for x in vals])

        formatter = mticker.ScalarFormatter(useMathText=True)
        formatter.set_powerlimits((0, 1))
        ax.yaxis.set_major_formatter(formatter)

        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)

        ax.set_xticks(x_axis)
        # ax2.set_xlim([2,3])

        return lines, labs

    def cvsq(
        self, ax, data, plist: list, x_axis: list, markersize: int, marker: str = "."
    ):
        """plot the data in the form of $1/p$"""
        labs = []
        lines = []
        for j in plist:
            y0 = [data[i][j] for i in range(len(data))]
            line = ax.scatter(
                x_axis, y0, label="p=" + str(j + 1), marker=marker, s=markersize
            )
            lines.append(line)
            labs.append(line.get_label())

        ax.set_ylabel("$1/\mathrm{P}_{gm}$")
        ax.set_xticks(x_axis)
        ax.set_yscale("log")

        return lines, labs


class SoluSpace(object):
    def __init__(self) -> None:
        pass
        # self.n = n
        # self.N = N

    def fixed_n(self, n: int, l: int):
        """Get the scale for the fixed n, with increasing l
        n: int, is the fixed of n
        l: (int), is the upper bound of the l
        return: x = the list of l,
                y1 = the list of the unconstratinted solution space size,
                y2 = the list of the constrainted solution space
        """
        x = [i for i in range(1, l)]
        y1 = [2 ** (n * j) for j in range(1, l)]
        y2 = [self.ScaleArith(n=n, l=j) for j in range(1, l)]

        return x, y1, y2

    def fixed_l(self, n: int, l: int):
        """Get the scale for the fixed l, with increasing n
        n: (int), is the upper bound of the n
        l: int, is the fixed of l

        return: x = the list of n,
                y1 = the list of the unconstratinted solution space size,
                y2 = the list of the constrainted solution space
        """

        x = [i for i in range(1, n)]
        y1 = [2 ** (j * l) for j in range(1, n)]
        y2 = [self.ScaleArith(n=j, l=l) for j in range(1, n)]

        return x, y1, y2

    def get_list(self, ns: list, ls: list):
        """Get the scale for two list inputs,
        ns (list), a list of n
        ls (list), a list of l

        return: x = the list of n,
                y1s = the list of the unconstratinted solution space size, with each row the growth of l, the column the fix l and grow n
                y2s = the list of the constrainted solution space, with each row the growth of l, the column the fix l and grow n
        """
        y1s = []
        y2s = []
        for i in ns:
            y1 = [2 ** (i * j) for j in ls]
            y2 = [self.ScaleArith(n=i, l=j) for j in ls]

            y1s.append(y1)
            y2s.append(y2)
        return np.array(y1s), np.array(y2s)

    def ScaleArith(self, n: int, l: int, verbose=False):
        """Used for caculating how many different solutions with math notion
        n: the number of the assets
        l: int the qubit block length
        """
        n = int(n)
        l = int(l)

        S = math.comb(2**l + n - 2, n - 1)  # this is the constraint solution space
        if verbose:
            print("The constrainted feasible space size is: ", S)
        return S
