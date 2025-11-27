import uuid
from datetime import datetime
from typing import Optional
class User:
    def __init__(
        self,
        email: str,
        name: str,
        user_id: Optional[str] = None,
        otp: Optional[str] = None,
        otp_expires_at: Optional[datetime] = None,
        email_verified: bool = False,
        status: str = 'active',
        user_type: str = 'user',
        created_at: Optional[datetime] = None
    ):
        self.id = user_id or str(uuid.uuid4())
        self.email = email.lower().strip()
        self.name = name
        self.otp = otp
        self.otp_expires_at = otp_expires_at
        self.email_verified = email_verified
        self.status = status
        self.type = user_type
        self.created_at = created_at or datetime.now()
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'otp': self.otp,
            'otp_expires_at': self.otp_expires_at.isoformat() if self.otp_expires_at else None,
            'email_verified': self.email_verified,
            'status': self.status,
            'type': self.type,
            'created_at': self.created_at.isoformat()
        }
    def to_public_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'email_verified': self.email_verified,
            'status': self.status,
            'type': self.type
        }
    @staticmethod
    def from_dict(data: dict):
        # Handle both string (SQLite) and datetime (PostgreSQL) formats
        def parse_datetime(value):
            if value is None:
                return None
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return datetime.fromisoformat(value)
            return None
        
        return User(
            email=data['email'],
            name=data.get('name'),
            user_id=data.get('id'),
            otp=data.get('otp'),
            otp_expires_at=parse_datetime(data.get('otp_expires_at')),
            email_verified=bool(data.get('email_verified', 0)),
            status=data.get('status', 'active'),
            user_type=data.get('type', 'user'),
            created_at=parse_datetime(data.get('created_at'))
        )