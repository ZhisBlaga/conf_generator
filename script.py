from tkinter import *
from tkinter import messagebox
from ipaddress import *
from tkinter.ttk import Combobox
import os
import re


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
    read_data = read_data.replace('{{STP_PRIORITY}}', stp_pri.get())
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
    if re.findall('[а-яА-ЯёЁ]+',hostname.get()):
        error_msg('Нельзя использовать руссские символы в hostname!')
        raise
    create_config(model.get())

window = Tk()
window.title("Конфиг генератор v2")
# window.geometry('450x250')



lbl = Label(window, text="IP", font=("Arial Bold", 12))
lbl.grid(column=0, row=0, sticky='w')

ip = Entry(window, width=15, font=("Arial Bold", 12))
ip.grid(column=1, row=0, sticky='w')



lbl = Label(window, text="/", font=("Arial Bold", 12))
lbl.grid(column=2, row=0, sticky='w')

mask = IntVar()
mask.set(28)
mask = Spinbox(window, from_=10, to=32, width=2, textvariable=mask, font=("Arial Bold", 12))
mask.grid(column=3, row=0, sticky='w')

lbl = Label(window, text="GW", font=("Arial Bold", 12))
lbl.grid(column=0, row=1, sticky='w')

gw = Entry(window, width=15, font=("Arial Bold", 12))
gw.grid(column=1, row=1, sticky='w')

lbl = Label(window, text="MGMT", font=("Arial Bold", 12))
lbl.grid(column=2, row=1, sticky='w')

mgmt_vlan = IntVar()
mgmt_vlan.set(4086)
mgmt_vlan = Spinbox(window, from_=2, to=4096, width=4, textvariable=mgmt_vlan, font=("Arial Bold", 12))
mgmt_vlan.grid(column=3, row=1, sticky='w')


lbl = Label(window, text="DATA VLAN", font=("Arial Bold", 12))
lbl.grid(column=0, row=5, sticky='w')

data_vlan = IntVar()
data_vlan.set(1000)
data_vlan = Spinbox(window, from_=2, to=4096, width=4, textvariable=data_vlan, font=("Arial Bold", 12))
data_vlan.grid(column=1, row=5, sticky='w')

lbl = Label(window, text="Hostname", font=("Arial Bold", 12))
lbl.grid(column=0, row=2, sticky='w')

hostname = Entry(window, width=15, font=("Arial Bold", 12))
hostname.grid(column=1, row=2, sticky='w')

lbl = Label(window, text="STP Pri.", font=("Arial Bold", 12))
lbl.grid(column=0, row=4, sticky='w')

stp_pri = Combobox(window,font=("Arial Bold", 12),width=14)
stp_pri['values'] = stp_priority
stp_pri.current(3)
stp_pri.grid(column=1, row=4, sticky='w')

lbl = Label(window, text="Шаблон конфигурации", font=("Arial Bold", 12))
lbl.grid(column=0, row=3, sticky='w')

model = Combobox(window, font=("Arial Bold", 12), width=14)
model['values'] = confs
model.grid(column=1, row=3, sticky='w')

btn = Button(window, text="Генерировать",command=check_fields, font=("Arial Bold", 12))
btn.grid(column=1, row=6)
window.mainloop()