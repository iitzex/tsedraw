# -*- coding: utf-8 -*-
from util import get_list


def generator(name):
    with open(name + '.html', 'w') as f:
        html_head = '''
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

        </head>
        <body >
    '''
        html_end = '''
        </body>
    </html>
    '''

        print('Generating HTML of ' + name.upper() + ' ...')
        html_body = ''
        for sid, title in get_list(name):
            html_body += "<p align=center>" + sid + title + "<p/>\n"
            html_body += "<img src='" + 'pic/' + sid + '.png' + "'  height='80%' width='100%' />\n"

        html_text = html_head + html_body + html_end
        f.write(html_text)


if __name__ == '__main__':
    generator('tse')
    generator('otc')
    generator('my')
    generator('watch')

