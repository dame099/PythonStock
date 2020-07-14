import win32com.client

explore = win32com.client.Dispatch("PowerPoint.Application")
explore.Visible = True