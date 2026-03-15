#!/usr/bin/env python3
"""
图片隐写术工具 - 完整图形化界面版本
加密和解密功能集成在一个窗口中
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import threading


class ImageSteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 图片隐写术工具 - 加密 & 解密")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        title_label = ttk.Label(
            main_frame, 
            text="🔐 图片隐写术工具", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.encrypt_frame = ttk.Frame(self.notebook, padding="10")
        self.decrypt_frame = ttk.Frame(self.notebook, padding="10")
        
        self.notebook.add(self.encrypt_frame, text="🔐 加密（隐藏信息）")
        self.notebook.add(self.decrypt_frame, text="🔓 解密（提取信息）")
        
        self.setup_encrypt_tab()
        self.setup_decrypt_tab()
        
    def setup_encrypt_tab(self):
        self.encrypt_image_path = None
        self.encrypt_output_path = None
        
        self.encrypt_frame.columnconfigure(0, weight=1)
        self.encrypt_frame.rowconfigure(2, weight=1)
        
        image_frame = ttk.LabelFrame(self.encrypt_frame, text="📷 选择图片", padding="10")
        image_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        image_frame.columnconfigure(1, weight=1)
        
        self.enc_image_label = ttk.Label(image_frame, text="未选择图片", foreground="gray")
        self.enc_image_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.enc_preview_label = ttk.Label(image_frame)
        self.enc_preview_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        select_btn = ttk.Button(
            image_frame, 
            text="📁 选择图片", 
            command=self.select_encrypt_image,
            width=20
        )
        select_btn.grid(row=2, column=0, columnspan=2)
        
        self.enc_info_label = ttk.Label(image_frame, text="", foreground="blue")
        self.enc_info_label.grid(row=3, column=0, columnspan=2, pady=(5, 0))
        
        message_frame = ttk.LabelFrame(self.encrypt_frame, text="💬 秘密信息", padding="10")
        message_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        message_frame.columnconfigure(0, weight=1)
        message_frame.rowconfigure(0, weight=1)
        
        self.enc_message_text = scrolledtext.ScrolledText(
            message_frame, 
            height=8, 
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.enc_message_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        hint_label = ttk.Label(
            message_frame, 
            text="💡 提示：支持多行文本，支持中文", 
            font=("Arial", 8),
            foreground="gray"
        )
        hint_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        self.enc_char_count_label = ttk.Label(
            message_frame, 
            text="字符数：0", 
            font=("Arial", 8)
        )
        self.enc_char_count_label.grid(row=2, column=0, sticky=tk.W, pady=(2, 0))
        
        self.enc_message_text.bind('<KeyRelease>', self.update_encrypt_char_count)
        
        output_frame = ttk.LabelFrame(self.encrypt_frame, text="💾 输出设置", padding="10")
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="输出路径:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.enc_output_entry = ttk.Entry(output_frame)
        self.enc_output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_btn = ttk.Button(
            output_frame, 
            text="浏览", 
            command=self.select_encrypt_output,
            width=10
        )
        browse_btn.grid(row=0, column=2)
        
        button_frame = ttk.Frame(self.encrypt_frame)
        button_frame.grid(row=4, column=0, pady=(0, 10))
        
        self.encrypt_btn = ttk.Button(
            button_frame, 
            text="🔐 开始加密", 
            command=self.encrypt_image,
            width=20,
            state=tk.DISABLED
        )
        self.encrypt_btn.grid(row=0, column=0, padx=5)
        
        clear_enc_btn = ttk.Button(
            button_frame, 
            text="🗑️ 清空", 
            command=self.clear_encrypt,
            width=15
        )
        clear_enc_btn.grid(row=0, column=1, padx=5)
        
        self.enc_progress_label = ttk.Label(
            self.encrypt_frame, 
            text="", 
            font=("Arial", 9),
            foreground="green"
        )
        self.enc_progress_label.grid(row=5, column=0)
        
    def setup_decrypt_tab(self):
        self.decrypt_image_path = None
        self.decrypted_message = ""
        
        self.decrypt_frame.columnconfigure(0, weight=1)
        self.decrypt_frame.rowconfigure(3, weight=1)
        
        image_frame = ttk.LabelFrame(self.decrypt_frame, text="📷 选择加密图片", padding="10")
        image_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        image_frame.columnconfigure(1, weight=1)
        
        self.dec_image_label = ttk.Label(image_frame, text="未选择图片", foreground="gray")
        self.dec_image_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.dec_preview_label = ttk.Label(image_frame)
        self.dec_preview_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        select_btn = ttk.Button(
            image_frame, 
            text="📁 选择图片", 
            command=self.select_decrypt_image,
            width=20
        )
        select_btn.grid(row=2, column=0, columnspan=2)
        
        self.dec_info_label = ttk.Label(image_frame, text="", foreground="blue")
        self.dec_info_label.grid(row=3, column=0, columnspan=2, pady=(5, 0))
        
        button_frame = ttk.Frame(self.decrypt_frame)
        button_frame.grid(row=1, column=0, pady=(0, 10))
        
        self.decrypt_btn = ttk.Button(
            button_frame, 
            text="🔓 开始解密", 
            command=self.decrypt_image,
            width=20,
            state=tk.DISABLED
        )
        self.decrypt_btn.grid(row=0, column=0, padx=5)
        
        clear_dec_btn = ttk.Button(
            button_frame, 
            text="🗑️ 清空", 
            command=self.clear_decrypt,
            width=15
        )
        clear_dec_btn.grid(row=0, column=1, padx=5)
        
        self.dec_progress_label = ttk.Label(
            self.decrypt_frame, 
            text="", 
            font=("Arial", 9),
            foreground="green"
        )
        self.dec_progress_label.grid(row=2, column=0, pady=(0, 10))
        
        result_frame = ttk.LabelFrame(self.decrypt_frame, text="📝 提取的秘密信息", padding="10")
        result_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        self.dec_result_text = scrolledtext.ScrolledText(
            result_frame, 
            height=12, 
            wrap=tk.WORD,
            font=("Consolas", 10),
            state=tk.DISABLED
        )
        self.dec_result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.dec_char_count_label = ttk.Label(
            result_frame, 
            text="", 
            font=("Arial", 8)
        )
        self.dec_char_count_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        action_frame = ttk.Frame(result_frame)
        action_frame.grid(row=2, column=0, pady=(10, 0))
        
        self.copy_btn = ttk.Button(
            action_frame, 
            text="📋 复制到剪贴板", 
            command=self.copy_to_clipboard,
            state=tk.DISABLED
        )
        self.copy_btn.grid(row=0, column=0, padx=5)
        
        self.save_btn = ttk.Button(
            action_frame, 
            text="💾 保存到文件", 
            command=self.save_to_file,
            state=tk.DISABLED
        )
        self.save_btn.grid(row=0, column=1, padx=5)
        
    def select_encrypt_image(self):
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.encrypt_image_path = file_path
            self.enc_image_label.config(text=os.path.basename(file_path), foreground="black")
            
            try:
                img = Image.open(file_path)
                width, height = img.size
                max_chars = (width * height * 3) // 8
                
                self.enc_info_label.config(
                    text=f"图片尺寸: {width}×{height} | 最大容量: {max_chars:,} 字符"
                )
                
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img)
                self.enc_preview_label.config(image=photo)
                self.enc_preview_label.image = photo
                
                default_output = os.path.splitext(file_path)[0] + "_encrypted.png"
                self.enc_output_entry.delete(0, tk.END)
                self.enc_output_entry.insert(0, default_output)
                self.encrypt_output_path = default_output
                
                self.check_encrypt_ready()
                
            except Exception as e:
                messagebox.showerror("错误", f"无法加载图片：{str(e)}")
                
    def select_encrypt_output(self):
        file_path = filedialog.asksaveasfilename(
            title="保存加密图片",
            defaultextension=".png",
            filetypes=[
                ("PNG图片", "*.png"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.encrypt_output_path = file_path
            self.enc_output_entry.delete(0, tk.END)
            self.enc_output_entry.insert(0, file_path)
            
    def update_encrypt_char_count(self, event=None):
        text = self.enc_message_text.get("1.0", tk.END).strip()
        char_count = len(text)
        self.enc_char_count_label.config(text=f"字符数：{char_count}")
        self.check_encrypt_ready()
        
    def check_encrypt_ready(self):
        text = self.enc_message_text.get("1.0", tk.END).strip()
        if self.encrypt_image_path and text:
            self.encrypt_btn.config(state=tk.NORMAL)
        else:
            self.encrypt_btn.config(state=tk.DISABLED)
            
    def text_to_binary(self, text):
        text_bytes = text.encode('utf-8')
        binary = ''.join(format(byte, '08b') for byte in text_bytes)
        return binary
        
    def encode_image(self, image_path, secret_message, output_path):
        img = Image.open(image_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = list(img.getdata())
        width, height = img.size
        
        delimiter = "<<<END>>>"
        message_with_delimiter = secret_message + delimiter
        
        binary_message = self.text_to_binary(message_with_delimiter)
        message_length = len(binary_message)
        
        max_capacity = width * height * 3
        
        if message_length > max_capacity:
            raise ValueError(f"消息太长！图片最多可以隐藏 {max_capacity // 8} 个字符，但消息有 {len(message_with_delimiter)} 个字符。")
        
        new_pixels = []
        message_index = 0
        
        for pixel in pixels:
            r, g, b = pixel
            
            if message_index < message_length:
                r = (r & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            if message_index < message_length:
                g = (g & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            if message_index < message_length:
                b = (b & 0xFE) | int(binary_message[message_index])
                message_index += 1
            
            new_pixels.append((r, g, b))
        
        encoded_img = Image.new('RGB', (width, height))
        encoded_img.putdata(new_pixels)
        encoded_img.save(output_path, 'PNG')
        
        return message_length, max_capacity
        
    def encrypt_image(self):
        if not self.encrypt_image_path:
            messagebox.showwarning("警告", "请先选择图片！")
            return
            
        secret_message = self.enc_message_text.get("1.0", tk.END).strip()
        
        if not secret_message:
            messagebox.showwarning("警告", "请输入要隐藏的秘密信息！")
            return
            
        output_path = self.enc_output_entry.get().strip()
        
        if not output_path:
            messagebox.showwarning("警告", "请指定输出路径！")
            return
            
        self.encrypt_btn.config(state=tk.DISABLED)
        self.enc_progress_label.config(text="🔄 正在加密，请稍候...", foreground="orange")
        
        def encrypt_thread():
            try:
                message_length, max_capacity = self.encode_image(
                    self.encrypt_image_path, 
                    secret_message, 
                    output_path
                )
                
                self.root.after(0, lambda: self.on_encrypt_success(
                    output_path, 
                    len(secret_message), 
                    message_length, 
                    max_capacity
                ))
                
            except Exception as e:
                self.root.after(0, lambda: self.on_encrypt_error(str(e)))
        
        thread = threading.Thread(target=encrypt_thread)
        thread.daemon = True
        thread.start()
        
    def on_encrypt_success(self, output_path, char_count, message_length, max_capacity):
        self.enc_progress_label.config(
            text=f"✅ 加密成功！已保存到: {os.path.basename(output_path)}", 
            foreground="green"
        )
        
        usage_percent = (message_length * 100) / max_capacity
        
        messagebox.showinfo(
            "加密成功", 
            f"✅ 秘密信息已成功隐藏到图片中！\n\n"
            f"📁 输出文件: {output_path}\n"
            f"📝 信息长度: {char_count} 个字符\n"
            f"📊 容量使用: {usage_percent:.2f}%\n\n"
            f"⚠️ 重要提示：\n"
            f"• 不要压缩或编辑加密后的图片\n"
            f"• 使用解密工具提取信息"
        )
        
        self.encrypt_btn.config(state=tk.NORMAL)
        
    def on_encrypt_error(self, error_msg):
        self.enc_progress_label.config(text="❌ 加密失败", foreground="red")
        messagebox.showerror("加密失败", f"发生错误：\n{error_msg}")
        self.encrypt_btn.config(state=tk.NORMAL)
        
    def select_decrypt_image(self):
        file_path = filedialog.askopenfilename(
            title="选择加密图片",
            filetypes=[
                ("PNG图片", "*.png"),
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.decrypt_image_path = file_path
            self.dec_image_label.config(text=os.path.basename(file_path), foreground="black")
            
            try:
                img = Image.open(file_path)
                width, height = img.size
                
                self.dec_info_label.config(text=f"图片尺寸: {width}×{height}")
                
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img)
                self.dec_preview_label.config(image=photo)
                self.dec_preview_label.image = photo
                
                self.decrypt_btn.config(state=tk.NORMAL)
                
            except Exception as e:
                messagebox.showerror("错误", f"无法加载图片：{str(e)}")
                
    def binary_to_text(self, binary):
        byte_array = bytearray()
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                byte_array.append(int(byte, 2))
        try:
            text = byte_array.decode('utf-8', errors='ignore')
        except:
            text = byte_array.decode('utf-8', errors='replace')
        return text
        
    def decode_image(self, image_path):
        img = Image.open(image_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = list(img.getdata())
        
        binary_message = ''
        
        for pixel in pixels:
            r, g, b = pixel
            
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)
        
        delimiter = "<<<END>>>"
        
        all_text = self.binary_to_text(binary_message)
        
        delimiter_index = all_text.find(delimiter)
        
        if delimiter_index == -1:
            raise ValueError("图片中没有找到隐藏的信息，或者信息已损坏。")
        
        secret_message = all_text[:delimiter_index]
        
        return secret_message
        
    def decrypt_image(self):
        if not self.decrypt_image_path:
            messagebox.showwarning("警告", "请先选择图片！")
            return
            
        self.decrypt_btn.config(state=tk.DISABLED)
        self.dec_progress_label.config(text="🔄 正在解密，请稍候...", foreground="orange")
        
        self.dec_result_text.config(state=tk.NORMAL)
        self.dec_result_text.delete("1.0", tk.END)
        self.dec_result_text.config(state=tk.DISABLED)
        
        def decrypt_thread():
            try:
                secret_message = self.decode_image(self.decrypt_image_path)
                self.root.after(0, lambda: self.on_decrypt_success(secret_message))
                
            except Exception as e:
                self.root.after(0, lambda: self.on_decrypt_error(str(e)))
        
        thread = threading.Thread(target=decrypt_thread)
        thread.daemon = True
        thread.start()
        
    def on_decrypt_success(self, secret_message):
        self.decrypted_message = secret_message
        
        self.dec_result_text.config(state=tk.NORMAL)
        self.dec_result_text.delete("1.0", tk.END)
        self.dec_result_text.insert("1.0", secret_message)
        self.dec_result_text.config(state=tk.DISABLED)
        
        char_count = len(secret_message)
        self.dec_char_count_label.config(text=f"✅ 成功提取 {char_count} 个字符")
        
        self.dec_progress_label.config(text="✅ 解密成功！", foreground="green")
        
        self.copy_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        self.decrypt_btn.config(state=tk.NORMAL)
        
        messagebox.showinfo(
            "解密成功", 
            f"✅ 成功从图片中提取秘密信息！\n\n"
            f"📝 信息长度: {char_count} 个字符\n\n"
            f"信息已显示在下方文本框中。"
        )
        
    def on_decrypt_error(self, error_msg):
        self.dec_progress_label.config(text="❌ 解密失败", foreground="red")
        messagebox.showerror(
            "解密失败", 
            f"无法从图片中提取信息：\n\n{error_msg}\n\n"
            f"可能的原因：\n"
            f"• 图片未包含隐藏信息\n"
            f"• 图片被压缩或编辑过\n"
            f"• 图片格式不正确"
        )
        self.decrypt_btn.config(state=tk.NORMAL)
        
    def copy_to_clipboard(self):
        if self.decrypted_message:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.decrypted_message)
            messagebox.showinfo("成功", "✅ 已复制到剪贴板！")
        
    def save_to_file(self):
        if not self.decrypted_message:
            return
            
        file_path = filedialog.asksaveasfilename(
            title="保存秘密信息",
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ],
            initialfile=os.path.splitext(os.path.basename(self.decrypt_image_path))[0] + "_decrypted.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.decrypted_message)
                messagebox.showinfo("成功", f"✅ 已保存到:\n{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{str(e)}")
        
    def clear_encrypt(self):
        self.encrypt_image_path = None
        self.encrypt_output_path = None
        self.enc_image_label.config(text="未选择图片", foreground="gray")
        self.enc_info_label.config(text="")
        self.enc_preview_label.config(image='')
        self.enc_message_text.delete("1.0", tk.END)
        self.enc_output_entry.delete(0, tk.END)
        self.enc_progress_label.config(text="")
        self.enc_char_count_label.config(text="字符数：0")
        self.encrypt_btn.config(state=tk.DISABLED)
        
    def clear_decrypt(self):
        self.decrypt_image_path = None
        self.decrypted_message = ""
        self.dec_image_label.config(text="未选择图片", foreground="gray")
        self.dec_info_label.config(text="")
        self.dec_preview_label.config(image='')
        self.dec_result_text.config(state=tk.NORMAL)
        self.dec_result_text.delete("1.0", tk.END)
        self.dec_result_text.config(state=tk.DISABLED)
        self.dec_progress_label.config(text="")
        self.dec_char_count_label.config(text="")
        self.decrypt_btn.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = ImageSteganographyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
