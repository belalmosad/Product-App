#--------------Imports-------------#
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#-----------------------------------#


#--------------App configs-------------#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newPass@localhost:5432/prod'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#-------------------------------------#


#--------------Models-------------#
class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    year = db.Column(db.Integer)
    comment = db.relationship('Comment', cascade="all,delete", backref='product')
    
class Comment(db.Model):
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))


#---------------------------------#



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add/product')
def add_product():
    return render_template('post_product.html')

@app.route('/add/product', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        description = request.form['description']
        year = request.form['year']
        newProduct = Product(name=name, description=description, year=year)
        db.session.add(newProduct)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('products'))

@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products = products)

@app.route('/product/<productId>')
def show_product(productId):
    product = Product.query.get(productId)
    if not product:
        return render_template('not_found.html')

    return render_template('product.html', product=product, comments = Comment.query.filter(Comment.product_id == productId).order_by('id').all())

@app.route('/product/<productId>/edit')
def edit_product(productId):
    product = Product.query.get(productId)
    return render_template('edit_product.html', product = product)

@app.route('/product/<productId>/edit', methods=['POST'])
def confirm_edit(productId):
    toEdit_product = Product.query.get(productId)
    try:
        name = request.form['name']
        description = request.form['description']
        year = request.form['year']
        toEdit_product.name = name
        toEdit_product.description = description
        toEdit_product.year = year
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_product', productId=productId))
        
@app.route('/product/<productId>/delete')
def delete_product(productId):
    product = Product.query.get(productId)
    try:
        db.session.delete(product)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('products'))

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    products = db.session.query(Product).filter(Product.name.ilike(f'%{search_term}%')).all()
    return render_template('search_item.html', products=products)
@app.route('/add/comment/for/<productId>', methods=['POST'])
def add_comment(productId):
    try:
        content = request.form['content']
        newComment = Comment(content = content, product_id = productId)
        db.session.add(newComment)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_product', productId=productId))
@app.route('/delete/<commentId>', methods=['DELETE'])
def del_comment(commentId):
    comment = Comment.query.get(commentId)
    try:
        db.session.delete(comment)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({'success' : True})

@app.route('/edit/comment/<commentId>', methods=['POST'])
def edit_comment(commentId):
    toEdit = Comment.query.get(commentId)
    productId = toEdit.product_id
    try:
        newComment = request.form['new_comment']
        toEdit.content = newComment
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_product', productId=productId))
app.run(debug=True)