import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from manim import *

config.disable_caching = True
config.verbosity = "WARNING"
config.media_width = "75%"
config.media_embed = True

Text.set_default(font="STIX Two Text")


class ManimScene(Scene):
    def construct(self):
        banner = ManimBanner()
        self.play(banner.create())
        self.play(banner.expand())
        self.wait(2)
        self.play(FadeOut(banner))
        self.wait(0.5)
