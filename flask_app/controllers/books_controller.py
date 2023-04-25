from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.book_model import Book

@app.route( "/books", methods=["GET"] )
def get_books():
    if "user_id" not in session:
        return redirect( "/" )
    all_books = Book.get_all_with_users()
    return render_template( "books.html", all_books = all_books )

@app.route( "/book/form", methods=["GET"] )
def display_book_form():
    if "user_id" not in session:
        return redirect( "/" )
    return render_template( "book_form.html" )

@app.route( "/book/new", methods=["POST"] )
def add_book():
    data = {
        **request.form,
        "user_id" : session["user_id"]
    }
    if Book.validate_book( data ) == False:
        return redirect( "/book/form" )
    Book.create_one( data )
    return redirect( "/books" )

@app.route( "/book/<int:id>", methods=["GET"] )
def get_book( id ):
    if "user_id" not in session:
        return redirect( "/" )
    data = {
        "id" : id
    }
    current_book = Book.get_one_with_user( data )
    return render_template( "book.html", current_book = current_book )

@app.route( "/book/remove/<int:id>", methods=["POST"] )
def delete_book( id ):
    data = {
        "id" : id
    }
    Book.delete_one( data )
    return redirect( "/books" )

@app.route( "/book/<int:id>/edit", methods=["GET"] )
def display_update_book_form( id ):
    if "user_id" not in session:
        return redirect( "/" )
    data = {
        "id" : id
    }
    current_book = Book.get_one( data )
    return render_template( "update_book.html", current_book = current_book )


@app.route( "/book/update/<int:id>", methods=["POST"] )
def update_book( id ):
    if Book.validate_book( request.form ) == False:
        return redirect( f"/book/{id}/edit" )
    data = {
        "id" : id,
        **request.form,
        "user_id" : session["user_id"]
    }
    Book.update_one( data )
    return redirect( f"/book/{id}" )

@app.route( "/logout", methods=["POST"] )
def process_logout():
    session.clear()
    return redirect( "/" )