from app import db


class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	slack_userid = db.Column(db.String)
	slack_teamid = db.Column(db.String)
	slack_name = db.Column(db.String)
	current_slack_question = db.Column(db.String)
	slack_question_date_string = db.Column(db.String)

	@staticmethod
	def get_by_id(user_id):
		return User.query.filter_by(id=user_id).first()

	@staticmethod
	def get_by_slack_ids(slack_userid, slack_teamid):
		return User.query.filter_by(slack_userid=slack_userid, slack_teamid=slack_teamid).first()


class DailyEntry(db.Model):
	__tablename__ = 'daily_entries'

	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer)
	date_string = db.Column(db.String)
	mood_score = db.Column(db.Integer)
	mood_reason = db.Column(db.Text)

	def __init__(self, userid=None, date_string=None, mood_score=None, mood_reason=None):
		self.userid = userid
		self.date_string = date_string
		self.mood_score = mood_score
		self.mood_reason = mood_reason

	@staticmethod
	def get_by_userid_and_ds(userid, ds):
		return DailyEntry.query.filter_by(userid=userid, date_string=ds).first()


class DailyUpdate(db.Model):
	__tablename__ = 'daily_updates'

	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer)
	entryid = db.Column(db.Integer)
	date_string = db.Column(db.String)
	body = db.Column(db.Text)

	def __init__(self, userid=None, entryid=None, date_string=None, body=None):
		self.userid = userid
		self.entryid = entryid
		self.date_string = date_string
		self.body = body


class DailyTag(db.Model):
	__tablename__ = 'daily_tags'

	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer)
	entryid = db.Column(db.Integer)
	updateid = db.Column(db.Integer)
	date_string = db.Column(db.String)
	tag = db.Column(db.String)

	def __init__(self, userid=None, entryid=None, updateid=None, date_string=None, tag=None):
		self.userid = userid
		self.entryid = entryid
		self.updateid = updateid
		self.date_string = date_string
		self.tag = tag


class WeeklyUpdate(db.Model):
	__tablename__ = 'weekly_updates'

	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer)
	date_string = db.Column(db.String)
	body = db.Column(db.Text)

	def __init__(self, userid=None, date_string=None, body=None):
		self.userid = userid
		self.date_string = date_string
		self.body = body


class WeeklyTag(db.Model):
	__tablename__ = 'weekly_tags'

	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer)
	updateid = db.Column(db.Integer)
	date_string = db.Column(db.String)
	tag = db.Column(db.String)

	def __init__(self, userid=None, updateid=None, date_string=None, tag=None):
		self.userid = userid
		self.updateid = updateid
		self.date_string = date_string
		self.tag = tag