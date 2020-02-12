import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS
import random
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models import setup_db, Book

BOOKS_PER_SHELF = 8

app = Flask(__name__)
setup_db(app)
CORS(app)


# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there. 
#     If you do not update the endpoints, the lab will not work - of no fault of your API code! 
#   - Make sure for each route that you're thinking through when to abort and with which kind of error 
#   - If you change any of the response body keys, make sure you update the frontend to correspond. 


#This function used to paginate boooks 
def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF
    
    books = [book.format() for book in selection]
    current_books = books[start:end]

# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__)
#     setup_db(app)
#     CORS(app)


# CORS Headers 
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response



# @TODO: Write a route that retrivies all books, paginated. 
#         You can use the constant above to paginate by eight books.
#         If you decide to change the number of books per page,
#         update the frontend to handle additional books in the styling and pagination
#         Response body keys: 'success', 'books' and 'total_books'
# TEST: When completed, the webpage will display books including title, author, and rating shown as stars

@app.route('/books')
def retrive_books(): 
    selection = Book.query.order_by(Book.id).all()
    print('\nselection => {}\n'.format(selection))
    current_book = paginate_books(request,selection)
              
    if current_books is None or len(current_book)==0: 
        abort(404)
    
    return jsonify({
        'success': True,
        'books':current_book,
        'total_books':len(Book.query.all())
    })
    
        
    

# @TODO: Write a route that will update a single book's rating. 
#         It should only be able to update the rating, not the entire representation
#         and should follow API design principles regarding method and route.  
#         Response body keys: 'success'
# TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh


# @TODO: Write a route that will delete a single book. 
#        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
#        Response body keys: 'success', 'books' and 'total_books'

# TEST: When completed, you will be able to delete a single book by clicking on the trashcan.


# @TODO: Write a route that create a new book. 
#        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
# TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books. 
#       Your new book should show up immediately after you submit it at the end of the page. 

if __name__ == '__main__':
    app.run()
    