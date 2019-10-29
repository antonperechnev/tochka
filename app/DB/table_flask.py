from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import UUID
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tochkatest@localhost/tochka'
db = SQLAlchemy(app)#, session_options={'autocommit': True})


class Clients(db.Model):
    __tablename__ = 'clients'

    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    fio = db.Column(db.Text, nullable=False)
    balance = db.Column(db.BigInteger, nullable=False)
    hold = db.Column(db.BigInteger, nullable=False)
    status = db.Column(db.Text, nullable=False)


if __name__ == '__main__':
    db.create_all()
    first = Clients(uuid=uuid.UUID('26c940a1-7228-4ea2-a3bc-e6460b172040'),
                    fio='Петров Иван Сергеевич',
                    balance=1700, hold=300, status='открыт')
    second = Clients(uuid=uuid.UUID('7badc8f8-65bc-449a-8cde-855234ac63e1'),
                     fio='Kazitsky Jason',
                     balance=200, hold=200, status='открыт')
    third = Clients(uuid=uuid.UUID('5597cc3d-c948-48a0-b711-393edf20d9c0'),
                    fio='Пархоменко Антон Александрович',
                    balance=10, hold=300, status='открыт')
    fourth = Clients(uuid=uuid.UUID('867f0924-a917-4711-939b-90b179a96392'),
                     fio='Петечкин Петр Измаилович',
                     balance=1_000_000, hold=1, status='закрыт')
    obj = [first, second, third, fourth]
    try:
        db.session.bulk_save_objects(obj)
    except IntegrityError:
        pass
