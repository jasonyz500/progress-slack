from slackclient import SlackClient


class ProgressSlackClient(SlackClient):
    def __init__(self, access_token):
        super(ProgressSlackClient, self).__init__(access_token)

    def get_user_info_from_id(self, id):
        resp = self.api_call('users.info', user=id)
        return resp.get('user')

    def get_recent_messages(self, channel_id):
        resp = self.api_call('conversations.history',
                             channel=channel_id)
        return resp.get('messages', [])

    def get_im_channel_id(self, user_id):
        resp = self.api_call('conversations.open',
                             users=user_id)
        if not resp.get('ok', False):
            return None
        return resp.get('channel').get('id')

    def send_message(self, message, channel_id):
        resp = self.api_call('chat.postMessage',
                             as_user='true',
                             link_names=1,
                             channel=channel_id,
                             text=message)
        return resp.get('ok', False)
