# from task_manager.domain import models
# from task_manager.domain.models import User
# from task_manager.domain.services.users_services import pwd_context
#
#
# class UserService:
#     async def create_user(
#             self,
#             user: User
#     ):
#         return models.User(
#             username=user.username,
#             hashed_password=pwd_context.hash(user.hashed_password),
#         )
