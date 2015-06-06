__author__ = 'beast'

from signals import post_save_activity, post_save_result

from flask import render_template
import grequests as requests


def subscribe():
    post_save_activity.connect(activity_created)
    post_save_result.connect(result_created)


def activity_created(sender, activity_id, inputs):
    print "Received Signal"

    if inputs['type'] == "A":



        template = render_template("system_a_template1.xml", reference_id = inputs["reference_id"])
        headers = {'content-type': 'text/xml'}

        requests.post('https://api.github.com/user', auth=('user', 'pass'), data=template)

    elif inputs['type'] == "B":




        r= requests.send(requests.get('https://blockchain.info/ticker'))


        json_result = r.json()
    else:
        pass


def result_created(activity_id, inputs):
    print "Received Signal"


subscribe()