from model.Model_dm import Model_dm
from datetime import datetime


dm = Model_dm()
x = dm.update_info_timestamps()

print(dm.last_chat_ts, dm.last_data_ts)

#x = "00000000000002"

#now = datetime.now()
#y = now.strftime("%Y%m%d%H%M%S")

#print(x, y, sep=f"\n")

#print(dm.now())
