from cliff.command import Command as BaseCommand
import logging
import shutil
import os


class Command(BaseCommand):
    """
    Generate .pot files from document sources, then update .po files from .pot files.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        TRANSLATION_PATH = os.path.join(self.app.doc_path, '_build/translation')

        shutil.rmtree(TRANSLATION_PATH)
        os.system('sphinx-build -b gettext %s %s' % (self.app.doc_path, TRANSLATION_PATH))

        for path, dirs, files in os.walk(TRANSLATION_PATH):
            for f in files:
                if f.endswith('.pot'):
                    pot_path = os.path.join(path, f)
                    p = pot_path[len(TRANSLATION_PATH) + 1:-1]
                    po_path = os.path.join(self.app.locale_path, p)

                    if not os.path.exists(os.path.dirname(po_path)):
                        os.makedirs(os.path.dirname(po_path))

                    if not os.path.exists(po_path):
                        os.system('msginit -i %s -o %s -l ru --no-translator' % (pot_path, po_path))
                    else:
                        os.system('msgmerge %s %s -U' % (po_path, pot_path))
