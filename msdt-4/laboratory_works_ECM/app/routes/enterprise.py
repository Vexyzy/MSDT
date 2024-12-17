from urllib.response import addbase

import sqlalchemy
from flask import Blueprint, render_template, request, flash, redirect
from sqlalchemy import text
from ..extensions import DB
from ..models.enterprise import Enterprise

ENTERPRISE = Blueprint('enterprise', __name__)

@ENTERPRISE.route('/enterprise', methods=['GET'])
def show_enterprise():
    enterprises = Enterprise.query.all()
    return render_template(
        '/enterprise/all.html',
        enterprises=enterprises
    )

@ENTERPRISE.route('/enterprise/create', methods=['GET', 'POST'])
def create_enterprise():
    if request.method == 'POST':
        enterprise_name = request.form['enterprise_name']
        address = request.form['address']
        phone = request.form['phone']
        enterprise = Enterprise(
            enterprise_name=enterprise_name,
            address=address,
            phone=phone
        )

        try:
            DB.session.add(enterprise)
            DB.session.commit()
            flash('Предприятие успешно добавлено!', 'success')
            return redirect('/enterprise')
        except Exception as e:
            flash('Произошла ошибка добавления')
            print(e)
            return redirect('./create')
    else:
        return render_template('enterprise/create.html')


@ENTERPRISE.route('/enterprise/<int:id>/update', methods=['GET', 'POST'])
def update_enterprise(id):
    enterprise = Enterprise.query.get(id)
    if request.method == 'POST':
        enterprise.enterprise_name = request.form['enterprise_name']
        enterprise.address = request.form['address']
        enterprise.phone = request.form['phone']

        try:
            DB.session.commit()
            flash('Предприятие успешно обновлено!', 'success')
            return redirect('/enterprise')
        except Exception as e:
            flash('Ошибка обновления данных\n' + str(e), 'danger')
            return render_template(
                'enterprise/update.html',
                enterprise=enterprise
            )
    else:
        return render_template(
            'enterprise/update.html',
            enterprise=enterprise
        )


@ENTERPRISE.route('/enterprise/<int:id>/delete', methods=['GET', 'POST'])
def delete_enterprise(id):
    enterprise = Enterprise.query.get(id)
    try:
        DB.session.delete(enterprise)
        DB.session.commit()
        flash('Предприятие успешно удалено!', 'success')
        return redirect('/enterprise')
    except sqlalchemy.exc.IntegrityError:
        flash('У предприятия есть на данный момент заказы. '
              'При удалении предприятия удаляться все ее заказы. '
              'А вместе с ними удаляться данные о доставках.\n'
              'Удалить все?', 'danger')
        return redirect('/enterprise/' + str(id) + '/delete-error')


@ENTERPRISE.route('/enterprise/<int:id>/delete-error', methods=['GET', 'POST'])
def integrity_error(id):
    enterprise = Enterprise.query.get(id)
    if request.method == 'POST':
        try:
            # Переместить доставки
            sql_replace_delivery = text(
                f"INSERT INTO delivery_deleted\n"
                f"SELECT * FROM delivery\n"
                f"WHERE cosmetic_order_id IN\n"
                f"(SELECT cosmetic_order_id FROM cosmetic_order\n"
                f"WHERE enterprise_id={id});"
            )
            # Удалить доставки
            sql_delete_delivery = text(
                f"DELETE FROM delivery\n"
                f"WHERE cosmetic_order_id IN\n"
                f"(SELECT cosmetic_order_id FROM cosmetic_order\n"
                f"WHERE enterprise_id={id});"
            )
            # Переместить заказы
            sql_replace_order = text(
                f"INSERT INTO cosmetic_order_deleted\n"
                f"SELECT * FROM cosmetic_order\n"
                f"WHERE enterprise_id={id};"
            )
            # Удалить заказы
            sql_delete_order = text(
                f"DELETE FROM cosmetic_order\n"
                f"WHERE cosmetic_order_id IN\n"
                f"(SELECT cosmetic_order_id FROM cosmetic_order\n"
                f"WHERE enterprise_id={id});"
            )
            # Переместить предприятия доставки
            sql_replace_enterprise = text(
                f"INSERT INTO enterprise_deleted\n"
                f"SELECT * FROM enterprise\n"
                f"WHERE enterprise_id={id};"
            )
            # Удалить предприятия доставки
            sql_delete_enterprise = text(
                f"DELETE FROM enterprise\n"
                f"WHERE enterprise_id={id};"
            )

            # Создаем транзакции по мягкому удалению данных
            # Доставки
            transaction_delivery_soft_delete = text(
                f"BEGIN;\n"
                f"{sql_replace_delivery};\n"
                f"{sql_delete_delivery};\n"
                f"COMMIT;"
            )
            # Заказы
            transaction_order_soft_delete = text(
                f"BEGIN;\n"
                f"{sql_replace_order};\n"
                f"{sql_delete_order};\n"
                f"COMMIT;"
            )
            # Предприятия
            transaction_enterprise_soft_delete = text(
                f"BEGIN;\n"
                f"{sql_replace_enterprise};\n"
                f"{sql_delete_enterprise};\n"
                f"COMMIT;"
            )

            # Выполняем транзакции
            with DB.engine.connect() as conn:
                print('Удаление доставок')
                conn.execute(transaction_delivery_soft_delete)
                print('Удаление заказов')
                conn.execute(transaction_order_soft_delete)
                print('Удаление предприятий')
                conn.execute(transaction_enterprise_soft_delete)
            flash('Доставки, заказы и предприятия успешно удалены!', 'success')
            return redirect('/enterprise')
        except Exception as e:
            flash('Произошла ошибка удалениея', 'danger')
            print(e)
            return redirect('/enterprise')

    else:
        return render_template(
            'enterprise/error/delete_error.html',
            enterprise=enterprise
        )



