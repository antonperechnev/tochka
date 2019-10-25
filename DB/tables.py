from sqlalchemy import create_engine, Text, BigInteger, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import MetaData
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util import KeyedTuple
import uuid

engine = create_engine('postgresql://postgres:Anton1995@localhost/tochka', isolation_level="AUTOCOMMIT")

meta = MetaData(engine)
base = declarative_base()
Session = sessionmaker(engine)
session = Session()


class Clients(base):
    __tablename__ = 'clients'

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    fio = Column(Text, nullable=False)
    balance = Column(BigInteger, nullable=False)
    hold = Column(BigInteger, nullable=False)
    status = Column(Text, nullable=False)


if __name__ == '__main__':
    base.metadata.create_all(engine, checkfirst=True)
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
        session.bulk_save_objects(obj)
    except IntegrityError:
        pass
