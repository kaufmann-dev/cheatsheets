#!/usr/bin/env python3
"""Render images with a tunable CMYK ordered-dither effect.

Requirements: Python 3.9+ and ImageMagick 7 (`magick`) on PATH.

Defaults reproduce the dark skull effect:
  CMYK -> 1%x1% contrast stretch -> h6x6a four-level screen -> sRGB
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


DEFAULT_SCREEN = "h6x6a"
DEFAULT_LEVELS = 4
DEFAULT_CONTRAST = "1%x1%"
DEFAULT_WORKING_COLORSPACE = "CMYK"
DEFAULT_OUTPUT_COLORSPACE = "sRGB"


class CliError(Exception):
    """Represent a user-facing CLI error."""

    def __init__(self, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class ArgumentParser(argparse.ArgumentParser):
    """Raise parse errors so JSON mode can preserve a stable error shape."""

    def error(self, message: str) -> None:
        raise CliError(message)


@dataclass(frozen=True)
class RenderSettings:
    screen: str
    levels: int
    contrast: str
    working_colorspace: str
    output_colorspace: str
    webp_lossless: bool
    webp_quality: int
    keep_metadata: bool


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 2:
        raise argparse.ArgumentTypeError("must be at least 2")
    return parsed


def webp_quality(value: str) -> int:
    parsed = int(value)
    if not 0 <= parsed <= 100:
        raise argparse.ArgumentTypeError("must be between 0 and 100")
    return parsed


def make_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="cmyk-screen",
        description=(
            "Render an image through a CMYK ordered-dither screen. Defaults "
            "match the dark, low-key skull effect."
        ),
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--version", action="version", version="cmyk-screen 1.0.0")

    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="check ImageMagick availability")
    doctor.add_argument(
        "--magick-bin",
        default="magick",
        help="ImageMagick executable to check (default: magick)",
    )

    render = subparsers.add_parser("render", help="apply the CMYK screen effect")
    render.add_argument("input", type=Path, help="source image path")
    render.add_argument("output", type=Path, help="destination image path")
    render.add_argument(
        "--screen",
        default=DEFAULT_SCREEN,
        help=f"ImageMagick threshold map (default: {DEFAULT_SCREEN})",
    )
    render.add_argument(
        "--levels",
        type=positive_int,
        default=DEFAULT_LEVELS,
        help=f"ordered-dither tonal levels (default: {DEFAULT_LEVELS})",
    )
    render.add_argument(
        "--contrast",
        default=DEFAULT_CONTRAST,
        help=(
            "ImageMagick contrast-stretch value "
            f"(default: {DEFAULT_CONTRAST.replace('%', '%%')})"
        ),
    )
    render.add_argument(
        "--working-colorspace",
        default=DEFAULT_WORKING_COLORSPACE,
        help=f"colorspace used for dithering (default: {DEFAULT_WORKING_COLORSPACE})",
    )
    render.add_argument(
        "--output-colorspace",
        default=DEFAULT_OUTPUT_COLORSPACE,
        help=f"output colorspace (default: {DEFAULT_OUTPUT_COLORSPACE})",
    )
    render.add_argument(
        "--lossless-webp",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="use lossless WebP output when the destination is .webp (default: enabled)",
    )
    render.add_argument(
        "--webp-quality",
        type=webp_quality,
        default=92,
        help="lossy WebP quality when --no-lossless-webp is used (default: 92)",
    )
    render.add_argument(
        "--keep-metadata",
        action="store_true",
        help="preserve input metadata instead of stripping it",
    )
    render.add_argument("--force", action="store_true", help="replace an existing output file")
    render.add_argument("--dry-run", action="store_true", help="print the ImageMagick command without running it")
    render.add_argument(
        "--magick-bin",
        default="magick",
        help="ImageMagick executable to run (default: magick)",
    )
    render.add_argument("--verbose", action="store_true", help="print the ImageMagick command")

    return parser


def resolve_binary(binary: str) -> str:
    resolved = shutil.which(binary)
    if not resolved:
        raise CliError(
            f"ImageMagick executable not found: {binary}. Install ImageMagick 7 or pass --magick-bin."
        )
    return resolved


def build_command(args: argparse.Namespace, binary: str) -> tuple[list[str], RenderSettings]:
    input_path = args.input.expanduser()
    output_path = args.output.expanduser()

    if not input_path.is_file():
        raise CliError(f"input image does not exist: {input_path}")
    if input_path.resolve() == output_path.resolve():
        raise CliError("input and output must be different paths")
    if not output_path.parent.is_dir():
        raise CliError(f"output directory does not exist: {output_path.parent}")
    if output_path.exists() and not args.force:
        raise CliError(f"output already exists: {output_path}. Pass --force to replace it.")

    settings = RenderSettings(
        screen=args.screen,
        levels=args.levels,
        contrast=args.contrast,
        working_colorspace=args.working_colorspace,
        output_colorspace=args.output_colorspace,
        webp_lossless=args.lossless_webp,
        webp_quality=args.webp_quality,
        keep_metadata=args.keep_metadata,
    )
    command = [
        binary,
        str(input_path),
        "-colorspace",
        settings.working_colorspace,
        "-contrast-stretch",
        settings.contrast,
        "-ordered-dither",
        f"{settings.screen},{settings.levels}",
        "-colorspace",
        settings.output_colorspace,
    ]
    if output_path.suffix.lower() == ".webp":
        if settings.webp_lossless:
            command.extend(["-define", "webp:lossless=true"])
        else:
            command.extend(["-quality", str(settings.webp_quality)])
    if not settings.keep_metadata:
        command.append("-strip")
    command.append(str(output_path))
    return command, settings


def run_doctor(args: argparse.Namespace) -> dict[str, object]:
    binary = resolve_binary(args.magick_bin)
    result = subprocess.run([binary, "-version"], capture_output=True, text=True, check=False)
    if result.returncode:
        message = result.stderr.strip() or "ImageMagick did not return a version."
        raise CliError(message, exit_code=result.returncode)
    version = result.stdout.splitlines()[0] if result.stdout else "unknown"
    return {
        "ok": True,
        "command": "doctor",
        "image_magick": {"available": True, "path": binary, "version": version},
        "defaults": asdict(
            RenderSettings(
                screen=DEFAULT_SCREEN,
                levels=DEFAULT_LEVELS,
                contrast=DEFAULT_CONTRAST,
                working_colorspace=DEFAULT_WORKING_COLORSPACE,
                output_colorspace=DEFAULT_OUTPUT_COLORSPACE,
                webp_lossless=True,
                webp_quality=92,
                keep_metadata=False,
            )
        ),
    }


def run_render(args: argparse.Namespace) -> dict[str, object]:
    binary = resolve_binary(args.magick_bin)
    command, settings = build_command(args, binary)
    payload: dict[str, object] = {
        "ok": True,
        "command": "render",
        "input": str(args.input.expanduser()),
        "output": str(args.output.expanduser()),
        "settings": asdict(settings),
        "magick_command": command,
        "dry_run": args.dry_run,
    }
    if args.verbose:
        print(" ".join(command), file=sys.stderr)
    if args.dry_run:
        return payload

    result = subprocess.run(command, capture_output=args.json, text=True, check=False)
    if result.returncode:
        message = result.stderr.strip() if args.json else "ImageMagick failed."
        raise CliError(message or "ImageMagick failed.", exit_code=result.returncode)
    return payload


def emit(payload: dict[str, object], json_mode: bool) -> None:
    if json_mode:
        print(json.dumps(payload, sort_keys=True))
        return
    if payload["command"] == "doctor":
        image_magick = payload["image_magick"]
        assert isinstance(image_magick, dict)
        print(f"ImageMagick: {image_magick['version']}")
        print(f"Path: {image_magick['path']}")
        return
    if payload["dry_run"]:
        print("Dry run:")
        print(" ".join(payload["magick_command"]))
        return
    print(f"Wrote {payload['output']}")


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    parser = make_parser()
    json_mode = "--json" in arguments
    try:
        args = parser.parse_args(arguments)
        payload = run_doctor(args) if args.command == "doctor" else run_render(args)
        emit(payload, args.json)
        return 0
    except CliError as error:
        if json_mode:
            print(json.dumps({"ok": False, "error": str(error), "exit_code": error.exit_code}, sort_keys=True))
        else:
            print(f"error: {error}", file=sys.stderr)
        return error.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
