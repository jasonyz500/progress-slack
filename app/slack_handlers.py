from flask import Blueprint, request
from messaging_logic import handle_response

import hashlib
import hmac
import os

bp = Blueprint('slack', __name__, url_prefix='/slack')


@bp.route('/event', methods=['POST'])
def handle_event():
    # check if the request is legit by checking signed token
    # if not validate_slack_signature(request):
        # return 'Bad signature'

    body = request.get_json()

    # handle challenge
    if body.get('challenge'):
        return body.get('challenge')

    event = body.get('event', {})
    # check message that triggered callback is not from a bot. this check is also in handle_response()
    if event.get('bot_id'):
        return 'Message was from a bot.'
    slack_user_id = event.get('user')
    channel_id = event.get('channel')
    team_id = event.get('team')
    message = event.get('text')
    msg_id = event.get('client_msg_id')
    handle_response(channel_id, slack_user_id, team_id, message, msg_id)
    return 'Success'


def validate_slack_signature(request):
    # https://api.slack.com/docs/verifying-requests-from-slack#about
    body = request.data
    headers = request.headers

    slack_signature = str(headers.get('X-Slack-Signature', ''))
    slack_request_timestamp = headers.get('X-Slack-Request-Timestamp', '')
    slack_signing_secret = os.environ.get('SLACK_SIGNING_SECRET')

    sig_basestring = 'v0:' + slack_request_timestamp + ':' + body
    my_signature = 'v0=' + hmac.new(slack_signing_secret, sig_basestring, digestmod=hashlib.sha256).hexdigest()

    return hmac.compare_digest(my_signature, slack_signature)
