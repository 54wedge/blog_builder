# README
## Introduction
A simple python script that copy the `body` tag in a html and paste it in template html then automatically generate navigation, archive and more.
## Feature
1. Take html file as input instead of Markdown file.
2. Simple and straight-forward template system without learning new stuff like `Jinja`
3. Build by amateur with the idea that even amateur should be able to understand what's going on during building
## Dependency
1. `bs4` for html parse
2. `maya` for time parse
3. `PyYAML` for meta data
4. `htmlmin` for minify html file
## Get started
1. `pip3 install bs4 maya PyYAML htmlmin`
2. `python3 build.py`
## meta data
Create a code block and specify the language to `meta` in the markdown editor so that the meta data can be read by the script. The meta data block should follow be in `yaml` style and here is an example:
```
Title: [the title you want]
Date: [the date you want]
Tag:
 - [one blank space only]
 - [second tag]
More_meta: [more meta you need]
```
The supported meta are below

| name     | type   | optional | fallback | Note |
|:---------|:-------|:---------|:---------|:-----|
| Title    | string | yes      | 1. `<h1>` tag in the html<br>2. Untitled | the `<h1>` tag will be removed is it is considered as title |
| Author   | string | yes      | Site-Author in config.yml |  |
| Date     | string | yes      | | Common styles of date string should be accepted.|
| Tag      | list   | yes      |  |  |
| Category | string | yes      | Default |  |
| Custom_name   | string | yes      |  | replace strings in the html braced with `%%` like %%Custom_name%% |
| Abstract      | string   | yes      | 1.strings before `<!--more-->`<br>2. No Abstract | the function is within index.py |

Note: missing the meta data block will give you a warning while missing meta data will not give you a warning 