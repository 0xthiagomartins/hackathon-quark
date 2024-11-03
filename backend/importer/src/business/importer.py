import base64
import pandas as pd
from src.db.controllers import ctrl_operation, ctrl_client
from werkzeug.exceptions import Unauthorized
from .utils import read_excel_from_bytes


class Importer:
    def __init__(self, session_data):
        self.session_data = session_data

    def __b64_to_df(self, b64: str):
        return read_excel_from_bytes(base64.b64decode(b64))

    def __assert_admin(self):
        if "ADMIN" not in [role["name"] for role in self.session_data["roles"]]:
            raise Unauthorized("Não é permitido um não ADMIN confirmar operações")

    def save_operation(self, row):
        ctrl_operation.create(
            dict(
                liq_date=pd.to_datetime(row["Liquidação"]),
                quote_id=row["Id Cotacao"],
                client_id=row["Cliente"],
                structure=row["Estrutura"],
                asset=row["Ativo"],
                entry_price=row["Spot Entrada"],
                amount=row["Quantidade"],
                strike_percent=row["%Strike"],
                barrier_percent=row["%Barreira"],
                status=row["Status"],
            )
        )

    def approve_operations(self):
        self.__assert_admin()
        with ctrl_operation:
            operations = ctrl_operation.list(
                filter={"approved": False}, mode="all", value=False
            )
            for each in operations:
                ctrl_operation.update(
                    by="id", value=each["id"], data={"approved": True}
                )

    def approve_clients(self):
        self.__assert_admin()
        with ctrl_client:
            clients = ctrl_client.list(
                filter={"approved": False}, mode="all", value=False
            )
            for each in clients:
                ctrl_client.update(by="id", value=each["id"], data={"approved": True})

    def save_client(self, row):
        ctrl_client.create(
            dict(
                assessor_id=row["Assessor"],
                name=row["Cliente"],
                account=row["Conta do Cliente"],
                approved=False,
            )
        )

    def import_operations(self, b64_data: str):
        df = self.__b64_to_df(b64_data)
        with ctrl_operation:
            for _, row in df.iterrows():
                self.save_operation(row)

    def import_clients(self, b64_data: str):
        df = self.__b64_to_df(b64_data)
        with ctrl_client:
            for _, row in df.iterrows():
                self.save_client(row)
