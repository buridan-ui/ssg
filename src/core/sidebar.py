import reflex as rx
import os


SIDEBAR_CLASSES = "flex flex-col items-center gap-y-4 pt-8"


def create_url_path(parent: str, child_file: str):
    """Convert parent & child file into /parent/child slug (without .md)."""
    child_slug = os.path.splitext(os.path.basename(child_file))[0]

    # If it's the index page, treat as root route
    if child_slug == "index":
        return "/"

    # Avoid double slashes in path
    return f"/{parent}/{child_slug}".replace("//", "/")


def sidebar(sidebar_title: str, sidebar_items: dict | str | None):
    """Render sidebar section with clickable links.

    Args:
        sidebar_title: Title to display at top of sidebar
        sidebar_items: Dict of {label: md_path} for navigation links

    Returns:
        Sidebar component or empty scroll area if no items provided
    """

    # Return empty sidebar if no valid items provided
    if not (isinstance(sidebar_items, dict) and sidebar_items):
        return rx.box(
            class_name="hidden xl:flex w-full max-w-52 sticky top-0 max-h-[90vh]"
        )

    # Generate navigation links from sidebar items
    links = [
        rx.link(
            label.replace("-", " ").title(),
            href=create_url_path(sidebar_title, md_path),
            class_name="text-sm no-underline font-medium",
            color=rx.color('slate', 11),
            _hover={'color': rx.color('slate', 12)}
        )
        for label, md_path in sidebar_items.items()
    ]

    # Create scrollable sidebar content
    child = rx.scroll_area(
        rx.text(
            sidebar_title.replace("-", " ").title(),
            class_name="font-bold text-sm"
        ),
        rx.box(
            *links,
            class_name="flex flex-col gap-y-2 pt-2"
        ),
        class_name=SIDEBAR_CLASSES,
    )

    # Return sticky positioned sidebar container
    return rx.box(
        child,
        class_name="hidden xl:flex w-full max-w-52 sticky top-0 max-h-[90vh]"
    )
