from wagtail.images.formats import Format, register_image_format


# Atempting to implement Image Size Options:
#    https://erev0s.com/blog/wagtail-list-tips-and-tricks/#add-a-custom-widthheight-image-in-the-rich-text-editor
register_image_format(Format('footer-col-head', 'footerColumnHeader25', 'richtext-image footer-col-head', 'max-25x25'))
register_image_format(Format('max-50', 'Max50', 'richtext-image max-50', 'max-50x50'))
register_image_format(Format('max-100', 'Max100', 'richtext-image max-100', 'max-100x100'))
register_image_format(Format('max-150', 'Max150', 'richtext-image max-150', 'max-150x150'))
register_image_format(Format('max-250', 'Max250', 'richtext-image max-250', 'max-250x250'))
register_image_format(Format('max-350', 'Max350', 'richtext-image max-350', 'max-350x350'))
register_image_format(Format('max-500', 'Max500', 'richtext-image max-500', 'max-500x500'))
register_image_format(Format('max-750', 'Max750', 'richtext-image max-750', 'max-750x750'))
