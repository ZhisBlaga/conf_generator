from tkinter import *
from tkinter import messagebox
from ipaddress import *
from tkinter.ttk import Combobox
import os


stp_priority = ['4096','8192','16384','32768']
confs = []

for a in os.listdir(path="default confs"):
    confs.append(a)


def create_config(file):
    ports = int(model.get().split('[')[1].split(']')[0])
    vlan = int(data_vlan.get())
    vlan_result = ''
    for i in range (0,ports):
        vlan_result+='create vlan VLAN'+str(vlan+i)+' tag '+str(vlan+i)+'\r'
        vlan_result+='config vlan VLAN'+str(vlan+i)+' add untagged '+str(i+1)+'\r'


    ip_addr = (IPv4Interface(ip.get()+'/'+mask.get()).with_netmask).split('/')[0]
    netmask = (IPv4Interface(ip.get() + '/' + mask.get()).with_netmask).split('/')[1]


    with open("default confs/"+file, 'r+') as f:
        read_data = f.read()
    read_data = read_data.replace('{{MGMT_VLAN}}', mgmt_vlan.get())
    read_data = read_data.replace('{{VLAN}}', vlan_result)
    read_data = read_data.replace('{{IP}}', ip_addr)
    read_data = read_data.replace('{{MASK}}', netmask)
    read_data = read_data.replace('{{HOSTNAME}}', hostname.get())
    read_data = read_data.replace('{{STP_PRIORITY}}', stp_prior.get())
    read_data = read_data.replace('{{GW}}',gw.get())
    with open (ip.get()+'.conf', 'w') as f:
        f.write(read_data)


def error_msg(text='Какая-то ошибка',title='Ошибка!'):
    messagebox.showinfo(title, text)

def check_fields():
    try:
        ip_address(ip.get())

    except ValueError:
        error_msg('Не верный IP')
        raise

    try:
        ip_address(gw.get())

    except ValueError:
        error_msg('Не верный GW')
        raise

    interface = IPv4Interface(gw.get()+'/'+mask.get())
    if IPv4Address(ip.get()) not in IPv4Network(interface.network):
        error_msg('IP: '+ip.get()+' не в сети '+ str(interface.network))
        raise
    if model.get() == '':
        error_msg('Выберите шаблон конфигурации!')
        raise
    create_config(model.get())

window = Tk()
window.title("Конфиг генератор v2")
window.geometry('450x250')

ip = Entry(window, width=15)
ip.grid(column=1, row=0)

lbl = Label(window, text="IP")
lbl.grid(column=0, row=0)

lbl = Label(window, text="/")
lbl.grid(column=2, row=0)

mask = IntVar()
mask.set(28)
mask = Spinbox(window, from_=10, to=32, width=2, textvariable=mask)
mask.grid(column=3, row=0)

lbl = Label(window, text="GW")
lbl.grid(column=0, row=1)

gw = Entry(window, width=15)
gw.grid(column=1, row=1)

lbl = Label(window, text="MGMT VLAN")
lbl.grid(column=2, row=1)

mgmt_vlan = IntVar()
mgmt_vlan.set(4086)
mgmt_vlan = Spinbox(window, from_=2, to=4096, width=4, textvariable=mgmt_vlan)
mgmt_vlan.grid(column=3, row=1)


lbl = Label(window, text="DATA VLAN")
lbl.grid(column=2, row=5)

data_vlan = IntVar()
data_vlan.set(1000)
data_vlan = Spinbox(window, from_=2, to=4096, width=4, textvariable=data_vlan)
data_vlan.grid(column=3, row=5)

lbl = Label(window, text="Hostname")
lbl.grid(column=0, row=2)

hostname = Entry(window, width=20)
hostname.grid(column=1, row=2)

lbl = Label(window, text="STP Pri.")
lbl.grid(column=0, row=4)

stp_pri = Combobox(window)
stp_pri['values'] = stp_priority
stp_pri.current(3)
stp_pri.grid(column=1, row=4)

lbl = Label(window, text="Шаблон конфигурации")
lbl.grid(column=0, row=3)

model = Combobox(window)
model['values'] = confs
model.grid(column=1, row=3)

btn = Button(window, text="Генерировать",command=check_fields)
btn.grid(column=3, row=10)
window.mainloop()