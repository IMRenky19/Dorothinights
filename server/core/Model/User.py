from sqlalchemy import Column, Integer, String, JSON, Null
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    pass

class Account(Base):
    
    __tablename__ = "account"
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    uid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    phone: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    secret: Mapped[str] = mapped_column(String(255))
    user: Mapped[str] = mapped_column(JSON)
    mails: Mapped[str] = mapped_column(JSON)
    assist_char_list: Mapped[str] = mapped_column(JSON)
    friend: Mapped[str] = mapped_column(JSON)
    ban: Mapped[int] = mapped_column(default=Null)
    notes: Mapped[str] = mapped_column(String(255))
    currentRogue: Mapped[str] = mapped_column(String(255))
    
    """def show_secret(self):
        print(self.user["status"])
        self.notes = "fk" """
        

#    def get_uid(self):
#        return self.uid
#
#    def set_uid(self, uid):
#        self.uid = uid
#
#    def get_phone(self):
#        return self.phone
#
#    def set_phone(self, phone):
#        self.phone = phone
#
#    def get_password(self):
#        return self.password
#
#    def set_password(self, password):
#        self.password = password
#
#    def get_secret(self):
#        return self.secret
#
#    def set_secret(self, secret):
#        self.secret = secret
#
#    def get_user(self):
#        return self.user
#
#    def set_user(self, user):
#        self.user = user
#
#    def get_mails(self):
#        return self.mails
#
#    def set_mails(self, mails):
#        self.mails = mails
#
#    def get_assist_char_list(self):
#        return self.assist_char_list
#
#    def set_assist_char_list(self, assist_char_list):
#        self.assist_char_list = assist_char_list
#
#    def get_friend(self):
#        return self.friend
#
#    def set_friend(self, friend):
#        self.friend = friend
#
#    def get_ban(self):
#        return self.ban
#
#    def set_ban(self, ban):
#        self.ban = ban
#
#    def get_notes(self):
#        return self.notes
#
#    def set_notes(self, notes):
#        self.notes = notes