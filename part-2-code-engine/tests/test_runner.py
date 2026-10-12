"""P2a tests: multi-language sandboxed runner.

The FIRST test is C++ — the mandated first proof of the engine.
"""
import shutil

import pytest
from fastapi.testclient import TestClient

from app.adapters.runners import CodeRunnerServiceImpl
from app.domain.execution import ExecutionError, ExecutionRequest, Limits
from app.main import create_app

CPP_HELLO = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    cout << "hello from c++" << endl;
    return 0;
}
'''

client = TestClient(create_app())
svc = CodeRunnerServiceImpl()


def _run(**kw):
    kw.setdefault("limits", {})
    r = client.post("/v1/run", json=kw)
    assert r.status_code == 200, r.text
    return r.json()


# ---------- the mandated first proof: C++ ----------

def test_cpp_hello_world_runs_sandboxed():
    res = _run(language="cpp", code=CPP_HELLO)
    assert res["verdict"] == "OK", res
    assert res["stdout"].strip() == "hello from c++"
    assert res["exit_code"] == 0
    assert res["timed_out"] is False
    assert res["cpu_ms"] is not None and res["cpu_ms"] >= 0
    assert res["peak_ram_mb"] is not None and res["peak_ram_mb"] > 0


def test_cpp_stdin_echo():
    code = r'''#include <bits/stdc++.h>
using namespace std;
int main() { string s; cin >> s; cout << "echo:" << s; return 0; }
'''
    res = _run(language="cpp", code=code, stdin="skillforge")
    assert res["verdict"] == "OK"
    assert res["stdout"] == "echo:skillforge"


def test_cpp_compile_error():
    res = _run(language="cpp", code="int main( { oops }")
    assert res["verdict"] == "COMPILE_ERROR"
    assert "error" in res["stderr"].lower()


# ---------- other languages ----------

def test_c_hello_world():
    res = _run(language="c", code='#include <stdio.h>\nint main(){printf("c-ok\\n");return 0;}')
    assert res["verdict"] == "OK"
    assert res["stdout"].strip() == "c-ok"


def test_python_hello_world():
    res = _run(language="python", code='print("py-ok")')
    assert res["verdict"] == "OK"
    assert res["stdout"].strip() == "py-ok"


def test_python_stdin_and_runtime_error():
    res = _run(language="python", code="import sys\nprint(sys.stdin.read().strip())", stdin="in-data")
    assert res["verdict"] == "OK" and res["stdout"].strip() == "in-data"
    res = _run(language="python", code="raise ValueError('boom')")
    assert res["verdict"] == "RUNTIME_ERROR"
    assert "boom" in res["stderr"]


@pytest.mark.skipif(not shutil.which("javac"), reason="no JDK here")
def test_java_hello_world():
    res = _run(language="java",
               code='public class Main { public static void main(String[] a){ System.out.println("java-ok"); } }')
    assert res["verdict"] == "OK"
    assert res["stdout"].strip() == "java-ok"


# ---------- sandbox guarantees ----------

def test_no_network_inside_sandbox():
    code = ("import socket\n"
            "try:\n"
            "    socket.create_connection(('8.8.8.8', 53), timeout=3)\n"
            "    print('REACHABLE')\n"
            "except Exception as e:\n"
            "    print('BLOCKED:', type(e).__name__)")
    res = _run(language="python", code=code)
    assert "REACHABLE" not in res["stdout"], res
    assert "BLOCKED" in res["stdout"], res


def test_infinite_loop_is_killed_tle():
    res = _run(language="python", code="while True:\n    pass",
               limits={"wall_time_s": 2})
    assert res["verdict"] == "TLE"
    assert res["timed_out"] is True


def test_output_truncation():
    res = _run(language="python", code="print('x' * 200000)")
    assert res["truncated"] is True
    assert len(res["stdout"].encode()) == 64 * 1024


def test_memory_hog_is_contained():
    code = ('#include <bits/stdc++.h>\nusing namespace std;\n'
            'int main(){ vector<char> v; '
            'for(int i=0;i<100;i++) v.insert(v.end(), 10*1024*1024, 1); '
            'cout << v.size(); return 0; }')
    res = _run(language="cpp", code=code, limits={"memory_mb": 64})
    assert res["verdict"] in ("MLE", "RUNTIME_ERROR"), res  # contained, never hangs host


def test_fork_bomb_is_contained():
    res = _run(language="python",
               code="import os\nwhile True:\n    os.fork()",
               limits={"wall_time_s": 3})
    assert res["verdict"] in ("TLE", "RUNTIME_ERROR"), res


# ---------- contract validation ----------

def test_empty_code_rejected():
    r = client.post("/v1/run", json={"language": "python", "code": "   "})
    assert r.status_code == 400
    assert r.json()["error"] == "empty_code"


def test_unsupported_language_rejected():
    r = client.post("/v1/run", json={"language": "rust", "code": "fn main(){}"})
    assert r.status_code == 400
    assert r.json()["error"] == "unsupported_language"


def test_bad_limits_rejected():
    r = client.post("/v1/run", json={"language": "python", "code": "print(1)",
                                     "limits": {"wall_time_s": 999}})
    assert r.status_code == 400


def test_request_id_echoed():
    r = client.post("/v1/run", json={"language": "python", "code": "print(1)"},
                    headers={"X-Request-ID": "test-123"})
    assert r.headers["x-request-id"] == "test-123"


def test_languages_endpoint():
    r = client.get("/v1/languages")
    assert r.status_code == 200
    langs = {l["id"]: l for l in r.json()["languages"]}
    assert set(langs) == {"python", "c", "cpp", "java"}
    assert langs["cpp"]["available"] is True


# ---------- domain unit tests ----------

def test_domain_rejects_oversize_code():
    with pytest.raises(ExecutionError):
        ExecutionRequest(language="python", code="x" * (100 * 1024 + 1))


def test_domain_rejects_bad_limits():
    with pytest.raises(ExecutionError):
        Limits(wall_time_s=0)
    with pytest.raises(ExecutionError):
        Limits(memory_mb=32)


def test_service_direct_call():
    res = svc.run(ExecutionRequest(language="cpp", code=CPP_HELLO))
    assert res.verdict == "OK"
    assert res.stdout.strip() == "hello from c++"
