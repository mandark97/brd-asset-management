from botocore.exceptions import ClientError
from jinja2 import Environment, FileSystemLoader

import boto3
import urllib.request
import json
import sys
import os
import webbrowser


def get_data(url):
    with urllib.request.urlopen(url) as json_data:
        data = []
        output = json.load(json_data)
        for index in range(len(output)):
            data.append(float(output[index]['VUAN']))
        return data


def get_latest_date(url):
    with urllib.request.urlopen(url) as json_data:
        return json.load(json_data)[0]['Data']


def set_values(data, units):
    for index in range(len(data)):
        data[index] = int(data[index] * units)
    return data


def render_template(simfonia, diverso, total, PLOT_MAX_PIXELS,
                    save_file=False):
    file_loader = FileSystemLoader('templates')

    env = Environment(loader=file_loader)

    template = env.get_template('email_template.j2')

    render = template.render(
        simfonia=simfonia,
        diverso=diverso,
        total=total,
        MAX_PIXELS=PLOT_MAX_PIXELS)

    if save_file:
        try:
            os.stat('generated')
        except:
            os.mkdir('generated')

        with open('generated/render.html', 'w') as file:
            file.write(render)

        web = webbrowser.get(using='firefox')

        render_path = os.path.abspath(os.getcwd()) + '/generated/render.html'

        web.open('file://' + render_path)

    return render


def send_email(SUBJECT, BODY_HTML, AWS_REGION, RECIPIENT, CHARSET, SENDER):

    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'statusCode': 502}

    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
