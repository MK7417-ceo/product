# Dedicated Sandbox Security Runner

## Why this runner exists

The normal GitHub-hosted CI runner does not grant the network-namespace capability required by the current fail-closed sandbox. As a result, the normal Code Engine job currently reports **21 passed, 14 skipped**. Those skips are not security passes.

This workflow provides a separate, manually dispatched integration job that must run on a dedicated disposable Linux VM with network namespace support. The test module checks `SKILLFORGE_REQUIRE_SANDBOX_TESTS=1` at collection time and fails immediately if the capability is absent; it cannot silently turn the security suite into skips.

## Runner provisioning requirements

1. Create a disposable Linux VM dedicated only to sandbox security tests.
2. Register a GitHub Actions self-hosted runner with labels `linux` and `sandbox-security`.
3. Do not attach production credentials, deployment secrets, SSH keys, cloud metadata permissions, or access to internal networks.
4. Ensure the runner account can successfully execute `unshare -n true`. Do not weaken the sandbox implementation to bypass this requirement.
5. Keep the VM isolated from production networks and destroy/rebuild it regularly.
6. Install Docker only if needed for VM lifecycle management; the current test job itself uses gcc, g++, a JDK and Python.

## Run

GitHub → Actions → **Sandbox Security Integration** → Run workflow.

The workflow runs the complete Code Engine test suite with strict mode enabled. It must report **zero skipped sandbox integration tests**. A green workflow is evidence for the tested runner image and commit only; it is not a substitute for a separate review of filesystem isolation, process-tree containment, seccomp, cgroups and the production execution boundary.

## Current security limitations (do not waive)

The current in-process sandbox uses a network namespace and rlimits, but does not yet provide a dedicated mount/filesystem namespace, seccomp policy, cgroup-based process-tree resource accounting, or a proven container/microVM boundary. The Python service also forks from a multithreaded server process (pytest currently emits the corresponding warning). Therefore:

- Do not expose public untrusted code execution in production.
- Do not describe the current sandbox as production-grade or security-certified.
- Prefer a dedicated execution worker using a maintained isolation runtime such as gVisor or Firecracker, with no shared host or credentials.
- Keep execution fail-closed until the runtime and adversarial tests are independently validated.
