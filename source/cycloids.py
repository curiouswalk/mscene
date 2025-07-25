"""
Mscene: Cycloids

https://mscene.curiouswalk.com/scenes/cycloids
"""

import sys

try:
    from mscene.roulette import *
except ImportError:
    print(
        "Error: 'mscene.roulette' not found.\nInstall: 'pip install mscene && mscene plugins'",
        file=sys.stderr,
    )
    sys.exit(1)

from manim import *


class Cycloids(Scene):
    def construct(self):

        radius = 0.8
        length = TAU * radius

        circle_one = Circle(radius=radius, color=ManimColor("#C5C9C7")).rotate(PI / 2)

        circle_two = Circle(radius=3 * radius, color=ManimColor("#C5C9C7")).rotate(
            PI / 2
        )

        line_end = circle_two.get_bottom()
        line_start = line_end + length * LEFT

        line = Line(line_start, line_end, color=ManimColor("#C5C9C7"))

        wheel = Wheel(radius=radius, color=ManimColor("#04D9FF"))

        self.play(GrowFromCenter(wheel))
        self.wait()

        self.play(Create(line), wheel.animate.move(line_start, UP))
        self.bring_to_front(wheel)

        marker = [(1, PI / 2, ManimColor("#6019E3"))]
        self.play(wheel.draw_markers(marker))

        path = wheel.trace_paths(dissipating_time=2)
        self.add(path)

        # rolls along the line
        self.play(wheel.roll(length * RIGHT, run_time=2.5))
        self.wait()

        self.play(ReplacementTransform(line, circle_one))
        self.wait()

        # rolls along the outer edge of circle one
        self.play(wheel.roll(TAU, about=circle_one, run_time=2.5))
        self.wait()

        self.play(ReplacementTransform(circle_one, circle_two))
        self.wait()

        # rolls along the inner edge of circle two
        self.play(wheel.roll(TAU, about=circle_two, run_time=3))
        self.wait(2)
        path.clear_updaters()
        self.remove(path)
        self.play(wheel.undraw_markers())

        self.play(Uncreate(circle_two), wheel.animate.move(ORIGIN))
        self.wait()

        self.play(ShrinkToCenter(wheel))
        self.wait(0.5)


def trochoid_scene(scene, title, markers):
    length = config.frame_width * 0.75
    radius = length / (2 * TAU)

    num_line = NumberLine(
        x_range=[-TAU, TAU, PI], length=length, color=ManimColor("#6F828A")
    ).shift(DOWN * radius)

    point = num_line.n2p(-TAU) + radius * UP

    wheel = Wheel(radius=radius, color=ManimColor("#04D9FF"), point=point)
    scene.play(GrowFromCenter(wheel), Create(num_line, lag_ratio=0))
    scene.wait()

    scene.play(wheel.draw_markers(markers), Write(title))
    scene.wait()

    path = wheel.trace_paths()
    scene.add(path)

    scene.play(wheel.roll(length * RIGHT, run_time=4))
    scene.wait()

    path.clear_updaters()
    scene.play(path.animate.fade(2 / 3))

    new_path = wheel.trace_paths(dissipating_time=2)
    scene.add(new_path)

    scene.play(wheel.roll(length * LEFT, run_time=4))
    scene.wait()

    scene.play(Unwrite(title), FadeOut(path))

    new_path.clear_updaters()
    scene.wait()

    scene.remove(new_path)
    scene.play(wheel.undraw_markers(), Unwrite(title))
    scene.wait()

    scene.play(ShrinkToCenter(wheel), Uncreate(num_line, lag_ratio=0))
    scene.wait(0.5)


class Cycloid(Scene):
    def construct(self):
        title = Text("Cycloid").to_edge(DOWN, buff=1.25)
        marker = [(1, PI / 2, ManimColor("#6019E3"))]

        trochoid_scene(self, title, marker)


class ProlateCycloid(Scene):
    def construct(self):
        title = Text("Prolate Cycloid").to_edge(DOWN, buff=1.25)
        marker = [(1.5, PI / 2, ManimColor("#E31937"))]

        trochoid_scene(self, title, marker)


class CurtateCycloid(Scene):
    def construct(self):
        title = Text("Curtate Cycloid").to_edge(DOWN, buff=1.25)
        marker = [(0.5, PI / 2, ManimColor("#19E360"))]

        trochoid_scene(self, title, marker)


class TwoMarkers(Scene):
    def construct(self):
        title = VMobject()
        marker = [
            (1, PI / 2, ManimColor("#6019E3")),
            (0.5, -PI / 2, ManimColor("#E31937")),
        ]

        trochoid_scene(self, title, marker)


class Trochoids(Scene):
    def construct(self):
        colors = [ManimColor(hex) for hex in ("#19E360", "#6019E3", "#E31937")]

        cycloids = [
            ("Curtate Cycloid", (0.5, PI / 2, colors[0])),
            ("Cycloid", (1, PI / 2, colors[1])),
            ("Prolate Cycloid", (1.5, PI / 2, colors[2])),
        ]

        title = VGroup()
        markers = []

        for i in cycloids:
            text = Text(i[0], font_size=40)
            dot = Dot(radius=0.125, color=i[1][2]).next_to(text[0], LEFT)
            title.add(VGroup(dot, text))
            markers.append(i[1])

        title.arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=1.25)
        markers.reverse()

        trochoid_scene(self, title, markers)


def epitrochoid_scene(
    scene,
    k,
    angle=-TAU,
    run_time=4,
    markers=[(1, PI / 2, ManimColor("#6019E3"))],
    scale=1,
    title=None,
):
    h = config.frame_height * scale * 3 / 8
    r = h / (2 + k)

    wheel = Wheel(radius=r, color=ManimColor("#04D9FF"), markers=markers)

    circle = Circle(radius=k * r, color=ManimColor("#6F828A"))

    txt = f"k = {k}" if title is None else f"{title}\nk = {k}"
    text = Text(txt).to_corner(UL, buff=2 / 3)

    wheel.move(circle.get_top(), UP)

    scene.play(FadeIn(text, circle, wheel))
    scene.wait(0.5)

    path = wheel.trace_paths()
    scene.add(path)

    scene.play(wheel.roll(angle, about=circle, run_time=run_time))

    path.clear_updaters()
    scene.wait(2)

    scene.play(FadeOut(path))
    scene.wait()

    scene.play(FadeOut(text, circle, wheel))
    scene.wait(0.5)


class EpicycloidOne(Scene):
    def construct(self):

        epitrochoid_scene(self, k=3, angle=-TAU, title="Epicycloid")


class EpicycloidTwo(Scene):
    def construct(self):
        k, angle, run_time = (1.5, -TAU * 2, 8)

        epitrochoid_scene(self, k, angle, run_time, title="Epicycloid")


class Epitrochoids(Scene):
    def construct(self):
        k, angle, run_time = (3, -TAU, 5)
        markers = [
            (2, PI / 2, ManimColor("#6019E3")),
            (0.5, -PI / 2, ManimColor("#E31937")),
        ]
        epitrochoid_scene(
            self, k, angle, run_time, markers, scale=0.875, title="Epitrochoids"
        )


class TwoRollingCircles(Scene):
    def construct(self):
        k, angle, run_time = (2.25, -4 * TAU, 16)
        h = config.frame_height * 3 / 8
        r = h / (2 + k)

        color_one = ManimColor("#6019E3")
        color_two = ManimColor("#E31937")

        wheel_one_markers = [(1, PI / 2, color_one)]
        wheel_two_markers = [(1, -PI / 2, color_two)]

        wheel_one = Wheel(
            radius=r, color=ManimColor("#04D9FF"), markers=wheel_one_markers
        )
        wheel_two = Wheel(
            radius=r, color=ManimColor("#04D9FF"), markers=wheel_two_markers
        )
        circle = Circle(radius=k * r, color=ManimColor("#6F828A"))

        wheel_one.move(circle.get_top(), UP)
        wheel_two.move(circle.get_top(), DOWN)

        self.play(FadeIn(circle, wheel_one, wheel_two))
        self.wait(0.5)

        wheel_one_path = wheel_one.trace_paths()
        wheel_two_path = wheel_two.trace_paths()
        self.add(wheel_one_path, wheel_two_path)

        self.play(
            wheel_one.roll(angle, about=circle, run_time=run_time),
            wheel_two.roll(angle, about=circle, run_time=run_time),
        )
        wheel_one_path.clear_updaters()
        wheel_two_path.clear_updaters()
        self.wait(2)

        self.play(FadeOut(wheel_one_path, wheel_two_path))
        self.wait()

        self.play(FadeOut(circle, wheel_one, wheel_two))
        self.wait(0.5)


def hypotrochoid_scene(
    scene,
    k,
    angle=-TAU,
    run_time=4,
    markers=[(1, PI / 2, ManimColor("#6019E3"))],
    scale=1,
    title=None,
):
    h = config.frame_height * scale * 3 / 8
    r = h / k

    wheel = Wheel(radius=r, color=ManimColor("#04D9FF"), markers=markers)

    circle = Circle(radius=k * r, color=ManimColor("#6F828A"))

    txt = f"k = {k}" if title is None else f"{title}\nk = {k}"
    text = Text(txt).to_corner(UL, buff=2 / 3)

    wheel.move(circle.get_top(), DOWN)

    scene.play(FadeIn(text, circle, wheel))
    scene.wait(0.5)

    path = wheel.trace_paths()
    scene.add(path)

    scene.play(wheel.roll(angle, about=circle, run_time=run_time))

    path.clear_updaters()
    scene.wait(2)

    scene.play(FadeOut(path))
    scene.wait()

    scene.play(FadeOut(text, circle, wheel))
    scene.wait(0.5)


class Hypocycloid(Scene):
    def construct(self):
        hypotrochoid_scene(self, k=3, angle=-TAU, title="Hypocycloid")


class Hypotrochoids(Scene):
    def construct(self):
        k, angle, run_time = (3, -TAU, 5)
        markers = [
            (2, PI / 2, ManimColor("#6019E3")),
            (0.5, -PI / 2, ManimColor("#E31937")),
        ]

        hypotrochoid_scene(self, k, angle, run_time, markers, scale=0.875)


class StraightLines(Scene):
    def construct(self):
        k, angle, run_time = (2, -2 * TAU, 8)
        markers = [
            (1, 0, ManimColor("#6019E3")),
            (1, PI / 2, ManimColor("#8C19AA")),
            (1, PI, ManimColor("#E31937")),
            (1, -PI / 2, ManimColor("#B71970")),
        ]

        hypotrochoid_scene(self, k, angle, run_time, markers)


class Ellipses(Scene):
    def construct(self):
        k, angle, run_time = (2, -2 * TAU, 8)
        markers = [
            (2, 0, ManimColor("#6019E3")),
            (0.5, PI, ManimColor("#E31937")),
        ]

        hypotrochoid_scene(self, k, angle, run_time, markers, scale=0.9)
