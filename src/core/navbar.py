import reflex as rx

ICON_BOX_STYLE = {
    "_hover": {"background": rx.color("gray", 3)},
    "border": f"0.81px solid {rx.color('gray', 5)}",
    "class_name": "flex flex-row cursor-pointer rounded-md flex items-center justify-center align-center py-1 px-1",
}

def create_theme_toggle():
    """Create theme toggle component."""
    return rx.box(
        rx.color_mode.icon(
            light_component=rx.icon("moon", size=13, color=rx.color("slate", 12)),
            dark_component=rx.icon("sun", size=13, color=rx.color("slate", 12)),
        ),
        title="Toggle theme",
        on_click=rx.toggle_color_mode,
        **ICON_BOX_STYLE,
    )


def drawer_sidebar():
    return rx.box(
        rx.drawer.root(
            rx.drawer.trigger(
                rx.el.button(
                    rx.icon(tag="square-menu", size=15),
                    class_name="cursor-pointer",

                )
            ),
            rx.drawer.overlay(z_index="999"),
            rx.drawer.portal(
                rx.drawer.content(
                    "asdasd",
                    class_name="h-[100%] top-auto right-auto w-full max-w-[300px]",
                    bg=rx.color('slate', 2),
                ),
                z_index="50",
            ),
            direction="left",
        ),
        class_name="flex lg:hidden"
    )


def navbar_site_name(site_name: str) -> rx.Component:
    return rx.text(site_name, class_name="text-md font-bold")

def navbar_links(nav_links: list) -> rx.Component:
    return rx.box(
        *[
            rx.link(
                item["title"].replace("-", " ").title(),
                href=item["url"],
                class_name="text-sm no-underline font-semibold",
                color=rx.color('slate', 12),
                _hover={'color': rx.color('slate', 12)})
            for item in nav_links
        ],
        class_name="hidden lg:flex flex-row gap-x-6 items-center"
    )

def navbar(site_name: str, main_nav: list):
    children = [drawer_sidebar(), navbar_site_name(site_name), navbar_links(main_nav)]
    return rx.box(
        rx.box(
            rx.box(*children, class_name="flex flex-row gap-x-6 items-center"),
            create_theme_toggle(),
            class_name="flex flex-row w-full max-w-[75rem] items-center justify-between px-4 xl:px-0"
        ),
        class_name="w-full flex flex-row h-12 items-center absolute justify-center z-[99]"
    )
