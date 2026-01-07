import asyncio
import argparse
import socket
import json
import csv
from datetime import datetime
from typing import List, Dict

class PortScanner:
    def __init__(
        self,
        target: str,
        ports: str,
        max_concurrent: int,
        timeout: int,
        verbose: bool,
        output: str,
        output_format: str,
        open_only: bool
    ):
        self.target = target
        self.ports = self.parse_ports(ports)
        self.timeout = timeout
        self.verbose = verbose
        self.output = output
        self.output_format = output_format
        self.open_only = open_only

        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.results: List[Dict] = []

        self.ip, self.family = self.resolve_target(target)

    @staticmethod
    def parse_ports(port_range: str) -> List[int]:
        if "-" in port_range:
            start, end = port_range.split("-")
            return list(range(int(start), int(end) + 1))
        return [int(port_range)]

    @staticmethod
    def resolve_target(target: str):
        try:
            info = socket.getaddrinfo(target, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
            family = info[0][0]
            ip = info[0][4][0]
            return ip, family
        except socket.gaierror:
            raise RuntimeError(f"Unable to resolve target: {target}")

    async def scan_port(self, port: int):
        async with self.semaphore:
            status = "closed"
            try:
                conn = asyncio.open_connection(
                    host=self.ip,
                    port=port,
                    family=self.family
                )
                reader, writer = await asyncio.wait_for(conn, timeout=self.timeout)
                status = "open"
                writer.close()
                await writer.wait_closed()

            except asyncio.TimeoutError:
                status = "filtered"
            except ConnectionRefusedError:
                status = "closed"
            except Exception:
                status = "error"

            result = {
                "target": self.target,
                "ip": self.ip,
                "port": port,
                "protocol": "TCP",
                "status": status,
                "timestamp": datetime.utcnow().isoformat()
            }

            self.results.append(result)

            if not self.open_only or status == "open":
                print(f"[{status.upper():8}] Port {port}")

    async def run(self):
        tasks = [self.scan_port(port) for port in self.ports]
        await asyncio.gather(*tasks)

    def export_results(self):
        if not self.output:
            return

        if self.output_format == "json":
            with open(self.output, "w") as f:
                json.dump(self.results, f, indent=4)

        elif self.output_format == "csv":
            with open(self.output, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                writer.writeheader()
                writer.writerows(self.results)

        print(f"\nResults exported to {self.output}")

    def summary(self):
        open_ports = sum(1 for r in self.results if r["status"] == "open")
        filtered = sum(1 for r in self.results if r["status"] == "filtered")

        print("\nScan Summary")
        print("-" * 40)
        print(f"Target       : {self.target} ({self.ip})")
        print(f"Total Ports  : {len(self.results)}")
        print(f"Open Ports   : {open_ports}")
        print(f"Filtered     : {filtered}")
        print(f"Closed/Error : {len(self.results) - open_ports - filtered}")

    def start(self):
        print("=" * 50)
        print(" Asynchronous TCP Port Scanner")
        print("=" * 50)
        print(f"Target      : {self.target}")
        print(f"Resolved IP : {self.ip}")
        print(f"IP Version  : {'IPv6' if self.family == socket.AF_INET6 else 'IPv4'}")
        print(f"Ports       : {self.ports[0]} - {self.ports[-1]}")
        print(f"Timeout     : {self.timeout}s")
        print("-" * 50)


def main():
    parser = argparse.ArgumentParser(description="Asynchronous TCP Port Scanner")

    parser.add_argument("-i", "--dname", default="127.0.0.1", help="Domain or IP (IPv4 / IPv6)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port or range (e.g. 80 or 1-1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Max concurrent connections")
    parser.add_argument("-e", "--expiry_time", type=int, default=2, help="Timeout in seconds")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--open-only", action="store_true", help="Show only open ports")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")

    args = parser.parse_args()

    scanner = PortScanner(
        target=args.dname,
        ports=args.ports,
        max_concurrent=args.threads,
        timeout=args.expiry_time,
        verbose=args.verbose,
        output=args.output,
        output_format=args.format,
        open_only=args.open_only
    )

    scanner.start()

    try:
        asyncio.run(scanner.run())
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")

    scanner.summary()
    scanner.export_results()


if __name__ == "__main__":
    main()
