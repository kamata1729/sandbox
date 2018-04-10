# coding: utf-8

from slackbot.bot import default_reply  #該当する応答がない場合に反応するデコーダ
import pylab as plt
import numpy as np
import requests
from slackclient import SlackClient

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない
@default_reply()
def default(message):
    message.reply("デフォルトの返答")

    text = message.body['text']
    try:
        pl_equation(text, outfile='output', padding=0.1)
        image_pass = 'output.png'
        # files = {'image': open(image_pass, 'rb')}
        # param = {"title": "output image", 'token': "xoxb-342789435984-HmOb1nseXolLo2VLaRUIuREs", 'channels': "C7EDDH883",}
        # requests.post(url="https://slack.com/api/files.upload", params=param, files=files)

        access_token = "xoxb-342789435984-HmOb1nseXolLo2VLaRUIuREs"
        CHANNEL_ID = "CA37HHE2G"
        with open(image_pass, 'rb') as f:
            param = {'token': access_token, 'channels': CHANNEL_ID, 'title': 'output_image'}
            r = requests.post("https://slack.com/api/files.upload", params=param, files={'file': f})
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
