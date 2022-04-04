import json, requests, subprocess
from flask import Flask, request, make_response
from slack_sdk import WebClient

token = "xoxb-3337896479552-3311261174037-8gtinA2F7fL8sXb9Parw3tsK" #Bot
app = Flask(__name__)

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)

def get_answer(user_query):
    return user_query

def event_handler(event_type, slack_event):
    channel = slack_event["event"]["channel"]
    string_slack_event = str(slack_event)
    if string_slack_event.find("{'type': 'user', 'user_id': ") != -1:  # 멘션으로 호출
        try:
            user_query = slack_event['event']['blocks'][0]['elements'][0]['elements'][1]['text']
            answer = get_answer(user_query)
            command=list(answer.strip().split(' '))
            cmd = command[1]
            ip = command[2]
            print(command)
            with open("/etc/ansible/hosts", "a") as f:
                f.write('\n'+ip)
                print('test')
                f.close()
            
            if command[0] == 'node-exporter':
                flag = subprocess.run(['ansible-playbook', 'node-play.yml'])
                print(flag)
                post_message(token, "grafana-alert", flag)

            subprocess.run(['sudo', 'sed', '-i','$d','/etc/ansible/hosts'])
            subprocess.run(['cd', '/home/daou_docker/nginx'])
            subprocess.run(['sudo', 'docker-compose', 'down'])
            subprocess.run(['sudo', 'docker-compose', 'up', '-d'])
            return make_response("ok", 200, )

        except IndexError:
            pass

    message = "[%s] cannot find event handler" % event_type
    return make_response(message, 200, {"X-Slack-No-Retry": 1})

@app.route('/', methods=['POST'])

def hello_there():

    slack_event = json.loads(request.data)

    if "challenge" in slack_event:

        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    if "event" in slack_event:

        event_type = slack_event["event"]["type"]

        return event_handler(event_type, slack_event)

    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})





if __name__ == '__main__':

    app.run(host = '0.0.0.0', debug=False, port=8000)

