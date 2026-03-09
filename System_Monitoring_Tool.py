import psutil
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

monitoring = True
after_job = None

#Log File
LOG_FILE = "system_log.txt"

#Store CPU history for graph
cpu_data = []
time_data = []


#---------------------------------
#Logging Function
#---------------------------------
def log_system_info(cpu,ram,disk):
    with open(LOG_FILE,"a") as file:
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        file.write(f"{timestamp} | CPU : {cpu}% | RAM: {ram}% | Disk: {disk}%\n")
        

#-------------------------------
#Update Graph
#-------------------------------
def update_graph():
    ax.clear()
    ax.plot(time_data,cpu_data)
    ax.set_title("CPU USAGE GRAPH")
    ax.set_ylabel("CPU %")
    ax.set_xlabel("Time")
    canvas.draw()
    

    
#--------------------------------
#Monitoring Loop
#--------------------------------
def update_System_info():
    global monitoring,after_job
    
    if not monitoring:
        return
    
    
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    cpu_label.config(text = f"CPU usage: {cpu}%")
    ram_label.config(text = f"RAM usage: {ram}%")
    disk_label.config(text = f"Disk usage: {disk}%")
    
    cpu_data.append(cpu)
    time_data.append(len(cpu_data))
    
    if len(cpu_data) > 20:
        cpu_data.pop(0)
        time_data.pop(0)
        
    update_graph()
    
    log_system_info(cpu,ram,disk)    
    
    root.after(2000,update_System_info)
    


#--------------------------------
#Show Running Processes
#--------------------------------
def show_processes():
    process_window = tk.Toplevel(root)
    process_window.title("Running Processes")
    
    text = tk.Text(process_window,width =60,height = 20)
    text.pack()
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            text.insert(tk.END, f"PID: {proc.info['pid']} | {proc.info['name']}\n")
        except:
            pass    


#--------------------------------
#Start Monitoring
#--------------------------------
def start_monitoring():
    global monitoring
    monitroing = True
    update_System_info()
    
#--------------------------------
#Stop Monitoring
#--------------------------------
def stop_monitoring():
    global monitoring
    monitoring = False
    
    if after_job is not None:
        root.after_cancel(after_job)
        
    messagebox.showinfo("System Monitor","Monitoring stopped Successfully")
    

#--------------------------------
#Kill Process
#--------------------------------
def kill_process():
    pid = pid_entry.get()
    
    try: 
        process = psutil.Process(int(pid))
        process.terminate()
        messagebox.showinfo("Success","Process terminated")
    except:
        messagebox.showerror("Error", "Invalid PID")
        process.terminate()    
        
        
#--------------------------------
#Exit Program
#--------------------------------
def exit_program():
    global monitoring
    
    if after_job is not None:
        root.after_cancel(after_job)
    
    root.destroy()
    root.quit()
    
    messagebox.showinfo("System Monitor","Program stopped Successfully.")

    
        
#--------------------------------
#GUI Setup
#--------------------------------
root = tk.Tk()
root.title("System Monitoring Tool")
root.geometry("800x600")        

title = tk.Label(root,text = "System Monitoring Dashboard", font =("Arial",16))
title.pack(pady=10)

cpu_label = tk.Label(root, text ="CPU Usage:", font = ("Arial",12))
cpu_label.pack()

ram_label = tk.Label(root,text = "RAM Usage:",font=("Arial",12))
ram_label.pack()

disk_label = tk.Label(root,text = "Disk Usage:",font=("Arial",12))
disk_label.pack()


#Buttons
start_button = tk.Button(root, text="Start Monitoring", command = start_monitoring)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Monitoring", command = stop_monitoring)
stop_button.pack(pady=5)


process_button = tk.Button(root, text = "Show Running Processes", command = show_processes)
process_button.pack(pady=5)

pid_entry = tk.Entry(root)
pid_entry.pack()

kill_button = tk.Button(root, text="Kill Process by PID", command=kill_process)
kill_button.pack(pady=5)


exit_button = tk.Button(root, text = "Exit Program", command = exit_program)
exit_button.pack(pady=5)


#-------------------------------------
#Graph setup
#-------------------------------------
fig,ax = plt.subplots(figsize=(5,3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()


#Start Monitoring
update_System_info()

root.mainloop()

    
            
        
        
    
    