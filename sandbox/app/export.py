# src/export.py
import reflex as rx
import yaml
import re
from pathlib import Path
import importlib.util
import inspect
from typing import Dict, Callable
import logging
from .core.template import template
from .parser import DelimiterParser

logger = logging.getLogger(__name__)

def kebab_case(text: str) -> str:
    """Convert 'Getting Started' -> 'getting-started'."""
    text = text.strip()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^\w\-]", "", text)
    return text.lower()

def build_main_nav(nav_raw):
    """
    From the raw nav list, build a list of dicts with title and URL for top-level nav items.
    """
    main_nav = []

    for item in nav_raw:
        if isinstance(item, dict):
            for title, val in item.items():
                url_part = kebab_case(title)

                if isinstance(val, str):
                    if val == "index.md":
                        url = "/"
                    else:
                        url = f"/{url_part}/"
                elif isinstance(val, list):
                    url = f"/{url_part}/"
                else:
                    url = f"/{url_part}/"

                main_nav.append({"title": title, "url": url})

        elif isinstance(item, str):
            title = item.replace(".md", "")
            url_part = kebab_case(title)
            if item == "index.md":
                url = "/"
            else:
                url = f"/{url_part}/"
            main_nav.append({"title": title.capitalize(), "url": url})

    return main_nav

def clean_nav(nav_raw, exclude_files):
    nav_dict = {}

    for item in nav_raw:
        if isinstance(item, dict):
            for title, val in item.items():
                if isinstance(val, str):
                    if val in exclude_files:
                        continue
                    nav_dict[kebab_case(title)] = val
                elif isinstance(val, list):
                    sub_dict = clean_nav(val, exclude_files)
                    if sub_dict:
                        nav_dict[kebab_case(title)] = sub_dict
        elif isinstance(item, str):
            if item not in exclude_files:
                nav_dict[kebab_case(item)] = item

    return nav_dict

def flatten_nav(nav_list, base_parts=None):
    base_parts = base_parts or []
    paths = set()

    for item in nav_list:
        if isinstance(item, dict):
            for title, val in item.items():
                if isinstance(val, list):
                    folder_name = title.lower().replace(" ", "_")
                    paths |= flatten_nav(val, base_parts + [folder_name])
                elif isinstance(val, str):
                    paths.add("/".join(base_parts + [val]))
        elif isinstance(item, str):
            paths.add("/".join(base_parts + [item]))

    return paths

def load_components_from_blocks(blocks_path: Path) -> Dict[str, Callable]:
    registry = {}
    if not blocks_path.exists():
        return registry

    for py_file in blocks_path.glob("*.py"):
        module_name = py_file.stem
        spec = importlib.util.spec_from_file_location(module_name, py_file)
        if spec is None:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) or callable(obj):
                if not name.startswith("_"):
                    registry[name] = obj

    return registry

def ensure_blocks_folder_for_page(md_file: Path):
    blocks_folder = md_file.parent / "blocks"
    if not blocks_folder.exists():
        blocks_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"[export] Created blocks folder at {blocks_folder.relative_to(md_file.parents[1])}")
    return blocks_folder

def extract_toc(markdown_content):
    toc = []
    for match in re.finditer(r'^(#{1,2})\s+(.+)', markdown_content, re.MULTILINE):
        level = len(match.group(1))
        text = match.group(2).strip()
        anchor = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
        toc.append({"level": level, "text": text, "anchor": anchor})
    return toc

def export_app(app: rx.App):
    base_path = Path(__file__).parent
    config_path = base_path / "config.yml"

    if not config_path.exists():
        logger.error(f"[export] config.yml not found at {config_path}")
        return

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    site_name = config.get("site_name", "Untitled Site")
    logger.info(f"[export] Building site: {site_name}")

    nav = config.get("nav", [])
    exclude_files = set(config.get("exclude_from_nav", []))
    logger.info(f"[export] Navigation structure: {nav}")
    logger.info(f"[export] Excluding from nav: {exclude_files}")

    pages_dir = base_path / "pages"
    pages_dir.mkdir(exist_ok=True)

    def create_page(file_path_parts):
        target_path = pages_dir.joinpath(*file_path_parts)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if not target_path.exists():
            target_path.write_text(f"# {target_path.stem}\n", encoding="utf-8")
            logger.info(f"[export] Created page: {target_path.relative_to(base_path)}")

    def process_nav(nav_list, base_parts=None):
        base_parts = base_parts or []

        for item in nav_list:
            if isinstance(item, dict):
                for title, value in item.items():
                    if isinstance(value, list):
                        folder_name = title.lower().replace(" ", "_")
                        process_nav(value, base_parts + [folder_name])
                    elif isinstance(value, str):
                        create_page(base_parts + [value])
                    else:
                        logger.warning(f"[export] Unexpected nav value type {type(value)} for {title}")
            elif isinstance(item, str):
                create_page(base_parts + [item])
            else:
                logger.warning(f"[export] Unexpected nav item type {type(item)}: {item}")

    process_nav(nav)

    _clean_nav = clean_nav(nav, exclude_files)
    main_nav = build_main_nav(nav)

    # Collect all markdown files in pages_dir relative to pages_dir
    all_md_files = set(str(p.relative_to(pages_dir)).replace("\\", "/") for p in pages_dir.rglob("*.md"))
    # Collect all referenced files from nav config
    nav_md_files = flatten_nav(nav)
    # Orphan files = actual files - referenced in nav
    orphan_files = all_md_files - nav_md_files

    # Filter out index.md files inside nav folders from orphan_files
    filtered_orphans = set()
    for orphan in orphan_files:
        path_obj = Path(orphan)
        if path_obj.name == "index.md":
            parent_slug = path_obj.parent.name.replace("_", "-").lower()
            if parent_slug in _clean_nav:
                continue
        filtered_orphans.add(orphan)

    orphan_files = filtered_orphans

    if orphan_files:
        formatted_orphans = "\n  - " + "\n  - ".join(sorted(orphan_files))
        logger.warning(f"[export] Found orphan markdown files (not in nav):{formatted_orphans}")
    else:
        logger.info("[export] No orphan markdown files found.")

    for md_file in pages_dir.rglob("*.md"):
        ensure_blocks_folder_for_page(md_file)

        blocks_folder = md_file.parent / "blocks"
        components_registry = load_components_from_blocks(blocks_folder)

        parser = DelimiterParser(components_registry)
        content = md_file.read_text(encoding="utf-8")
        toc = extract_toc(content)
        parsed_components = parser.parse_and_render(content)

        rel_parts = md_file.with_suffix("").relative_to(pages_dir).parts
        first_part = rel_parts[0].replace("_", "-")

        if first_part in _clean_nav and _clean_nav[first_part]:
            sidebar_items = _clean_nav[first_part]
        else:
            sidebar_items = {}

        def make_page(parsed_components):
            @template(
                site_name=site_name,
                main_nav=main_nav,
                sidebar_title=md_file.with_suffix("").relative_to(pages_dir).parts[0].replace("_", "-"),
                sidebar_items=sidebar_items,
                toc=toc,
            )
            def page():
                return rx.box(*parsed_components)
            return page

        page = make_page(parsed_components)

        rel_path = md_file.with_suffix("").relative_to(pages_dir)
        if md_file.name == "index.md":
            if len(rel_path.parts) == 1:
                route = "/"
            else:
                route = "/" + "/".join(rel_path.parts[:-1]) + "/"
        else:
            route = "/" + "/".join(rel_path.parts)

        route = route.replace("\\", "/").replace("_", "-")

        app.add_page(page, route=route)

    logger.info("[export] Done building site!")
