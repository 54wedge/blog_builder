README
### Introduction
A simple python script that copy the `<body>` tag in a html file and paste it into template html file then automatically generate navigation, archive and more.

### Feature
1. Take html file as input instead of Markdown file.
2. Simple and straight-forward template system without learning new stuff like `Jinja`
3. Build by amateur with the idea that even amateur should be able to understand what's going on during building

### Dependency
1. `bs4` for html parse
3. `PyYAML` for meta data
4. `htmlmin` for minify html file

### Get started
1. `pip3 install bs4 PyYAML htmlmin`
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
| Custom_name   | string | yes      |  | replace strings in the html like {@Custom_name@} |
| Abstract      | string   | yes      | 1.strings before `<!--more-->`<br>2. "No Abstract" | the function is within index.py |

Note: Missing the meta data block will give you a warning while missing meta data will not give you a warning

### Template
#### Template related
Can be found in `template.html`, `archive.html`, `category.html`, `home.html` and `tag.html`

| Variable | Usage | Optional |
|:--|:--|:--|
| {@Page_Title@} | The title of the page | NO |
| {@Base@} | Site prefix | NO |

| Module | Usage | Optional |
|:--|:--|:--|
| {&Content&} | Use for user content | NO |
| {&Nav_module&} | Use for navigation | NO |
| {&Post_module&} | Use for list of posts | NO |
| {&Home_mini_post_list&} | Use for list of posts for home page | NO |
| {&Archive_post_list&} | Use for list of posts for archive page | NO |

#### User content related
Can be found in `post.html` and `page.html`.
These variables are defined in meta data

| Variable | Usage | Optional |
|:--|:--|:--|
| {@Title@} | Title | Yes |
| {@Author@} | Author | Yes |
| {@Date@} | Date | Yes |
| {@Category@} | Category | Yes |
| {@Tag@} | Tag | Yes |
| {@Variable@} | Variable | Yes |

| Module | Usage | Optional |
|:--|:--|:--|
| {&Body&} | User content | NO |
| {&Category&} | A link to Category page | Yes |
| {&Tag&} | Links to Tag pages | Yes |

### Performance
different option in safe_saving() and time spent:
str(100%) < minify(~300%) < prettify(~400%)

### Known issue
1. save prettified html will add extra blankspace in `<code>` tag. Use prettify option for debug.

### Credit
- The github flavor markdown stylesheet is obtained from [github-markdown-css](https://github.com/sindresorhus/github-markdown-css)
- The nightmode of the github flavor markdown stylesheet is obtained from [iA-Writer-Templates](https://github.com/iainc/iA-Writer-Templates/blob/master/GitHub.iatemplate/Contents/Resources/github-markdown-night-mode.css) with modify
