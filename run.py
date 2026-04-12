import argparse
import pathlib
import os
import subprocess

def parse_args(parser = argparse.ArgumentParser()):
    parser.add_argument("-p", "--project", required=True)
    parser.add_argument("-a", "--action", required=True, choices=["export", "image"])
    return parser.parse_args()

def run_cmd(cmd, show=True):
    if show:
        print(f"Running '{cmd}'")
    os.system(cmd)

def action_export(path):
    r_path = (path / "export")
    w_path = (path / "STLs")
    w_path.mkdir(exist_ok=True)
    for file in r_path.iterdir():
        run_cmd(f"openscad -o {str(w_path / file.stem) + '.stl'} --export-format binstl {r_path / file.name}")

def action_image(path):
    w_path = (path / "media")
    w_path.mkdir(exist_ok=True)
    for file in path.iterdir():
        if file.is_dir():
            continue
        print(f"Checking {file} ({file.name})")
        if file.name.startswith("demo") and file.name.endswith(".scad"):
            run_cmd(f"openscad -o {w_path / f'{file.stem}.png'} --colorscheme Starnight {path / file.name}")

def main():
    parser = argparse.ArgumentParser()
    args = parse_args(parser)
    ROOT = subprocess.getoutput("git rev-parse --show-toplevel")
    if "fatal:" in ROOT:
        ROOT = pathlib.Path(__file__).parent.parent
    else:
        ROOT = pathlib.Path(ROOT)

    projects = args.project.split(",")
    for prj in projects:
        path = (ROOT / prj)
        print(f"Starting {args.action} on {path}")
        if args.action == "export":
            action_export(path)
        elif args.action == "image":
            action_image(path)


if __name__ == "__main__":
    main()
