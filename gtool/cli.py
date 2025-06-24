import os
import sys
import argparse
import subprocess
from datetime import datetime

def run_command(command, **kwargs):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, **kwargs)
        if result.stdout:
            print(result.stdout.strip())
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {' '.join(command)}", file=sys.stderr)
        if e.stderr:
            print(e.stderr.strip(), file=sys.stderr)
        if e.stdout:
            print(e.stdout.strip(), file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        sys.exit(1)

def handle_acp():
    commit_message = sys.argv[1] if len(sys.argv) > 1 else None
    current_branch = run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    print(f"✅ On branch: {current_branch}")
    print("-> Staging all changes...")
    run_command(['git', 'add', '.'])
    if not commit_message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto-commit: {timestamp}"
        print(f"ℹ No commit message provided. Using default: '{commit_message}'")
    print(f"-> Committing with message: '{commit_message}'")
    run_command(['git', 'commit', '-m', commit_message])
    print(f"-> Pushing to origin/{current_branch}...")
    run_command(['git', 'push', '-u', 'origin', current_branch])
    print("\n✅ ACP process completed successfully!")

def handle_gnew():
    """
    Handles creating a new repo, and pushing it to a remote.
    """
    if len(sys.argv) < 3:
        print("Usage: gnew <directory> <remote_url>", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]
    remote_url = sys.argv[2]
    setup_uv = sys.argv[3]

    try:
        print(f"-> Creating directory '{directory}'...")
        os.makedirs(directory)

        readme_path = os.path.join(directory, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {directory}\n")
        print("-> Created initial README.md")

        cwd = directory

        print("-> Initializing Git repository...")
        run_command(['git', 'init'], cwd=cwd)

        if setup_uv == "use_uv":
            print("-> Setting up UV virtual environment...")
            try:
                run_command(["uv", "init"])
                run_command(["uv", "venv"])
                run_command(["source", ".venv/bin/activate"], cwd=cwd)
            except subprocess.CalledProcessError as e:
                print("Error setting up UV virtual environment. Ensure UV is installed and configured correctly.", file=sys.stderr)

        print("-> Staging changes...")
        run_command(['git', 'add', '.'], cwd=cwd)

        commit_message = "Initial commit"
        print(f"-> Committing with message: '{commit_message}'...")
        run_command(['git', 'commit', '-m', commit_message], cwd=cwd)

        print("-> Renaming branch to 'main'...")
        run_command(['git', 'branch', '-M', 'main'], cwd=cwd)

        print(f"-> Adding remote origin: {remote_url}...")
        run_command(['git', 'remote', 'add', 'origin', remote_url], cwd=cwd)

        print("-> Pushing to origin/main...")
        run_command(['git', 'push', '-u', 'origin', 'main'], cwd=cwd)

        print(f"\n✅ New repository '{directory}' created and pushed successfully!")

    except FileExistsError:
        print(f"Error: Directory '{directory}' already exists.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="A command line tool to make using Git easier.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    parser_acp = subparsers.add_parser('acp', help='Add, Commit, and Push in one go.')
    parser_acp.add_argument('message', nargs='?', default=None, help='The commit message.')

    parser_gnew = subparsers.add_parser('gnew', help='Create a new local and remote repository.')
    parser_gnew.add_argument('directory', help='The name of the new project directory.')
    parser_gnew.add_argument('remote_url', help='The full URL of the remote Git repository.')
    parser_gnew.add_argument("setup_uv", nargs='?', default=None, help="To set up a virtual environment with UV, use 'use_uv'.")
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    if args.command == 'acp':
        sys.argv = ['acp'] + ([args.message] if args.message else [])
        handle_acp()
    elif args.command == 'new':
        sys.argv = ['gnew', args.directory, args.remote_url, args.setup_uv]
        handle_gnew()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()