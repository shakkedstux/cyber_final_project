# CYBER PROJECT - CLIENT ( VERSION 1.0 ) BY SHAKKED STUX


from tkinter import *
import pickle
import socket
import select
import time


def new_member(member, groupname):

    global group, membersList

    try: # global may not exist, and mambersList.insert could not exist
        # So - what it is , is : if you are in a group page and same group (all of this same in new_massage)
        if group == groupname:
            membersList.insert(END, ", "+member)
    except:
        pass


def create_group(groupname):

    if groupname == "":
        create_join_group_page("Field is empty.")
    else:
        massageType = "8"
        send([massageType, groupname])


def contact_user(username):

    if username == "":
        create_join_group_page("Field is empty.")
    else:
        massageType = "7"
        send([massageType, username])


def quit_group_page(groupname):

    massageType = "6"
    send([massageType, groupname])


def log_out():

    massageType = "5"
    send([massageType])

    create_login_page("Fill the form to get in again.")


def new_massage(massageInfo):

    global group, massagesList
    groupname = massageInfo[2]
    sender = massageInfo[0]

    try:
        if group == groupname or group == sender:
            massagesList.config(state="normal")
            massagesList.insert(END, massageInfo[0] + ": " +  massageInfo[4])
            massagesList.insert(END, massageInfo[3].split()[1] + "\n \n")
            massagesList.see(END)
            massagesList.config(state="disabled")
    except:
        pass


def click(evt):
    try:
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print(value)
        massageType = "9"
        send([massageType, value])
    except:
        pass


def create_private_group_page(username, massages):

    global frame, group
    group = username
    frame.destroy()

    frame = Frame(window, height=300, width=400) # create new page
    frame.pack_propagate(0)
    frame.pack()

    top_widgets_frame = Frame(frame, height=50)
    top_widgets_frame.pack_propagate(0)
    Button(top_widgets_frame, text="Back", command = lambda: quit_group_page(username)).pack(side="right", fill=Y)
    Label(top_widgets_frame, text=" "+username+" ").pack(side="left", fill=Y)
    top_widgets_frame.pack(fill=X)

    scrollbarFrame = Frame(frame)
    scrollbar = Scrollbar(scrollbarFrame)
    scrollbar.pack(side="right", fill=Y)

    global massagesList
    massagesList = Text(scrollbarFrame, yscrollcommand = scrollbar.set, cursor="arrow")


    for massage in massages:
        massagesList.insert(END, massage[0] + ": " +  massage[4])
        massagesList.insert(END, massage[3].split()[1] + "\n \n")

    massagesList.config(state="disabled")
    massagesList.pack(fill=X)
    scrollbar.config(command = massagesList.yview)

    massagesList.see(END)

    send_massage_frame = Frame(frame, height="50")
    send_massage_frame.pack_propagate(0)
    Button(send_massage_frame, text="Send", command = lambda: [send_massage(username, "p", massageEntry.get("1.0",END)), massageEntry.delete('1.0', END)]).pack(fill=BOTH, side="right")
    massageEntry = Text(send_massage_frame, width="50")
    massageEntry.pack(fill=Y, side="left")
    send_massage_frame.pack(fill=X, side="bottom")

    scrollbarFrame.pack(fill=BOTH)


def send_massage(groupname, private, msg):

    massageType = "4"
    send([massageType, groupname, private, msg])


def create_group_page(groupname, massages, members):

    global frame, group
    group = groupname
    frame.destroy()

    frame = Frame(window, height=300, width=400) # create new page
    frame.pack_propagate(0)
    frame.pack()

    top_widgets_frame = Frame(frame, height=50)
    top_widgets_frame.pack_propagate(0)

    Button(top_widgets_frame, text="Back", command = lambda: quit_group_page(groupname)).pack(side="right", fill=Y)

    Label(top_widgets_frame, text=" "+groupname+" ").pack(side="left", fill=Y)

    membersScrollbarFrame = Frame(top_widgets_frame)
    scrollbar = Scrollbar(membersScrollbarFrame, orient='horizontal')
    scrollbar.pack(side="top", fill=X)

    global membersList
    membersList = Text(membersScrollbarFrame, xscrollcommand = scrollbar.set, cursor="arrow", relief='flat', padx=5)
    membersList.configure(background='SystemButtonFace')

    membersList.config(wrap='none')
    membersList.insert(END, ", ".join(members))

    membersList.pack(fill=BOTH)
    scrollbar.config(command = membersList.xview)

    membersScrollbarFrame.pack(side="left", fill=BOTH)
    top_widgets_frame.pack(fill=X)


    scrollbarFrame = Frame(frame)
    scrollbar = Scrollbar(scrollbarFrame)
    scrollbar.pack(side="right", fill=Y)

    global massagesList
    massagesList = Text(scrollbarFrame, yscrollcommand = scrollbar.set, cursor="arrow")

    for massage in massages:
        massagesList.insert(END, massage[0] + ": " +  massage[4])
        massagesList.insert(END, massage[3].split()[1] + "\n \n")

    massagesList.config(state="disabled")
    massagesList.pack(fill=X)
    scrollbar.config(command = massagesList.yview)

    massagesList.see(END)

    send_massage_frame = Frame(frame, height=50)
    send_massage_frame.pack_propagate(0)
    Button(send_massage_frame, text="Send", command = lambda: [send_massage(groupname, "g", massageEntry.get("1.0",END)), massageEntry.delete('1.0', END)]).pack(fill=BOTH, side="right")
    massageEntry = Text(send_massage_frame, width=50)
    massageEntry.pack(fill=Y, side="left")
    send_massage_frame.pack(fill=X, side="bottom")

    scrollbarFrame.pack(fill=BOTH)


def i_need_groups():

    massageType = "3"
    send([massageType])


def join_group(groupname):

    if groupname == "":
        create_join_group_page("Field is empty.")
    else:
        massageType = "2"
        send([massageType, groupname])


def create_join_group_page(msg):

    global frame
    frame.destroy()

    frame = Frame(window, height=300, width=400) # create new page
    frame.pack_propagate(0)
    frame.pack()

    button_frame = Frame(frame)
    Button(button_frame, text="Back", command = lambda: i_need_groups()).pack(side="left")
    button_frame.pack(fill=X)

    Label(frame, text=msg).pack()

    groupnameEntry = Entry(frame)
    groupnameEntry.pack()

    Button(frame, text="Contact user", command = lambda: contact_user(groupnameEntry.get())).pack()
    Button(frame, text="Join existing group", command = lambda: join_group(groupnameEntry.get())).pack()
    Button(frame, text="Create new group", command = lambda: create_group(groupnameEntry.get())).pack()


def create_groups_page(groups):

    global frame
    frame.destroy()

    frame = Frame(window, height=300, width=400) # create new page
    frame.pack_propagate(0)

    buttons_frame = Frame(frame)
    Button(buttons_frame, text="Connect to others", command = lambda: create_join_group_page("Enter name of group or user.")).pack(side="right")
    Button(buttons_frame, text="Log Out", command = lambda: log_out()).pack(side="left")
    buttons_frame.pack(fill=X)

    Label(frame, text="My contacts:").pack()


    scrollbarFrame = Frame(frame)
    scrollbar = Scrollbar(scrollbarFrame)
    scrollbar.pack(side="right", fill=Y)

    global groupsList
    groupsList = Listbox(scrollbarFrame, yscrollcommand = scrollbar.set)
    groupsList.bind("<<ListboxSelect>>", click)

    for group in groups:
        groupsList.insert(END, group[0])

    groupsList.pack(fill=BOTH)
    scrollbar.config(command = groupsList.yview)

    scrollbarFrame.pack(fill=BOTH)
    frame.pack()


def create(username, password):

    if len(username) == 0 or len(password) == 0:
        create_login_page("One field [or more] is empty.")
    else:
        global myName
        myName = username # you can put it at the beginning too, here is more efficient
        massageType = "0"
        send([massageType, username, password])


def login(username, password):

    global myName
    myName = username # all this in order for the window title to my name

    massageType = "1"
    send([massageType, username, password])


def create_login_page(msg):

    global frame, window
    window.title("")
    try: frame.destroy()
    except: pass

    frame = Frame(window, height=300, width=400) # create new page
    frame.pack_propagate(0)
    frame.pack()

    Label(frame).pack()
    Label(frame, text=msg).pack()

    Label(frame, text="Username:").pack()
    usernameEntry = Entry(frame)
    usernameEntry.pack()

    Label(frame, text="Password:").pack()
    passwordEntry = Entry(frame)
    passwordEntry.pack()

    Button(frame, text="Create user", command = lambda: create(usernameEntry.get(), passwordEntry.get())).pack()
    Button(frame, text="Log in", command = lambda: login(usernameEntry.get(), passwordEntry.get())).pack()


def send(massage):

    massage = pickle.dumps(massage)
    clientSocket.send(massage)


def massage(words):

    global window, myName
    massageType = words[0]

    if massageType == "0": # login fail
        create_login_page("No such user. Try again.")

    if massageType == "1": # server send groups list
        window.title(myName)
        create_groups_page(words[1])

    if massageType == "2": # server send massages in a group
        create_group_page(words[1], words[2], words[3])

    if massageType == "3": # the user you created already exist, or it is a name of a group
        create_login_page("Choose different username.")

    if massageType == "4": # server send massages in a private group
        create_private_group_page(words[1], words[2])

    if massageType == "5": # you have just ..
        create_join_group_page(words[1])

    if massageType == "6": # new massage
        new_massage(words[1])

    if massageType == "7": # new massage
        new_member(words[1], words[2])

    if massageType == "8": # new massage
        create_login_page("Someone logged in to this account.")


def listen():

    global clientSocket
    clientSocket = socket.socket(socket.SOCK_DGRAM)
    with open("connection_details.txt") as fp:
        lines = fp.read().splitlines()
        serverIp = lines[0].split(" ")[-1] # last word of first line
        port = lines[1].split(" ")[-1] # last word of second line
    clientSocket.connect((serverIp,int(port)))

    serverIsFine = True
    windowIsOpen = True
    size = 512
    while serverIsFine and windowIsOpen: # while server is still working
        rlist, wlist, xlist = select.select([clientSocket], [clientSocket], [])
        if len(rlist) != 0:
            try:
                msg = b''
                while True:
                    x = clientSocket.recv(size)
                    msg = msg + x
                    if len(x) < size:
                        break
                words = pickle.loads(msg)
                massage(words)
            except:
                serverIsFine = False

        try:
            window.update()
        except:
            windowIsOpen = False

        break_length = 0.2
        time.sleep(break_length)


def main():

    global window, frame
    window = Tk()
    window.title("")
    # window.geometry("300x240")
    window.option_add("*Font", ("Times New Roman",15))
    create_login_page("Welcome! Fill the form to get in.")
    listen()


if __name__ == '__main__':
    main()