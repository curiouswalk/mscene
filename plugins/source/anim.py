from manim import *


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
