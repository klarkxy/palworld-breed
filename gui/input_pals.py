import os
import tkinter as tk, tkinter.ttk

class InputPalsWindow():
    pal_img = {}  # 帕鲁头像
    pal_no_list = []  # 帕鲁编号列表
    pal_name_list = []  # 帕鲁名字列表
    pal_no_name_dict = {}  # 帕鲁编号-名字对应表
    pal_name_no_dict = {}  # 帕鲁名字-编号对应表
    _last_select = ""  # 上次选择的帕鲁

    @classmethod
    def sort_pal_list(cls):
        from pypinyin import pinyin, Style
        def camp_no(x : str):
            # 按照编号排序，空<B<T<S
            if x.endswith('B'):
                return float(x[:-1]) + 0.3
            elif x.endswith('T'):
                return float(x[:-1]) + 0.5
            elif x.endswith('S'):
                return float(x[:-1]) + 0.7
            else:
                return float(x)
                
        cls.pal_no_list.sort(key=camp_no)
        cls.pal_name_list.sort(key = lambda x : pinyin(x, style=Style.TONE3))
        
    @classmethod
    def init(cls):
        if len(cls.pal_img) != 0:
            return
        # 读入images下所有的图片
        for file in os.listdir('images'):
            filename = file[:-4]
            no, name = filename.split('.')
            cls.pal_img[filename] = cls.pal_img[name] = cls.pal_img[no] = tk.PhotoImage(file=f'images/{file}')
            cls.pal_no_list.append(no)
            cls.pal_name_list.append(name)
            cls.pal_no_name_dict[no] = name
            cls.pal_name_no_dict[name] = no
            if cls._last_select == "":
                cls._last_select = no
        cls.sort_pal_list()

    def create_pal_img_label(self, win : tk.Toplevel):
        self.pal_img_label = tk.Label(win)
        if self._last_select != "":
            self.pal_img_label.config(image=self.pal_img[self._last_select])
            
    def create_pal_no_combobox(self, win : tk.Toplevel):
        self.pal_no_combobox = tk.ttk.Combobox(win, width=15, values=self.pal_no_list)
        if self._last_select != "":
            self.pal_no_combobox.set(self._last_select)
        
        def select(*args):
            self._last_select = self.pal_no_combobox.get()
            self.pal_img_label.config(image=self.pal_img[self._last_select])
            self.pal_name_combobox.set(self.pal_no_name_dict[self._last_select])

        self.pal_no_combobox.bind("<<ComboboxSelected>>", select)
        return self.pal_no_combobox
    
    def create_pal_name_combobox(self, win : tk.Toplevel):
        self.pal_name_combobox = tk.ttk.Combobox(win, width=15, values=self.pal_name_list)
        if self._last_select != "":
            self.pal_name_combobox.set(self.pal_no_name_dict[self._last_select])
        
        def select(*args):
            self._last_select = self.pal_name_no_dict[self.pal_name_combobox.get()]
            self.pal_img_label.config(image=self.pal_img[self._last_select])
            self.pal_no_combobox.set(self._last_select)

        self.pal_name_combobox.bind("<<ComboboxSelected>>", select)
        return self.pal_name_combobox

    def open_window(self, master):
        """打开\"录入帕鲁\"窗口"""
        self.init()
        win = tk.Toplevel(master)
        win.title('录入帕鲁')
        # 创建组件
        self.create_pal_img_label(win)
        self.create_pal_no_combobox(win)
        self.create_pal_name_combobox(win)
        # 布局
        self.pal_img_label.pack()
        self.pal_no_combobox.pack()
        self.pal_name_combobox.pack()

if __name__ == '__main__':
    main = tk.Tk()
    win = InputPalsWindow()
    win.open_window(main)
    main.mainloop()