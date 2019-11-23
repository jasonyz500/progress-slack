import datetime
import psycopg2
import os
import subprocess
import sys
from app import db
from message_consts import *
from slack_client import ProgressSlackClient

ACCESS_TOKEN = os.environ.get('SLACK_ACCESS_TOKEN')
slack_client = ProgressSlackClient(ACCESS_TOKEN)
DATABASE_URL = os.environ.get('DATABASE_URL')

def cron_kickoff(slack_user_id, team_id):
    # get channel id
    channel_id = slack_client.get_im_channel_id(slack_user_id)

    # format greeting message
    user_info = slack_client.get_user_info_from_id(slack_user_id)
    full_name = user_info.get('full_name', ' ')
    first_name = full_name.split(' ')[0]
    greeting_message = GREETINGS.format(first_name)

    # update user's current question
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cursor.execute("""
        update users 
        set current_slack_question = 'mood_score' 
        where slack_userid = %s and slack_teamid = %s""",
        (slack_user_id, team_id))
    conn.commit()

    # send
    slack_client.send_message(greeting_message, channel_id)
    slack_client.send_message(MOOD_SCORE_MESSAGE, channel_id)


if __name__ == "__main__":
    # only run on weekdays
    # todo: support multiple time zones
    if ((datetime.datetime.today() - datetime.timedelta(hours=8)).weekday() <= 4 and len(sys.argv) == 3):
        cron_kickoff(sys.argv[1], sys.argv[2])