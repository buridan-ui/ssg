import reflex as rx

SIDEBAR_TOC_CLASSES = "flex flex-col max-w-[300px] w-full gap-y-2 align-start sticky top-0 left-0 [&_.rt-ScrollAreaScrollbar]:mr-[0.1875rem] [&_.rt-ScrollAreaScrollbar]:mt-[4rem] z-[10] [&_.rt-ScrollAreaScrollbar]:mb-[1rem]"

def table_of_content(toc: list):
    return rx.box(
        rx.text("Table of Contents", class_name="font-bold text-sm"),
        rx.box(
            *[
                rx.link(
                    item["text"],
                    href=f"#{item['text']}",
                    class_name="text-sm no-underline font-medium", color=rx.color('slate', 11), _hover={'color': rx.color('slate', 12)}
                )
                for item in toc
            ],
            class_name="flex flex-col gap-y-2 pt-2",
        ),
        height="100vh",
        class_name=f"hidden xl:flex {SIDEBAR_TOC_CLASSES} self-start pt-11 px-4",
    )
