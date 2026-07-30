#!/usr/bin/env python3
"""Capture traffic for one IPv4 host and write request observations to CSV.

This is a maintained replacement for the original state-file-based monitor.
It is intentionally an observation tool, not an intrusion detector.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import ipaddress
import sys
import time
from collections import deque
from pathlib import Path
from typing import Any, Deque, Iterator

import pyshark


CSV_FIELDS = (
    "timestamp_utc",
    "source_ip",
    "source_port",
    "destination_ip",
    "destination_port",
    "protocol",
    "http_method",
    "http_uri",
    "requests_last_60s",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Record packets involving one IPv4 host as CSV observations."
    )
    parser.add_argument("target_ip", type=ipaddress.IPv4Address)
    parser.add_argument("--interface", default="any")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("observations.csv"),
        help="CSV destination (default: observations.csv)",
    )
    parser.add_argument(
        "--request-threshold",
        type=int,
        default=7000,
        help="Warn when the trailing 60-second request count exceeds this value.",
    )
    parser.add_argument(
        "--packet-count",
        type=int,
        default=0,
        help="Stop after this many matching packets; 0 means run until interrupted.",
    )
    args = parser.parse_args()
    if args.request_threshold < 1:
        parser.error("--request-threshold must be at least 1")
    if args.packet_count < 0:
        parser.error("--packet-count cannot be negative")
    return args


def field(layer: Any, name: str) -> str:
    value = getattr(layer, name, "")
    return str(value) if value is not None else ""


def packets(capture: pyshark.LiveCapture, packet_count: int) -> Iterator[Any]:
    limit = packet_count if packet_count else None
    yield from capture.sniff_continuously(packet_count=limit)


def main() -> int:
    args = parse_args()
    target_ip = str(args.target_ip)
    request_times: Deque[float] = deque()
    capture = pyshark.LiveCapture(
        interface=args.interface,
        display_filter=f"ip.addr == {target_ip}",
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    print(
        f"Capturing traffic for {target_ip} on {args.interface}; "
        f"writing {args.output}. Press Ctrl+C to stop.",
        file=sys.stderr,
    )

    try:
        with args.output.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
            writer.writeheader()

            for packet in packets(capture, args.packet_count):
                if not hasattr(packet, "ip"):
                    continue

                now = time.time()
                http = getattr(packet, "http", None)
                method = field(http, "request_method") if http else ""
                uri = (
                    field(http, "request_full_uri")
                    or field(http, "request_uri")
                    if http
                    else ""
                )
                if method or uri:
                    request_times.append(now)
                while request_times and request_times[0] < now - 60:
                    request_times.popleft()

                transport_name = getattr(packet, "transport_layer", None)
                transport = (
                    packet[transport_name]
                    if transport_name and hasattr(packet, transport_name.lower())
                    else None
                )
                writer.writerow(
                    {
                        "timestamp_utc": dt.datetime.fromtimestamp(
                            now, tz=dt.timezone.utc
                        ).isoformat(),
                        "source_ip": field(packet.ip, "src"),
                        "source_port": field(transport, "srcport") if transport else "",
                        "destination_ip": field(packet.ip, "dst"),
                        "destination_port": (
                            field(transport, "dstport") if transport else ""
                        ),
                        "protocol": transport_name or "",
                        "http_method": method,
                        "http_uri": uri,
                        "requests_last_60s": len(request_times),
                    }
                )
                stream.flush()

                if len(request_times) > args.request_threshold:
                    print(
                        "Warning: request-rate threshold exceeded "
                        f"({len(request_times)} requests in trailing 60 seconds).",
                        file=sys.stderr,
                    )
    except KeyboardInterrupt:
        print("\nCapture stopped.", file=sys.stderr)
    finally:
        capture.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
