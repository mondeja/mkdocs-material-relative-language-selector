# mkdocs-material-relative-language-selector

Edit the builtin [mkdocs-material site selector][mkdocs-material-ss-link] to
make the links between languages relative.

- If you have in Github Pages the URL `https://foo.github.io/bar/es/config/`,
 you can access it from the URL `https://foo.github.io/bar/config/` selecting
 Spanish in the language selector.
- The current language being displayed will be removed from the language
 selector, so you will only capable to access to other languages than the
 current.

## Installation

```
pip install mkdocs-material-relative-language-selector
```

## Example configuration

### With [mkdocs-mdpo-plugin][mkdocs-mdpo-plugin-link]

```yaml

theme:
  name: material
  language: en

plugins:
  - search
  - material-relative-language-selector
  - mdpo

extra:
  alternate:
    - name: English
      lang: en
    - name: Español
      link: es
      lang: es

```

## Projects using it

- [mkdocs-mdpo-plugin][mkdocs-mdpo-plugin-link]


[mkdocs-material-ss-link]: https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/#site-language-selector
[mkdocs-mdpo-plugin-link]: https://mondeja.github.io/mkdocs-mdpo-plugin/
