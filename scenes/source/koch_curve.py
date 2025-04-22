"""
Mscene: Koch Curve

https://mscene.curiouswalk.com/scenes/koch-curve
"""

from manim import *
from mscene.plugins import *


class SceneOne(Scene):
    def construct(self):

        kc = KochCurve(2)
        self.add(kc)

        self.play(kc.animate.next_level())
        self.wait()

        self.play(kc.animate.prev_level())
        self.wait()


class SceneTwo(Scene):
    def construct(self):

        kc1 = KochCurve(level=1, stroke_width=6)
        kc2 = KochCurve(level=2, stroke_width=6, group=False)
        kc3 = KochCurve(level=3, stroke_width=6, group=False)
        colors = color_gradient((PURE_RED, PURE_BLUE), 4)

        for i, j, c in zip(kc2, kc3, colors):
            i.set_color(c)
            j.set_color(c)

        self.add(kc1)
        self.play(kc1.animate.next_level())
        self.wait()

        self.play(FadeTransform(kc1, kc2))
        self.wait()

        self.play(Transform(kc2, kc3, rate_func=there_and_back_with_pause, run_time=3))
        self.wait()

        self.play(FadeTransform(kc2, kc1))
        self.wait()

        self.play(kc1.animate.prev_level())
        self.wait()


class KochCurveScene(Scene):
    def construct(self):

        color = [ManimColor(hex) for hex in ("#0A68EF", "#0ADBEF", "#0A68EF")]

        kc = KochCurve(level=0, stroke_width=8, stroke_color=color)
        title = Text("Koch Curve\nLevel 0").to_corner(UL, buff=0.75)

        self.add(title, kc)
        self.wait()

        levels = (1, 2, 3, 2, 1, 0)

        for level in levels:
            self.play(
                kc.animate(run_time=1.5).new_level(level, stroke_width=8 - level),
                Transform(title[-1], Text(str(level)).move_to(title[-1])),
            )
            self.wait()


class SnowflakeScene(Scene):
    def construct(self):

        color = [ManimColor(hex) for hex in ("#0ADBEF", "#0A68EF", "#1F0AEF")]

        ks = KochSnowflake(level=0, fill_color=color)
        title = Text("Koch Snowflake\nLevel 0").to_corner(UL, buff=0.75)

        self.add(title, ks)
        self.wait()

        levels = (1, 2, 3, 2, 1, 0)

        for level in levels:
            self.play(
                ks.animate(run_time=1.5).new_level(level),
                Transform(title[-1], Text(str(level)).move_to(title[-1])),
            )
            self.wait()


class AntisnowflakeScene(Scene):
    def construct(self):

        color = [ManimColor(hex) for hex in ("#1F0AEF", "#0A68EF", "#0ADBEF")]

        ks = KochSnowflake(level=0, invert=True, fill_color=color)
        title = Text("Koch Anti-\nsnowflake\nLevel 0").to_corner(UL, buff=0.75)

        self.add(title, ks)
        self.wait()

        levels = (1, 2, 3, 2, 1, 0)

        for level in levels:
            self.play(
                ks.animate(run_time=1.5).new_level(level),
                Transform(title[-1], Text(str(level)).move_to(title[-1])),
            )
            self.wait()


class DualFlakesScene(Scene):
    def construct(self):

        ks1 = KochSnowflake(level=1, fill_color=ManimColor("#5d06e9"))
        ks2 = KochSnowflake(
            level=1, invert=True, fill_color=ManimColor("#9e0168")
        ).align_to(ks1, UP)

        self.add(ks1, ks2)
        self.wait()

        levels = (2, 3, 2, 1)

        for level in levels:
            self.play(
                ks1.animate.new_level(level), ks2.animate.new_level(level), run_time=1.5
            )
            self.wait()
