from app import db


class TrackRate(db.Model):
    __tablename__ = 'trackrate'

    id = db.Column(db.Integer, primary_key=True)
    rate_id = db.Column(db.Integer, db.ForeignKey('exchangerate.id'))
    rate = db.relationship('ExchangeRate', foreign_keys=rate_id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'rate_base': self.rate.base,
            'rate_to': self.rate.to
        }


class ExchangeRate(db.Model):
    __tablename__ = 'exchangerate'

    id = db.Column(db.Integer, primary_key=True)
    base = db.Column(db.String(5), nullable=False)
    to = db.Column(db.String(5), nullable=False)
    rate_data = db.relationship('RateData', backref=db.backref('exchangerate'),
                                lazy=True)

    def serialize(self):
        return{
            'id': self.id,
            'base': self.base,
            'to': self.to
        }


class ExchangeRateData(db.Model):
    __tablename__ = 'exchangeratedata'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    rate_value = db.Column(db.Numeric, nullable=False)
    exchangerate_id = db.Column(db.Integer, db.ForeignKey('exchangerate.id'))
