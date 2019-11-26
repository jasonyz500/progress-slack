import os
from app import db
from message_consts import *
from slack_client import ProgressSlackClient
from models import User, DailyEntry, DailyUpdate, DailyTag, WeeklyUpdate, WeeklyTag

ACCESS_TOKEN = os.environ.get('SLACK_ACCESS_TOKEN')
slack_client = ProgressSlackClient(ACCESS_TOKEN)


def handle_response(channel_id, slack_user_id, team_id, message):
    user = User.get_by_slack_ids(slack_user_id, team_id)
    if not user:
        return

    # todo: abort if user has already filled out the entry

    current_question = user.current_slack_question
    err = save_to_db(user.id, current_question, user.slack_question_date_string, message)

    if err:
        slack_client.send_message(response, channel_id)
        return

    if current_question == 'daily_updates' and is_eow(user.id):
        response = WEEKLY_UPDATES_MESSAGE
        next_question = 'weekly_updates'
    else:
        response = NEXT_MESSAGE_MAP.get(current_question, 'YUI!')
        next_question = NEXT_QUESTION_MAP.get(current_question, None)
        
    user.current_slack_question = next_question
    db.session.add(user)
    db.session.commit()
    slack_client.send_message(response, channel_id)
    return


def check_if_eow(user_id):
    return False


def parse_updates_and_tags(body):
    # returns a list of objects {update: '', tags: ['tag1', 'tag2']}
    res = []
    # update delimiter is newline
    update_strs = body.split('\n')
    for update_str in update_strs:
        try:
            update_body, tags_str = update_str.strip().split('[')
            assert tags_str[-1] == ']'
            tags_str = tags_str[:-1]
        except (ValueError, AssertionError):
            update_body, tags_str = update_str.strip(), ''
        res.append({ 'update': update_body, 'tags': [tag.strip() for tag in tags_str.split(',')] })
    return res


def save_to_db(user_id, current_question, ds, body):
    if current_question == 'mood_score':
        try:
            body = int(body)
            assert body <= 5
            assert body >= 1
        except (ValueError, AssertionError):
            return MOOD_SCORE_FAILURE_MESSAGE
        # write to db
        entry = DailyEntry(user_id, ds, body)
        db.session.add(entry)
        db.session.commit()
    elif current_question == 'mood_reason':
        entry = DailyEntry.get_by_userid_and_ds(user_id, ds)
        entry.mood_reason = body
        db.session.add(entry)
        db.session.commit()
    elif current_question == 'daily_updates':
        updates = parse_updates_and_tags(body)
        # get entryid
        entry = DailyEntry.get_by_userid_and_ds(user_id, ds)
        entry_id = entry.id
        # save all updates
        for update in updates:
            update_obj = DailyUpdate(user_id, entry_id, ds, update['update'])
            db.session.add(update_obj)
            # auto populate next ID into update_obj
            db.session.flush()
            for tag in update['tags']:
                tag_obj = DailyTag(user_id, entry_id, update_obj.id, ds, tag)
                db.session.add(tag_obj)
        db.session.commit()
    elif current_question == 'weekly_updates':
        updates = parse_updates_and_tags(body)
        for update in updates:
            update_obj = WeeklyUpdate(user_id, ds, update['update'])
            db.session.add(update_obj)
            # auto populate next ID into update_obj
            db.session.flush()
            for tag in update['tags']:
                tag_obj = WeeklyTag(user_id, update_obj.id, ds, tag)
                db.session.add(tag_obj)
        db.session.commit()
    return None



