from tkinter import Tk, Label, Entry, Button, StringVar, IntVar
import labeling_system as label_sys

def modify_count(plus_or_minus):
    if plus_or_minus == True:
        processed_img_num.set(processed_img_num.get() + 1)
    elif plus_or_minus == False:
        processed_img_num.set(processed_img_num.get() - 1)

def submit():

    host = host_var.get()
    sample_num = sample_num_bar.get()
    db_name = db_name_var.get()
    collection_name = collection_name_var.get()
    
    label_sys.set_env(host, db_name, collection_name)
    datas = label_sys.get_datas(sample_num)
    
    label_sys.open_cv()

    index = 0
    while index < len(datas):
        state = label_sys.run(datas[index])

        if state == 2:
            index -= 1
            modify_count(False)
        elif state == 1:
            index += 1
            modify_count(True)
        elif state == 0:
            break
        root.update()
        
    label_sys.close_cv()
    
    return True

def quit_app():
    root.destroy()

if __name__ == "__main__":
    root = Tk()

    #---------------------------------------------------------
    Label(root, text="DB HOST:").pack()
    host_var = StringVar(value="mongodb://localhost:27018/")
    Entry(root, textvariable=host_var).pack()

    Label(root, text="Sample Num:").pack()
    sample_num_bar = IntVar(value=100)
    Entry(root, textvariable=sample_num_bar).pack()

    Label(root, text="DB Name:").pack()
    db_name_var = StringVar(value="DBproduct_eng")
    Entry(root, textvariable=db_name_var).pack()

    Label(root, text="Collection Name:").pack()
    collection_name_var = StringVar(value="product_detection_data")
    Entry(root, textvariable=collection_name_var).pack()

    Button(root, text="Submit", command=submit).pack()
    #---------------------------------------------------------

    processed_img_num = IntVar()
    Label(root, text="Processed_Data:").pack()
    Label(root, textvariable=processed_img_num).pack()


    root.mainloop()