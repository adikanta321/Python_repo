import tkinter

window=tkinter.Tk()

window.geometry("800x500+100+50")

window.title("Employee Registration")

window['bg']='#00ffaa'

window.config(bg="#00ffff")

header=tkinter.Label(window,text= "Employee Registration",font=("Arial",22),fg="blue",bg="#00ffff",justify='center')
l1=tkinter.Label(window,text="EmployeeNo",font=("Arial",18),fg="red",bg="#00ffff",justify='center')
l2=tkinter.Label(window,text="EmployeeName",font=("Arial",18),fg="red",bg="#00ffff",justify='center')
l3=tkinter.Label(window,text="EmployeeJob",font=("Arial",18),fg="red",bg="#00ffff",justify="center")
l4=tkinter.Label(window,text="EmployeeSalary",font=("Arial",18),fg="red",bg="#00ffff",justify='center')
header.place(x=650,y=20)
l1.place(x=550,y=100)
l2.place(x=550,y=150)
l3.place(x=550,y=200)
l4.place(x=550,y=250)
window.mainloop()