document.getElementById("header")
    .innerHTML = `
<div class="header-section">

    <div class="banner-section">

        <img src="images/cw.png" width="135px" style="float:left; margin-right: 25px;">

        <div style="margin-bottom:25px;">
            <a class="button" href="https://www.curiouswalk.com">
                <span>&nbsp;CuriousWalk&nbsp;</span>
                <span class="hover-text">&nbsp;CuriousWalk&nbsp;</span>
                <span class="link-text">curiouswalk.com</span>
            </a>
        </div>

        <div style="margin-bottom:25px;">
            <a class="button" href="https://github.com/curiouswalk/manimscene">
                <span>&nbsp;Mscene&nbsp;</span>
                <span class="hover-text">&nbsp;Mscene&nbsp;</span>
                <span class="link-text">Open&nbsp;in&nbsp;GitHub</span>
            </a>
        </div>

        <h1 style="font-weight: normal; margin-bottom:0px">Program Animations With Manim</h1>
    
    </div>

</div>

</div>
`;

let vid = '';

let github_url = 'https://github.com/curiouswalk/manimscene/tree/main/source/';

let colab_url = 'https://colab.research.google.com/github/curiouswalk/manimscene/blob/main/source/';

let youtube_url = 'https://www.youtube.com/watch?v=';

const v = document.getElementsByClassName("scene");

for (var n = 0; n < v.length; n++) {

    let id = v[n].getAttribute("id");

    let file = v[n].getAttribute("file");

    let name = v[n].getAttribute("name");

    let html = '<h2><a href="' + github_url + file + '">' + name + '</a></h2>';

    html += '<div id="vid_+' + id + '" ><a href="javascript:void(0)" onclick=playYT("' + id + '")><img class="ytframe" src="images/' + id + '.jpeg"/></a></div>';

    html += '<div class="badge"> <a href="' + colab_url + file + '/' + file + '.ipynb"><img class="colab-badge"></a>';

    html += '<a href="' + github_url + file + '"><img class="github-badge"></a>';

    html += '<a href="' + youtube_url + id + '"><img class="youtube-badge"></a></div>';

    html += v[n].innerHTML;

    v[n].style.display = 'inline-block';

    v[n].innerHTML = html;

}

function playYT(id) {

    if (vid != '') {
        let imageHtml = '<a href="javascript:void(0)" onclick=playYT("' + vid + '")><img class="ytframe" src="images/' + vid + '.jpeg"/></a>';
        document.getElementById('vid_+' + vid)
            .innerHTML = imageHtml;
    }

    vid = id;

    let videoHtml = '<iframe class="ytframe" src="https://www.youtube.com/embed/' + vid + '?autoplay=1&color=white&rel=0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>';
    document.getElementById('vid_+' + vid)
        .innerHTML = videoHtml;
}

let contentHtml = '<div class="body-section">';

// about section

contentHtml += `
<div class="scene" style="display: inline-block;">

    <p><strong>Mscene</strong> is a Python library for programming animation scenes with Manim in Google Colab to create science animations directly in the browser.</p>

    <p>Manim is an animation engine designed to program precise animations for science videos. Google Colab (Colaboratory) is a hosted Jupyter Notebook service that requires no setup and provides free access to computing resources, including GPUs and TPUs.</p>

    <blockquote>
        The Manim Community Developers. <cite>Manim — Mathematical Animation Framework</cite> [Computer software].<br><a href="https://https://www.manim.community/">www.manim.community</a>
    </blockquote>

    <a href="https://mscene.curiouswalk.com/colab">
        <img src="https://img.shields.io/badge/Manim_in_Colab-link?style=flat&logo=googlecolab&labelColor=grey&color=blue" height="26px">
    </a><br><a href="https://mscene.curiouswalk.com/colab">mscene.curiouswalk.com/colab</a>

</div>
`;

contentHtml += document.getElementById("content")
    .innerHTML;

contentHtml += '</div>';

document.getElementById("content")
    .innerHTML = contentHtml;

const year = new Date()
    .getFullYear()

document.getElementById("footer")
    .innerHTML = `
<footer style="margin: 0;">
<p style="color: slategray; text-align: center; margin: 25px auto;">
  Copyright &copy; ${year} CuriousWalk<br>
  <a href="https://www.curiouswalk.com">curiouswalk.com</a>
</p>
</footer>
`;

function parallaxHeight() {
    var scroll_top = $(this)
        .scrollTop();
    var sample_section_top = $(".body-section")
        .offset()
        .top;
    var header_height = $(".banner-section")
        .outerHeight();
    $(".body-section")
        .css({
            "margin-top": header_height
        });
    $(".header-section")
        .css({
            height: header_height - scroll_top
        });
}

parallaxHeight();

$(window)
    .scroll(function () {
        parallaxHeight();
    });

$(window)
    .resize(function () {
        parallaxHeight();
    });
