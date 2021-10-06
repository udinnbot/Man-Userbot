try:
    from userbot.modules.sql_helper import BASE, SESSION
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String


class NoUserBot(BASE):
    __tablename__ = "nouserbot"
    chat_id = Column(String(20), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)


NoUserBot.__table__.create(checkfirst=True)


def get_nouserbot():
    try:
        return SESSION.query(NoUserBot).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_nouserbot(chat_id):
    adder = NoUserBot(str(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def del_nouserbot(chat_id):
    rem = SESSION.query(NoUserBot).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def del_nouserbot_all():
    SESSION.execute("""TRUNCATE TABLE NoUserBot""")
    SESSION.commit()
