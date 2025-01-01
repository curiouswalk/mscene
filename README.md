![mscene_banner](https://mscene.curiouswalk.com/assets/mscene_banner.png)

# Mscene

### Program Animations Online<br>&nbsp;&nbsp;[mscene.curiouswalk.com](https://mscene.curiouswalk.com)

**Mscene** is a Python library for programming animation scenes with Manim in Google Colab to create science videos directly in the browser.

[Manim in Colab]&nbsp;&nbsp;[mscene.curiouswalk.com/colab](https://colab.research.google.com/github/curiouswalk/mscene/blob/main/scenes/colab/mscene.ipynb)

#### Animate With Manim in Colab

- Open Google Colab
  - [colab.research.google.com#create=true](http://colab.research.google.com#create=true)
- Install Mscene: `%pip install mscene`
- Import Mscene: `import mscene`
  - View Commands: `%mscene -h`
- Setup Manim: `%mscene -l manim`

Example Scene

```python
%%manim -qm ExampleScene
class ExampleScene(Scene):
    def construct(self):
        banner = ManimBanner()
        self.play(banner.create())
        self.play(banner.expand())
        self.wait(1.5)
```

[Manim Gallery](https://docs.manim.community/en/stable/examples.html)

Manim is an animation engine designed to program precise animations for science videos.<br>Google Colab (Colaboratory) is a hosted Jupyter Notebook service that requires no setup and provides free access to computing resources, including GPUs and TPUs.

>**Manim**<br>The Manim Community Developers. *Manim &mdash; Mathematical Animation Framework* [Computer software].<br>[www.manim.community](https://www.manim.community)

---
