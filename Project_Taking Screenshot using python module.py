# Program to take screenshot

import pyscreenshot
from PIL import Image
# To capture the screen
#image=Image.new("RGB",(100,100),color="red")
image = pyscreenshot.grab()

# To display the captured screenshot
image.show()

# To save the screenshot
image.save("GeeksforGeeks.png")
