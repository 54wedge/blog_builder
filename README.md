README
### Introduction
A simple python script that copy the `<body>` tag in a html file and paste it into template html file then automatically generate navigation, archive and more.

### Feature
1. Take html file as input instead of Markdown file.
2. Simple and straight-forward template system without learning new stuff like `Jinja`
3. Build by amateur with the idea that even amateur should be able to understand what's going on during building

### Dependency
1. `bs4` for html parse
2. `maya` for time parse
3. `PyYAML` for meta data
4. `htmlmin` for minify html file

### Get started
1. `pip3 install bs4 maya PyYAML htmlmin`
2. `python3 build.py`

### Pages
- Register `[Page_name]` in `config.yml` when adding a new page
- Name rendered html as `index.html` and put it in a folder with `[Page_name]` folder
- Put the `[Page_name]` folder in `/[Source_folder]`
- There are two buildin page `_Home` and `_Archive`
- Sort pages in `config.yml`
- Case matters
- Include meta data in page

### Posts
- Put rendered html file in `/[Source_folder]/post`
- `[html_name]` will be part of the permalink to the post
- Include meta data in post

### Sample file tree for source folder
```
/source folder
  |- /post
       |- post_1.html
       |- post_2.html
  |- /page_1
       |- index.html
  |- /page_2
       |- index.html
```
Note: You can put your local images anywhere inside `/[Source_folder]` as long as they are accessible by source html file. (You can see the image when you open the source html file)

### Meta data
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
| Abstract      | string   | yes      | 1.strings before `<!--more-->`<br>2. "No Abstract" | the function is within index.py |

Note: Missing the meta data block will give you a warning while missing meta data will not give you a warning

### Template
Working
