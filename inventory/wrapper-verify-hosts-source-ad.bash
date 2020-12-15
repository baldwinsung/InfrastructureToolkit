#!/bin/bash

SYBASE_OCS=OCS-12_5
SYBASE=/usr/local/sybase
ODBCSYSINI=/opt/sybase/sybase-odbc-15.5

export SYBASE_OCS SYBASE ODBCSYSINI
/path/to/verify-hosts-source-ad.py | mail -s "verify" name@blah.comm
