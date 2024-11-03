import base64
import pytest
from src.business.importer import Importer
from src.db.controllers import ctrl_client, ctrl_operation


@pytest.fixture
def admin_session_data():
    return {"roles": [{"name": "ADMIN"}, {"name": "USER"}]}


def encode_file(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def test_import_and_approve(admin_session_data):
    importer = Importer(session_data=admin_session_data)

    clientes_b64 = encode_file("./resources/CLIENTES.xlsx")
    operacoes_b64 = encode_file("./resources/OPERAÇÕES.xlsx")

    importer.import_clients(clientes_b64)
    importer.import_operations(operacoes_b64)

    importer.approve_clients()
    importer.approve_operations()

    clients = ctrl_client.list(filter={"approved": True})
    operations = ctrl_operation.list(filter={"approved": True})

    assert len(clients) > 0, "No clients were imported and approved."
    assert len(operations) > 0, "No operations were imported and approved."
