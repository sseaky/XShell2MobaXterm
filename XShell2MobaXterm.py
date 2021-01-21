#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Seaky
# @Date:   2021/1/19 9:51

from configparser import RawConfigParser
from pathlib import Path
from copy import deepcopy
import sys

import os

PATTERN1 = '{name}=#{icon}#{protocol}%{host}%{port}%{user}'
PATTERN2 = '#MobaFont%10%0%0%0%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0#0#{description} #-1'

CLASS = {
    'SSH': {
        'data':
            {'name': '', 'icon': 109, 'protocol': 0, 'host': '', 'port': 22, 'user': '', 'keyfile': '',
             'description': ''},
        'pattern':
            PATTERN1 + '%%-1%-1%%%22%%0%0%0%{keyfile}%%-1%0%0%0%%1080%%0%0%1' + PATTERN2
    },
    'TELNET': {
        'data':
            {'name': '', 'icon': 98, 'protocol': 1, 'host': '', 'port': 23, 'user': '', 'description': ''},
        'pattern':
            PATTERN1 + '%%2%%22%%%0%0%%1080%' + PATTERN2
    },
    'FTP': {
        'data':
            {'name': '', 'icon': 130, 'protocol': 6, 'host': '', 'port': 21, 'user': '', 'description': ''},
        'pattern':
            PATTERN1 + '%-1%%0%0%0%0%%21%%%0%0%-1%0%0%0%' + PATTERN2
    },
}


def convert(source_dir, output):
    open(output, 'w').write('')
    for i, objs in enumerate(os.walk(source_dir)):
        root, dirs, files = objs
        open(output, 'a').write('[Bookmarks{}]\n'.format('_{}'.format(i) if i else ''))
        open(output, 'a').write('SubRep={}\n'.format(root))
        open(output, 'a').write('ImgNum=41\n')
        dir_path = Path(root)
        for file_name in files:
            if not file_name.endswith('.xsh'):
                continue
            file_path = dir_path / file_name
            # ConfigParser() 不能解析含 % 的字串
            config = RawConfigParser()
            config.read_file(open(file_path, encoding='utf-16'))
            protocol = config.get("CONNECTION", "Protocol")
            if protocol in ['SSH', 'FTP', 'TELNET']:
                d = deepcopy(CLASS[protocol]['data'])
                d.update({
                    'name': file_path.stem,
                    'host': config.get("CONNECTION", "Host"),
                    'port': config.get("CONNECTION", "Port"),
                    'user': config.get("CONNECTION:AUTHENTICATION", "UserName"),
                    'description': config.get("CONNECTION", "Description"),
                })
                open(output, 'a').write(CLASS[protocol]['pattern'].format(**d) + '\n')
            else:
                print('unknown {}, {}'.format(protocol, file_path))
        open(output, 'a').write('\n')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python XShell2MobaXterm.py <XShell_Sessions_dir>')
    elif not Path(sys.argv[1]).is_dir():
        print('Error: {} is not a valid source'.format(sys.argv[1]))
    else:
        source_dir = sys.argv[1]
        output = 'Xshell2MobaXterm.mxtsessions'
        convert(source_dir, output)
        print('Export {} to {} done.'.format(source_dir, output))
