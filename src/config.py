class Configuration:
    """
    App Configurations
    """

    def __init__(self):
        self.title = "Audiofy your Blogs"
        self.subtitle = "Convert your Medium blogs to podcasts"
        self.icon = "HeadsetSolid"
        self.icon_color = "$white"

        self.boxes = {
            "header": "1 1 11 1",
            "sidebar": "1 2 3 9",
            "description": "4 2 8 2",
            "audio": "4 4 8 2",
            "summary": "4 6 8 5",
        }


config = Configuration()
