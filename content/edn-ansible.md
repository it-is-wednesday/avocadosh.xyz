Title: Personal EDN Ansible Playbooks
Date: 2022-02-15
Tags: Ansible, Clojure

# Peek
Here's how most of the tasks look like:

```clojure
[{:name "hi"
  :hosts ["localhost"]

  :vars {:user "_____"
          :home "/home/{{ user }}"}

  :tasks
  [{:file {:path "{{ home }}/{{ item }}"
            :state "directory"}
    :loop [".local/bin"
            ".config/fish/functions"
            ".local/share/qutebrowser/userscripts"]}

    ...
```

Using multiline strings is straightforward, despite not being the prettiest thing I've seen:

```clojure
{:name "Sway environment variables"
  :blockinfile {:path "/etc/environment"
                :block "# https://wiki.archlinux.org/index.php/Wayland#Qt_5
export QT_QPA_PLATFORMTHEME=qt5ct
# https://github.com/swaywm/sway/issues/595
export _JAVA_AWT_WM_NONREPARENTING=1"}}
```

# Rationale
Nothing special, it's just fun to write in Clojure :) I do generally dislike YAML because of its extreme, uncalled-for minimalism. It may or may not lead to me shooting myself in the foot (it does).

If anything goes south, I can always resort back to it, anyways:

```sh
cat playbook.edn | bb '(-> *in* slurp edn/read-string (yaml/generate-string :dumper-options {:flow-style :block}))'
```

# Setup
Since every Ansible command I run requires a compilation step, I've written a short [Babashka](https://babashka.org/) script to act as a middleman on each Ansible run. Luckily, Babashka comes with YAML (and obviously EDN) support built-in.

```clojure
#!/bin/env bb
(import [java.io File])
(require '[clojure.core.match :refer [match]])
(require '[babashka.process :refer [process check]])

(defn edn->yaml
  [file-path]
  (-> file-path
      slurp
      edn/read-string
      (yaml/generate-string :dumper-options {:flow-style :block})))

(defn main
  [action edn-playbook extra-args]
  (let [exec      (format "ansible-%s" action)
        yaml-file (.getAbsolutePath (File/createTempFile "playbook" ".yaml"))
        cmd       (into [exec yaml-file] extra-args)]
    (spit yaml-file (edn->yaml edn-playbook))
    @(process cmd {:out :inherit})))

(match (vec *command-line-args*)
  [action playbook & args] (main action playbook args)
  [action playbook] (main action playbook [])
  :else (println "Usage: ednsible ACTION PLAYBOOK [EXTRA_ARGS]"))

nil
```

I saved the script as `ednsible` and created these two aliases to avoid unfortunate scenarios:

```shell
alias ednsible-playbook="ednsible playbook"
alias ednsible-lint="ednsible lint"
```

## Why convert to YAML instead of JSON?
An alternative path would be to generate JSON instead of YAML, since [JSON is supposedly a subset of YAML 1.2](https://yaml.org/spec/1.2.2/#12-yaml-history). However:

1. `ansible-lint` doesn't work at all when given a JSON playbook, even when
   given a JSON playbook that works perfectly with `ansible-playbook`
2. Seems like the subsettery topic is
   [controversial](https://metacpan.org/pod/JSON::XS#JSON-and-YAML). With my
   luck, I'm sure I'll step on a mine in this area; So I'd rather take the path
   of least resistance as YAML support is baked into Babashka :)
3. The YAML parser that comes with Babashka is
   [clj-yaml](https://github.com/clj-commons/clj-yaml), which is a wrapper
   around [SnakeYAML](https://mvnrepository.com/artifact/org.yaml/snakeyaml),
   which is a 1.1 parser 🙃

# Tooling
-   [zprint](https://cljdoc.org/d/zprint/zprint/)
    [[AUR](https://aur.archlinux.org/packages/zprint-bin)] for formatting. Its
    default style is a bit too agressive (mostly Clojure-focused, I guess) so I
    use `{:style :indent-only}`.
-   [clj-kondo](https://github.com/clj-kondo/clj-kondo) for linting, although
    admittedly there isn't a whole lot to lint here. Duplicate keys and
    mismatched quotes are the only possible pain points.

