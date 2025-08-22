# USB-Stegano-Toolkit

Steganography Toolkit on USB.  

A lightweight Python-based tool to hide and extract secret files inside images. Designed to be run directly from a USB drive for portability.  

## Features
- Hide text or small files inside PNG images.
- Passphrase protection for extraction.  
- Disguise hidden PNGs as '.jpg' files for stealth.  
- Lightweight -- only requires Python + Pillow.  
- Portable -- run it from your USB stick.

## Requirements

- Windows 10/11, Linux, or macOS
- Python 3.9+
- USB drive (for portable use)

## Steps

1. Upgrade your terminal to the latest version (mandatory). If using Windows just like my scenario, and you need visual guidance, can watch and follow this video : https://www.youtube.com/watch?v=z4w0OYi5L4M
   
2. Install Python if you don’t already have it, or upgrade if your version is outdated. Visual guidance : https://www.youtube.com/watch?v=lGAI9Z6egl0
   
3. Pick a file (this can be your password text file or any other secret files)

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/6842aea9d936de6f6bc9c585ffbfa5b684bfb52c/Screenshots/1.png" alt="screenshot" width="400"/>

4. If you have Git installed on your windows, Here’s the command to download the source files into your Desktop:

```
cd $HOME\Desktop
git clone https://github.com/KarmaResistance/USB-Stegano-Toolkit.git
```

You can manually download the source files too. Then, put your secret file and a picture in the toolkit folder. Make sure your picture is private one and not taken from internet as investigators or hackers can compare its hash with the "original" from the internet. Any difference may indicate tampering. Picture will be in JPG, so convert it to PNG by opening your picture in your Paint Application and save it as 'PNG'. PNG can retain the content of your secret file much better than JPG.

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/6842aea9d936de6f6bc9c585ffbfa5b684bfb52c/Screenshots/2.png" alt="screenshot" width="400"/>

5. Now, open your terminal. Navigate to the folder where you downloaded the toolkit files. (Tip: Right-click inside the folder and select Open in Terminal.
 
6. Insert these commands :

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```   

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/3.png" alt="screenshot" width="400"/>

7. Insert your USB and keep it ready.

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/6842aea9d936de6f6bc9c585ffbfa5b684bfb52c/Screenshots/2.png" alt="screenshot" width="400"/>

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/5.png" alt="screenshot" width="400"/>

8. Now, Insert this command in your terminal:

```
python .\steg_tool.py embed -i .\Gathering.png -o E:\27967_673425.png -f .\test.txt
```
   
<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/6.png" alt="screenshot" width="400"/>

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/7.png" alt="screenshot" width="400"/>

Don’t use a passphrase that is too simple. The embedded file should be saved in your usb.

9. Now in terminal, insert this command :

```
Rename-Item E:\27967_673425.png E:\IMG_6734.jpg
```

This is done so that the picture looks like a normal camera JPEG while still holding your hidden data. Most apps use the image's magic bytes (file signature) to decide how to open it, not just the extension. So a PNG named '.jpg' usually still opens fine, and your stego bits remain intact. This makes the picture appear like a normal camera JPEG, making it less suspicious. You can also rename it to look like a typical camera filename (e.g., IMG_6734.jpg)

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/8.png" alt="screenshot" width="400"/>

10. Now, if you want to extract the hidden file from the embedded picture that was saved in USB, here's the command :

```
python .\steg_tool.py extract -i E:\IMG_4563.jpg -o "$HOME\Desktop\recovered.txt"
```

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/9.png" alt="screenshot" width="400"/>

You can set the location you want to obtain the recovered secret file. Enter the same passphrase you set while you were embedding the picture with secret file. You should be able to get your secret file back with no content erased.

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/10.png" alt="screenshot" width="400"/>


## Security Notes

- Steganography is a form of **obfuscation**, not guaranteed protection. Skilled investigators, forensic analysts or government agencies may still detect that an image has been modified.  
- Detection does **not** equal access. if you use a strong passphrase, the extracted data will still be **encrypted gibberish** without your key.  
- Always use a **strong, unique passphrase** (avoid simple ones like `1234`, `password` or personal names).  
- Avoid uploading stego-images to platforms that **recompress or resize images** (e.g., WhatsApp, Facebook, Instagram, Twitter). This usually destroys the hidden data.  
- Works best with **PNG images**. JPEG files may corrupt or strip out hidden data.  
- Keep your **payload small** (e.g., text files, notes, passwords). Very large hidden files may cause suspiciously large image sizes.  
- For maximum safety, combine steganography with **encryption**. Encrypt your file first, then embed it.  
- Renaming `.png` files to `.jpg` adds disguise, but remember the file is still technically a PNG. Some forensic tools may notice the mismatch.  
- This project is intended for **educational purposes only**. Use responsibly.  

