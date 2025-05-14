from manim import *
config.disable_caching = True
config.verbosity = "WARNING"
config.media_width = "50%"
config.media_embed = True

Text.set_default(font="STIX Two Text")

class ManimScene(Scene):
    def construct(self):
        banner = ManimBanner()
        self.play(banner.create())
        self.play(banner.expand())
        self.wait(1.5)