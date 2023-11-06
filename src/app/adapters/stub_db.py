from app.application.schemas import User
from app.application.protocols.database import DatabaseGateway


class StubDatabaseGateway(DatabaseGateway):
    def add_one(self, user: User) -> None:
        pass
