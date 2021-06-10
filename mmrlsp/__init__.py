"""mkdocs-material-relative-language-selector-plugin"""

import os
import tempfile

import mkdocs
from mkdocs.config.config_options import Type


__version__ = '1.1.0'


class MkdocsMaterialRelativeLanguageSelectorPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('github_pages', Type(bool, default=True)),
        ('root_domain', Type(bool, default=False)),
    )

    def __init__(self, *args, **kwargs):
        self._docs_assets_javascript_path = None

    def on_config(self, config, **kwargs):
        if self.config['root_domain']:
            self.config['github_pages'] = False
        elif not self.config['github_pages']:
            self.config['github_pages'] = True

    def on_files(self, files, config):
        """Add 'relative-material-language-selector.js' script to the files
        of the build.
        """
        new_files = files

        if config['theme'].name != 'material':  # not using material theme
            msg = (
                'relative-material-language-selector only available with'
                ' mkdocs-material theme'
            )
            raise mkdocs.config.base.ValidationError(msg)

        theme_language = config['theme']['language']
        if not theme_language:
            msg = (
                'relative-material-language-selector only available defining'
                ' the \'language\' option of mkdocs-material theme'
                ' configuration'
            )
            raise mkdocs.config.base.ValidationError(msg)

        if config.get('extra_javascript'):
            docs_assets_javascripts_dir = os.path.abspath(
                os.path.join(
                    config['docs_dir'],
                    os.path.dirname(config['extra_javascript'][0]),
                ),
            )
        else:
            docs_assets_dir = os.path.join(config['docs_dir'], 'assets')
            if not os.path.isdir(docs_assets_dir):
                os.mkdir(docs_assets_dir)
            docs_assets_javascripts_dir = os.path.join(
                docs_assets_dir,
                'javascripts',
            )

            config['extra_javascript'] = []

        if not os.path.isdir(docs_assets_javascripts_dir):
            os.mkdir(docs_assets_javascripts_dir)

        filename = 'material-relative-language-selector.js'
        docs_assets_javascript_path = os.path.join(
            docs_assets_javascripts_dir,
            filename,
        )

        self._docs_assets_javascript_path = docs_assets_javascript_path

        if not os.path.isfile(docs_assets_javascript_path):
            with tempfile.TemporaryDirectory() as dirname:
                javascript_template_filepath = os.path.join(
                    os.path.abspath(os.path.dirname(__file__)),
                    filename,
                )

                temp_filepath = os.path.join(dirname, 'mmrlsp.js')
                with open(javascript_template_filepath) as f:
                    template_content = f.read()

                new_content = template_content.replace(
                    '{{original_lang}}',
                    theme_language,
                ).replace(
                    '{{root_domain}}',
                    'true' if self.config['root_domain'] else 'false',
                )

                with open(temp_filepath, 'w') as f:
                    f.write(new_content)

                os.rename(temp_filepath, docs_assets_javascript_path)

        rel_assets_javascript_path = os.path.relpath(
            docs_assets_javascript_path,
            config['docs_dir'],
        )

        config['extra_javascript'].append(rel_assets_javascript_path)

        rel_mls_filepath = mkdocs.structure.files.File(
            rel_assets_javascript_path,
            config['docs_dir'],
            config['site_dir'],
            config['use_directory_urls'],
        )
        new_files.append(rel_mls_filepath)

        return new_files

    def on_post_build(self, config):
        if os.path.isfile(self._docs_assets_javascript_path):
            try:
                os.remove(self._docs_assets_javascript_path)
            except PermissionError:
                pass
