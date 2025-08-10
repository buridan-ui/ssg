import reflex as rx
import os


SIDEBAR_CLASSES = "hidden pt-24 lg:px-10 lg:flex flex-col items-center max-w-[300px] w-full gap-y-4 sticky top-0 left-0 [&_.rt-ScrollAreaScrollbar]:mr-[0.1875rem] [&_.rt-ScrollAreaScrollbar]:mt-[4rem] [&_.rt-ScrollAreaScrollbar]:mb-[1rem]"



def create_url_path(parent: str, child_file: str):
    """Convert parent & child file into /parent/child slug (without .md)."""
    child_slug = os.path.splitext(os.path.basename(child_file))[0]
    # If it's the index page, treat as root route
    if child_slug == "index":
        return "/"
    return f"/{parent}/{child_slug}".replace("//", "/")  # avoid double slashes

def sidebar(sidebar_title: str, sidebar_items: dict | str | None):
    """Render sidebar section with clickable links.

    Returns None if no sidebar items, so you can skip rendering.
    """
    # Only accept dict with items
    if not (isinstance(sidebar_items, dict) and sidebar_items):
        # No sidebar items, so no sidebar rendered at all
        return rx.scroll_area(
            height="100vh",
            class_name=SIDEBAR_CLASSES,
        )

    # Build links stacked vertically
    links = [
        rx.link(label.replace("-", " ").title(), href=create_url_path(sidebar_title, md_path), class_name="text-sm no-underline font-medium", color=rx.color('slate', 11), _hover={'color': rx.color('slate', 12)})
        for label, md_path in sidebar_items.items()
    ]

    return rx.scroll_area(
        rx.text(sidebar_title.replace("-", " ").title(), class_name="font-bold text-sm"),
        rx.box(*links, class_name="flex flex-col gap-y-2 pt-2"),
        height="100vh",
        class_name=SIDEBAR_CLASSES,
    )
