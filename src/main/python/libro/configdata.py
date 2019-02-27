from libro.ui.style import Style, AccentColor

style = [('OS default', Style.default),
         ('Fusion bright', Style.bright),
         ('Fusion dark', Style.dark)]

accent_color = [('Theme default', AccentColor.default),
                ('Blue', AccentColor.blue),
                ('Red', AccentColor.red),
                ('Orange', AccentColor.orange),
                ('Yellow', AccentColor.yellow),
                ('Green', AccentColor.green),
                ('Purple', AccentColor.purple),
                ('Rose', AccentColor.rose),
                ('Gray', AccentColor.gray)]

output_format = ['epub', 'mobi', 'azw3', 'kepub']
notes_type = ['default', 'float', 'inline', 'block']
apnx_type = ['none', 'eink', 'app']
log_level = ['none', 'normal', 'debug']
log_mode = ['append', 'overwrite']

title_format = ['#title',
                '{(#abbrseries{ #padnumber}) }#title',
                '{(#ABBRseries{ #padnumber}) }#title',
                '#title{ (#series{ #number})}']

author_format = ['{#f }#l', '#l{ #f{ #m}}', '#l{ #f}']
