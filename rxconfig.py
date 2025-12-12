import reflex as rx

config = rx.Config(
    app_name="reflex_tree",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)