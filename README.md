# USB-Stegano-Toolkit

Steganography Toolkit on USB.  

A lightweight Python-based tool to hide and extract secret files inside images. Designed to be run directly from a USB drive for portability.  

## Features
- Hide text or small files inside PNG images.
- Passphrase protection for extraction.  
- Disguise hidden PNGs as '.jpg' for stealth.  
- Lightweight -- only requires Python + Pillow.  
- Portable -- run it from your USB stick.

## Requirements

- Windows 10/11, Linux, or macOS
- Python 3.9+
- USB

## Steps

1. Upgrade your terminal to the latest(mandatory). If using Windows just like my scenario, and you need visual guidance, can watch and follow this video : https://www.youtube.com/watch?v=z4w0OYi5L4M
   
2. Install python if you didn't or upgrade it if it's older version. Visual guidance : https://www.youtube.com/watch?v=lGAI9Z6egl0
   
3. Pick a file (this can your password text file or any other secret files)
<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/6842aea9d936de6f6bc9c585ffbfa5b684bfb52c/Screenshots/1.png" alt="screenshot" width="400"/>

4. If you have Git installed on your windows, here's the command you can put in the terminal to download the source files:
   = cd $HOME\Desktop
   = git clone https://github.com/KarmaResistance/USB-Stegano-Toolkit.git
You can manually download the source files too. Then, put your secret file and a picture in the toolkit folder. Make sure your picture is private one and not taken from internet as investigators or hackers can compare its hash with the "original" from the internet. Any difference may indicate tampering. Picture will be in JPG, so convert it to PNG by opening your picture in your Paint Application and save it as 'PNG'. PNG can retain the content of your secret file much better than JPG.

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/6842aea9d936de6f6bc9c585ffbfa5b684bfb52c/Screenshots/2.png" alt="screenshot" width="400"/>

5. Now, open your terminal. Direct it to folder where you downloaded the toolkit files.(You can right click on free space inside the folder and choose 'open in terminal'.
 
6. Insert these commands
   = python -m venv .venv
   = .\.venv\Scripts\Activate.ps1
   = pip install -r requirements.txt
   
<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/3.png" alt="screenshot" width="400"/>

7. Insert your USB and keep it ready.
<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/6842aea9d936de6f6bc9c585ffbfa5b684bfb52c/Screenshots/2.png" alt="screenshot" width="400"/>

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/5.png" alt="screenshot" width="400"/>

8. Now, Insert this command in your terminal:
   = python .\steg_tool.py embed -i .\Gathering.png -o E:\27967_673425.png -f .\test.txt
   
<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/6.png" alt="screenshot" width="400"/>

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/7.png" alt="screenshot" width="400"/>

Dont keep passphrase thats too simple. The embedded file should be saved in your usb.

9. Now in terminal, insert this command :
   = Rename-Item E:\27967_673425.png E:\IMG_6734.jpg
This is done so that the picture looks like a normal camera JPEG while still holding your hidden data. Most apps use the image's magic bytes (file signature) to decide how to open it, not just the extension. So a PNG named '.jpg' usually still opens fine, and your stego bits remain intact. Investigators or hackers will be less suspicious of your picture. Name the picture like a camera file too.

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/8.png" alt="screenshot" width="400"/>

10. Now, if you want to decrypt the embedded picture that was saved in USB, here's the command :
    = python .\steg_tool.py extract -i E:\IMG_4563.jpg -o "$HOME\Desktop\recovered.txt"

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/9.png" alt="screenshot" width="400"/>

You can set the location you want to obtain the recovered secret file. Enter the same passphrase you set while you were embedding the picture with secret file. You should be able to get your secret file back with no content erased.

<img src="https://github.com/KarmaResistance/USB-Stegano-Toolkit/blob/de46c593cec9b3e225b225b34df02f67a0528e40/Screenshots/10.png" alt="screenshot" width="400"/>















