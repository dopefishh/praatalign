#!/bin/env python
# -*- coding: utf-8 -*-

import mistune
with open('README.md', 'r') as f1:
    with open('README.html', 'w') as f2:
        f2.write("""\
<html>
    <head>
        <meta charset="UTF-8">
        <style>
            table, th, td {{
                border: 1px solid black;
                border-collapse: collapse;
            }}
            td {{
                vertical-align: baseline;
            }}
        </style>
        <title>Manual for praatalign</title>
    </head>
    <body>
    {}
    </body>
    </html>""".format(mistune.markdown(f1.read())))
