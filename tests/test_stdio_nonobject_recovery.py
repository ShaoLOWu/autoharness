import io
import json

from autoharness.stage_skill import server


def test_nonobject_json_requests_return_error_and_continue_serving():
    output = io.StringIO()
    server.serve(io.StringIO('{broken\n42\n[]\nnull\n' + json.dumps({'jsonrpc': '2.0', 'id': 7, 'method': 'tools/list'}) + '\n'), output)
    replies = [json.loads(line) for line in output.getvalue().splitlines()]
    assert [r['error']['code'] for r in replies[:4]] == [-32700, -32600, -32600, -32600]
    assert all(r['id'] is None for r in replies[:4])
    assert replies[4]['id'] == 7 and replies[4]['result']['tools']
