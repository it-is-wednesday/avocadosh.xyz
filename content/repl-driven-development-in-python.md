Title: Attempting REPL-Driven Development in Python
Slug: repl-driven-development-in-python
Date: 2021-10-07
Tags: Python

Be wary that this article is Emacs-centric, but you can take some ideas out of
here for other editors as well. A lot of the heavy lifting here is done by
IPython, therefore is ideally editor-agnostic.

Here are a couple of plugins/articles for other editors that may be relevant:

- [https://github.com/jpalardy/vim-slime](https://github.com/jpalardy/vim-slime)
- [https://code.visualstudio.com/docs/python/editing#_run-selectionline-in-terminal-repl](https://code.visualstudio.com/docs/python/editing#_run-selectionline-in-terminal-repl)
-   [https://marketplace.visualstudio.com/items?itemName=pancho111203.vscode-ipython](https://marketplace.visualstudio.com/items?itemName=pancho111203.vscode-ipython)

# Defining REPL-Driven Development
I'd rather have you read the article [What makes a good
REPL?](https://vvvvalvalval.github.io/posts/what-makes-a-good-repl.html) by
Valentin Waeselynck than reading me pretentiously attempting to write *yet
another* definition, but the main gist for me with RDD is having a tighter
feedback loop during the exploration part of writing a program.  I can inspect
each variable's current value instantly, building upon the already evaluated
program state. Using a REPL saves me from:

- Re-writing the boilerplate setup code for fiddling
- Waiting for re-compilation
- Waiting for database queries/network requests/long computations (more than
  half a second)

I have frequently found myself losing my train of thought within a measly
amount of time, and shaving the above list off my workflow indeed helped me. Is
it a generational thing?

Do note that all of this hassle is mainly for *convenience*. It's not make or
break. However, it is more *fun* to program with instant feedback, and some
argue it's more productive. I'm not here for productivity, though.

Here's a nice screencast by Sean Corfield demonstrating RDD:  
[https://www.youtube.com/watch?v=UFY2rd05W2g](https://www.youtube.com/watch?v=UFY2rd05W2g)

## Other Forms of Interactive Development
RDD isn't the only way to get a tighter feedback loop! The official Clojure
guide [suggests a couple of
alternatives](https://clojure.org/guides/repl/guidelines_for_repl_aided_development#_the_repl_is_not_the_only_tool_for_interactive_development)
itself: auto-reloading tests, static analysis, and live reload. They all sound
fun as well and can be achieved with Python:

- [https://github.com/watchexec/watchexec](https://github.com/watchexec/watchexec) -
  run a command on file change; can be used to run tests
- [http://mypy-lang.org/](http://mypy-lang.org/) - crippled static analysis
- [https://github.com/teodorlu/hotload](https://github.com/teodorlu/hotload) -
  live code reload

# Module Auto-Reload
Mikel Evins mentions in [this
article](https://mikelevins.github.io/posts/2020-12-18-repl-driven/) the
feature of automatic change detection and re-evaluation:

> [...] try this in your favorite repl:
>
> Define a datatype. I mean a class, a struct, a record type--whatever
> user-defined type your favorite language supports. Make some instances
> of it. Write some functions (or methods, or procedures, or whatever)
> to operate on them.
>
> Now change the definition of the type. What happens?
>
> Does your language runtime notice that the definition of the type has
> changed? Does it realize that the existing instances have a new
> definition? When something touches one of them, does it automatically
> reinitialize it to conform to the new definition, or, if it doesn't
> know how to do that, does it start a breakloop and ask you what to do
> about it?
>
> If the answer is "yes," then you're probably using a Lisp or Smalltalk
> system. If the answer is "no," then you're missing a crucial element
> of repl-driven development.

IPython's [built-in autoreload
extension](https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html)
can imitate this effect. Dump the following into
`~/.ipython/profile_default/ipython_config.py`:

```python
c.InteractiveShellApp.extensions = ["autoreload"]
c.InteractiveShellApp.exec_lines = ["%autoreload 2"]
```

`%autoreload 2` instructs IPython to automatically
[reload](https://docs.python.org/dev/library/importlib.html#importlib.reload)
modules that have been imported in the current session once their files change
on disk. It does satisfy the realization and automatic reinitialization bit.

The breakloop bit maybe can be imitated with IPython's `--pdb` flag,
but I don't regularly use it. Don't count on me.

!!! cautious ""
    Python modules were not designed to be constantly reloaded, and this
    hack may peskily backfire. Make sure to read these before using this
    trick:
    
    - [https://nedbatchelder.com/blog/201908/why_your_mock_doesnt_work.html](https://nedbatchelder.com/blog/201908/why_your_mock_doesnt_work.html)
    -   [https://docs.python.org/dev/library/importlib.html#importlib.reload](https://docs.python.org/dev/library/importlib.html#importlib.reload)
    -   [https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html#caveats](https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html#caveats)
    
    Thanks to HN user sedachv for linking these pages in [this
    comment](https://news.ycombinator.com/item?id=25626085).

# Object Exploration
Part of REPL-driven development is constantly evaluating variables,
either because they changed or you forgot their value.

Python's heavy usage of objects imposes a bit of a challenge here, as
opposed to Clojure's preference of primitives. We'll talk about my
half-assed solution to this later; let's start with the low hanging
fruits instead :)

## Expanding Primitives

You have a variable holding a primitive value or an expression that can
be evaluated into a primitive value. You evaluate it and see its value
in the REPL. Not rocket science. Here's the function I use to achieve
it, along with an example usage GIF:

```emacs-lisp
(defun print-python-expression-in-repl ()
  "Implying the first statement of the line is actually an expression, prints
its value at the REPL."
  (interactive)
  (let ((initial-point (point)))
    ;; mark expression at point
    (beginning-of-line)
    (set-mark (point))
    (python-nav-end-of-statement)

    ;; print marked expression in python shell
    (let* ((region-start (min (+ 1 (point)) (point-max)))
           (expr (string-trim-right
                  (buffer-substring-no-properties region-start (mark)))))
      (python-shell-send-string
       (format "print(); print('=> %s'); print(%s, end='')" expr expr)))

    (deactivate-mark)
    (goto-char initial-point)))

(define-key python-mode-map (kbd "C-c C-k") 'print-python-expression-in-repl)
```

![Print Expression](static/python-rdd/print-expression.gif)

## Exploring Complex Class Instances

UPDATE 2021/10/18: I've written
[pyinspect.el](https://github.com/it-is-wednesday/pyinspect.el) to solve
this problem more formally. Take a look!

While enlightened programmers like us prefer to overuse dictionaries,
most Python libraries tend to make extensive usage of objects instead.
This tendency doesn't cleanly align with our development method, which
is constantly peeking at our variables\' values.

Examining objects isn't that smooth of a process since many of the info
we'll need is idiomatically hidden behind methods that may execute
arbitrary code. Non-method fields are a different story, though, and
inspecting them is often useful.

[SymonSoft's ppretty library](https://github.com/symonsoft/ppretty)
comes in clutch and does exactly that --- list an object's current
fields and their values, without cluttering our screen with all of its
methods. Let's integrate it into our workflow. IPython config:

```python
c.InteractiveShellApp.exec_lines = [
    "%autoreload 2",
    """
    from ppretty import ppretty as ppretty_temp
    def ppretty(obj):
        print(ppretty_temp(obj, seq_length=99, show_properties=True, depth=3), end='')
    """,
]
```

Emacs function:

```emacs-lisp
(defun print-python-object-fields-in-repl ()
  "Sends symbol at point to IPython REPL with the `ppretty' function defined in ipython_config.
Lists the object's non-method fields and their respective current values."
  (interactive)
  (let ((sym (symbol-at-point)))
    (python-shell-send-string
     (format "print(); print('=> %s'); ppretty(%s)" sym sym))))

(define-key python-mode-map (kbd "C-c C-o") 'print-python-object-fields-in-repl)
```

Here's how it looks like: ![ppretty](static/python-rdd/ppretty.gif)

## Exploring Functionality
IPython exposes a handy shortcut for the built-in `help()` function:
[the ?
operator](https://ipython.readthedocs.io/en/stable/interactive/tutorial.html#exploring-your-objects).
It may not as essential for RDD as the rest of things I mention in this
article, yet I still use it a lot. Here's how it looks like:

![Magic "?"](static/python-rdd/magic-question-mark.png)

# Rich Comment Blocks
Writing [Rich Comment
Blocks](https://betweentwoparens.com/blog/rich-comment-blocks/) is a common
Clojure practice for having "save point" or boilerplate for your REPL-driven
development journey. It's a comment block below your actual code, it's only
evaluated by you when you use the REPL, and it's ignored outside of it.
Here's what it looks like:

```clojure
(comment
  (do
   (require '[my.app.db :as app.db])
   (require '[my.app.cart :as cart])
   (def db (app.db/connection!)))

  (cart/add db {:item-name "iPhone"})
  )
```

The gist is that everything inside `(comment)` is ignored by the Clojure
compiler, and is only evaluated manually by the programmer in their editor.
This functionality isn't possible in Python, but if we pretend it is, here's
how the above code would look like translated into idiomatic Python:

```python
everything_here_is_ignored_by_the_interpreter:
     import my_app_db as app_db
     db = app_db.connection()
     db.add_to_cart("iPhone")
```

We probably *could* find a pretentious way to achieve the same functionality by
abusing some obscure feature combination of IPython, but they would all confuse
your teammates. I feel like the most straightforward solution is having a
temporary throwaway buffer to experiment in. I've written a small function to
achieve this:

```emacs-lisp
(defun python-testbed ()
  "Throwaway buffer with no syntax checking, merely mimicking Clojure's rich comment blocks."
  (interactive)
  (split-window-vertically)
  (other-window 1)
  (generate-new-buffer "Python testbed")
  (switch-to-buffer (format "%s testbed" (buffer-name)))
  (python-mode)
  (flycheck-mode 0))
```

Here's how the workflow looks like:

![Testbed Buffer](static/python-rdd/testbed-example.gif)

# Looking Forward
Packing all these tricks into an [nREPL
server](https://nrepl.org/nrepl/beyond_clojure.html) might make some lives
easier. Stay tuned eh?
