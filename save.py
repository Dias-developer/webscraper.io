import openpyxl

def save_excel(products):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Cars'

    ws.append(['Name of Car', 'Price'])

    for item in products:
        ws.append([
            item.get('title'),
            item.get('price')
        ])
    wb.save('cars.xlsx')