from manim import *


class FlashFade(AnimationGroup):
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
        """
        Animation for VMobject to fade-in or fade-out with flashing outline.

        Args:
            mob: The VMobject to animate.
            mode: IN for fade-in, OUT for fade-out, or None for both.
            reverse: If True, reverses the animation direction.
            color: The color of the flash outline.
            width: The stroke width of the flash outline.
            time_width: The relative duration of the flash effect.
            run_time: The duration of each sub-animation.
            lag_ratio: The lag ratio between sub-animations.
            **kwargs: Additional keyword arguments for AnimationGroup.
        """

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
