from init import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(org_id):
	return Org.query.get(int(org_id))


class Org(db.Model,UserMixin):
	__tablename__ = "org"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False) 
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	#image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
	def __repr__(self):
		return f"Org('{self.name}', '{self.email}', '{self.password}')"   


class ImageLink(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    link = db.Column(db.String(1000),nullable=False)
    def __repr__(self):
        return '<Task %r>' % self.id