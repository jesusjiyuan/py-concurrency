#!/usr/local/python27/bin/python2.7
# -*- coding: utf-8 -*-

import os
import socket
import sys
from supervisor import childutils
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def send_mail(info):
    mail_host = "smtp.163.com"
    mail_user = "python@163.com"
    mail_pass = "123456"
    from_addr = 'python@163.com'
    to_addr = ['123@qq.com']

    msg = MIMEText(info, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'supervisord 管理员 <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(u'测试 supervisord Exit', 'utf-8').encode()

    smtpObj = smtplib.SMTP_SSL(mail_host,465)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(from_addr, to_addr, msg.as_string())


class CrashMail:
    def __init__(self):

        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def runforever(self, test=False):
        # 死循环, 处理完 event 不退出继续处理下一个
        while 1:
            # 使用 self.stdin, self.stdout, self.stderr 代替 sys.* 以便单元测试
            headers, payload = childutils.listener.wait(self.stdin, self.stdout)

            if test:
                # headers = {'ver': '3.0', 'poolserial': '4', 'len': '79', 'server': 'supervisor', 'eventname': 'PROCESS_STATE_EXITED', 'serial': '4', 'pool': 'crashmail'}
                self.stderr.write(str(headers) + '\n')

                # payload = 'processname:00 groupname:showImageWater from_state:RUNNING expected:1 pid:19499'
                self.stderr.write(payload + '\n')
                self.stderr.flush()

            if not headers['eventname'] == 'PROCESS_STATE_EXITED':
                # 如果不是 PROCESS_STATE_EXITED 类型的 event, 不处理, 直接向 stdout 写入"RESULT\nOK"
                childutils.listener.ok(self.stdout)
                continue

            # 解析 payload, 这里我们只用这个 pheaders.
            # pdata 在 PROCESS_LOG_STDERR 和 PROCESS_COMMUNICATION_STDOUT 等类型的 event 中才有
            # pheaders = {'from_state': 'RUNNING', 'processname': '00', 'pid': '19494', 'expected': '0', 'groupname': 'EvalueShow'}

            pheaders, pdata = childutils.eventdata(payload + '\n')

            # 过滤掉 expected 的 event, 仅处理 unexpected 的
            # 当 program 的退出码为对应配置中的 exitcodes 值时, expected=1; 否则为0
            if int(pheaders['expected']):
                childutils.listener.ok(self.stdout)
                continue

            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            # 构造报警内容
            msg = "Host: %s(%s)\nProcess: %s\nPID: %s\nEXITED unexpectedly from state: %s" % \
                  (hostname, ip, pheaders['groupname'], pheaders['pid'], pheaders['from_state'])

            self.stderr.write('unexpected exit, mailing\n')
            self.stderr.flush()

            send_mail(msg)

            # 向 stdout 写入"RESULT\nOK"，并进入下一次循环
            childutils.listener.ok(self.stdout)


def main():

    # listener 必须交由 supervisor 管理, 自己运行是不行的
    if not 'SUPERVISOR_SERVER_URL' in os.environ:
        sys.stderr.write('crashmail must be run as a supervisor event '
                         'listener\n')
        sys.stderr.flush()
        return

    prog = CrashMail()
    prog.runforever(test=True)


if __name__ == '__main__':
    main()