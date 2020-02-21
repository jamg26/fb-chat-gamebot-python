from fb_normal.define import *
from fb_normal.meme import *

st = "!meme 5440182433#Hi#Hello"
t_id = st.split('#')[0].split()[1]
msg1 = st.split('#')[1]
msg2 = st.split('#')[2]

print(msg1, msg2, t_id)
