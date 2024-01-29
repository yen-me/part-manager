from tkinter import *
from tkinter import messagebox
from turtle import clear
from typing import List
from db import Database


db = Database('store.db')


def populate_list():
    parts_list.delete(0, END)
    for row in db.fetch():
        parts_list.insert(END, row)


def add_item():
    if part_text.get() == '' or customer_text.get() == '' or retailer_text.get() == '' or price_text.get() == '':
        messagebox.showerror('Required Fields', 'Please enter all the fields.')

    db.insert(part_text.get(), customer_text.get(),
              retailer_text.get(), price_text.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (part_text.get(), customer_text.get(),
                      retailer_text.get(), price_text.get()))
    clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)

        # Clear textbox value and populate the selected row's value:
        part_entry.delete(0, END)
        part_entry.insert(END, selected_item[1])

        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])

        retailer_entry.delete(0, END)
        retailer_entry.insert(END, selected_item[3])

        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])

    # Clear the deleted row values from the textbox:
    clear_text()

    populate_list()


def update_item():
    db.update(selected_item[0], part_text.get(
    ), customer_text.get(), retailer_text.get(), price_text.get())
    populate_list()


def clear_text():
    # Clear the deleted row values from the textbox:
    part_entry.delete(0, END)
    customer_entry.delete(0, END)
    retailer_entry.delete(0, END)
    price_entry.delete(0, END)


# Create window object
app = Tk()


# Part
part_text = StringVar()
part_label = Label(app, text='Part Name', font=('bold', 14), pady=20, padx=20)
part_label.grid(row=0, column=0, sticky=W)  # sticky west: left

part_entry = Entry(app, textvariable=part_text)
part_entry.grid(row=0, column=1)

# Customer
customer_text = StringVar()
customer_label = Label(app, text='Customer', font=('bold', 14), padx=20)
customer_label.grid(row=0, column=2, sticky=W)  # sticky west: left

customer_entry = Entry(app, textvariable=customer_text)
customer_entry.grid(row=0, column=3)

# Retailer
retailer_text = StringVar()
retailer_label = Label(app, text='Retailer', font=('bold', 14), padx=20)
retailer_label.grid(row=1, column=0, sticky=W)  # sticky west: left

retailer_entry = Entry(app, textvariable=retailer_text)
retailer_entry.grid(row=1, column=1)


# Price
price_text = StringVar()
price_label = Label(app, text='Price', font=('bold', 14), padx=20)
price_label.grid(row=1, column=2, sticky=W)  # sticky west: left

price_entry = Entry(app, textvariable=price_text)
price_entry.grid(row=1, column=3)


# Parts List (Listbox)
parts_list = Listbox(app, height=8, border=0)
parts_list.grid(row=3, column=0, columnspan=4,
                rowspan=6, pady=20, padx=20, sticky=NSEW)

# Create scroll bar:
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3, sticky=NS, pady=20, rowspan=3)
scrollbar.place(x=678, y=178)

# Set scroll to listbox:
parts_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=parts_list.yview)  # Scroll along the y axis

# Bind select:
parts_list.bind('<<ListboxSelect>>', select_item)

# Buttons:
add_btn = Button(app, text='Add Part', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20, padx=20)

remove_btn = Button(app, text='Remove Part', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Update Part', width=12, command=update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Clear Input', width=12, command=clear_text)
clear_btn.grid(row=2, column=3)


app.title('Part Manager')
app.geometry('700x350')  # widthxheight


# Populate data
populate_list()

# Start program
app.mainloop()
