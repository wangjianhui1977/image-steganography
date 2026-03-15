# Image Steganography Tool

Hide secret messages within images and extract them securely. Built using LSB (Least Significant Bit) steganography technique.

---

## Features

- ✅ **Highly Concealed**: Messages are embedded in image pixels, invisible to the naked eye
- ✅ **Long Text Support**: Can hide large amounts of text information
- ✅ **Easy to Use**: Interactive interface with command-line support
- ✅ **Auto Detection**: Automatically checks image capacity to prevent overflow
- ✅ **Multiple Formats**: Supports common image formats (JPG, PNG, BMP, etc.)
- ✅ **Unicode Support**: Full support for Chinese and other Unicode characters

---

## Requirements

- Python 3.6 or higher
- PIL/Pillow library

---

## Installation

```bash
# Install Pillow
pip install Pillow
```

---

## Usage

### Method 1: GUI (Recommended)

Run the integrated tool with all functions in one window:

```bash
python image_steganography_gui.py
```

**Features:**
- **Click-based Operation**: No commands needed, full mouse interaction
- **Image Preview**: Real-time preview of selected images
- **Capacity Display**: Shows maximum characters the image can hide
- **Instant Feedback**: Real-time progress display for encryption/decryption
- **One-click Save**: Save or copy decrypted messages to clipboard

**How to Use:**

**Encryption (Hide Message):**
1. Switch to the "Encrypt" tab
2. Click "Select Image" to choose your source image
3. Enter your secret message in the text box (supports multiline and Chinese)
4. Click "Start Encryption"
5. Done! The encrypted image is saved

**Decryption (Extract Message):**
1. Switch to the "Decrypt" tab
2. Click "Select Image" to choose the encrypted image
3. Click "Start Decryption"
4. View the extracted secret message
5. Optional: Click "📋 Copy to Clipboard" or "💾 Save to File"

---

### Method 2: Command Line (For Terminal Users)

#### Encrypt (Hide Message)

```bash
python encrypt_image.py
```

Follow the prompts:
1. Enter the source image path
2. Enter your secret message (multiline supported, type `END` to finish)
3. Enter output image path (or press Enter for default)

#### Decrypt (Extract Message)

```bash
python decrypt_image.py
```

Follow the prompts:
1. Enter the encrypted image path
2. View the extracted secret message
3. Choose whether to save to a text file

---

## How It Works

### LSB (Least Significant Bit) Steganography

This tool uses LSB steganography to hide information in the least significant bits of image pixels.

#### Principle:

1. **RGB Pixels**: Each pixel consists of Red (R), Green (G), and Blue (B) channels, each with a value range of 0-255

2. **Binary Representation**: For example, red value `200` in binary is `11001000`

3. **Modify LSB**: Only modify the last bit (least significant bit):
   - Original: `11001000` (200)
   - Modified: `11001001` (201)
   - Visual difference: Almost unnoticeable!

4. **Information Encoding**:
   - Convert text to binary
   - Store binary bits sequentially in RGB channel LSBs
   - Each pixel can store 3 bits (1 bit per R, G, B)

5. **End Marker**: Uses special marker `<<<END>>>` to indicate message end

#### Capacity Calculation:

```
Max Capacity (characters) = (Image Width × Image Height × 3) ÷ 8
```

Examples:
- 1920×1080 image can hide approximately **777,600 characters**
- 800×600 image can hide approximately **180,000 characters**

---

## Important Notes

### Warnings

1. **Save Format**:
   - Output images **must** be saved in **PNG** format (lossless compression)
   - **Do not** use JPG format (lossy compression will destroy hidden data)

2. **Image Processing**:
   - Do not compress, resize, or crop encrypted images
   - Avoid uploading to social media (automatic compression will occur)
   - Use original file transfer methods (cloud storage, USB, email attachments)

3. **Security**:
   - This is **not** true encryption, just data hiding
   - Professional tools can detect LSB steganography
   - For real security, encrypt text with AES first, then hide it

4. **Image Selection**:
   - Choose colorful, detailed images (better concealment)
   - Avoid solid colors or simple patterns (easier to detect)

---

## Use Cases

1. **Password Management**: Hide important passwords in family photos
2. **Backup Keys**: Store recovery keys hidden in images
3. **Privacy Protection**: Share private messages within public images
4. **Digital Watermark**: Embed copyright information in images
5. **Learning**: Understand steganography principles and applications

---

## Security Recommendations

For higher security, consider combining with:

### 1. Encrypt Then Hide

```python
# Use AES encryption (requires pycryptodome)
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def encrypt_text(text, password):
    # Encryption code example
    pass

# Encrypt text first
encrypted_text = encrypt_text("secret message", "strong_password")

# Then hide in image
# python encrypt_image.py photo.jpg encrypted_text output.png
```

### 2. Password Protection

Modify the script to add password verification.

### 3. Multi-layer Hiding

Hide the encrypted image inside another image.

---

## Technical Specifications

| Item | Details |
|------|---------|
| Steganography Method | LSB (Least Significant Bit) |
| Supported Formats | JPG, PNG, BMP, GIF, etc. |
| Output Format | PNG (lossless) |
| Character Encoding | UTF-8 (Chinese supported) |
| End Marker | `<<<END>>>` |
| Bits per Pixel | 3 bits (1 per RGB channel) |

---

## License

MIT License

---

## Author

wangjianhui1977
