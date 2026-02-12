import os
import polib

def generate_mo_from_po(po_path, mo_path):
    """Compile a .po file to .mo format using polib"""
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    
    # Load the .po file explicitly using UTF-8 to avoid decoding issues
    try:
        po = polib.pofile(po_path, encoding='utf-8')
    except TypeError:
        # Older polib versions may not accept the encoding kwarg; read file text instead
        with open(po_path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        po = polib.pofile(content)

    # Save as .mo file
    po.save_as_mofile(mo_path)
    print(f'Compiled {mo_path}')

# Compile the files
base_path = 'core/locales'
for lang in ['fa', 'de', 'fr']:
    po_file = f'{base_path}/{lang}/LC_MESSAGES/messages.po'
    mo_file = f'{base_path}/{lang}/LC_MESSAGES/messages.mo'
    if os.path.exists(po_file):
        generate_mo_from_po(po_file, mo_file)
    else:
        print(f'⚠ Skipped {po_file} (not found)')


