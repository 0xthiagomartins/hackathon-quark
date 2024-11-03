from .models import Client, Operation
from sqlmodel_controller import Controller
from . import engine


ctrl_operation = Controller[Operation](engine=engine.get())
ctrl_client = Controller[Client](engine=engine.get())
