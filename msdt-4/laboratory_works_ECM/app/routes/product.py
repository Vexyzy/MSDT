import psycopg2
import sqlalchemy

from ..models.brand import Brand
from ..extensions import DB
from ..models.product import Product
from sqlalchemy import text
from flask import Blueprint, render_template, request, flash, redirect

PRODUCT = Blueprint('product', __name__)

@PRODUCT.route('/', methods=['GET', 'POST'])
@PRODUCT.route('/product', methods=['GET'])
def show_product():
    product_name = request.args.get('product_name')
    sql_request = text('SELECT '
                    'p.product_id, '
                    'p.product_name, '
                    'b.brand_name, '
                    'p.measurement, '
                    'p.price '
                    'FROM product p '
                    'JOIN brand b ON b.brand_id = p.brand_id')
    with DB.engine.connect() as conn:
        products = conn.execute(sql_request).fetchall()

    return render_template(
        'product/all.html',
        products=products
    )

@PRODUCT.route('/product/search', methods=['GET'])
def search_product():
    product_name = request.args.get('product_name')
    sql_request = text(f"SELECT "
                       f"p.product_id, "
                       f"p.product_name, "
                       f"b.brand_name, "
                       f"p.measurement, "
                       f"p.price "
                       f"FROM product p "
                       f"JOIN brand b ON b.brand_id = p.brand_id "
                       f"WHERE p.product_name ILIKE '%{product_name}%';")
    with DB.engine.connect() as conn:
        products = conn.execute(sql_request).fetchall()
    return render_template(
        'product/search_result.html',
        products=products
    )

@PRODUCT.route('/product/order-delivered', methods=['GET'])
def order_delivered():
    select_order_delivered = text(
        f"SELECT "
        f"p.product_name, "
        f"SUM(co.quantity_of_product) AS total_ordered, "
        f"SUM(COALESCE(d.quantity_of_product, 0)) AS total_delivered "
        f"FROM "
        f"product p "
        f"INNER JOIN "
        f"cosmetic_order co ON p.product_id = co.product_id "
        f"LEFT JOIN "
        f"delivery d ON co.cosmetic_order_id = d.cosmetic_order_id "
        f"GROUP BY "
        f"p.product_name;")
    with DB.engine.connect() as conn:
        products = conn.execute(select_order_delivered).fetchall()
    return render_template(
        'product/order-delivered.html',
        products=products
    )

@PRODUCT.route('/product/most-sell', methods=['GET'])
def show_most_sell_product():
    sql_request = text(
        "SELECT product.product_id, product.product_name, "
        "SUM(cosmetic_order.quantity_of_product) "
        "AS total_quantity_in_orders "
        "FROM product "
        "JOIN cosmetic_order "
        "ON product.product_id = cosmetic_order.product_id "
        "GROUP BY product.product_id "
        "ORDER BY total_quantity_in_orders DESC "
        "LIMIT 5;"
    )
    with DB.engine.connect() as conn:
        products = conn.execute(sql_request).fetchall()

    return render_template('product/most_sell_products.html', products=products)

@PRODUCT.route('/product/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        brand_id = request.form['brand_id']
        measurement = request.form['measurement']
        price = request.form['price']

        product = Product(
            product_name=product_name,
            brand_id=brand_id,
            measurement=measurement,
            price=price
        )

        try:
            DB.session.add(product)
            DB.session.commit()
            flash('Товар успешно добавлен', 'success')
            return redirect('/product/create')
        except sqlalchemy.exc.IntegrityError:
            flash('Такого id бренда не существует', 'danger')
            return render_template(
                'product/create.html',
                product=product
            )
        except Exception as e:
            print(e)
            flash(str(e))
            return render_template(
                'product/create.html',
                product=product
            )
    else:
        return render_template(
    'product/create.html',
                       product=None
        )


@PRODUCT.route('/product/<int:id>/update', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.product_name = request.form['product_name']
        product.brand_id = int(request.form['brand_id'])
        product.measurement = request.form['measurement']
        product.price = int(request.form['price'])
        try:
            DB.session.commit()
            flash('Товар успешно обновлен!', 'success')
            return redirect('/product')
        except (sqlalchemy.exc.IntegrityError,
                psycopg2.errors.ForeignKeyViolation):
            DB.session.rollback()
            flash('Такого id бренда не существует', 'danger')
            return render_template(
                'product/update.html',
                product=product
            )
        except Exception as e:
            DB.session.rollback()  # Откат транзакции для любых других ошибок
            flash('Произошла ошибка при обновлении товара')
            return render_template(
                'product/update.html',
                product=product
            )

    else:
        return render_template(
            'product/update.html',
            product=product
        )


@PRODUCT.route('/product/<int:id>/delete', methods=['POST', 'GET'])
def delete_product(id):
    product = Product.query.get(id)
    try:
        DB.session.delete(product)
        DB.session.commit()
        flash('Товар успешно удален', 'success')
        return redirect('/product')
    except sqlalchemy.exc.IntegrityError:
        flash('На этот товар есть заказы. При удалении они удаляться'
              'вместе с нис, а также удалятся все доставки '
              'с этими товарами.\n'
              'Всё равно удалить?', 'danger')
        return redirect('/product/' + str(id) + '/delete-error')


@PRODUCT.route('/product/<int:id>/delete-error', methods=['GET', 'POST'])
def integrity_error(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        try:
            # Мягко удаляем данные о доставке
            sql_replace_delivery= text(
                f"INSERT INTO delivery_deleted\n"
                f"SELECT * FROM delivery\n"
                f"WHERE cosmetic_order_id IN\n"
                f"(SELECT cosmetic_order_id\n"
                f"FROM cosmetic_order WHERE\n"
                f"product_id={product.product_id})"
            )
            sql_delete_delivery = text(
                f"DELETE FROM delivery\n"
                f"WHERE cosmetic_order_id IN\n"
                f"(SELECT cosmetic_order_id FROM\n"
                f"cosmetic_order WHERE\n"
                f"product_id={product.product_id})"
            )
            # Мягко удаляем данные о заказах
            sql_replace_order = text(
                f"INSERT INTO cosmetic_order_deleted\n"
                f"SELECT * FROM cosmetic_order WHERE\n"
                f"product_id={product.product_id}"
            )
            sql_delete_order = text(
                f"DELETE FROM cosmetic_order\n"
                f"WHERE product_id={product.product_id}"
            )
            # Мягко удаляем данные о товарах
            sql_replace_product = text(
                f"INSERT INTO product_deleted\n"
                f"SELECT * FROM product WHERE\n"
                f"product_id={product.product_id}"
            )
            sql_delete_product = text(
               f"DELETE FROM product\n"
               f"WHERE product_id={product.product_id}"
            )

            # Создаем транзакции
            transaction_delivery_soft_delete = text(
                f"BEGIN\n;"
                f"{sql_replace_delivery};\n"
                f"{sql_delete_delivery};\n"
                f"COMMIT;"
            )
            transaction_order_soft_delete = text(
                f"BEGIN\n;"
                f"{sql_replace_order};\n"
                f"{sql_delete_order};\n"
                f"COMMIT;"
            )
            transaction_product_soft_delete = text(
                f"BEGIN\n;"
                f"{sql_replace_product};\n"
                f"{sql_delete_product};\n"
                f"COMMIT;"
            )

            # Выполняем все транзакции
            with DB.engine.connect() as conn:
                print('Начало удаление доставок')
                conn.execute(transaction_delivery_soft_delete)
                print('Доставки успешно удалены')
                print('Начало удаление заказов')
                conn.execute(transaction_order_soft_delete)
                print('Заказы успешно удалены')
                print('Начало удаление продуктов')
                conn.execute(transaction_product_soft_delete)
                print('Продукты успешно удалены')
            flash('Продукция, заказы и достаки успешно удалены', 'success')
            return redirect('/product')
        except Exception as e:
            flash('Произошла ошибка удалениея', 'danger')
            print(e)
            return redirect('/product')
    else:
        return render_template(
            'product/error/delete_error.html',
            product=product
        )
