import random
import datetime
from calendar import different_locale

import flask
import psycopg2
import sqlalchemy

from ..extensions import DB
from ..models.cosmetic_order import CosmeticOrder
from ..models.product import Product
from ..models.delivery import Delivery
from sqlalchemy import text
from flask import Blueprint, render_template, request, redirect, flash

ORDER = Blueprint('order', __name__)

@ORDER.route('/order', methods=['GET'])
def show_order():
    sql_request = text(
        'SELECT '
        'c.cosmetic_order_id, '
        'e.enterprise_id, '
        'e.enterprise_name, '
        'p.product_id, '
        'p.product_name, '
        'c.quantity_of_product, '
        'c.order_date, '
        'c.execution_date '
        'FROM cosmetic_order c '
        'JOIN product p ON c.product_id = p.product_id '
        'JOIN enterprise e ON c.enterprise_id = e.enterprise_id '
    )
    with DB.engine.connect() as conn:
        orders = conn.execute(sql_request).fetchall()

    return render_template('order/all.html', orders=orders)

@ORDER.route('/order/create', methods=['POST', 'GET'])
def create_order():
    product_id = request.args.get('product_id')
    print(product_id)
    if product_id is None or product_id == '':
        error = 'Не передан продукт'
        flash(error, 'danger')
        return redirect('/order')

    if not product_id.isdigit():
        error = 'Такого продукта не существует'
        flash(error, 'danger')
        return redirect('/order')

    product = Product.query.get(int(product_id))
    if product is None:
        error = 'Такого продукта не существует'
        flash(error, 'danger')
        return redirect('/order')

    if request.method == 'POST':
        enterprise_id = request.form.get('enterprise_id')
        quantity = request.form.get('quantity')
        order_date = datetime.datetime.now()
        execution_date = order_date + datetime.timedelta(
            days=random.randint(3,20)
        )

        try:
            order = CosmeticOrder(
                enterprise_id=enterprise_id,
                product_id=product_id,
                quantity_of_product=int(quantity),
                order_date=order_date,
                execution_date=execution_date
            )
            DB.session.add(order)
            DB.session.commit()
            order_id = order.cosmetic_order_id
            print('/delivery/create?order_id=' + str(order_id))
            return redirect('/delivery/create?order_id=' + str(order_id))


        except (sqlalchemy.exc.IntegrityError,
                psycopg2.errors.ForeignKeyViolation):
            DB.session.rollback()
            flash('Такого id предприятия не существует', 'danger')
            return render_template(
                'order/create.html',
                product=product
            )
    else:
        return render_template(
            'order/create.html',
            product=product
        )


@ORDER.route('/order/<int:id>/delete', methods=['POST', 'GET'])
def delete_order(id: int):
        order = CosmeticOrder.query.get(id)
        print(order.cosmetic_order_id)
        select_delivery_by_order = text(
            f"SELECT delivery_id FROM delivery\n"
            f"WHERE cosmetic_order_id={id};"
        )
        with DB.engine.connect() as conn:
            delivery = conn.execute(select_delivery_by_order).fetchall()
        print(delivery)
        if not delivery:
            # мягкое удаление заказа
            replace_order = text(
                f"INSERT INTO cosmetic_order_deleted\n"
                f"SELECT * FROM cosmetic_order\n"
                f"WHERE cosmetic_order_id={id};"
            )
            delete_order = text(
                f"DELETE FROM cosmetic_order\n"
                f"WHERE cosmetic_order_id={id};"
            )
            transaction_safe_delete = text(
                f"BEGIN;"
                f"{replace_order};"
                f"{delete_order};"
                f"COMMIT;"
            )
            with DB.engine.connect() as conn:
                print("Мягкое удаление завершено!")
                conn.execute(transaction_safe_delete)
            flash('Успешно удален заказ!')
            return redirect('/order')
        else:
            flash('У заказа уже есть доставки. В случае'
                  ' удаления заказа они удалять вместе с ними\n'
                  'Продолжить удаление?', 'danger')
            return redirect('/order/' + str(id) + '/delete-error')


@ORDER.route('/order/<int:id>/delete-error', methods=['POST', 'GET'])
def integrity_error(id: int):
    if request.method == 'POST':
        try:
            # Мягко удаляем доставку
            replace_delivery = text(
                f"INSERT INTO delivery_deleted\n"
                f"SELECT * FROM delivery\n"
                f"WHERE cosmetic_order_id={id};"
            )
            delete_delivery = text(
                f"DELETE FROM delivery\n"
                f"WHERE cosmetic_order_id={id};"
            )
            # Мягко удаляем заказы
            replace_order = text(
                f"INSERT INTO cosmetic_order_deleted\n"
                f"SELECT * FROM cosmetic_order\n"
                f"WHERE cosmetic_order_id={id};"
            )
            delete_order = text(
                f"DELETE FROM cosmetic_order\n"
                f"WHERE cosmetic_order_id={id};"
            )
            transaction_safe_delete_delivery = text(
                f"BEGIN;"
                f"{replace_delivery};"
                f"{delete_delivery};"
                f"COMMIT;"
            )
            transaction_safe_delete_order = text(
                f"BEGIN;"
                f"{replace_order};"
                f"{delete_order};"
                f"COMMIT;"
            )

            with DB.engine.connect() as conn:
                print('Удаление транзакций')
                conn.execute(transaction_safe_delete_delivery)
                print('Удаление заказов')
                conn.execute(transaction_safe_delete_order)

            flash('Все успешно удалено!', 'success')
            return redirect('/order')
        except Exception as e:
            print(e)
            flash('Произошла ошибка удаления', 'danger')
            return redirect('/order')
    elif request.method == 'GET':
        return render_template(
            'order/error/delete_error.html'
        )
