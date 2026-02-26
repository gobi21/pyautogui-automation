import pyautogui
import pyperclip
import time
import webbrowser

# Step 1: Open the browser and go to Google
search_query = "India vs Zimbabwe T20 World Cup live score"
webbrowser.open("https://www.google.com")

# Wait for browser to open
time.sleep(5)

# Step 2: Type the search query using PyAutoGUI
pyautogui.write(search_query, interval=0.05)
pyautogui.press("enter")

# Wait for search results to load
time.sleep(5)

# Step 3: Use mouse to click the first score widget (coordinates may need adjustment)
# You can move your mouse to the score widget and note the coordinates using:
# pyautogui.position() in interactive mode
score_x, score_y = 700, 300  # Example coordinates; adjust to your screen
pyautogui.moveTo(score_x, score_y, duration=1)
pyautogui.click()

# Step 4: Select and copy the score text
pyautogui.hotkey("ctrl", "c")

# Step 5: Get the score from clipboard
score_text = pyperclip.paste()

print("Current India vs Zimbabwe T20 Score:")
print(score_text)