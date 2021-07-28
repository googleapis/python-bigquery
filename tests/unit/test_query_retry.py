from .helpers import make_connection

def test_rateLimitExceeded_in__begin(client):
    err = dict(reason='rateLimitExceeded')
    client._connection = conn = make_connection(
        dict(status=dict(status='DONE', errors=[err], errorResult=err)),
        dict(status=dict(status='DONE', errors=[err], errorResult=err)),
        dict(status=dict(status='DONE')),
        )
    breakpoint()
    client.query("select 1")
