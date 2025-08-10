import argparse
import subprocess
import sys
import os
import shutil
import yaml
from pathlib import Path

def check_reflex_installed():
    return shutil.which("reflex") is not None

def run_reflex_init(target_dir=".", app_name=None):
    print(f"Running reflex init in '{target_dir}' with app name: {app_name}")

    os.makedirs(target_dir, exist_ok=True)
    cmd = ["reflex", "init"]
    if app_name:
        cmd += ["--name", app_name]

    try:
        subprocess.run(
            cmd,
            input=b"0\n",
            stdout=sys.stdout,
            stderr=sys.stderr,
            check=True,
            cwd=target_dir,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running reflex init: {e}")
        sys.exit(1)

def get_main_app_folder(target_dir, app_name=None):
    if app_name:
        return os.path.join(target_dir, app_name)
    else:
        return os.path.join(target_dir, os.path.basename(os.path.normpath(target_dir)))

def copy_file(src_path, dest_path):
    if not os.path.isfile(src_path):
        print(f"Warning: {os.path.basename(src_path)} not found at {src_path}. Skipping copy.")
        return
    try:
        shutil.copy2(src_path, dest_path)
        print(f"Copied {os.path.basename(src_path)} to {dest_path}")
    except Exception as e:
        print(f"Failed to copy {os.path.basename(src_path)}: {e}")

def copy_folder(src_folder, dest_folder):
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    try:
        shutil.copytree(src_folder, dest_folder)
        print(f"Copied folder {os.path.basename(src_folder)} to {dest_folder}")
    except Exception as e:
        print(f"Failed to copy folder {os.path.basename(src_folder)}: {e}")

def copy_config_file(target_dir, app_name=None):
    main_app_folder = get_main_app_folder(target_dir, app_name)
    src_config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    dest_config_path = os.path.join(main_app_folder, "config.yml")
    copy_file(src_config_path, dest_config_path)

def copy_export_file(target_dir, app_name=None):
    main_app_folder = get_main_app_folder(target_dir, app_name)
    src_export_path = os.path.join(os.path.dirname(__file__), "export.py")
    dest_export_path = os.path.join(main_app_folder, "export.py")
    copy_file(src_export_path, dest_export_path)

def copy_parser_file(target_dir, app_name=None):
    main_app_folder = get_main_app_folder(target_dir, app_name)
    src_parser_path = os.path.join(os.path.dirname(__file__), "parser.py")
    dest_parser_path = os.path.join(main_app_folder, "parser.py")
    copy_file(src_parser_path, dest_parser_path)

def copy_core_folder(target_dir, app_name=None):
    main_app_folder = get_main_app_folder(target_dir, app_name)
    src_core_folder = os.path.join(os.path.dirname(__file__), "core")
    dest_core_folder = os.path.join(main_app_folder, "core")
    copy_folder(src_core_folder, dest_core_folder)

def copy_state_folder(target_dir, app_name=None):
    main_app_folder = get_main_app_folder(target_dir, app_name)
    src_state_folder = os.path.join(os.path.dirname(__file__), "states")
    dest_state_folder = os.path.join(main_app_folder, "states")
    copy_folder(src_state_folder, dest_state_folder)

def create_pages_folder_with_index(target_dir, app_name=None):
    main_app_folder = get_main_app_folder(target_dir, app_name)
    pages_folder = os.path.join(main_app_folder, "pages")
    os.makedirs(pages_folder, exist_ok=True)

    index_md_path = os.path.join(pages_folder, "index.md")
    if not os.path.exists(index_md_path):
        with open(index_md_path, "w") as f:
            f.write("# Index")  # blank file
        print(f"Created blank index.md at {index_md_path}")
    else:
        print(f"index.md already exists at {index_md_path}, skipping creation.")

def overwrite_main_app_file(target_dir, app_name=None):
    main_app_folder = get_main_app_folder(target_dir, app_name)
    # The main app file is always named <app_folder_name>.py inside main_app_folder
    main_file_name = f"{os.path.basename(main_app_folder)}.py"
    main_file_path = os.path.join(main_app_folder, main_file_name)

    content = (
        "import reflex as rx\n"
        "from .export import export_app\n\n"
        "app = rx.App()\n"
        "export_app(app)\n"
    )

    try:
        with open(main_file_path, "w") as f:
            f.write(content)
        print(f"Overwritten main app file at {main_file_path}")
    except Exception as e:
        print(f"Failed to overwrite main app file: {e}")

def create_missing_indexes(target_dir, app_name=None):
    main_app_folder = Path(get_main_app_folder(target_dir, app_name))
    pages_folder = main_app_folder / "pages"
    config_path = main_app_folder / "config.yml"

    if not config_path.exists():
        print(f"config.yml not found at {config_path}, skipping index creation.")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    nav = config.get("nav", [])

    def traverse_nav(nav_list, base_parts=None):
        base_parts = base_parts or []

        for item in nav_list:
            if isinstance(item, dict):
                for title, val in item.items():
                    if isinstance(val, list):
                        # This nav item has children — check for index.md
                        folder_name = title.lower().replace(" ", "_")
                        folder_path = pages_folder.joinpath(*base_parts, folder_name)
                        index_file = folder_path / "index.md"
                        if not index_file.exists():
                            folder_path.mkdir(parents=True, exist_ok=True)
                            with open(index_file, "w", encoding="utf-8") as f:
                                f.write(f"# {title} Index\n")
                            print(f"Created missing index.md at {index_file.relative_to(main_app_folder)}")
                        # Recurse into children
                        traverse_nav(val, base_parts + [folder_name])
                    elif isinstance(val, str):
                        # single page — do nothing here
                        pass
            elif isinstance(item, str):
                # single page string, do nothing
                pass

    traverse_nav(nav)

def buridan_init(target_dir=".", app_name=None):
    if not check_reflex_installed():
        print(
            "Reflex is not installed. Please install it first:\n\n"
            "    pip install reflex\n"
        )
        sys.exit(1)

    print(f"Initializing Reflex project at '{target_dir}'...")
    run_reflex_init(target_dir, app_name)
    overwrite_main_app_file(target_dir, app_name)
    copy_config_file(target_dir, app_name)
    copy_export_file(target_dir, app_name)
    copy_parser_file(target_dir, app_name)
    copy_core_folder(target_dir, app_name)
    copy_state_folder(target_dir, app_name)
    create_pages_folder_with_index(target_dir, app_name)
    create_missing_indexes(target_dir, app_name)
    print("Initialization complete.")

def main():
    parser = argparse.ArgumentParser(prog="buridan-ssg")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize a new Reflex site")
    init_parser.add_argument(
        "target_dir", nargs="?", default=".", help="Target directory to initialize"
    )
    init_parser.add_argument(
        "--name",
        dest="app_name",
        default=None,
        help="Name of the Reflex app to create",
    )

    args = parser.parse_args()

    if args.command == "init":
        buridan_init(args.target_dir, args.app_name)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
