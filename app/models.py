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


class DailyTag(db.Model):
	__tablename__ = 'daily_tags'

	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer)
	entryid = db.Column(db.Integer)
	updateid = db.Column(db.Integer)
	date_string = db.Column(db.String)
	tag = db.Column(db.String)


class WeeklyUpdate(db.Model):
	__tablename__ = 'weekly_updates'

	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer)
	date_string = db.Column(db.String)
	body = db.Column(db.Text)


class WeeklyTag(db.Model):
	__tablename__ = 'weekly_tags'

	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer)
	updateid = db.Column(db.Integer)
	date_string = db.Column(db.String)
	tag = db.Column(db.String)