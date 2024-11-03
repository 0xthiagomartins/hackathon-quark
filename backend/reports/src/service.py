from nameko.rpc import rpc
from nameko.dependency_providers import DependencyProvider
from .business.generators import (
    ClientReportsGenerator,
    ActiveOperationsReportsGenerator,
    CurrentOperationsReportsGenerator,
)


class SessionDataDependency(DependencyProvider):

    def get_dependency(self, worker_ctx):
        try:
            session_data = worker_ctx.data["session_data"]
        except KeyError:
            session_data = None
        except AttributeError:
            session_data = None
        return session_data


class ReporterRPC:
    name = "report"
    session_data: dict = SessionDataDependency()

    @rpc
    def my_clients(self) -> str:
        return ClientReportsGenerator(self.session_data).generate()

    @rpc
    def active_operations(self) -> str:
        return ActiveOperationsReportsGenerator(self.session_data).generate()

    @rpc
    def current_operations(self) -> str:
        return CurrentOperationsReportsGenerator(self.session_data).generate()
