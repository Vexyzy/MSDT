import psycopg2.errors
from flask import Blueprint, render_template, request, flash, redirect
from sqlalchemy import text
from ..extensions import DB
from ..models.cosmetic_order import CosmeticOrder
from ..models.delivery import Delivery

MAX_QUANTITY_OF_PRODUCT = 20
DELIVERY = Blueprint('delivery', __name__)

@DELIVERY.route('/delivery')
def show_delivery():
    select_deliveries_with_product_name = text (
        f"SELECT d.delivery_id,\n"
        f"d.quantity_of_product AS quantity,\n"
        f"d.execution_date,\n"
        f"p.product_name\n"
        f"FROM delivery d\n"
        f"JOIN cosmetic_order c\n"
        f"ON c.cosmetic_order_id = d.cosmetic_order_id\n"
        f"JOIN product p ON c.product_id=p.product_id;"
    )

    with DB.engine.connect() as conn:
        deliveries = conn.execute(
            select_deliveries_with_product_name
        ).fetchall()

    return render_template(
        'delivery/all.html',
        deliveries=deliveries
    )

@DELIVERY.route('/delivery/create', methods=['GET', 'POST'])
def create_delivery():
    # Допустим в 1 доставке не может быть больше 20 позиций
    order_id = request.args.get('order_id')
    if order_id is None or order_id == '':
        error = 'Не передан заказ'
        flash(error, 'danger')
        return redirect('/delivery')

    if not order_id.isdigit():
        error = 'Такого заказа не существует'
        flash(error, 'danger')
        return redirect('/delivery')

    order = CosmeticOrder.query.get(order_id)
    if order is None:
        error = 'Такого заказа не существует'
        flash(error, 'danger')
        return redirect('/delivery')

    total_product_quantity = int(order.quantity_of_product)
    execution_date = order.execution_date
    while total_product_quantity > 0:
        if total_product_quantity >= MAX_QUANTITY_OF_PRODUCT:
            delivery = Delivery(
                cosmetic_order_id=order_id,
                quantity_of_product=MAX_QUANTITY_OF_PRODUCT,
                execution_date=execution_date
            )
            DB.session.add(delivery)
            DB.session.commit()
            total_product_quantity -= MAX_QUANTITY_OF_PRODUCT
        else:
            delivery = Delivery(
                cosmetic_order_id=order_id,
                quantity_of_product=total_product_quantity,
                execution_date=execution_date
            )
            DB.session.add(delivery)
            DB.session.commit()
            total_product_quantity = 0
    flash('Заказ и доставки сформированы', 'success')
    return redirect('/order')

@DELIVERY.route('/delivery/<int:id>/delete', methods=['GET', 'POST'])
def delete_delivery(id):
    delivery = Delivery.query.get(id)
    try:
        replace_delivery = text(
            f"INSERT INTO delivery_deleted\n"
            f"SELECT * FROM delivery "
            f"WHERE delivery_id={id}"
        )
        with DB.engine.connect() as conn:
            conn.execute(replace_delivery)
        
        DB.session.delete(delivery)
        DB.session.commit()
        flash('Доставка успешно удалена', 'success')
        print('удален')
        return redirect('/delivery')
    except psycopg2.errors.ForeignKeyViolation as e:
        print(str(e))
        flash('НЕОБРАБОТАННАЯ ОШИБКА', 'danger')
        return redirect('/delivery')