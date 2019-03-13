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
            'rate': self.rate.serialize()
        }


class ExchangeRate(db.Model):
    __tablename__ = 'exchangerate'

    id = db.Column(db.Integer, primary_key=True)
    base = db.Column(db.String(5), nullable=False)
    to = db.Column(db.String(5), nullable=False)
    rate_data = db.relationship('ExchangeRateData',order_by='desc(ExchangeRateData.date)', backref=db.backref('exchangerate'),
                                lazy='dynamic')

    def statistic(self, date):
        rate_datas = self.rate_data.filter(ExchangeRateData.date <= date).limit(7)
        min = float('inf')
        max = float('-inf')
        total = 0
        for data in rate_datas:
            if data.rate_value > max:
                max = data.rate_value
            if data.rate_value < min:
                min = data.rate_value
            total = total + data.rate_value
        return {
            'variance': max - min,
            'average': total/rate_datas.count()
        }

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

    def serialize(self):
        return{
            'id': self.id,
            'date': str(self.date),
            'rate_value': self.rate_value
        }
