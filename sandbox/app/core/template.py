import reflex as rx
from functools import wraps

from .sidebar import sidebar
from .navbar import navbar
from .toc import table_of_content


def template(site_name: str, main_nav: list, sidebar_title: str, sidebar_items: dict, toc: list):
    """Create a base page template decorator."""
    def decorator(content):
        @wraps(content)
        def template():
            return rx.box(
                navbar(site_name, main_nav),
                rx.scroll_area(
                    rx.box(
                        sidebar(sidebar_title, sidebar_items),
                        rx.box(
                            content(),
                            class_name="flex w-full pt-8 lg:pr-16 min-h-screen",
                        ),
                        table_of_content(toc),
                        class_name="w-full max-w-[75rem] mx-auto h-full flex flex-row gap-x-0",
                    ),
                    class_name="px-4 xl:px-0 pt-12 h-screen w-full overflow-y-auto [&_.rt-ScrollAreaScrollbar]:mt-[4rem] [&_.rt-ScrollAreaScrollbar]:mb-[1rem]",
                ),
                bg=rx.color('slate', 2),
                class_name="w-full h-screen flex flex-col gap-y-0",
            )
        return template

    return decorator
