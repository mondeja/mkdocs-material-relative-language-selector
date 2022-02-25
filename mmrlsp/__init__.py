"""mkdocs-material-relative-language-selector-plugin"""

import os
import tempfile
import uuid

import mkdocs
from mkdocs.config.config_options import Type


__version__ = '1.1.1'


class MkdocsMaterialRelativeLanguageSelectorPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('github_pages', Type(bool, default=True)),
        ('root_domain', Type(bool, default=False)),
    )

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

        tempdir = tempfile.gettempdir()

        temp_filepath_exists = True
        while temp_filepath_exists:
            temp_filepath = os.path.join(
                tempdir,
                uuid.uuid4().hex + '.js',
            )
            temp_filepath_exists = os.path.exists(temp_filepath)

        javascript_template_filepath = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'material-relative-language-selector.js',
        )

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

        clean_temp_filepath = os.path.join(tempdir, 'mmrls.js')
        if os.path.isfile(clean_temp_filepath):
            os.remove(clean_temp_filepath)
        os.rename(
            temp_filepath,
            clean_temp_filepath,
        )

        rel_mls_filepath = mkdocs.structure.files.File(
            os.path.basename(clean_temp_filepath),
            tempdir,
            os.path.join(config['site_dir'], 'assets'),
            config['use_directory_urls'],
        )
        new_files.append(rel_mls_filepath)

        return new_files
