GREETINGS = "Hi {0}! It's time for your daily work tracker. Please answer the following questions:"

MOOD_SCORE_MESSAGE = 'On a scale of 1 to 5, how did you feel about your work today?'

MOOD_SCORE_FAILURE_MESSAGE = 'Sorry, please provide a number between 1 and 5.'

MOOD_REASON_MESSAGE = 'What were some reasons for your mood score today?'

DAILY_UPDATES_MESSAGE = '''
    What did you work on today? Separate your entries with newlines and add tags in square brackets.
    Example: Shipped the dashboard [Revenue dashboard, Tag 2]
'''

WEEKLY_UPDATES_MESSAGE = '''
    What did you work on this week? Separate your entries with newlines and add tags in square brackets.
    Example: Shipped the dashboard [Revenue dashboard, Tag 2]
'''

UPDATES_PARSE_FAILURE_MESSAGE = '''
    Sorry, I couldn't parse that message. Try again or navigate to https://progress-client.herokuapp.com to fill it in.
'''

FAREWELL_MESSAGE = "Thanks! Check out your dashboard at https://progress-client.herokuapp.com. That's all for now!"

NEXT_MESSAGE_MAP = {
  'mood_score': MOOD_REASON_MESSAGE,
  'mood_reason': DAILY_UPDATES_MESSAGE,
  'daily_updates': FAREWELL_MESSAGE,
  'weekly_updates': FAREWELL_MESSAGE
}

NEXT_QUESTION_MAP = {
  'mood_score': 'mood_reason',
  'mood_reason': 'daily_updates',
  'daily_updates': 'finished',
  'weekly_updates': 'finished'
}