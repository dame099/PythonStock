from pywinauto import application
from pywinauto import timings
import time
import os

app = application.Application()
app.start("C:/KiwoomFlash3/Bin/NKMiniStarter.exe")

#Password & Cert
ID_Password = "dltpwns9"
Cert_Password = "dltpwns99@"


title = "번개3 Login"
dlg = timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

#버튼 이름 알아야 할때는 SWAPY사용 (https://github.com/pywinauto/SWAPY)

pass_ctrl = dlg.Edit2
pass_ctrl.SetFocus()
pass_ctrl.TypeKeys(ID_Password)

cert_ctrl = dlg.Edit3
cert_ctrl.SetFocus()
cert_ctrl.TypeKeys(Cert_Password)

btn_ctrl = dlg.Button0
btn_ctrl.Click()


time.sleep(100)
os.system("taskkill /im NKMini.exe")