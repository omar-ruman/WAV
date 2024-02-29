from tkinter import *
from tkinter import messagebox as msg
import tkinter as tk
import pandas as pd
from datetime import datetime
import datetime

import time
import serial
import serial.tools.list_ports # for arduino autoconnection
import winsound
from pathlib import Path
import os
import sys

import cv2
from PIL import Image, ImageTk


global total_weight_v 
global total_volume_v
total_volume_v = 0
total_weight_v = 0
global df 

def data_frame_creator_load_dataset():
    global df

    exist_excel_name = 'data\\wav_' + str(datetime.datetime.now().strftime("%d_%m_%Y")) + '_machine_data.xlsx'
    try :
        df = pd.read_excel(exist_excel_name)
    except:
        _df = pd.DataFrame(columns=["System_id","Date_Time","Weight(KG)","Height(CM)","Lenght(CM)","Wide(CM)","Volume"])
        _df.to_excel(exist_excel_name,index=False)
        df = pd.read_excel(exist_excel_name)

data_frame_creator_load_dataset()


global e_system_id_v
global e_weight_v
global e_height_v
global e_length_v
global e_width_v

'''
########################################################### capture Image #################################################

sys_id_image = 'test'
vid_image = cv2.VideoCapture(1)

vid_image.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
vid_image.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
def ab(a):
    global vid_image
    vid_image = cv2.VideoCapture(a)

    vid_image.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    vid_image.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def capture_image():
    global sys_id_image, vid_image
    

    ret, frame = vid_image.read()
    if ret:
        # Get the current date and time
        now = datetime.now()
        dt_string = str(sys_id_image) + now.strftime("_%d_%m_%Y_%H%M%S")
        # Create the picture folder if it does not exist
        if not os.path.exists("pictures"):
            os.makedirs("pictures")
        # Save the captured image in the pictures folder
        image_name = os.path.join("pictures", f"{dt_string}.png")
        cv2.imwrite(image_name, frame)
        print(f"Image saved as {image_name}")
    else:
        print("Error: failed to capture image")
############################################################################################################################
'''
arduino_port = 0
def machine_auto_connection():
    # auto_connection_trying_count = 0
    arduino_baudrate = 115200
    global arduino_port,arduinoData

    time.sleep(0.5)
    # Get a list of all available serial ports
    ports = serial.tools.list_ports.comports()

    # Look for a port with matching baud rate
    for port in ports:
        try:
            # Try to open the port with the Arduino's baud rate
            ser = serial.Serial(port.device, arduino_baudrate)
            ser.close()
            # Store the COM port number in a variable
            arduino_port = port.device
            arduinoData = serial.Serial(str(arduino_port).lower(),115200)
            time.sleep(0.5)
            try:
                a,b,c,d = get_mdata()
            except:
                pass
            btn_con = Button(root,text="Connect",width=7,background = 'green', activebackground='red',foreground='white',activeforeground='white',borderwidth=4,font=('arial',8,'bold'),height=1,command=connect_machine).place(x=910,y=670)
            msg.showinfo('Message','Machine is connected!')
        except:
            try:
                a,b,c,d = get_mdata()
                btn_con = Button(root,text="Connect",width=7,background = 'green', activebackground='red',foreground='white',activeforeground='white',borderwidth=4,font=('arial',8,'bold'),height=1,command=connect_machine).place(x=910,y=670)
                msg.showinfo('Message','Machine is already connected!!!')
            except:
                msg.showerror('ERROR','Unable to connect Automaticall. Please select com port and click on CONNECT button or Try Again !')

def connect_machine():

    global arduinoData
    manual_comnumber = com_option.get()
    print(manual_comnumber)
    if manual_comnumber == 'com0':
        machine_auto_connection()

    else:
        try :
            data_frame_creator_load_dataset()
            comnumber = com_option.get()
            arduinoData = serial.Serial(comnumber,115200)

            webnumber = int(web_option.get())
            #ab(webnumber)

            #msg.showinfo('Message','WAV and Camera are connected!')
            btn_con = Button(root,text="Connect",width=7,background = 'green', activebackground='red',foreground='white',activeforeground='white',borderwidth=4,font=('arial',8,'bold'),height=1,command=connect_machine).place(x=910,y=670)
            msg.showinfo('Message','Machine is connected!')

        except:
            try:
                try:
                    data_frame_creator_load_dataset()
                    comnumber = com_option.get()
                    arduinoData = serial.Serial(comnumber,115200)
                    btn_con = Button(root,text="Connect",width=7,background = 'green', activebackground='red',foreground='white',activeforeground='white',borderwidth=4,font=('arial',8,'bold'),height=1,command=connect_machine).place(x=910,y=670)
                    msg.showinfo('Message','Only WAV is connected!')
                except:
                    a,b,c,d = get_mdata()
                    btn_con = Button(root,text="Connect",width=7,background = 'green', activebackground='red',foreground='white',activeforeground='white',borderwidth=4,font=('arial',8,'bold'),height=1,command=connect_machine).place(x=910,y=670)
                    msg.showinfo('Message','Machine is already connected!!!')
            except:
                msg.showerror('ERROR','Machine is not connected!')



# df updation 
def df_updator(df_sys_val,df_w_val,df_hei_val,df_len_val,df_wide_val):
    global df,sys_id_image

    #print('df updation')
    df_append_time_now = datetime.datetime.now().replace(microsecond=0)
    df_vol_val = float(df_hei_val)*float(df_len_val)*float(df_wide_val)



    if (len(df[df["System_id"]==df_sys_val])>0): # if system_id is duplicated then just updates the values for the same system_id 
        index_val = df[df["System_id"]==df_sys_val].index[0]
        df['Date_Time'].iloc[index_val] = df_append_time_now
        df['Weight(KG)'].iloc[index_val]= df_w_val
        df['Height(CM)'].iloc[index_val] = df_hei_val
        df['Lenght(CM)'].iloc[index_val] = df_len_val
        df['Wide(CM)'].iloc[index_val] = df_wide_val
        df['Volume'].iloc[index_val]= df_vol_val
        #print(df_append_time_now,df_sys_val,df_w_val,df_hei_val,df_len_val,df_wide_val,df_vol_val,"duplicate")

    else:
        df_append_data_list = [[df_sys_val,df_append_time_now,df_w_val,df_hei_val,df_len_val,df_wide_val,df_vol_val]]
        df1 = pd.DataFrame(df_append_data_list,columns=["System_id","Date_Time","Weight(KG)","Height(CM)","Lenght(CM)","Wide(CM)","Volume"])
        df = pd.concat([df,df1],axis=0)
        #print(df_append_time_now,df_sys_val,df_w_val,df_hei_val,df_len_val,df_wide_val,df_vol_val)

    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True,inplace=True)

    #taking image 
  
    #print('run')
    
# showing total weight and volume value
def show_total():
    global cantotalw,cantotalv,df
    canvas.itemconfig(cantotalw,text=round(df["Weight(KG)"].astype('float').sum(),2))
    canvas.itemconfig(cantotalv,text=round(df["Volume"].astype('float').sum(),2))

    
# showing latest weight and volume value
def show_lates_value(sidlast,weightlast,heightlast,lenlast,wde):
    global can1,can2,can3,can4,can5,can6,df

    pc = df.last_valid_index()+1

    canvas.itemconfig(can1,text=pc)
    canvas.itemconfig(can2,text=sidlast)
    canvas.itemconfig(can3,text=weightlast)
    canvas.itemconfig(can4,text=heightlast)
    canvas.itemconfig(can5,text=lenlast)
    canvas.itemconfig(can6,text=wde)


# key_input method
def key_input():
    #e_system_id_v,e_weight_v,e_height_v,e_length_v,e_width_v,total_weight_v,total_volume_v):
    global total_volume_v,total_weight_v,e_system_id_v,e_weight_v,e_height_v,e_length_v,e_width_v
    e_system_id_v = e_system_id.get()
    e_weight_v = e_weight.get()
    e_height_v = e_height.get()

    e_length_v = e_length.get()
    e_width_v = e_width.get()


    try:
        total_weight_v = total_weight_v+float(e_weight_v)
    except:
        msg.showwarning('Warning','Enter Correct Weight')
        pass

    try:
        total_volume_v = float(total_volume_v) + (float(e_height_v)*float(e_length_v)*float(e_width_v))
    except:
        msg.showwarning('Warning','Enter Correct Height,Length,Width')
        pass # warning -- please input right value for height,length,width

    #df_updator()  ------ will update here with new value
    try:
        df_updator(e_system_id_v,e_weight_v,e_height_v,e_length_v,e_width_v)
        show_lates_value(e_system_id_v,e_weight_v,e_height_v,e_length_v,e_width_v)
        show_total()
    except:
        print('key input is not working')
        pass
        

def get_mdata():
    global bfinal,afinal,cfinal,dfinal #x,y,z,w
    try:
        loopcount = 0
        while True :
            time.sleep(0.5)
            
            firstval = (arduinoData.read(arduinoData.inWaiting()).decode("utf-8").split("\n")[-2]).split(',')
            #time.sleep(2)
            time.sleep(1)
            secondval = (arduinoData.read(arduinoData.inWaiting()).decode("utf-8").split("\n")[-2]).split(',')
            #time.sleep(2)
            time.sleep(0.5)
            thirdval = (arduinoData.read(arduinoData.inWaiting()).decode("utf-8").split("\n")[-2]).split(',')

            a1 = round(float(firstval[0]))
            a2 = round(float(secondval[0]))
            a3 = round(float(thirdval[0]))

            b1 = round(float(firstval[1]))
            b2 = round(float(secondval[1]))
            b3 = round(float(thirdval[1]))

            c1 = round(float(firstval[2]))
            c2 = round(float(secondval[2]))
            c3 = round(float(thirdval[2]))

            d1 = round(float(firstval[3])/1000,2)
            d2 = round(float(secondval[3])/1000,2)
            d3 = round(float(thirdval[3])/1000,2)

            if ((abs(a1-a2)+abs(a1-a3)+abs(a2-a3)<=3)&(abs(b1-b2)+abs(b1-b3)+abs(b2-b3)<=3)&(abs(c1-c2)+abs(c1-c3)+abs(c2-c3)<=3)&(abs(d1-d2)+abs(d1-d3)+abs(d2-d3)<=0.09)):
                afinal = round((a1+a2+a3)/3) #y
                bfinal = round((b1+b2+b3)/3) #x
                cfinal = round((c1+c2+c3)/3) #z
                dfinal = round((d1+d2+d3)/3,2) #w
                #print('wide:',121-afinal,'--height:',115-cfinal,'--length:',bfinal,dfinal)
                return(bfinal,afinal,cfinal,dfinal)
            else:
                loopcount = loopcount+1
                if (loopcount>4):
                    msg.showwarning("Warning!","Try Again . Unable to Detect the object")
                    break

                #print('hoinai')
                pass
    except:
        pass

def get_data_by_getbtn():
    global x,y,z,final_w # x=wide y=length z=height
    try:
        system_id_in_get_btn = 'parcel_'+str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        x,y,z,final_w = get_mdata()
        x = x if x>4 else 0
        y = y if y>4 else 0
        z = z if z>2 else 0
        final_w = final_w if final_w>20 else 0

        df_updator(system_id_in_get_btn,final_w,z,x,y)
       
        show_lates_value(system_id_in_get_btn,final_w,z,x,y)
        show_total()
        #winsound.MessageBeep()
    except:
        msg.showwarning('Warning','Please check the Machine Connections !!!')

def get_data_by_Auto():

    global auto_after_id
    qr.focus_set()
    try:
        qrresult = str(qr.get())
        if len(qrresult)>12 & (len(qrresult)<30):
            #print('halaluiya')
            system_id_in_auto = qrresult
            x,y,z,final_w = get_mdata() # x=wide y=length z=height

            x = x if x>4 else 0
            y = y if y>4 else 0
            z = z if z>2 else 0
            final_w = final_w if final_w>20 else 0


            df_updator(system_id_in_auto,final_w,z,x,y)
            show_lates_value(system_id_in_auto,final_w,z,x,y)
            show_total()
            #winsound.MessageBeep()
            qr.delete(0,'end')
        else:
            pass

        auto_after_id = root.after(2000,get_data_by_Auto)
    except:
        btn_auto = Button(root,text="AUTO",width=10,height=3,background = '#1f6086', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4,font=('arial',11,'bold'),command=get_data_by_Auto_first).place(x=205,y=139)

        msg.showwarning('WARNNIG!','Please check the Connections !')


def get_data_by_Auto_first():
    btn_auto = Button(root,text="AUTO",width=10,height=3,background = '#52c401', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4,font=('arial',11,'bold')).place(x=205,y=139)

    get_data_by_Auto()


def download_df():
    exist_excel_name = 'data\\wav_' + str(datetime.datetime.now().strftime("%d_%m_%Y")) + '_machine_data.xlsx'
    df.to_excel(exist_excel_name,index=False)

    ask = msg.askquestion('Message','Do you want to download the data ?')
    if ask == 'yes':  
            try:
                path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
                filename=path_to_download_folder+'\\weight_and_volume_file_'+str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))+'.xlsx'
                df.to_excel(filename,index=False)
                msg.showinfo('Message','Data has been downloaded successfully !!!')
            except:
                filename='weight_and_volume_file_'+str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))+'.xlsx'
                df.to_excel(filename,index=False)
                msg.showinfo('Message','Data has been downloaded successfully !!!')
    else:
        pass

def stop_all_functin():
    qr.delete(0,'end')

    btn_auto = Button(root,text="AUTO",width=10,height=3,background = '#1f6086', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4,font=('arial',11,'bold'),command=get_data_by_Auto_first).place(x=205,y=139)
    
    root.after_cancel(auto_after_id)





root = Tk()
root.title("WaV by COCOO")
root.geometry("1100x750")
root.resizable(False,False)
root.config(bg='#ff0000')
root.iconbitmap('weighing-machine.ico')
#appicon = PhotoImage(file="D:\\# aaa weight machine\\python code\\tkinter code\\wmicon.png")
#root.iconphoto(True,appicon)

canvas = Canvas(root, width=1100, height=750,bg='blue')
phto = PhotoImage(file='bg2.png')
canvas.create_image(0,0,image=phto,anchor=NW)

#,activeforeground='white'6
#154c79, #1f6086,
#063970

########################## B U T T O N S ################################
btn_home = Button(root,text="Home",width=5,height=2,background = '#1f6086', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4, font=('time',11,'bold'),command=stop_all_functin).place(x=522,y=81)
btn_auto = Button(root,text="AUTO",width=10,height=3,background = '#1f6086', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4,font=('arial',11,'bold'),command=get_data_by_Auto_first).place(x=205,y=139)
btn_get = Button(root,text="GET",width=10,height=3,background = '#1f6086', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4,font=('arial',11,'bold'),command=get_data_by_getbtn).place(x=371,y=139)
btn_small_pac = Button(root,text="Small Package",background = '#1f6086', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4,font=('arial',11,'bold'),width=15,height=2).place(x=640,y=271)
btn_large_pac = Button(root,text="Large Package",background = '#1f6086', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4,font=('arial',11,'bold'),width=15,height=2).place(x=860,y=271)
btn_key_inp = Button(root,text="Key Input",background = '#1f6086', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4,font=('arial',11,'bold'),width=15,height=2,command=key_input).place(x=745,y=395)
btn_con = Button(root,text="Connect",width=7,background = 'red', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4,font=('arial',8,'bold'),height=1,command=connect_machine).place(x=910,y=670)
btn_download = Button(root,text="Download",width=7,height=1,background = '#1f6086', activebackground='#063970',foreground='white',activeforeground='white',borderwidth=4,font=('arial',8,'bold'),command=download_df).place(x=991,y=670)

#btn_home.configure(background='red',foreground='while') exxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

'''ellipse = canvas.create_oval(10,10,100,100,outlook='black',fill='red')
buttonxx = tk.Button(canvas,text='exx')
canvas.create_window(50,50,window=buttonxx,width=80,height=80)'''




########################### com dropdown ###################################
com_option = StringVar()
com_option.set('com0')
com_dropdown = OptionMenu(root,com_option,'com1','com2','com3','com4','com5','com6','com7','com8')
com_dropdown.configure(background='#cfcfcf',font=('arial',8,'bold'))
com_dropdown.place(x=820,y=671)

web_option = StringVar()
web_option.set('0')
web_dropdown = OptionMenu(root,web_option,'0','1','2')
web_dropdown.configure(background='#cfcfcf',font=('arial',8,'bold'))
web_dropdown.place(x=760,y=671)

canvas.create_text(858,710,text='wav_com',fill='Black',font=('arial',8,'bold'))
canvas.create_text(783,710,text='web_cam',fill='Black',font=('arial',8,'bold'))


########################## area ################################
# serial number
canvas.create_rectangle(165, 220, 280, 250 , fill='#23bdfa')
canvas.create_rectangle(165, 265, 535, 295, fill='#23bdfa')
canvas.create_rectangle(165, 310, 535, 340, fill='#23bdfa')
canvas.create_rectangle(165, 355, 535, 385, fill='#23bdfa')
canvas.create_rectangle(165, 400, 535, 430, fill='#23bdfa')
canvas.create_rectangle(165, 445, 535, 475, fill='#23bdfa')

# total weight and total volume
canvas.create_rectangle(165, 520, 340, 550, fill='#23bdfa')
canvas.create_rectangle(355, 520, 535, 550, fill='#23bdfa')

# df
canvas.create_rectangle(50, 600, 750, 700)

# menu bar
canvas.create_rectangle(1, 1, 1099, 40,fill='#04484b')



########################## label out area ################################
canvas.create_text(105,237,text='Parcel Count',fill='Black',font=('arial',11,'bold'))
canvas.create_text(300,237,text='QR',fill='Black',font=('arial',11,'bold'))
canvas.create_text(105,282,text='System ID',fill='Black',font=('arial',11,'bold'))
canvas.create_text(105,328,text='Weight',fill='Black',font=('arial',11,'bold'))
canvas.create_text(105,373,text='Height',fill='Black',font=('arial',11,'bold'))
canvas.create_text(105,418,text='Length',fill='Black',font=('arial',11,'bold'))
canvas.create_text(105,463,text='Width',fill='Black',font=('arial',11,'bold'))
canvas.create_text(247,505,text='Total Weight',fill='Black',font=('arial',11,'bold'))
canvas.create_text(437,505,text='Total Volume',fill='Black',font=('arial',11,'bold'))
#Label (root, text='Serial NO',bg='blue').place(x=80,y=224)
#Label (root, text='System ID',font=('time',11),bg='blue').place(x=80,y=269)
#Label (root, text='Weight').place(x=88,y=314)
#Label (root, text='Height').place(x=91,y=359)
#Label (root, text='Length').place(x=89,y=404) 16 16
#Label (root, text='Width').place(x=93,y=449)

#Label (root, text='Total Weight').place(x=210,y=495)
#Label (root, text='Total Volume').place(x=400,y=495)
canvas.create_text(513,327,text='(KG)',fill='Black',font=('arial',11,'bold'))
canvas.create_text(511,372,text='(CM)',fill='Black',font=('arial',11,'bold'))
canvas.create_text(511,417,text='(CM)',fill='Black',font=('arial',11,'bold'))
canvas.create_text(511,462,text='(CM)',fill='Black',font=('arial',11,'bold'))

#Label (root, text='(KG)').place(x=500,y=314)
#Label (root, text='(CM)').place(x=498,y=359)
#Label (root, text='(CM)').place(x=498,y=404)
#Label (root, text='(CM)').place(x=498,y=449)

canvas.create_text(655,345,text='System ID',fill='Black',font=('arial',11,'bold'))
canvas.create_text(745,345,text='Weight',fill='Black',font=('arial',11,'bold'))
canvas.create_text(837,345,text='Height',fill='Black',font=('arial',11,'bold'))
canvas.create_text(925,345,text='Length',fill='Black',font=('arial',11,'bold'))
canvas.create_text(1015,345,text='Width',fill='Black',font=('arial',11,'bold'))
#Label (root, text='System ID').place(x=620,y=332)
#Label (root, text='Weight').place(x=720,y=332)

#Label (root, text='Height').place(x=812,y=332)
#Label (root, text='Length').place(x=905,y=332)
#Label (root, text='Width').place(x=995,y=332)
################################# creating empty values of total and others ########################

can1 = canvas.create_text(200,235,text='',fill='Black',font=('arial',15)) # percel count
can2 = canvas.create_text(250,280,text='',fill='Black',font=('arial',10)) # system id
can3 = canvas.create_text(200,325,text='',fill='Black',font=('arial',15)) # weight
can4 = canvas.create_text(200,370,text='',fill='Black',font=('arial',15)) # height
can5 = canvas.create_text(200,415,text='',fill='Black',font=('arial',15)) # length
can6 = canvas.create_text(200,460,text='',fill='Black',font=('arial',15)) # wide


cantotalw = canvas.create_text(215,535,text='',fill='Black',font=('arial',15)) #total weight
cantotalv = canvas.create_text(430,535,text='',fill='Black',font=('arial',15)) #total volume

canvas.create_text(1050,735,text= 'COOCO',fill='Black',font=('italic',14))

########################### entry values ###################################
e_system_id = Entry(root,background ='#cfcfcf' ,borderwidth=3)
qr = Entry(root,background='#cfcfcf',borderwidth=2)
e_weight = Entry(root,background ='#cfcfcf' ,borderwidth=3)
e_height = Entry(root,background ='#cfcfcf' ,borderwidth=3)
e_length = Entry(root,background ='#cfcfcf' ,borderwidth=3)
e_width = Entry(root,background ='#cfcfcf' ,borderwidth=3)

e_system_id.place(x=610,y=355,height=27, width=90)
qr.place(x=320,y=223,height=27,width=210)
e_weight.place(x=700,y=355,height=27, width=90)
e_height.place(x=790,y=355,height=27, width=90)
e_length.place(x=880,y=355,height=27, width=90)
e_width.place(x=970,y=355,height=27, width=90)


canvas.pack()

def closefun():
    exist_excel_name = 'data\\wav_' + str(datetime.datetime.now().strftime("%d_%m_%Y")) + '_machine_data.xlsx'
    df.to_excel(exist_excel_name,index=False)

    ask = msg.askquestion('Message','Do you want to download the data and close the app?')
    if ask == 'yes':    
        filename='weight_and_volume_file_'+str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))+'.xlsx'
        df.to_excel(filename,index=False)
        msg.showinfo('Message','Data has been downloaded successfully !!!')
        root.destroy()
    else:
        root.destroy()

root.protocol("WM_DELETE_WINDOW",closefun)
root.mainloop()
