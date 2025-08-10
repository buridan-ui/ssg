import reflex as rx


SIDEBAR_TOC_CLASSES = "flex flex-col items-center gap-y-4 pt-8"


def table_of_content(toc: list):
    """Render table of contents sidebar with hierarchical links."""

    # Generate TOC links with conditional indentation for level 2 items
    links = [
        rx.link(
            item["text"],
            href=f"#{item['text']}",
            class_name=(
                "text-sm no-underline font-medium" +
                (" pl-4" if item['level'] == 2 else "")
            ),
            color=rx.color('slate', 11),
            _hover={'color': rx.color('slate', 12)}
        )
        for item in toc
    ]

    # Create scrollable content area
    child = rx.scroll_area(
        rx.text(
            "Table of Contents",
            class_name="font-bold text-sm"
        ),
        rx.box(
            *links,
            class_name="flex flex-col gap-y-2 pt-2"
        ),
        class_name=SIDEBAR_TOC_CLASSES
    )

    # Return sticky positioned container
    return rx.box(
        child,
        class_name="hidden lg:flex w-full max-w-52 sticky top-0 max-h-[90vh]"
    )
