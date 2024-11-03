import pytest
from unittest.mock import patch, MagicMock
from src.business.generators import (
    ClientReportsGenerator,
    ActiveOperationsReportsGenerator,
    CurrentOperationsReportsGenerator,
)

mock_clients = [
    {"id": 1, "name": "Client A", "account": "ACC123"},
    {"id": 2, "name": "Client B", "account": "ACC456"},
]

mock_operations = [
    {
        "id": 1,
        "liq_date": "2023-10-10",
        "quote_id": "Q123",
        "client_id": 1,
        "structure": "Structure A",
        "asset": "Asset A",
        "entry_price": 100.0,
        "amount": 10,
        "strike_percent": 5.0,
        "barrier_percent": 10.0,
        "status": "active",
        "approved": True,
    },
    {
        "id": 2,
        "liq_date": "2023-10-11",
        "quote_id": "Q124",
        "client_id": 2,
        "structure": "Structure B",
        "asset": "Asset B",
        "entry_price": 200.0,
        "amount": 20,
        "strike_percent": 10.0,
        "barrier_percent": 15.0,
        "status": "active",
        "approved": True,
    },
]


@pytest.fixture
def session_data_admin():
    return {"user_id": 1, "roles": ["ADMIN"]}


@pytest.fixture
def session_data_assessor():
    return {"user_id": 2, "roles": ["ASSESSOR"]}


@pytest.fixture
def session_data_trainee():
    return {"user_id": 3, "roles": ["TRAINEE"]}


@pytest.mark.parametrize(
    "generator_class",
    [
        ClientReportsGenerator,
        ActiveOperationsReportsGenerator,
        CurrentOperationsReportsGenerator,
    ],
)
@patch("src.business.generators.my_clients.ctrl_client")
@patch("src.business.generators.active_operations.ctrl_operation")
@patch("src.business.generators.current_operations.ctrl_operation")
def test_generate_methods(
    mock_ctrl_op_current,
    mock_ctrl_op_active,
    mock_ctrl_client,
    generator_class,
    session_data_admin,
):
    if generator_class == ClientReportsGenerator:
        mock_ctrl_client.list.return_value = mock_clients
    elif generator_class in [
        ActiveOperationsReportsGenerator,
        CurrentOperationsReportsGenerator,
    ]:
        mock_ctrl_op_active.list.return_value = mock_operations
        mock_ctrl_op_current.list.return_value = mock_operations

    generator = generator_class(session_data=session_data_admin)
    output = generator.generate()
    assert isinstance(output, str)


def test_generate_with_different_roles(
    session_data_admin, session_data_assessor, session_data_trainee
):
    generators = [
        ClientReportsGenerator(session_data_admin),
        ActiveOperationsReportsGenerator(session_data_admin),
        CurrentOperationsReportsGenerator(session_data_admin),
        ClientReportsGenerator(session_data_assessor),
        ActiveOperationsReportsGenerator(session_data_assessor),
        CurrentOperationsReportsGenerator(session_data_assessor),
        ClientReportsGenerator(session_data_trainee),
        ActiveOperationsReportsGenerator(session_data_trainee),
        CurrentOperationsReportsGenerator(session_data_trainee),
    ]

    with patch(
        "src.business.generators.my_clients.ctrl_client.list", return_value=mock_clients
    ), patch(
        "src.business.generators.active_operations.ctrl_operation.list",
        return_value=mock_operations,
    ), patch(
        "src.business.generators.current_operations.ctrl_operation.list",
        return_value=mock_operations,
    ):

        for generator in generators:
            output = generator.generate()
            assert isinstance(output, str)
