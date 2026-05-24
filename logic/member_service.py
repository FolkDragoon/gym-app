import uuid
from datetime import datetime
from dateutil.relativedelta import relativedelta
from database.db import Session
from database.models import Member, Log

def get_member_by_qr(qr_code: str):
    with Session() as s:
        return s.query(Member).filter_by(qr_code=qr_code).first()

def get_member_by_id(member_id: str):
    with Session() as s:
        return s.query(Member).filter_by(id=member_id).first()

def add_member(name: str, phone: str = None, subscription_months: int = 1, birthday=None):
    with Session() as s:
        member_id = str(uuid.uuid4())
        expires = datetime.now() + relativedelta(months=subscription_months)
        member = Member(
            id=member_id,
            name=name,
            phone=phone,
            qr_code=member_id,
            birthday=birthday,
            subscription_months=subscription_months,
            subscription_expires=expires
        )
        s.add(member)
        s.commit()
        return member.id, member.qr_code

def log_action(member_id: str, action: str):
    with Session() as s:
        log = Log(member_id=member_id, action=action)
        s.add(log)
        s.commit()

def get_last_action(member_id: str):
    with Session() as s:
        log = s.query(Log).filter_by(member_id=member_id)\
                          .order_by(Log.timestamp.desc()).first()
        return log.action if log else None

def get_all_logs():
    with Session() as s:
        logs = s.query(Log, Member)\
                .join(Member, Log.member_id == Member.id)\
                .order_by(Log.timestamp.desc())\
                .all()
        return [
            (member.id, member.name, member.subscription_months, log.action, log.timestamp)
            for log, member in logs
        ]

def get_member_logs(member_id: str):
    with Session() as s:
        logs = s.query(Log).filter_by(member_id=member_id)\
                           .order_by(Log.timestamp.desc())\
                           .limit(20).all()
        return [(log.action, log.timestamp) for log in logs]
    
def get_all_members():
    with Session() as s:
        return s.query(Member).order_by(Member.name).all()