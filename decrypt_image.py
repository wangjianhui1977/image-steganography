#!/usr/bin/env python3
"""
图片解密脚本 - 从图片中提取隐藏的秘密信息
使用LSB（最低有效位）隐写术技术
"""

from PIL import Image
import sys
import os


def binary_to_text(binary):
    """将二进制字符串转换为文本"""
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


def decode_image(image_path):
    """
    从图片中解码秘密信息
    
    参数:
        image_path: 包含隐藏信息的图片路径
    
    返回:
        解码后的秘密信息
    """
    try:
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
        
        all_text = binary_to_text(binary_message)
        
        delimiter_index = all_text.find(delimiter)
        
        if delimiter_index == -1:
            raise ValueError("错误：图片中没有找到隐藏的信息，或者信息已损坏。")
        
        secret_message = all_text[:delimiter_index]
        
        return secret_message
        
    except FileNotFoundError:
        print(f"❌ 错误：找不到图片文件 '{image_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：{str(e)}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("🔓 图片解密工具 - 从图片中提取隐藏的秘密信息")
    print("=" * 60)
    print()
    
    if len(sys.argv) == 2:
        image_path = sys.argv[1]
    else:
        image_path = input("📷 请输入要解密的图片路径: ").strip()
        
        if not os.path.exists(image_path):
            print(f"❌ 错误：文件 '{image_path}' 不存在！")
            sys.exit(1)
    
    print()
    print("🔄 正在解密...")
    print()
    
    secret_message = decode_image(image_path)
    
    print("✅ 成功！从图片中提取到隐藏的信息：")
    print()
    print("=" * 60)
    print("📝 秘密信息内容：")
    print("=" * 60)
    print()
    print(secret_message)
    print()
    print("=" * 60)
    print(f"📊 信息长度: {len(secret_message)} 个字符")
    print("=" * 60)
    
    save_option = input("\n💾 是否保存到文本文件？(y/n): ").strip().lower()
    if save_option == 'y':
        output_file = os.path.splitext(image_path)[0] + "_decrypted.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(secret_message)
        print(f"✅ 已保存到: {output_file}")


if __name__ == "__main__":
    main()
