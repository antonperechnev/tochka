import schedule
import time

from DB.tables import Clients

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://postgres:Anton1995@localhost/tochka', isolation_level="AUTOCOMMIT")

meta = MetaData(engine)
base = declarative_base()


def hold_update():
    Session = sessionmaker(engine)
    session = Session()
    users = session.query(Clients).all()
    for user in users:
        user.balance -= user.hold
        user.hold = 0
    session.commit()


schedule.every(10).minutes.do(hold_update)
while 1:
    schedule.run_pending()
    time.sleep(1)