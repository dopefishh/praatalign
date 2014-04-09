#!/bin/env python
# -*- coding: utf-8 -*-

import phonetizer

ph = phonetizer.PhonetizerTzeltal(ruleset='./ruleset.tze')
print ph.phonetize('ma\'rt')
print ph.phonetize('mart')
