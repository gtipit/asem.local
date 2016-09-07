#!/usr/bin/env python
# -*- coding: utf-8 -*-

from asem import asem
asem.debug = True


if __name__ == "__main__":
    asem.run(port=7777, host='0.0.0.0')
    #asem.run()


