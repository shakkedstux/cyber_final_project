# CYBER PROJECT - SERVER ( VERSION 1.0 ) BY SHAKKED STUX


import socket
import select
import time
import pickle
import sqlite3
from datetime import datetime


def get_user_out(username):

    global sockets

    socket = username_socket(username)

    log_out(username)

    massageType = "8"
    send(socket, [massageType])


def send_new_member(socket, username, group):

    massageType = "7"
    massage = [massageType, username, group]

    send(socket, massage)


def send_new_member_to_all(groupname, username):

    global conn, usernames

    members = conn.execute("SELECT username FROM groups WHERE type = 'g' and contact = '{}'".format(groupname)).fetchall() # (usernames)

    for member in members:
        if member[0] in usernames: # members looks like - [('a',),('b',),('c',)..]
            send_new_member(username_socket(member[0]), username, groupname)


def go_to_massages(username, group):

    global conn

    x = conn.execute("SELECT type FROM groups WHERE contact = '{}' and username = '{}'".format(group, username)).fetchall()
    if x[0][0] == "c": # group is private
        return private_massages(username, group)
    return massages(group)


def contact_user(username, contact):

    global conn

    x = conn.execute("SELECT COUNT(1) FROM groups WHERE type = 'g' and contact = '{}'".format(contact)).fetchall()
    if x[0][0] == 0: # if connection wasn't made yet
        conn.execute("INSERT INTO groups (type, contact, username) VALUES ('c', '{}', '{}')".format(contact, username))
        conn.commit()

        return private_massages(username, contact)

    massageType = "5"
    return ([massageType, "Please choose different user."])


def create_group(username, groupname):

    global conn

    y = conn.execute("SELECT COUNT(1) FROM groups WHERE contact = '{}'".format(groupname)).fetchall() # not even letting you take a name that someone contacted , but not exists
    x = conn.execute("SELECT COUNT(1) FROM users WHERE username = '{}'".format(groupname)).fetchall()
    if y[0][0] + x[0][0] == 0: # if group not exist
        conn.execute("INSERT INTO groups (type, contact, username) VALUES ('g', '{}', '{}')".format(groupname, username))
        conn.commit()

        return massages(groupname)

    massageType = "5"
    return ([massageType, "Please choose different name."])


def quit_group_page(username, groupname):

    # inserting time to groups table where username = {} and groupname = {}
    # for now - works exactly like groups()

    return groups(username)


def log_out(username):

    global usernames
    index = usernames.index(username)
    usernames[index] = ""


def send_massage(socket, massageInfo):

    massageType = "6"
    massage = [massageType, massageInfo]

    send(socket, massage)


def send_massage_to_all(massageInfo):

    global conn, usernames

    groupname = massageInfo[2]
    members = conn.execute("SELECT username FROM groups WHERE contact = '{}'".format(groupname)).fetchall() # (usernames)

    for member in members:
        if member[0] in usernames: # members looks like - [('a',),('b',),('c',)..]
            send_massage(username_socket(member[0]), massageInfo)


def private_massages(username1, username2):

    global conn

    massages = conn.execute('''SELECT * FROM massages WHERE sendto = '{}' AND sender = '{}' OR
        sendto = '{}' AND sender = "{}" ORDER BY time'''.format(username1, username2, username2, username1)).fetchall()

    massageType = "4"
    return [massageType, username2, massages]


def new_massage(username, sendto, private, msg):

    global conn
    now = datetime.now()
    formattedNow = now.strftime('%Y-%m-%d %H:%M:%S')
    massageInfo = [username, private, sendto, formattedNow, msg] # sendto - groupname (or username)

    conn.execute('''INSERT INTO massages (sender, private, sendto, time, text)
    VALUES ('{}', '{}', '{}', '{}', '{}')'''.format(*massageInfo))
    conn.commit()

    if private == "p":
        send_massage(username_socket(username), massageInfo)
        if sendto in usernames:
            send_massage(username_socket(sendto), massageInfo)

    else:
        send_massage_to_all(massageInfo)


def massages(groupname): # returns massages and members in group , and also groupname

    global conn
    massages = conn.execute("SELECT * FROM massages WHERE sendto = '{}' ORDER BY time".format(groupname)).fetchall()
    members = conn.execute("SELECT username FROM groups WHERE contact = '{}'".format(groupname)).fetchall()
    for i in range(len(members)):
        members[i] = members[i][0]

    massageType = "2"

    return [massageType, groupname, massages, members]


def join_group(username, groupname):

    global conn

    y = conn.execute("SELECT COUNT(1) FROM groups WHERE type = 'g' and contact = '{}'".format(groupname)).fetchall()
    if y[0][0] != 0: # if there is a group
        x = conn.execute("SELECT COUNT(1) FROM groups WHERE type = 'g' and contact = '{}' AND username = '{}'".format(groupname, username)).fetchall()
        if x[0][0] == 0: # if he is not in it

            send_new_member_to_all(groupname, username)
            conn.execute("INSERT INTO groups (type, contact, username) VALUES ('g', '{}', '{}')".format(groupname, username))
            conn.commit()

        return massages(groupname)

    massageType = "5"
    return ([massageType, "No such group."])


def groups(username):

    global conn

    groupnames = conn.execute("SELECT contact FROM groups WHERE username = '{}'".format(username)).fetchall()

    massageType = "1"
    return [massageType, groupnames]


def login(username, password, socket):

    global conn, usernames, sockets
    x = conn.execute("SELECT COUNT(1) FROM users WHERE username = '{}' AND password = '{}'".format(username, password)).fetchall()

    if x[0][0] == 1:
        if username in usernames: # the user is already connected (ideally from another device)
            get_user_out(username)

        usernames[sockets.index(socket)] = username

        return groups(username)

    return ["0"]


def create_user(username, password, socket):

    global conn, usernames, sockets
    x = conn.execute("SELECT COUNT(1) FROM users WHERE username = '{}'".format(username)).fetchall()
    y = conn.execute("SELECT COUNT(1) FROM groups WHERE contact = '{}' and type = 'g'".format(username)).fetchall() # letting you take the name also if someone contacted this name

    if x[0][0] + y[0][0] >= 1:
        return ["3"]

    conn.execute("INSERT INTO users (username, password) VALUES ('{}', '{}')".format(username, password))
    conn.commit()

    usernames[sockets.index(socket)] = username

    massageType = "1"
    return [massageType, []] # [] - groups


def username_socket(x):

    if type(x) == str: # x is username
        return sockets[usernames.index(x)]

    return usernames[sockets.index(x)]


def send(socket, massage):

    massage = pickle.dumps(massage)
    if type(socket) == str: # clientSocket represent username, find the socket.
        socket = username_socket(socket)

    socket.send(massage)


def massage(words, socket):

    massageType = words[0]
    username = username_socket(socket)

    if massageType == "0": # client create user
        send(socket, create_user(words[1], words[2], socket))

    if massageType == "1": # client log in
        send(socket, login(words[1], words[2], socket))


    if massageType == "2": # client join group (2,7,8)
        send(socket, join_group(username, words[1]))


    if massageType == "3": # client need groups table
        send(socket, groups(username))

    if massageType == "4": # client send massage
        new_massage(username, words[1], words[2], words[3])

    if massageType == "5": # client logs out
        log_out(username)

    if massageType == "6": # client quits group(chat) page - For now SAME as "3"
        send(socket, quit_group_page(username, words[1]))

    if massageType == "7": # client contact user
        send(socket, contact_user(username, words[1]))

    if massageType == "8": # client creates group
        send(socket, create_group(username, words[1]))

    if massageType == "9": # client creates group
        send(socket, go_to_massages(username, words[1]))


def listen():

    serverSocket = socket.socket()
    port = 7784
    serverSocket.bind(("0.0.0.0",port))
    serverSocket.listen(10)

    global sockets, usernames
    sockets = []
    usernames = []
    size = 512
    while True:
        rlist, wlist, xlist = select.select([serverSocket] + sockets, sockets, [])

        for userSocket in rlist:

            if userSocket is serverSocket: # new user connected
                (new_socket, address) = serverSocket.accept()
                sockets.append(new_socket)
                usernames.append("")

            else:
                try:
                    msg = b''
                    while True:
                        x = userSocket.recv(size)
                        msg = msg + x
                        if len(x) < size:
                            break
                    words = pickle.loads(msg)
                    massage(words, userSocket)
                except: # user exited
                    index = sockets.index(userSocket)
                    sockets.pop(index)
                    usernames.pop(index)

        break_length = 0.2
        time.sleep(break_length)


def create_DB():

    global conn
    conn = sqlite3.connect('database.db')
    conn.execute("CREATE TABLE IF NOT EXISTS users (username text, password text);")
    conn.execute("CREATE TABLE IF NOT EXISTS groups (type text, contact text, username text);")
    conn.execute('''CREATE TABLE IF NOT EXISTS massages
        (sender text, private text, sendto text, time time, text text);''')


def main():

    create_DB() # if not exist
    listen()


if __name__ == '__main__':
    main()