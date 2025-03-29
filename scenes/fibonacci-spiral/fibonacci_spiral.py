from manim import *


def fib_seq(n, a=0, b=1):
    seq = []
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


def seq2str(seq):
    seq_str = ", ".join(map(str, seq)) + ", ..."
    return seq_str


def fib_spiral_mobj(seq):
    """Returns Mobjects for Fibonacci spiral.

    Args:
        seq (list[int]): List of Fibonacci numbers.

    Returns:
        VGroup: A group of Mobjects:
            Square, Text, ArcBetweenPoints and Dot.
    """

    mobjects = VGroup()
    squares = VGroup()

    direction = (UP, RIGHT, DOWN, LEFT)
    corner = (DL, UL)
    dot_index = (0, 0, -1, -1)

    for i, n in enumerate(seq):
        square = Square(n, stroke_width=6).next_to(squares, direction[i % 4], buff=0)
        dots = VGroup(
            Dot(square.get_corner(corner[i % 2]), color="#cfff04"),
            Dot(square.get_corner(-corner[i % 2]), color="#cfff04"),
        )
        spiral = ArcBetweenPoints(
            dots[dot_index[i % 4]].get_center(),
            dots[dot_index[i % 4] + 1].get_center(),
            angle=-PI / 2,
            color="#04d9ff",
            stroke_width=6,
        )
        num = (
            Text(f"{n}×{n}", fill_opacity=2 / 3)
            .scale_to_fit_width(square.width * 0.5)
            .move_to(square)
        )
        squares.add(square)
        mobjects.add(VGroup(square, spiral, dots, num))
        mobjects.center()

    return mobjects


def text_anim(scene):
    """A text animation that spirals in and out."""

    tex_width = config.frame_width / 2

    text = VGroup(
        Text("Fibonacci").scale_to_fit_width(tex_width),
        Text("Spiral").scale_to_fit_width(tex_width),
    ).arrange(DOWN)

    text_group = VGroup(*text[0], *text[1])

    scene.play(SpiralIn(text_group, scale_factor=1))

    scene.wait(1.5)

    scene.play(
        SpiralIn(
            text_group,
            scale_factor=1,
            rate_func=lambda t: smooth(1 - t),
            remover=True,
        )
    )


def spiral_scene(scene, mobj):
    """A Fibonacci spiral animation with the camera zooming out to fit the scene. The scene must be an instance of MovingCameraScene for animation."""

    # increasing stroke width and dot size
    for j, i in enumerate(mobj):
        if j < 6:
            s = 6 + 2 * j
        else:
            s = (j - 1) ** 2
        i[1].set_stroke(width=s)
        i[2][0].scale(1 + s * 0.1)
        i[2][1].scale(1 + s * 0.1)

    # move and zoom camera to first element of mobj
    scene.camera.frame.move_to(mobj[0].get_center()).scale_to_fit_height(
        mobj[0].height * 3.75
    )

    for j, i in enumerate(mobj, 1):
        anim = [FadeIn(i[0]), Create(i[1]), FadeIn(i[2]), Write(i[3])]

        # adjust camera frame to fit the scene
        if mobj[:j].height > scene.camera.frame.height:
            anim.append(
                scene.camera.frame.animate.scale_to_fit_height(
                    mobj[:j].height * 1.25
                ).move_to(mobj[:j].get_center())
            )
        else:
            anim.append(scene.camera.frame.animate.move_to(mobj[:j].get_center()))

        scene.play(*anim, run_time=1.5)

        scene.wait(0.5)

    scene.wait(1)

    scene.play(
        scene.camera.frame.animate(run_time=2)
        .move_to(mobj[0].get_center())
        .scale_to_fit_height(mobj[0].height * 3.75)
    )


class SceneOne(Scene):
    def construct(self):
        size = 6
        seq = fib_seq(size, 1)
        mobj = fib_spiral_mobj(seq)
        mobj.scale_to_fit_height(config.frame_height * 2 / 3)
        text = Text(f"Fibonacci\nSequence: {seq2str(seq)}", font_size=36).to_corner(DL)

        anim_in = [
            [FadeIn(i[0]), Create(i[1]), FadeIn(i[2]), Write(i[3])] for i in mobj
        ]
        anim_out = [
            [FadeOut(i[0]), Uncreate(i[1]), FadeOut(i[2]), Unwrite(i[3])]
            for i in mobj[::-1]
        ]

        self.play(AnimationGroup(Write(text), *anim_in, lag_ratio=0.125))
        self.wait(3)
        self.play(AnimationGroup(*anim_out, Unwrite(text), lag_ratio=0.125))
        self.wait(0.5)


class SceneTwo(Scene):
    def construct(self):
        size = 12
        seq = fib_seq(size, 1)
        mobj = fib_spiral_mobj(seq)
        mobj.scale_to_fit_height(config.frame_height * 0.75)
        sf = mobj.height / mobj[0].height

        self.add(mobj)
        self.wait(0.5)

        self.play(
            mobj.animate(run_time=4)
            .scale(sf)
            .move_to(-sf * (mobj[0].get_center() + mobj.get_center()))
        )
        self.wait(2)

        self.play(mobj.animate(run_time=4).scale(1 / sf).center())
        self.wait(0.5)


class SpiralScene(MovingCameraScene):
    def construct(self):
        size = 12
        mobj = fib_spiral_mobj(fib_seq(size, 1))

        text_anim(self)
        self.wait()

        spiral_scene(self, mobj)
        self.wait(0.5)

        self.play(FadeOut(mobj))
        self.wait(0.5)
