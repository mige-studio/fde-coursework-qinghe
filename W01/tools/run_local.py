"""Load this practice copy's private model configuration and run a course tool."""
import os
import sys
from pathlib import Path
from urllib.request import getproxies

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"product.py", "verify_product.py", "finalize_evaluation.py", "eval"}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ALLOWED:
        raise SystemExit("Choose product.py, verify_product.py, finalize_evaluation.py or eval")
    config = ROOT / ".env"
    if not config.is_file():
        raise SystemExit("Local model configuration is missing")
    for line in config.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        name, sep, value = line.partition("=")
        if not sep or not name.startswith("FDE_"):
            raise SystemExit("Invalid local configuration entry")
        os.environ[name] = value
    # Preserve detected external proxies, but keep the local sample API local.
    proxies = getproxies()
    for scheme in ("http", "https"):
        if scheme in proxies:
            os.environ.setdefault(scheme + "_proxy", proxies[scheme])
    excluded = os.environ.get("no_proxy", os.environ.get("NO_PROXY", ""))
    os.environ["no_proxy"] = ",".join(filter(None, [excluded, "127.0.0.1", "localhost"]))
    if sys.argv[1] == "eval":
        os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
        os.environ["PROMPTFOO_DISABLE_TELEMETRY"] = "1"
        os.environ["PROMPTFOO_PYTHON"] = sys.executable
        os.chdir(ROOT / "evals")
        os.execvp("npx", ["npx", "--yes", "promptfoo@0.122.2", "eval", "--config", "promptfooconfig.yaml", "--no-cache", "--output", "../artifacts/w01/promptfoo-results.json"])
    os.chdir(ROOT)
    os.execv(sys.executable, [sys.executable, str(ROOT / "tools" / sys.argv[1]), *sys.argv[2:]])


if __name__ == "__main__":
    main()
