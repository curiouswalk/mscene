from manim import *

__scenes__ = ["SceneOne", "SceneTwo", "SceneThree"]


def fib_seq(n, a=0, b=1):
    """Returns a list of the first n terms, starting with the values a and b."""
    seq = []
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


def seq2str(seq):
    """Returns a string of numbers in sequence."""
    seq_str = ", ".join(map(str, seq)) + ", ..."
    return seq_str


def fib_spiral_mobj(seq, sf=1, add_dots=True):
    """Returns Mobjects for Fibonacci spiral.

    Args:
        seq (list[int]): List of Fibonacci numbers.

    Returns:
        VGroup: A group of Mobjects:
                Square, Text, ArcBetweenPoints and Dot.
    """

    sqr_clr, dot_clr, sprl_clr = [
        ManimColor(hex) for hex in ("#214761", "#cfff04", "#04d9ff")
    ]

    mobjects = VGroup()
    squares = VGroup()

    direction = (UP, RIGHT, DOWN, LEFT)
    corner = (DL, UL)
    dot_index = (0, 0, -1, -1)

    for i, n in enumerate(seq):
        square = Square(n * sf, stroke_width=6, color=sqr_clr).next_to(
            squares, direction[i % 4], buff=0
        )

        dots = VGroup(
            Dot(square.get_corner(corner[i % 2]), color=dot_clr),
            Dot(square.get_corner(-corner[i % 2]), color=dot_clr),
        )

        spiral = ArcBetweenPoints(
            dots[dot_index[i % 4]].get_center(),
            dots[dot_index[i % 4] + 1].get_center(),
            angle=-PI / 2,
            color=sprl_clr,
            stroke_width=6,
        )
        num = (
            Text(f"{n}×{n}", fill_opacity=2 / 3)
            .scale_to_fit_width(square.width * 0.5)
            .move_to(square)
        )

        squares.add(square)

        if add_dots:

            vgroup = VGroup(square, num, spiral, dots)
        else:
            vgroup = VGroup(square, num, spiral)

        vgroup[1:].set_z_index(1)
        mobjects.add(vgroup)
        mobjects.center()

    return mobjects


def text_spiral_anim(text):
    """Text animation that spirals in and out."""
    text_group = VGroup()
    for t in text:
        text_group.add(*t)

    anim_in = SpiralIn(text_group, scale_factor=0)
    anim_out = SpiralIn(
        text_group,
        scale_factor=0,
        rate_func=lambda t: smooth(1 - t),
    )

    anim = (anim_in, anim_out)

    return anim


class SceneOne(Scene):
    def construct(self):
        size = 6
        seq = fib_seq(size, 1)
        frame_sizes = (config.frame_width, config.frame_height)
        sf = frame_sizes[size % 2] / sum(seq[-2:]) * 0.75
        mobj = fib_spiral_mobj(seq, sf)

        text_width = config.frame_width / 2
        text_group = VGroup(
            *[Text(t).scale_to_fit_width(text_width) for t in ("Fibonacci", "Spiral")]
        ).arrange(DOWN)
        text_anim_in, text_anim_out = text_spiral_anim(text_group)

        spiral_anim_in = [
            (FadeIn(i[0]), Write(i[1]), Create(i[2]), FadeIn(i[3])) for i in mobj
        ]
        spiral_anim_out = [
            (FadeOut(i[0]), Unwrite(i[1]), Uncreate(i[2]), FadeOut(i[3]))
            for i in mobj[::-1]
        ]

        self.play(text_anim_in)
        self.wait()
        self.play(text_anim_out)
        self.wait()
        self.play(AnimationGroup(*spiral_anim_in, lag_ratio=0.125))
        self.wait(2.5)
        self.play(AnimationGroup(*spiral_anim_out, lag_ratio=0.125))
        self.wait(0.5)


class SceneTwo(Scene):
    def construct(self):
        size = 18
        seq = fib_seq(size, 1)
        frame_sizes = (config.frame_width, config.frame_height)
        sf1 = frame_sizes[size % 2] / sum(seq[-2:]) * 0.75
        sf2 = frame_sizes[1] * 0.5
        mobj1 = fib_spiral_mobj(seq, sf1, add_dots=False)
        mobj2 = fib_spiral_mobj(seq, sf2, add_dots=False)
        point = mobj2.get_center() - mobj2[0].get_center()
        mobj2.move_to(point)
        mobj1.save_state()
        self.add(mobj1)
        self.wait()
        self.play(Transform(mobj1, mobj2, run_time=3))
        self.wait(2)
        self.play(Restore(mobj1, run_time=3))
        self.wait()


class SceneThree(Scene):
    def construct(self):
        # sequence range: i to n
        i, n = 1, 8
        # i, n = 8,12 # try this!
        print(fib_seq(n + 1)[i:])
        seq = fib_seq(i, 1)
        frame_sizes = (config.frame_width, config.frame_height)
        sf = frame_sizes[i % 2] / sum(seq[-2:]) * 0.75
        mobj = fib_spiral_mobj(seq, sf, add_dots=False)
        anim_in = [(FadeIn(i[0]), Write(i[1]), Create(i[2])) for i in mobj]
        self.play(*anim_in)
        self.wait()

        for j in range(i + 1, n + 1):
            seq = fib_seq(j, 1)
            sf = frame_sizes[j % 2] / sum(seq[-2:]) * 0.75
            _mobj = fib_spiral_mobj(seq, sf, add_dots=False)
            # transforms existing elements and then adds new ones
            self.play(ReplacementTransform(mobj, _mobj[:-1]))
            self.play(FadeIn(_mobj[-1][0]), Write(_mobj[-1][1]), Create(_mobj[-1][2]))
            self.wait()
            mobj = _mobj

        anim_out = [(FadeOut(i[0]), Unwrite(i[1]), Uncreate(i[2])) for i in mobj]
        self.wait()
        self.play(*anim_out)
        self.wait()
