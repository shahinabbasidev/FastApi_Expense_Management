from core.i18n.translator import get_translator
for lang in ['de','fr','fa','en']:
    tr=get_translator(lang)
    print(lang, tr.gettext('User has been removed successfully.'))
