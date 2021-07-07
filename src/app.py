from .utils import *
from .config import config
from h2o_wave import Q, ui, app, main, data, on, handle_on, site


def init(q: Q):
    q.page["meta"] = ui.meta_card(
        title="Audiophy",
        box="",
        layouts=[
            ui.layout(
                breakpoint="xs",
                zones=[
                    ui.zone("header", size="80px"),
                    ui.zone("sidebar", size="350px"),
                    ui.zone("description", size="100px"),
                    ui.zone("audio", size="200px"),
                    ui.zone("summary", size="200px"),
                ],
            ),
            ui.layout(
                breakpoint="m",
                zones=[
                    ui.zone("header", size="80px"),
                    ui.zone(
                        "body",
                        size="800px",
                        direction=ui.ZoneDirection.ROW,
                        zones=[
                            ui.zone("sidebar", size="300px"),
                            ui.zone(
                                "right-pane",
                                direction=ui.ZoneDirection.COLUMN,
                                zones=[
                                    ui.zone("description", size="200px"),
                                    ui.zone("audio", size="300px"),
                                    ui.zone("summary", size="300px"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ui.layout(
                breakpoint="xl",
                width="1600px",
                zones=[
                    ui.zone("header", size="80px"),
                    ui.zone(
                        "body",
                        size="800px",
                        direction=ui.ZoneDirection.ROW,
                        zones=[
                            ui.zone("sidebar", size="300px"),
                            ui.zone(
                                "right-pane",
                                direction=ui.ZoneDirection.COLUMN,
                                zones=[
                                    ui.zone("description", size="200px"),
                                    ui.zone("audio", size="300px"),
                                    ui.zone("summary", size="300px"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    q.page.add(
        "header",
        ui.header_card(
            box="header",
            title=config.title,
            subtitle=config.subtitle,
            icon=config.icon,
            icon_color=config.icon_color,
        ),
    )

    q.page["description"] = ui.form_card(box="description", items=[])
    q.page["audio"] = ui.form_card(box="audio", items=[])
    q.page["summary"] = ui.form_card(box="summary", items=[])
    q.page["sidebar"] = ui.form_card(
        box="sidebar",
        items=[
            ui.textbox(
                name="url",
                label="Enter URL",
                tooltip="Required",
                visible=True,
                icon="Search",
                required=True,
                value="https://pandeyparul.medium.com/h2o-ai-hybrid-cloud-democratizing-ai-for-every-person-and-every-organization-8ebe770f15e8",
            ),
            ui.combobox(
                name="accent",
                # value="English (United States)",
                placeholder="Select",
                label="Local Accents",
                choices=[
                    "English (Australia)",
                    "English (United Kingdom)",
                    "English (United States)",
                    "English (Canada)",
                    "English (India)",
                    "English (Ireland)",
                    "English (South Africa)",
                    "French (Canada)",
                    "French (France)",
                    "Mandarin (China Mainland)",
                    "Mandarin (Taiwan)",
                    "Portuguese (Brazil)",
                    "Portuguese (Portugal)",
                    "Spanish (Mexico)",
                    "Spanish (Spain)",
                ],
            ),
            ui.buttons(
                [
                    ui.button(
                        name="convert",
                        label="Convert",
                        primary=True,
                        icon="PasteAsCode",
                    ),
                    ui.button(
                        name="refresh",
                        label="Refresh",
                        primary=True,
                        icon="EraseTool",
                    ),
                ]
            ),
            ui.toggle(name="theme", label="Dark Theme", trigger=True),
            ui.progress(
                "Be patient!This will take some time",
                visible=False,
            ),
        ],
    )


async def convert(q: Q):
    if not q.args.accent:
        q.args.accent = "English (United States)"

    q.page["sidebar"].items[4].progress.visible = True
    await q.page.save()
    article = MediumArticle(q.args.url)
    q.page["description"] = ui.form_card(
        box="description",
        items=[
            ui.text_m("<b>Title</b> : " + article.title),
            ui.text_m("<b>Author</b> : " + article.author),
        ],
    )
    audio_path = article.get_audio(
        languages_dict.get(q.args.accent)[0], languages_dict.get(q.args.accent)[1]
    )
    path_mp3, *_ = await q.site.upload([audio_path])
    q.page["audio"] = ui.form_card(
        box="audio",
        items=[
            ui.text_l("<b>Audio</b>"),
            ui.text(
                content=f"""<audio controls><source src="{path_mp3}" type="audio/mp3"></audio>"""
            ),
            ui.link(
                label="Link to download audio file",
                path=path_mp3,
                download=True,
                button=False,
            ),
        ],
    )

    q.page["summary"] = ui.form_card(
        box="summary",
        items=[ui.text_l("<b>Summary</b>"), ui.text_m(content=article.get_summary())],
    )

    q.page["sidebar"].items[4].progress.visible = False
    await q.page.save()


@app("/")
async def serve(q: Q):
    if not q.client.initialized:
        init(q)
        q.client.initialized = True

    if q.args.convert:
        await convert(q)
    elif q.args.refresh:
        init(q)

    dark_theme = q.args.theme
    if dark_theme is not None:
        if dark_theme:
            q.page["meta"].theme = "neon"

        else:
            q.page["meta"].theme = "default"

        q.page["sidebar"].items[3].toggle.value = dark_theme

    await q.page.save()
