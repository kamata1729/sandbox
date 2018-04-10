# coding: utf-8

from slackbot.bot import default_reply
import pylab as plt
import numpy as np

@default_reply()
def default(message):
    text = message.body['text']
    try:
        pl_equation(text, outfile='output', padding=0.1)
        image_pass = 'output.png'
        message.channel.upload_file(fname='output', fpath=image_pass)
    except:
        message.reply("画像に変換できません")


def pl_equation(eq, fontsize=50, outfile=None, padding=0.1):
    """Plot an equation as a matplotlib figure.
    Parameters
    ----------
    eq : string
        The equation that you wish to plot. Should be plottable with
        latex. If `$` is included, they will be stripped.
    fontsize : number
        The fontsize passed to plt.text()
    outfile : string
        Name of the file to save the figure to.
    padding : float
        Amount of padding around the equation in inches.
    Returns
    -------
    ax : matplotlib axis
        The axis with your equation.
    """
    # clean equation string
    eq = eq.strip('$').replace(' ', '')

    # set up figure
    f = plt.figure()
    ax = plt.axes([0, 0, 1, 1])
    r = f.canvas.get_renderer()

    # display equation
    t = ax.text(0.5, 0.5, '${}$'.format(eq), fontsize=fontsize,
                horizontalalignment='center', verticalalignment='center')

    # resize figure to fit equation
    bb = t.get_window_extent(renderer=r)
    w, h = bb.width / f.dpi, np.ceil(bb.height / f.dpi)
    f.set_size_inches((padding + w, padding + h))

    # set axis limits so equation is centered
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    ax.grid(False)
    ax.set_axis_off()

    if outfile is not None:
        plt.savefig(outfile)

    return ax
