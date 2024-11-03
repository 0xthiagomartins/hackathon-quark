from .models import UserRole, User, Role, Permission, RolePermission
from sqlmodel_controller import Controller
from . import engine


ctrl_user_role = Controller[UserRole](engine=engine.get())
ctrl_user = Controller[User](engine=engine.get())
ctrl_role = Controller[Role](engine=engine.get())
ctrl_permission = Controller[Permission](engine=engine.get())
ctrl_role_permission = Controller[RolePermission](engine=engine.get())
