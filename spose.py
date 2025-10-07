#!/usr/bin/env python3

import sys
import argparse
import urllib.request
import socket
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from url_request import URLRequest  # Ensure this is in the same directory

init(autoreset=True)

class Spose:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Squid Proxy Port Scanner with Threading and Banner Grabbing'
        )
        parser.add_argument("--proxy", help="Proxy address (e.g. http://127.0.0.1:3128)",
                            required=True)
        parser.add_argument("--target", help="Target IP behind the proxy",
                            required=True)
        parser.add_argument("--ports", help="Comma-separated ports to scan (default: top ports)")
        parser.add_argument("--allports", help="Scan all 65535 ports",
                            action="store_true")
        parser.add_argument("--threads", help="Concurrent threads (default: 50)",
                            type=int, default=50)

        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)

        args = parser.parse_args()

        self.target = args.target
        self.proxy = args.proxy
        self.threads = args.threads

        if args.allports:
            self.ports = range(1, 65536)
            print(f"{Fore.YELLOW}Scanning all 65,535 ports...{Style.RESET_ALL}")
        elif args.ports:
            self.ports = [int(p.strip()) for p in args.ports.split(',')]
            print(f"{Fore.YELLOW}Scanning specified ports: {args.ports}{Style.RESET_ALL}")
        else:
            self.ports = [21, 22, 23, 25, 53, 69, 80, 110, 143, 443,
                          993, 995, 3306, 3389, 8080, 8443, 10000]
            print(f"{Fore.YELLOW}Scanning default common ports...{Style.RESET_ALL}")

        print(f"{Fore.CYAN}Using proxy: {self.proxy}{Style.RESET_ALL}")
        self.scan_ports()

    def scan_ports(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.check_port, port) for port in self.ports]
            for future in as_completed(futures):
                future.result()

    def check_port(self, port):
        try:
            banner = self.grab_banner(port)
            if banner:
                print(f"{Fore.GREEN}[OPEN] {self.target}:{port}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA} └─ Banner: {banner.strip()}{Style.RESET_ALL}")
        except Exception as e:
            # Optional: uncomment to debug individual failures
            # print(f"[DEBUG] Port {port} error: {e}")
            pass

    def grab_banner(self, port):
        try:
            parsed = urlparse(self.proxy)
            proxy_host = parsed.hostname
            proxy_port = parsed.port

            with socket.create_connection((proxy_host, proxy_port), timeout=5) as proxy_sock:
                # Step 1: CONNECT
                connect_payload = f"CONNECT {self.target}:{port} HTTP/1.1\r\nHost: {self.target}:{port}\r\n\r\n"
                proxy_sock.sendall(connect_payload.encode())
                response = proxy_sock.recv(4096)

                if b"200 Connection established" not in response:
                    return None  # Proxy failed to connect

                # Step 2: Send a probe (default = HTTP HEAD)
                proxy_sock.settimeout(3)
                probe = b"HEAD / HTTP/1.1\r\nHost: %b\r\nConnection: close\r\n\r\n" % self.target.encode()
                proxy_sock.sendall(probe)

                banner = proxy_sock.recv(4096)
                if banner:
                    return banner.decode(errors='ignore').split('\r\n')[0]
        except Exception:
            return None


if __name__ == "__main__":
    Spose()
