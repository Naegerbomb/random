import pyautogui
import time
import webbrowser
import os

def wait_for_image(image_path, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if pyautogui.locateOnScreen(image_path):
            return True
        time.sleep(0.5)
    return False

def get_registration_status():
    if pyautogui.locateOnScreen('yes_registered.png'):
        return "Yes, you are registered!"
    elif pyautogui.locateOnScreen('no_record.png'):
        return "No voter record matched your search criteria."
    else:
        return "Unable to determine registration status."

# Open the specified URL in the default web browser
url = "https://mvic.sos.state.mi.us/Voter/Index"
webbrowser.open(url)

# Wait for the browser and page to load by checking for a specific element
image_path = os.path.join(os.path.dirname(__file__), 'Content/Images/RegisterToVoteSmall.png')
if not wait_for_image(image_path):
    print("Page did not load in time.")
    exit()

# Start automation
pyautogui.press('tab')          # Press Tab
pyautogui.press('enter')        # Press Enter
pyautogui.press('tab')          # Press Tab
pyautogui.press('tab')          # Press Tab
pyautogui.typewrite('James')    # Type "James"
pyautogui.press('tab')          # Press Tab
pyautogui.typewrite('Naeger')   # Type "Naeger"
pyautogui.press('tab')          # Press Tab
pyautogui.press('down')         # Press Down
pyautogui.press('down')         # Press Down
pyautogui.press('down')         # Press Down
pyautogui.press('enter')        # Press Enter
pyautogui.press('tab')          # Press Tab
pyautogui.typewrite('1986')     # Type "1986"
pyautogui.press('tab')          # Press Tab
pyautogui.typewrite('48084')    # Type "48084"
pyautogui.press('tab')          # Press Tab
pyautogui.press('tab')          # Press Tab
pyautogui.press('enter')        # Press Enter

time.sleep(2)  # Adjust if your internet connection is slower

# Check registration status
status = get_registration_status()
print(status)

print("Automation complete.")