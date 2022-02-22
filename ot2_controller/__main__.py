import logging
from argparse import ArgumentParser
from typing import Optional
from uuid import UUID

from .server import Server

logger = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser(prog="ot2-controller", description="Start this SiLA 2 server")

    parser.add_argument("-o", "--ot2-ip-address", required=True, help="The IP address of the Opentrons OT-2 system")

    parser.add_argument("-a", "--ip-address", default="127.0.0.1", help="The IP address (default: '127.0.0.1')")
    parser.add_argument("-p", "--port", type=int, default=50064, help="The port (default: 50064)")
    parser.add_argument("--server-uuid", type=UUID, default=None, help="The server UUID (default: create random UUID)")
    parser.add_argument("--disable-discovery", action="store_true", help="Disable SiLA Server Discovery")

    parser.add_argument("--insecure", action="store_true", help="Start without encryption")
    parser.add_argument("-k", "--private-key-file", default=None, help="Private key file (e.g. 'server-key.pem')")
    parser.add_argument("-c", "--cert-file", default=None, help="Certificate file (e.g. 'server-cert.pem')")
    parser.add_argument(
        "--ca-export-file",
        default=None,
        help="When using a self-signed certificate, write the generated CA to this file",
    )

    log_level_group = parser.add_mutually_exclusive_group()
    log_level_group.add_argument("-q", "--quiet", action="store_true", help="Only log errors")
    log_level_group.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    log_level_group.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")

    return parser.parse_args()


def run_server(args):
    # prepare args
    ot2_ip_address: str = args.ot2_ip_address
    insecure: bool = args.insecure
    cert: Optional[bytes] = open(args.cert_file, "rb").read() if args.cert_file is not None else None
    private_key: Optional[bytes] = (
        open(args.private_key_file, "rb").read() if args.private_key_file is not None else None
    )
    ca_export_file: Optional[str] = args.ca_export_file
    address: str = args.ip_address
    port: int = args.port
    enable_discovery: bool = not args.disable_discovery
    server_uuid: Optional[UUID] = args.server_uuid

    if (insecure or ca_export_file is not None) and (cert is not None or private_key is not None):
        raise ValueError("Cannot use --insecure or --ca-export-file with --private-key-file or --cert-file")
    if sum(par is None for par in (cert, private_key)) not in (0, 2):
        raise ValueError("Either provide both --private-key-file and --cert-file, or none of them")
    if insecure and ca_export_file is not None:
        raise ValueError("Cannot use --export-ca-file with --insecure")

    # run server
    server = Server(ot2_ip_address=ot2_ip_address, server_uuid=server_uuid)
    try:
        if insecure:
            server.start_insecure(address, port, enable_discovery=enable_discovery)
        else:
            server.start(address, port, cert_chain=cert, private_key=private_key, enable_discovery=enable_discovery)
            if ca_export_file is not None:
                with open(ca_export_file, "wb") as fp:
                    fp.write(server.generated_ca)
                print(f"Wrote generated CA to '{ca_export_file}'")
        print("Server startup complete, press Enter to stop")

        try:
            input()
        except KeyboardInterrupt:
            pass
    finally:
        server.stop()
        print("Stopped server")


def setup_basic_logging(args):
    level = logging.WARNING
    if args.verbose:
        level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    if args.quiet:
        level = logging.ERROR

    logging.basicConfig(level=level, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")


if __name__ == "__main__":
    args = parse_args()
    setup_basic_logging(args)
    run_server(args)
