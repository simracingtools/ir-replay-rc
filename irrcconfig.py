# Copyright (C) 2020 rbaus
# 
# This file is part of ir-replay-rc.
# 
# ir-replay-rc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ir-replay-rc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ir-replay-rc.  If not, see <http://www.gnu.org/licenses/>.

import configparser
import sys

class IrrcConfig:

    def __init__(self):
        self.config = configparser.ConfigParser()    
        try: 
            self.config.read('irrc.ini')
        except Exception as ex:
            print('unable to read configuration: ' + str(ex))
            sys.exit(1)

    def getWsUrl(self):
        if self.config.has_option('connect', 'wsUrl'):
            return self.config['connect']['wsUrl']
        else:
            return ''
