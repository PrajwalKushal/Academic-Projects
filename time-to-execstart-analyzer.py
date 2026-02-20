#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone

from time_to_execstart_analyzer.ssh import SSHClient
from time_to_execstart_analyzer.systemd import collect_systemd_data


def main():
    parser = argparse.ArgumentParser(
        description="Analyze systemd service time-to-ExecStart over SSH"
    )
    parser.add_argument("hostname", help="Hostname or IP to connect to")
    parser.add_argument("key", help="Path to SSH private key")
    parser.add_argument(
        "--out-file",
        help="Path to store JSON output (prints to stdout if omitted)"
    )

    args = parser.parse_args()

    ssh = SSHClient(args.hostname, args.key)
    services = collect_systemd_data(ssh)

    output = {
        "metadata": {
            "hostname": args.hostname,
            "collected_at": datetime.now(timezone.utc).isoformat() ,
            "service_count": len(services),
        },
        "services": services,
    }

    if args.out_file:
        with open(args.out_file, "w") as f:
            json.dump(output, f, indent=2)
    else:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

