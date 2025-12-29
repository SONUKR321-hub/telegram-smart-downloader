#!/usr/bin/env python3
"""
tdl_downloader.py
A small Python wrapper around tdl.exe to download Telegram message links non-interactively.

Features:
- Locate `tdl.exe` (looks in env TDL_PATH, repo bin folder, or PATH)
- Accept single link(s) or a file with links (one per line)
- Run `tdl download` with common flags and report output
- Optional `--login` to trigger interactive login before download
- `--check` to verify tdl is callable and print version

Usage examples:
  python tdl_downloader.py --link "https://t.me/c/12345/678" --out downloads
  python tdl_downloader.py --file links.txt --out downloads --takeout
  python tdl_downloader.py --check

"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_tdl():
    # Check environment override
    env = os.environ.get('TDL_PATH')
    if env:
        p = Path(env)
        if p.exists():
            return str(p)

    # Check common repo bin location
    repo_bin = Path(__file__).resolve().parent / 'tdl' / 'bin' / 'tdl.exe'
    if repo_bin.exists():
        return str(repo_bin)

    # Check current folder's bin
    local_bin = Path.cwd() / 'bin' / 'tdl.exe'
    if local_bin.exists():
        return str(local_bin)

    # On PATH
    exe = shutil.which('tdl') or shutil.which('tdl.exe')
    if exe:
        return exe

    return None


def run(cmd, capture=False):
    try:
        if capture:
            res = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            return res.returncode, res.stdout
        else:
            res = subprocess.run(cmd, check=False)
            return res.returncode, None
    except Exception as e:
        return 1, str(e)


def main():
    p = argparse.ArgumentParser(description='Wrapper to run tdl downloads non-interactively')
    group = p.add_mutually_exclusive_group(required=False)
    group.add_argument('--link', '-u', action='append', help='Telegram message link (can be specified multiple times)')
    group.add_argument('--file', '-f', help='File with message links, one per line')
    p.add_argument('--out', '-d', default=str(Path.cwd() / 'downloads'), help='Output directory')
    p.add_argument('--group', action='store_true', help='Treat albums/groups')
    p.add_argument('--takeout', action='store_true', help='Use takeout mode')
    p.add_argument('--desc', action='store_true', help='Download newest first')
    p.add_argument('--login', action='store_true', help='Run interactive login before download')
    p.add_argument('--check', action='store_true', help='Check tdl availability and print version')
    p.add_argument('--tdl-path', help='Explicit path to tdl executable')

    args = p.parse_args()

    tdl = args.tdl_path or find_tdl()
    if not tdl:
        print('tdl executable not found. Set TDL_PATH or place tdl.exe in e.g. ./tdl/bin/tdl.exe or on PATH.', file=sys.stderr)
        sys.exit(2)

    # Normalize path
    tdl = str(Path(tdl).resolve())

    if args.check:
        code, out = run([tdl, 'version'], capture=True)
        if code == 0:
            print(out)
            sys.exit(0)
        else:
            print('Failed to run tdl:', out, file=sys.stderr)
            sys.exit(code)

    if args.login:
        # interactive login (will prompt user)
        print('Running interactive login...')
        rc, _ = run([tdl, 'login', '-T', 'code'])
        if rc != 0:
            print('Login failed or was cancelled.', file=sys.stderr)
            sys.exit(rc)

    links = []
    if args.link:
        links.extend(args.link)

    if args.file:
        fp = Path(args.file)
        if not fp.exists():
            print(f'Link file not found: {fp}', file=sys.stderr)
            sys.exit(2)
        with fp.open('r', encoding='utf-8') as fh:
            for line in fh:
                s = line.strip()
                if s:
                    links.append(s)

    if not links:
        print('No links provided. Use --link or --file.', file=sys.stderr)
        sys.exit(2)

    # Build tdl args
    base = [tdl, 'download']
    for l in links:
        base += ['-u', l]
    base += ['-d', args.out]
    if args.group:
        base += ['--group']
    if args.takeout:
        base += ['--takeout']
    if args.desc:
        base += ['--desc']

    print('Running tdl with:', ' '.join(base))

    rc, _ = run(base)
    if rc != 0:
        print('tdl download returned non-zero exit code:', rc, file=sys.stderr)
        sys.exit(rc)

    print('Download finished. Files saved to:', args.out)


if __name__ == '__main__':
    main()
