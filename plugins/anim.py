from manim import *


class DashFlow(DashedVMobject):
    """
    A dashed VMobject with its dash offset continuously shifting for a flowing effect.

    Args:
        vmob (VMobject): The VMobject to be dashed and animated.
        rate (float): The rate of shifting dash offset over time. Defaults to 1.
        **kwargs: Additional keyword arguments passed to DashedVMobject.

    Methods:
        play():
            Resume updater to play animation.
        pause():
            Suspend updater to pause animation.
        stop():
            Clear updater to stop animation.
    """

    def __init__(self, vmob, rate=1, dash_offset=0, **kwargs):
        vmob = vmob.copy()
        super().__init__(vmob, dash_offset=dash_offset, **kwargs)

        self.rate = rate
        self.offset = dash_offset

        def _updater(mobj, dt):
            self.offset = (self.offset + dt * self.rate) % 1
            mobj.become(DashedVMobject(vmob, dash_offset=self.offset, **kwargs))

        self.add_updater(_updater)

    def play(self):
        self.resume_updating()

    def pause(self):
        self.suspend_updating()

    def stop(self):
        self.clear_updaters()


class DrawArc(Succession):
    def __init__(self, arc, reverse=False, run_time=2, **kwargs):
        quarter_time = run_time / 4
        half_time = run_time / 2

        if reverse:
            line = Line(
                arc.get_arc_center(),
                arc.get_end(),
                stroke_width=arc.get_stroke_width(),
                stroke_color=arc.get_stroke_color(),
            )
            create_arc = Uncreate(arc, run_time=half_time)
            rotate_line = Rotate(
                line, -arc.angle, about_point=arc.get_arc_center(), run_time=half_time
            )
        else:
            line = Line(
                arc.get_arc_center(),
                arc.get_start(),
                stroke_width=arc.get_stroke_width(),
                stroke_color=arc.get_stroke_color(),
            )
            create_arc = Create(arc, run_time=half_time)
            rotate_line = Rotate(
                line, arc.angle, about_point=arc.get_arc_center(), run_time=half_time
            )

        super().__init__(
            Create(line, run_time=quarter_time),
            AnimationGroup(
                create_arc,
                rotate_line,
            ),
            Uncreate(line, run_time=quarter_time),
            **kwargs,
        )


class FlashFade(AnimationGroup):
    """
    Animation for VMobject to fade in or out with flashing outline effect.

    Args:
        vmob: The VMobject to animate.
        mode: IN for fade-in, OUT for fade-out, None for fade-in then fade-out. Defaults to None.
        reverse: If True, reverses the animation direction. Defaults to False.
        color: The color of the flash outline. Defaults to None.
        width: The stroke width of the flash outline. Defaults to None.
        time_width: The relative duration of the flash effect. Defaults to 0.5.
        run_time: The duration of each sub-animation. Defaults to 1.0.
        lag_ratio: The lag ratio between sub-animations. Defaults to 0.125.
        **kwargs: Additional keyword arguments for AnimationGroup.
    """

    def __init__(
        self,
        vmob: VMobject,
        mode=None,
        reverse=False,
        color=None,
        width=None,
        time_width=0.5,
        run_time=1.0,
        lag_ratio=0.125,
        **kwargs,
    ):
        if reverse:
            vmob = vmob[::-1]
            vcopy = vmob.copy()
            vcopy.set_fill(opacity=0).set_stroke(color=color, width=width)
            for vm in vcopy:
                vm = vm.reverse_direction()
        else:
            vcopy = vmob.copy()
            vcopy.set_fill(opacity=0).set_stroke(color=color, width=width)

        n = len(vmob)
        anim = []

        if mode is IN:
            for i in range(n):
                anim.append(
                    AnimationGroup(
                        FadeIn(vmob[i]),
                        ShowPassingFlash(vcopy[i], time_width=time_width),
                        run_time=run_time,
                    )
                )
        elif mode is OUT:
            for i in range(n):
                anim.append(
                    AnimationGroup(
                        FadeOut(vmob[i]),
                        ShowPassingFlash(vcopy[i], time_width=time_width),
                        run_time=run_time,
                    )
                )
        else:
            for i in range(n):
                anim.append(
                    AnimationGroup(
                        FadeIn(vmob[i].copy(), rate_func=there_and_back_with_pause),
                        ShowPassingFlash(vcopy[i], time_width=time_width),
                        run_time=run_time,
                    )
                )

        super().__init__(*anim, lag_ratio=lag_ratio, **kwargs)
