from datetime import datetime
from firm import db,login_manager
from flask_login import UserMixin,current_user

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model,UserMixin):
      __tablename__ = 'users'
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(120), unique=True, nullable=False)
      email = db.Column(db.String(120), unique=True, nullable=False)
      designation = db.Column(db.String(120), nullable=False)
      image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
      password = db.Column(db.String(60), nullable=False)
      is_admin = db.Column(db.Boolean,default = True)
      invoice = db.relationship('Invoice',backref='author', lazy=True)
      def __repr__(self):
        return f" User('{self.username}','{self.email}','{self.designation}','{self.image_file}')"

class Invoice(db.Model):
    __tablename__ = 'invoice' 
    id = db.Column(db.Integer, primary_key=True)
    #ref_number = db.Column(db.Integer,unique=True, nullable=False)
    ref_number = db.Column(db.String(),nullable=False)
    name_to = db.Column(db.String(200),  nullable=False)
    address_to = db.Column(db.String, nullable=False)

    telephone_to = db.Column(db.String, nullable=True)
    email_to = db.Column(db.String, nullable=True)
    box_number_to = db.Column(db.String, nullable=True)
    terms = db.Column(db.String,nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    due_date =db.Column(db.Date,nullable=False)
    vat = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)

    def get_last_id():

        qry = Invoice.query.order_by(Invoice.id.desc()).first()
        x = qry.id
        ym = date.today().strftime("%y%m")
        q_custom_id = "" + ym + str(x).zfill(3) + ""

        return q_custom_id

    def __init__(self,ref_number,name_to,address_to,telephone_to,email_to, box_number_to,vat,terms,issue_date,due_date,user_id):
        self.ref_number = ref_number
        self.name_to = name_to
        self.address_to = address_to
        self.telephone_to = telephone_to
        self.email_to=email_to 
        self.box_number_to = box_number_to
        self.vat= vat
        self.terms=terms
        self.issue_date =issue_date
        self.due_date=due_date
        self.user_id=user_id
        

class InvoiceLineItem(db.Model):
    __tablename__ = 'line_items' 
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(255), nullable=False)
    disbursements =db.Column(db.String, nullable=True)
    professional_fees =db.Column(db.String, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
        # Relationship
    invoice = db.relationship(
        'Invoice',
        backref=db.backref('laps', lazy='dynamic', collection_class=list)

    )
