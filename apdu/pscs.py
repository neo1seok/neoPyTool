
from __future__ import print_function
from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString

for reader in readers():
    try:
        connection = reader.createConnection()
        connection.connect()
        print(reader, toHexString(connection.getATR()))

        SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
        DF_TELECOM = [0x7F, 0x10]
        data, sw1, sw2 = connection.transmit(SELECT + DF_TELECOM)

    except NoCardException:
        print(reader, 'no card inserted')

import sys
if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)