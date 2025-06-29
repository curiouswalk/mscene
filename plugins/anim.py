from manim import *


class DashFlow(DashedVMobject):
    """A dashed VMobject with its dash offset continuously shifting for a flowing effect.

    Args:
        vmob (VMobject): The VMobject to animate.
        rate (float): The rate of shifting dash offset over time (default: 1.0).
        **kwargs: Additional keyword arguments passed to DashedVMobject.

    Methods:
        play():
            Resume updater to play animation.
        pause():
            Suspend updater to pause animation.
        stop():
            Clear updater to stop animation.
    """

    def __init__(self, vmob, rate=1.0, dash_offset=0, **kwargs):
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
    """Animation for fading VMobjects with flashing outlines.

    Args:
        vmob (VMobject): The VMobject to animate.
        mode (str): "IN" to fade in, "OUT" to fade out, "AUTO" to fade in and out (default: "AUTO").
        reverse (bool): If True, reverses the animation direction (default: False).
        color (ManimColor | None): The stroke color of the flash outline (default: None).
        width (float | None): The stroke width of the flash outline (default: None).
        opacity (float | None): The stroke opacity of the flash outline (default: None).
        time_width (float): The length of the sliver relative to the length of the stroke (default: 0.5).
        duration (float): The duration of each sub-animation (default: 1.0).
        lag_ratio (float): The lag ratio between sub-animations (default: 0.125).
        **kwargs: Additional keyword arguments for AnimationGroup.
    """

    def __init__(
        self,
        vmob: VMobject,
        mode="AUTO",
        reverse=False,
        color=None,
        width=None,
        opacity=None,
        time_width=0.5,
        duration=1.0,
        lag_ratio=0.125,
        **kwargs,
    ):
        if reverse:
            vmob = vmob[::-1]
            vcopy = vmob.copy()
            vcopy.set_fill(opacity=0).set_stroke(color, width, opacity)
            for vm in vcopy:
                vm = vm.reverse_direction()
        else:
            vcopy = vmob.copy()
            vcopy.set_fill(opacity=0).set_stroke(color, width, opacity)

        mode = mode.upper()
        n = len(vmob)
        anim = []

        if mode == "IN":
            for i in range(n):
                anim.append(
                    AnimationGroup(
                        FadeIn(vmob[i]),
                        ShowPassingFlash(vcopy[i], time_width=time_width),
                        duration=duration,
                    )
                )
        elif mode == "OUT":
            for i in range(n):
                anim.append(
                    AnimationGroup(
                        FadeOut(vmob[i]),
                        ShowPassingFlash(vcopy[i], time_width=time_width),
                        duration=duration,
                    )
                )
        else:
            for i in range(n):
                anim.append(
                    AnimationGroup(
                        FadeIn(vmob[i].copy(), rate_func=there_and_back_with_pause),
                        ShowPassingFlash(vcopy[i], time_width=time_width),
                        duration=duration,
                    )
                )

        super().__init__(*anim, lag_ratio=lag_ratio, **kwargs)
