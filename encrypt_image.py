#!/usr/bin/env python3
"""
图片加密脚本 - 将秘密信息隐藏在图片中
使用LSB（最低有效位）隐写术技术
"""

from PIL import Image
import sys
import os


def text_to_binary(text):
    """将文本转换为二进制字符串"""
    text_bytes = text.encode('utf-8')
    binary = ''.join(format(byte, '08b') for byte in text_bytes)
    return binary


def encode_image(image_path, secret_message, output_path):
    """
    将秘密信息编码到图片中
    
    参数:
        image_path: 原始图片路径
        secret_message: 要隐藏的秘密信息
        output_path: 输出图片路径
    """
    try:
        img = Image.open(image_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = list(img.getdata())
        width, height = img.size
        
        delimiter = "<<<END>>>"
        message_with_delimiter = secret_message + delimiter
        
        binary_message = text_to_binary(message_with_delimiter)
        message_length = len(binary_message)
        
        max_capacity = width * height * 3
        
        if message_length > max_capacity:
            raise ValueError(f"错误：消息太长！图片最多可以隐藏 {max_capacity // 8} 个字符，但消息有 {len(message_with_delimiter)} 个字符。")
        
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
        
        print(f"✅ 成功！秘密信息已隐藏到图片中")
        print(f"📁 原始图片: {image_path}")
        print(f"💾 输出图片: {output_path}")
        print(f"📝 隐藏信息长度: {len(secret_message)} 个字符")
        print(f"📊 使用容量: {message_length}/{max_capacity} 位 ({message_length*100/max_capacity:.2f}%)")
        
    except FileNotFoundError:
        print(f"❌ 错误：找不到图片文件 '{image_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：{str(e)}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("🔐 图片加密工具 - 将秘密信息隐藏在图片中")
    print("=" * 60)
    print()
    
    if len(sys.argv) == 4:
        image_path = sys.argv[1]
        secret_message = sys.argv[2]
        output_path = sys.argv[3]
    else:
        image_path = input("📷 请输入原始图片路径: ").strip()
        
        if not os.path.exists(image_path):
            print(f"❌ 错误：文件 '{image_path}' 不存在！")
            sys.exit(1)
        
        print()
        print("💬 请输入要隐藏的秘密信息（可以多行，输入 'END' 结束）:")
        lines = []
        while True:
            line = input()
            if line == 'END':
                break
            lines.append(line)
        secret_message = '\n'.join(lines)
        
        if not secret_message:
            print("❌ 错误：秘密信息不能为空！")
            sys.exit(1)
        
        print()
        default_output = os.path.splitext(image_path)[0] + "_encrypted.png"
        output_path = input(f"💾 请输入输出图片路径 (默认: {default_output}): ").strip()
        
        if not output_path:
            output_path = default_output
    
    print()
    print("🔄 正在加密...")
    print()
    
    encode_image(image_path, secret_message, output_path)
    
    print()
    print("=" * 60)
    print("🎉 加密完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
