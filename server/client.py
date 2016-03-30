#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, select, string, sys, json, base64

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

#main function
if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print 'Usage : python ', __file__,' hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to remote host
    try :
        s.connect((host, port))
        s.setblocking(0)
    except :
        print 'Unable to connect'
        sys.exit()


    print 'Connected to remote host. Start sending messages'
    prompt()

    while 1:
        rlist = [sys.stdin, s]

        # Get the list sockets which are readable
        read_list, write_list, error_list = select.select(rlist , [], [])


        for sock in read_list:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print datan
                    remain = ''
                    datalist = data.split('}')[:-1]
                    for data in datalist:
                        data = remain + data + '}'
                        print '\n Server: ',
                        try:
                            data = json.loads(data)
                        except ValueError, e:
                            remain += data
                            continue

                        sys.stdout.write(json.dumps(data))

                        if data.get('action', None) == 0 and data['behave'] == 'file_upload':
                            s.send(json.dumps(dict(
                                action = 0, # user type
                                behave = 'file_program'
                            )) + '\n')
                        print
                    prompt()

            #user entered a message
            else :
                msg = sys.stdin.readline()
                msg = msg[:-1]
                s.send(msg + '\n')
                prompt()
