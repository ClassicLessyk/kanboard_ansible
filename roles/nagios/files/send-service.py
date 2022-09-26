#!/usr/bin/python3

import sys
from discord_webhook import DiscordWebhook, DiscordEmbed

HOOK = "https://discord.com/api/webhooks/1022803986656542760/W-iJ5QuZMb-FQmQAHxSpKXTIYfmte9yJxfXsnwmF7mDhjuTU2e0XG0CRyXAFVolJHN9L"
KEYS = ['type', 'servdesc', 'host', 'hostaddr', 'servstate',  'output']
DOMAIN = "10.26.0.92"


def codecolor(alerttype):
    clr_red = 13632027
    clr_yel = 16098851
    clr_grn = 8311585

    if alerttype == 'PROBLEM':
        return clr_red
    elif alerttype == 'RECOVERY':
        return clr_grn
    else:
        return clr_yel


def main(nag_in):
    cmd = nag_in.pop(0)
    data = {KEYS[i]: nag_in[i] for i in range(len(KEYS))}

    link = "http://" + DOMAIN + "/nagios/cgi-bin/extinfo.cgi?type=2&host=" + data['host'] + "&service=" + data['servdesc']

    line1 = "**<" + data['type'] + ">** " + data['host'] + " - " + data['servdesc'] + ": " + data['servstate']
    line2 = data['hostaddr'] + " " + data['output']

    webhook = DiscordWebhook(url=HOOK)
    # create embed object for webhook
    embed = DiscordEmbed(title=line1, description=line2, color=codecolor(data['type']))
    embed.set_author(name='Open Nagios service detail', url=link)

    # set timestamp
    #embed.set_timestamp(int(data['time']))

    # add embed object to webhook
    webhook.add_embed(embed)

    res = webhook.execute()


main(sys.argv)
