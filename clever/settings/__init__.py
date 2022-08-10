from .base import *

if os.environ['CLEVER']  == 'prod':
   from .prod import *
   print("settings = prod")
else:
   from .dev import *
   print("settings = dev")
      