import reflex as rx



def drawer_sidebar():
    return rx.drawer.root(
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
    )


def navbar(site_name: str, main_nav: list):
    return rx.box(
        rx.box(
            rx.box(drawer_sidebar(), class_name="flex lg:hidden"),
            rx.text(site_name, class_name="text-md font-bold"),
            rx.box(
                *[
                    rx.link(item["title"].replace("-", " ").title(), href=item["url"], class_name="text-sm no-underline font-semibold", color=rx.color('slate', 12), _hover={'color': rx.color('slate', 12)})
                    for item in main_nav
                ],
            class_name="hidden lg:flex flex-row gap-x-6 items-center"
            ),
            class_name="flex flex-row gap-x-6 items-center"
        ),
        rx.color_mode.button(),
        # background=rx.color('indigo'),
        class_name="flex flex-row w-full h-12 items-center justify-between lg:px-10 px-4 gap-x-6 fixed top-0 left-0 z-[99]"
    )
