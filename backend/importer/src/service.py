from nameko.rpc import rpc
from nameko.dependency_providers import DependencyProvider
from .business.importer import Importer


class SessionDataDependency(DependencyProvider):

    def get_dependency(self, worker_ctx):
        try:
            session_data = worker_ctx.data["session_data"]
        except KeyError:
            session_data = None
        except AttributeError:
            session_data = None
        return session_data


class ImporterRPC:
    name = "importer"
    session_data: dict = SessionDataDependency()

    @rpc
    def import_operations(
        self,
        b64_file: str,
    ):
        return Importer(self.session_data).import_operations(b64_file)

    @rpc
    def approve_operations(self):
        Importer(self.session_data).approve_operations()

    @rpc
    def import_clients(
        self,
        b64_file: str,
    ):
        return Importer(self.session_data).import_clients(b64_file)

    @rpc
    def approve_clients(self):
        Importer(self.session_data).approve_clients()
