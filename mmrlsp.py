"""mkdocs-material-relative-language-selector-plugin"""

import os
import tempfile

import mkdocs


class MkdocsMaterialRelativeLanguageSelectorPlugin(mkdocs.plugins.BasePlugin):
    def on_files(self, files, config):
        """Add 'relative-material-language-selector.js' script to the files
        of the build.
        """
        new_files = mkdocs.structure.files.Files([])

        if config['theme'].name != 'material':  # not using material theme
            msg = (
                'relative-material-language-selector only available with'
                ' mkdocs-material theme'
            )
            raise mkdocs.config.base.ValidationError(msg)

        theme_language = config['theme'].get('language')
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
