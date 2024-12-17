import psycopg2.errors
import sqlalchemy.exc
from flask import Blueprint, render_template, request, flash, redirect
from sqlalchemy import text
from ..extensions import DB
from ..models.brand import Brand

BRAND = Blueprint('brand', __name__)


@BRAND.route('/brand', methods=['GET'])
def show_brand():
    brands = Brand.query.all()
    return render_template('brand/all.html', brands=brands)


@BRAND.route('/brand/create', methods=['GET', 'POST'])
def create_brand():
    if request.method == 'POST':
        brand_name = request.form['brand_name']
        brand = Brand(brand_name=brand_name)

        try:
            DB.session.add(brand)
            DB.session.commit()
            flash('Бренд успешно добавлен!', 'success')
            return render_template('brand/create.html')
        except Exception as e:
            flash('Произошла ошибка!', 'danger')
            return redirect('./create')
    else:
        return render_template('brand/create.html')


@BRAND.route('/brand/<int:id>/update', methods=['GET', 'POST'])
def update_brand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        brand.brand_name = request.form['brand_name']
        try:
            DB.session.commit()
            flash('Бренд успешно обновлен!', 'success')
            return redirect('/brand')
        except Exception as e:
            flash('Ошибка обновления данных\n' + str(e), 'danger')
            return render_template('brand/update.html')
    else:
        return render_template(
            'brand/update.html',
            brand=brand
        )


@BRAND.route('/brand/<int:id>/delete', methods=['POST', 'GET'])
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    try:
        DB.session.delete(brand)
        DB.session.commit()
        flash('Бренд успешно удален', 'success')
        print('удален')
        return redirect('/brand')
    except psycopg2.errors.ForeignKeyViolation as e:
        print(str(e))
        flash('НЕОБРАБОТАННАЯ ОШИБКА', 'danger')
        return redirect('/brand')
    except sqlalchemy.exc.IntegrityError as e:
        flash('У этого бренда есть товары. При удалении они удаляться '
              'вместе с брендом, а также удалятся все заказы '
              'с этими товарами.\n'
              'Всё равно удалить?', 'danger')
        return redirect('/brand/' + str(id) + '/delete-error')


@BRAND.route('/brand/<int:id>/delete-error', methods=['GET', 'POST'])
def integrity_error(id):
    brand = Brand.query.get(id)
    if request.method == 'POST':
        try:
            # Перемещаем в таблицу удаленных данных продукты,
            sql_request_replace_product = text(
                f"INSERT INTO product_deleted\n"
                f"(SELECT * FROM product\n"
                f"WHERE brand_id={id})\n"
            )
            # Удаляем продукты из таблицы продуктов
            sql_request_delete_product = text(
                f"DELETE FROM product\n"
                f"WHERE brand_id={id}\n"
            )
            # Перемещаем данные в таблицу удаленных брендов
            sql_request_replace_brand = text(
                f"INSERT INTO brand_deleted\n"
                f"(SELECT * FROM brand\n"
                f"WHERE brand_id={id})\n"
            )
            # Удаляем бренды из таблицы брендов
            sql_request_delete_brand = text(
                f"DELETE FROM brand\n"
                f"WHERE brand_id={id}\n"
            )
            # Перемещаем в таблицу удаленных заказов заказы на удаления
            sql_request_replace_orders = text(
                f"INSERT INTO cosmetic_order_deleted\n"
                f"(SELECT * FROM cosmetic_order\n"
                f"WHERE product_id IN (SELECT product_id\n"
                f"FROM PRODUCT WHERE brand_id={id})\n)"
            )
            # Удаляем заказы из таблицы заказов
            sql_request_delete_orders = text(
                f"DELETE FROM cosmetic_order\n"
                f"WHERE product_id IN\n"
                f"(SELECT product_id\n"
                f"FROM product WHERE\n"
                f"brand_id={id})\n"
            )
            # Перемещаем доставки
            sql_request_replace_delivery = text(
                f"INSERT INTO delivery_deleted\n"
                f"(SELECT * FROM delivery\n"
                f"WHERE cosmetic_order_id IN\n"
                f"(SELECT cosmetic_order_id\n"
                f"FROM cosmetic_order WHERE\n"
                f"product_id IN\n"
                f"(SELECT product_id FROM\n"
                f"product WHERE brand_id={id})))\n"
            )
            # Удаляем доставки
            sql_request_delete_delivery = text(
                f"DELETE FROM delivery\n"
                f"WHERE cosmetic_order_id IN\n"
                f"(SELECT cosmetic_order_id\n"
                f"FROM cosmetic_order WHERE\n"
                f"product_id IN\n"
                f"(SELECT product_id FROM\n"
                f"product WHERE brand_id={id}))\n"
            )
            # Создаем транзацию мягкого удаления доставок
            transaction_delivery_soft_delete = text(
                f"BEGIN;\n"
                f"{sql_request_replace_delivery};\n"
                f"{sql_request_delete_delivery};\n"
                f"COMMIT;\n"
            )
            # Создаем транзацию мягкого удаления заказов
            transaction_order_soft_delete = text(
                f"BEGIN;\n"
                f"{sql_request_replace_orders};\n"
                f"{sql_request_delete_orders};\n"
                f"COMMIT;\n"
            )
            # Создаем транзакцию мягкого удаления продуктов
            transaction_product_soft_delete = text(
                f"BEGIN;\n"
                f"{sql_request_replace_product};\n"
                f"{sql_request_delete_product};\n"
                f"COMMIT;\n"
            )
            # Создаем транзакцию мягкого удаления брендов
            transaction_brand_soft_delete = text(
                f"BEGIN;\n"
                f"{sql_request_replace_brand};\n"
                f"{sql_request_delete_brand};\n"
                f"COMMIT;\n"
            )
            # Выполняем транзакции
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
                print('Начало удаление брендов')
                conn.execute(transaction_brand_soft_delete)
                print('Бренды успешно удалены')
            flash(
                'Продукция, бренд, заказы и достаки успешно удалены',
                  'success'
            )
            return redirect('/brand')
        except Exception as e:
            flash('Произошла ошибка удаления', 'danger')
            print(e)
            return redirect('/brand')
    else:
        return render_template(
            'brand/error/delete_error.html',
            brand=brand
        )
