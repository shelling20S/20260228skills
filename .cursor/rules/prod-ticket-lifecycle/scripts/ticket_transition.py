#!/usr/bin/env python3
import argparse
import pathlib
import sys

from ticket_lib import (
    append_status_history,
    ensure_meta_defaults,
    now_jst,
    parse_frontmatter,
    quote_value,
    strip_quotes,
    write_frontmatter,
)


ALLOWED_TRANSITIONS = {
    "open": {"open", "in_progress"},
    "in_progress": {"in_progress", "implemented"},
    "implemented": {"implemented", "in_progress", "closed"},
    "closed": {"closed"},
}


def parse_args():
    p = argparse.ArgumentParser(description="Transition ticket status with guardrails")
    p.add_argument("ticket", help="ticket markdown file")
    p.add_argument("--to", required=True, choices=["open", "in_progress", "implemented", "closed"])
    p.add_argument("--note", default="")
    p.add_argument("--set-test-status", choices=["pending", "running", "passed", "failed", "blocked"])
    p.add_argument("--set-last-error", default="")
    p.add_argument("--set-test-evidence", default="")
    return p.parse_args()


def pick_archive_path(ticket_path: pathlib.Path) -> pathlib.Path:
    archive_dir = ticket_path.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    candidate = archive_dir / ticket_path.name
    if not candidate.exists():
        return candidate

    stem = ticket_path.stem
    suffix = ticket_path.suffix
    for i in range(1, 1000):
        candidate = archive_dir / f"{stem}_{i:03d}{suffix}"
        if not candidate.exists():
            return candidate

    raise RuntimeError(f"failed to choose archive path for {ticket_path.name}")


def main():
    args = parse_args()
    ticket_path = pathlib.Path(args.ticket)

    if not ticket_path.exists():
        print(f"ticket not found: {ticket_path}", file=sys.stderr)
        return 1

    meta, body = parse_frontmatter(ticket_path)
    ensure_meta_defaults(meta)

    current = meta.get("ticket_status", "open")
    target = args.to

    if current not in ALLOWED_TRANSITIONS:
        print(f"invalid current ticket_status: {current}", file=sys.stderr)
        return 1
    if target not in ALLOWED_TRANSITIONS[current]:
        print(f"disallowed transition: {current} -> {target}", file=sys.stderr)
        return 1

    if args.set_test_status:
        meta["test_status"] = args.set_test_status
    if args.set_last_error:
        meta["last_error"] = quote_value(args.set_last_error)
    if args.set_test_evidence:
        meta["test_evidence"] = quote_value(args.set_test_evidence)

    if target == "implemented" and not meta.get("test_status"):
        meta["test_status"] = "pending"

    if target == "closed":
        test_status = meta.get("test_status", "")
        evidence = strip_quotes(meta.get("test_evidence", ""))
        if test_status != "passed":
            print("close rejected: test_status must be passed", file=sys.stderr)
            return 1
        if not evidence:
            print("close rejected: test_evidence must be non-empty", file=sys.stderr)
            return 1

    now = now_jst()
    meta["ticket_status"] = target
    meta["status_updated_at"] = now
    if target in ("in_progress", "implemented", "closed") and "last_error" not in meta:
        meta["last_error"] = '""'

    note = args.note or "-"
    body = append_status_history(body, now, target, note)

    write_frontmatter(ticket_path, meta, body)
    if target == "closed":
        archive_path = pick_archive_path(ticket_path)
        ticket_path.rename(archive_path)
        print(f"{ticket_path}: {current} -> {target} (moved to {archive_path})")
        return 0

    print(f"{ticket_path}: {current} -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
