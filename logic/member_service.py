import uuid
import state
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from database.db import supabase


# ── Helpers ────────────────────────────────────────────────

def _parse_date(s):
    if not s or isinstance(s, date): return s
    return datetime.strptime(str(s)[:10], "%Y-%m-%d").date()

def _parse_dt(s):
    if not s or isinstance(s, datetime): return s
    return datetime.fromisoformat(str(s).replace("Z", "")).replace(tzinfo=None)

class MemberObj:
    """Wraps a Supabase dict so the rest of the app uses dot notation."""
    def __init__(self, d):
        self.id                  = d["id"]
        self.name                = d["name"]
        self.phone               = d.get("phone")
        self.qr_code             = d["qr_code"]
        self.birthday            = _parse_date(d["birthday"])
        self.branch              = d["branch"]
        self.subscription_months = d["subscription_months"]
        self.subscription_expires = _parse_dt(d["subscription_expires"])
        self.created_at          = _parse_dt(d.get("created_at"))


# ── Member queries ──────────────────────────────────────────

def get_member_by_qr(qr_code: str):
    res = supabase.table("members").select("*").eq("qr_code", qr_code).execute()
    return MemberObj(res.data[0]) if res.data else None

def get_member_by_id(member_id: str):
    res = supabase.table("members").select("*").eq("id", member_id).execute()
    return MemberObj(res.data[0]) if res.data else None

def get_all_members():
    res = supabase.table("members")\
                  .select("*")\
                  .order("name")\
                  .execute()
    return [MemberObj(m) for m in res.data]

def add_member(name: str, phone=None, subscription_months: int = 1, birthday=None):
    member_id = str(uuid.uuid4())
    expires = datetime.now() + relativedelta(months=subscription_months)
    data = {
        "id":                   member_id,
        "name":                 name,
        "phone":                phone,
        "qr_code":              member_id,
        "birthday":             birthday.isoformat() if birthday else None,
        "branch":               state.CURRENT_BRANCH,
        "subscription_months":  subscription_months,
        "subscription_expires": expires.isoformat(),
    }
    supabase.table("members").insert(data).execute()
    return member_id, member_id


# ── Log queries ─────────────────────────────────────────────

def log_action(member_id: str, action: str):
    supabase.table("logs").insert({
        "member_id": member_id,
        "action":    action,
        "branch":    state.CURRENT_BRANCH,
    }).execute()

def get_last_action(member_id: str):
    res = supabase.table("logs")\
                  .select("action")\
                  .eq("member_id", member_id)\
                  .order("timestamp", desc=True)\
                  .limit(1)\
                  .execute()
    return res.data[0]["action"] if res.data else None

def get_all_logs():
    res = supabase.table("logs")\
                  .select("*, members(name, subscription_months)")\
                  .eq("branch", state.CURRENT_BRANCH)\
                  .order("timestamp", desc=True)\
                  .execute()
    result = []
    for log in res.data:
        member = log.get("members") or {}
        result.append((
            log["member_id"],
            member.get("name", "Unknown"),
            member.get("subscription_months", 1),
            log["action"],
            _parse_dt(log["timestamp"]),
        ))
    return result

def get_member_logs(member_id: str):
    res = supabase.table("logs")\
                  .select("action, timestamp")\
                  .eq("member_id", member_id)\
                  .order("timestamp", desc=True)\
                  .limit(20)\
                  .execute()
    return [(r["action"], _parse_dt(r["timestamp"])) for r in res.data]