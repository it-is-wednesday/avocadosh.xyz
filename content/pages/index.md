title: ʕ •́؈•̀)
date: 2022-02-21
save_as: index.html

{% macro fruit(url, title, desc, lang) -%}
    {% set lang_name = {"clojure": "clojure", "python": "🐍", "ocaml": "ocaml🐪", "elisp": "emacs lisp🦬"}[lang] -%}
    <li>
        <div>
            <a href="{{ url }}">{{ title }}</a>
        </div>

        <div>{{ desc }}</div>

        <div>
            <span class="dot color-{{ lang }}"></span> {{ lang_name }}
        </div>
    </li>
{%- endmacro %}


<div class="index">
<div class="walked-inland">
    <div>I walked inland with water pouring out of my suitcase</div>
    <div>It was heavy so I dumped it out and stuck all the plastic bags back in</div>
    <div>The time was probably around two</div>
    <div>I had spent quite a while trying to decide on the water filtration system</div>
</div>

<ul class="fruit-list">
    {{ fruit(
        "https://github.com/it-is-wednesday/cute-sway-recorder",
        "cute-sway-recorder",
        "graphical screen recorder for sway and other <code>wlroots</code>-based window managers",
        "python"
    ) }}

    {{ fruit(
        "https://github.com/it-is-wednesday/pyinspect.el",
        "pyinspect.el",
        "quirky object fields inspection in running python process",
        "elisp"
    ) }}

    {{ fruit(
        "https://github.com/it-is-wednesday/pitzulit",
        "pitzulit",
        "shatter youtube albums into separate track files according to timestamps in the description",
        "ocaml"
    ) }}

    {{ fruit(
        "https://web-ebook.avocadosh.xyz/",
        "web-ebook.avocadosh.xyz",
        "converts webpages into <i>readable</i> epub/mobi/pdf files. like, removes the usual webshit clutter",
        "clojure") }}
</ul>
<a href="{{ SITEURL }}/theme/lastfm-collage.webp">
    <img class="wide-image" src="{{ SITEURL }}/theme/lastfm-collage.webp">
</a>
</div>
