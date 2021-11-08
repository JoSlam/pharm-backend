from flask import request

from App import parse
from App.models import Product
from App.database import db
from App.modules.serialization_module import serializeList

# creates a new product for /create-product endpoint
def create_product(code, name, category, supplier_price, supplier, qoh, stock, unit_price, total, image=None):
    newProd = Product(code=code, product_name=name, category=category, supplier_cost_price=supplier_price,
                      supplier=supplier, QoH=qoh, stock_unit=stock, unit_retail_price=unit_price, total_retail_price=total)
    db.session.add(newProd)
    db.session.commit()
    #print("Successfully added")
    return newProd


# calls the parse.py view method to parse the given excel products file
def parse_excel():
    print('Product controller parse excel')
    prodList = parse.parse()

    print('Inserting products in DB (This may take several minutes).....')
    if prodList:
        for p in prodList:
            # print('Code: {}\nProduct Name: {}\nCategory: {}\nSupplier Cost Price: {}\nSupplier: {}\nQoH: {}\nStock Unit: {}\nUnit Retail: {}\nTotal Retail Price: {}\n'
            # .format(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]))

            x = create_product(p[0], p[1], p[2], p[3],
                               p[4], p[5], p[6], p[7], p[8])
        print('Finished!')
        return 1
    else:
        print('No products parsed')
        return 0


# gets 20 products (pagination) per page
ROWS_PER_PAGE = 20
def get_products_page(page):
    print('getting {0} products'.format(ROWS_PER_PAGE))
    page = request.args.get('page', page, type=int)
    query = Product.query.paginate(
        page=page, per_page=ROWS_PER_PAGE, error_out=False)
    products = query.items
    return serializeList(products)

# wasn't in use yet - made in case you'd want to get numbers instead of
# previous and next buttons for pagination
def get_page_details(page):
    page = request.args.get('page', page, type=int)
    query = Product.query.paginate(
        page=page, per_page=ROWS_PER_PAGE, error_out=False)
    #total_products = query.total
    total_pages = query.pages
    has_next = query.has_next
    has_prev = query.has_prev
    page_details = [{
        "total_pages": total_pages,
        "has_prev": has_prev,
        "has_next": has_next,
    }]
    return page_details

# gets a list of distinct categories from the products
def get_product_categories():
    query = Product.query.with_entities(Product.category).distinct()
    titles = [row.category for row in query.all()]
    return titles

# get all products from DB
def get_products():
    print('Fetching all products')
    products = Product.query.all()
    return serializeList(products)


# delete all products from DB
def delete_products():
    print('Deleting all products')
    x = Product.query.delete()
    db.session.commit()
    print('Rows deleted: ', x)
    return 0

# search through products; used in /search endpoint
def get_products_by_term(term):
    products = Product.query.filter(
        Product.product_name.contains(term)
        | Product.category.contains(term)
        | Product.code.contains(term)
        | Product.supplier.contains(term)
    )
    return serializeList(products)


# get a particular product by its URL-Friendly slug
def get_product_by_slug(slug):
    print(f"Fetching product with slug {slug}")
    p_name = slug.replace("-", " ")
    product = Product.query.filter(Product.product_name==p_name).first()
    return product

# delete a particular product by its URL-Friendly slug
def delete_product_by_slug(slug):
    product = get_product_by_slug(slug)

    print(f"Deleting product with slug {slug}")
    if product:
        if product.orders:
            print("Cannot delete product with existing orders")
            return False

        db.session.delete(product)
        db.session.commit()
        return True
    return False
