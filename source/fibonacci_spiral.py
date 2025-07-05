"""
Mscene: Fibonacci Spiral

https://mscene.curiouswalk.com/scenes/fibonacci-spiral
"""

from manim import *


def fseq(n, a=0, b=1):
    """Return the first n Fibonacci numbers starting with a and b."""
    seq = []
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


def fsmob(n, width=None, height=None):
    """VGroup of Mobjects creating the Fibonacci spiral.

    Args:
        n (int): Number of first Fibonacci terms.
        width (float | None): Width of the object (default: None).
        height (float | None): Height of the object (default: None).

    Returns:
        VGroup of Square, Text, ArcBetweenPoints and Dot.
    """
    sqr_color = ManimColor("#214761")
    txt_color = ManimColor("#516572")
    arc_color = ManimColor("#04d9ff")
    dot_color = ManimColor("#cfff04")

    seq = fseq(n, 1)

    if width and not height:
        scale = width / sum(seq[-2:])
    elif height and not width:
        scale = height / seq[-1]
    else:
        scale = 1

    mobjects = VGroup()
    squares = VGroup()

    if len(seq) % 2:
        angle = PI / 2
        direction = (RIGHT, UP, LEFT, DOWN)
        dot_index = (0, -1, -1, 0)
    else:
        angle = -PI / 2
        direction = (UP, RIGHT, DOWN, LEFT)
        dot_index = (0, 0, -1, -1)

    corner = (DL, UL)

    for i, t in enumerate(seq):
        square = Square(t * scale, stroke_width=6, color=sqr_color).next_to(
            squares,
            direction[i % 4],
            buff=0,
        )

        dots = VGroup(
            Dot(square.get_corner(corner[i % 2]), color=dot_color),
            Dot(square.get_corner(-corner[i % 2]), color=dot_color),
        )

        arc = ArcBetweenPoints(
            dots[dot_index[i % 4]].get_center(),
            dots[dot_index[i % 4] + 1].get_center(),
            angle=angle,
            color=arc_color,
            stroke_width=6,
        )

        text = (
            Text(f"{t}×{t}", color=txt_color)
            .scale_to_fit_width(square.width * 0.5)
            .move_to(square)
        )

        vgrp = VGroup(square, text, arc, dots)
        vgrp[2:].set_z_index(1)
        squares.add(square)
        mobjects.add(vgrp)

    mobjects.center()

    return mobjects


def spiral_anim(mob, mode="IN", lag_ratio=0.125, **kwargs):
    """Return an AnimationGroup for spiral animation."""

    if mode == "IN":

        anim = [(FadeIn(i[0]), Write(i[1]), Create(i[2]), FadeIn(i[3])) for i in mob]
    elif mode == "OUT":
        anim = [
            (FadeOut(i[0]), Unwrite(i[1]), Uncreate(i[2]), FadeOut(i[3]))
            for i in mob[::-1]
        ]
    else:
        raise ValueError("mode must be 'IN' or 'OUT'")

    return AnimationGroup(*anim, lag_ratio=lag_ratio, **kwargs)


class SceneOne(Scene):
    def construct(self):
        seq = fseq(25)
        width = config.frame_width * 3 / 4
        seq_str = ", ".join(map(str, seq)) + ", ..."

        title = Text("Fibonacci Sequence").scale_to_fit_width(width * 3 / 4)
        text = MarkupText(seq_str, width=width, justify=True, font_size=130)
        VGroup(title, text).arrange(DOWN, buff=3 / 4)

        self.play(Write(title), Write(text, run_time=3))
        self.wait(3)


class SceneTwo(Scene):
    def construct(self):
        manim_image(self)
        width = config.frame_width * 3 / 4
        mob = fsmob(6, width=width)

        self.play(spiral_anim(mob))
        self.wait(2.5)

        self.play(spiral_anim(mob, mode="OUT"))
        self.wait(0.5)


class SceneThree(Scene):
    def construct(self):
        width = config.frame_width * 3 / 4
        terms = [4, 8, 12]
        term = None
        mob = None

        for n in terms:
            _mob = fsmob(n, width)

            if mob is None:
                self.play(spiral_anim(_mob))
            else:
                i = term if term < n else -1
                self.play(ReplacementTransform(mob, _mob[:i]))
                self.wait(0.5)
                self.play(spiral_anim(_mob[i:]))

            mob = _mob
            term = n
            self.wait(1.5)

        self.play(spiral_anim(mob, mode="OUT", lag_ratio=0))
        self.wait(0.5)


class SceneFour(Scene):
    def construct(self):
        n = 12
        width = config.frame_width * 3 / 4
        mob = fsmob(n, width)
        mob.save_state()

        width *= sum(fseq(n)[-2:]) * 3 / 4
        _mob = fsmob(n, width)
        _mob.shift(-_mob[0].get_center())

        self.add(mob)
        self.wait(0.5)

        self.play(Transform(mob, _mob, run_time=6))
        self.wait(2)

        self.play(Restore(mob, run_time=4))
        self.wait(0.5)
