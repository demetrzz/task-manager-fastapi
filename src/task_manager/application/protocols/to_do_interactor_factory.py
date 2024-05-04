# from abc import ABC, abstractmethod
# from contextlib import asynccontextmanager
# from typing import AsyncContextManager
#
# from task_manager.application.to_do_create_user import CreateUser
#
#
# class InteractorFactory(ABC):
#     @abstractmethod
#     @asynccontextmanager
#     async def create_user(
#             self
#     ) -> AsyncContextManager[CreateUser]:
#         raise NotImplementedError
