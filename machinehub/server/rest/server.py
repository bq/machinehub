import bottle
from machinehub.server.rest.api_v1 import ApiV1


class MachinehubServer(object):
    """
        Server class. Instances api_v1 application and run it.
        Receives the store.

    """
    store = None
    root_app = None

    def __init__(self, run_port, ssl_enabled, credentials_manager,
                 updown_auth_manager, authorizer, authenticator,
                 file_manager, server_version):

        self.api_v1 = ApiV1(credentials_manager, updown_auth_manager, ssl_enabled, server_version)

        self.root_app = bottle.Bottle()
        self.root_app.mount("/v1/", self.api_v1)
        self.run_port = run_port

        self.api_v1.authorizer = authorizer
        self.api_v1.authenticator = authenticator
        self.api_v1.file_manager = file_manager
        self.api_v1.setup()

    def run(self, **kwargs):
        port = kwargs.pop("port", self.run_port)
        debug_set = kwargs.pop("debug", False)
        host = kwargs.pop("host", "localhost")
        bottle.Bottle.run(self.root_app, host=host,
                          port=port, debug=debug_set, reloader=False)
