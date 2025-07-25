"""
Mscene: Koch Curve

https://mscene.curiouswalk.com/scenes/koch-curve
"""

import sys

try:
    from mscene.fractal import *
except ImportError:
    print(
        "Error: 'mscene.fractal' not found.\nInstall: 'pip install mscene && mscene plugins'",
        file=sys.stderr,
    )
    sys.exit(1)

from manim import *


class ExampleOne(Scene):
    def construct(self):
        kc = KochCurve(2)
        self.add(kc)

        self.play(kc.animate.next_level())
        self.wait()

        self.play(kc.animate.prev_level())
        self.wait()


class ExampleTwo(Scene):
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
        kc = KochCurve(level=1, stroke_width=8, stroke_color=color)
        title = Text("Koch Curve\nLevel 1").to_corner(UL, buff=0.75)

        self.add(title, kc)
        self.wait()

        for level in (2, 3, 2, 1):
            self.play(
                kc.animate.new_level(level, stroke_width=8 - level),
                Transform(title[-1], Text(str(level)).move_to(title[-1])),
            )
            self.wait()


class Snowflake(Scene):
    def construct(self):
        color = [ManimColor(hex) for hex in ("#0ADBEF", "#0A68EF", "#1F0AEF")]
        ks = KochSnowflake(level=1, fill_color=color)
        title = Text("Koch Snowflake\nLevel 1").to_corner(UL, buff=0.75)

        self.add(title, ks)
        self.wait()

        for level in (2, 3, 2, 1):
            self.play(
                ks.animate.new_level(level),
                Transform(title[-1], Text(str(level)).move_to(title[-1])),
            )
            self.wait()


class Antisnowflake(Scene):
    def construct(self):
        color = [ManimColor(hex) for hex in ("#1F0AEF", "#0A68EF", "#0ADBEF")]
        ks = KochSnowflake(level=1, invert=True, fill_color=color)
        title = Text("Koch Anti-\nsnowflake\nLevel 1").to_corner(UL, buff=0.75)

        self.add(title, ks)
        self.wait()

        for level in (2, 3, 2, 1):
            self.play(
                ks.animate.new_level(level),
                Transform(title[-1], Text(str(level)).move_to(title[-1])),
            )
            self.wait()


class DualFlakes(Scene):
    def construct(self):
        snowflake = KochSnowflake(level=1, fill_color=ManimColor("#5d06e9"))
        anti_snowflake = KochSnowflake(
            level=1, invert=True, fill_color=ManimColor("#9e0168")
        ).align_to(snowflake, UP)

        self.add(snowflake, anti_snowflake)
        self.wait()

        for level in (2, 3, 2, 1):
            self.play(
                snowflake.animate.new_level(level),
                anti_snowflake.animate.new_level(level),
                run_time=1.5,
            )
            self.wait(1.5)
