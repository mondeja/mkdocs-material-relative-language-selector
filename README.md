# mkdocs-material-relative-language-selector

[![PyPI version][project-pypi-version-badge]][project-pypi-link]

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

## Configuration

- If you want to publish your site in Github Pages, you don't need to define any
 setting because is the default configuration.
- If you want to serve your site
 under a custom root domain, define `root_domain: true` to get correct links
 between languages.

## Projects using it

- [mkdocs-mdpo-plugin][mkdocs-mdpo-plugin-link]


[mkdocs-material-ss-link]: https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/#site-language-selector
[mkdocs-mdpo-plugin-link]: https://mondeja.github.io/mkdocs-mdpo-plugin/
[project-pypi-version-badge]: https://img.shields.io/pypi/v/mkdocs-material-relative-language-selector?label=version
[project-pypi-link]: https://pypi.org/project/mkdocs-material-relative-language-selector/
