import win32com.client

def save_excel():
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    wb = excel.Workbooks.Add()
    ws = wb.Worksheets("Sheet1")
    ws.Cells(1,1).Value = 'python'
    wb.SaveAs('C:\\Users\\sejun\\Documents\\Python_Code\\PythonStock\\Ch9\\test.xlsx')
    excel.Quit()

def load_excel():
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    wb = excel.Workbooks.Open('C:\\Users\\sejun\\Documents\\Python_Code\\PythonStock\\Ch9\\test.xlsx')
    ws = wb.ActiveSheet
    print(ws.Cells(1,1).Value)
    excel.Quit()

def color_excel():
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    wb = excel.Workbooks.Open('C:\\Users\\sejun\\Documents\\Python_Code\\PythonStock\\Ch9\\test.xlsx')
    ws = wb.ActiveSheet
    ws.Cells(1,2).Value = 'is'
    ws.Range('C1').Value = 'good'
    ws.Range('B1:C1').Interior.ColorIndex = 10
    excel.Quit()

    
if __name__ == "__main__":
    #save_excel()
    #load_excel()
    color_excel()