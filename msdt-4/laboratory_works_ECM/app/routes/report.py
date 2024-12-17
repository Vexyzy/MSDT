import datetime
import os

import flask
from flask import Blueprint
from sqlalchemy import text

from ..extensions import DB
import xlsxwriter


REPORT = Blueprint('report', __name__)

REPORT_NAME_WITH_PATH = (f'/Users/ivanaleksandrovci/code/ssau_laboratory/'
                         f'laboratory_works_ECM/excel/uploads/'
                         f'Сведения об исполненных заказах на поставку '
                         f'косметической продукции'
               f'предприятиям торговли и сервиса за '
               f'{datetime.datetime.now().year} год.xlsx'
)


@REPORT.route('/report', methods=['GET', 'POST'])
def create_report():
    try:
        os.remove(REPORT_NAME_WITH_PATH)
    except OSError:
        pass
    workbook = xlsxwriter.Workbook(REPORT_NAME_WITH_PATH)
    worksheet = workbook.add_worksheet()
    cell_format_bolt = workbook.add_format({'bold': True})
    cell_format_money = workbook.add_format(
        {
            'num_format': '#,##,00 р'
        }
    )

    # Получаем id всех предприятий
    sql_get_enterprises_id = text(
        f"SELECT enterprise_id FROM enterprise;"
    )

    with DB.engine.connect() as conn:
        enterprises_id = conn.execute(
            sql_get_enterprises_id
        ).fetchall()

    row_id = 0
    total_sum = 0
    enterprise_sum = 0
    # Проходимся по всем полученные id предприятий доставки
    for enterprise_id in enterprises_id:
        # Получить все данные по id предпреятия
        order_info = get_order_by_enterprise_id(enterprise_id[0])
        # Если предприятия нет, то пропуск
        if not order_info:
            continue

        # Написать именования колонок
        worksheet.write(row_id, 0, 'Наименование товара', cell_format_bolt)
        worksheet.write(row_id, 1, 'Наименование бренда', cell_format_bolt
        )
        worksheet.write(row_id, 2, 'Дата исполенения заказа', cell_format_bolt
        )
        worksheet.write(row_id, 3,
                        'Количество товара в доставке', cell_format_bolt
        )
        worksheet.write(row_id, 4, 'Цена, руб.', cell_format_bolt)
        worksheet.write(row_id, 5, 'Стоимость, руб.', cell_format_bolt)
        row_id += 1

        # Пройтись по всем данным
        for i in range(0, len(order_info)):
            print(order_info[i])
            # Записать каждую информацию о заказе в строку
            worksheet.write(row_id, 0, str(order_info[i][0]))
            worksheet.write(row_id, 1, str(order_info[i][1]))
            worksheet.write(row_id, 2, str(order_info[i][2]))
            worksheet.write(row_id, 3, order_info[i][3])
            worksheet.write(row_id, 4, order_info[i][4], cell_format_money)
            worksheet.write(row_id, 5, order_info[i][5], cell_format_money)
            row_id += 1
            # Прибавить к сумме предприятия сумму заказа
            enterprise_sum += int(order_info[i][5])
        # Написать суммарную сумму по предприятию и ее название
        worksheet.write(row_id, 0, 'Предприятие')
        enterprise_name = get_enterprise_name(enterprise_id[0])
        worksheet.write(row_id, 1, enterprise_name)
        row_id += 1
        worksheet.write(row_id, 0, 'Итого по предприятию: ')
        worksheet.write(row_id, 1, enterprise_sum, cell_format_money)
        # Прибать сумму предприятия к полной и обнулить сумму предприятия
        total_sum += enterprise_sum
        enterprise_sum = 0
        # Поставить черту и сделать отстпуп
        row_id += 3
    worksheet.write(row_id, 0, 'Итого по всем предприятиям')
    worksheet.write(row_id, 1, total_sum, cell_format_money)
    worksheet.autofit()
    workbook.close()

    return flask.send_file(REPORT_NAME_WITH_PATH, as_attachment=True)

def get_enterprise_name(enterprise_id: int) -> str:
    sql_get_enterprise_name = text(
        f"SELECT enterprise_name FROM enterprise "
        f"WHERE enterprise_id = {enterprise_id};"
    )

    with DB.engine.connect() as conn:
        enterprise_name = conn.execute(sql_get_enterprise_name).fetchone()[0]
    return enterprise_name

def get_order_by_enterprise_id(enterprise_id: int) -> list:
    sql_get_report = text(
        f"SELECT\n"
        f"p.product_name,\n"
        f"b.brand_name,\n"
        f"d.execution_date,\n"
        f"SUM(d.quantity_of_product) AS total_quantity,\n"
        f"p.price,\n"
        f"p.price * SUM(d.quantity_of_product) AS total_price\n"
        f"FROM\n"
        f"product p\n"
        f"JOIN brand b ON p.brand_id = b.brand_id\n"
        f"JOIN cosmetic_order co ON co.product_id = p.product_id\n"
        f"JOIN enterprise e ON co.enterprise_id = e.enterprise_id\n"
        f"JOIN delivery d ON\n"
        f"d.cosmetic_order_id = co.cosmetic_order_id\n"
        f"WHERE e.enterprise_id = {enterprise_id}\n"
        f"GROUP BY p.product_id, d.execution_date, b.brand_name;\n"
    )

    with DB.engine.connect() as conn:
        order_info = conn.execute(sql_get_report).fetchall()
    print(order_info)
    return order_info



