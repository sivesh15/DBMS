from flask import Flask, render_template_string, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123",
        database="library_db"
    )

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Library Management System</title>
<style>

body {
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    color: #333;
    margin: 35px;
}

h1 {
    color: #23436b;
    margin-bottom: 25px;
}

h2 {
    color: #333;
    margin-top: 25px;
}

form {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px #0000000d;
}

input {
    padding: 10px;
    margin: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

input:focus {
    outline: 1px solid #3269ad;
}

button {
    padding: 10px 16px;
    background: #3269ad;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background: #234b80;
}

table {
    width: 100%;
    margin-top: 20px;
    background: white;
    border-collapse: collapse;
    border-radius: 8px;
    overflow: hidden;
}

th, td {
    padding: 13px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}

th {
    background: #e8eef7;
    color: #23436b;
}

tr:hover {
    background: #f5f8fc;
}

a {
    color: #3269ad;
}

</style>
</head>
<body>
<h1>Library Book Inventory Management</h1>
<form method="post" action="/add">
<input name="title" placeholder="Book title" required>
<input name="author" placeholder="Author" required>
<input name="category" placeholder="Category">
<input name="quantity" type="number" min="0" placeholder="Quantity" required>
<input name="price" type="number" min="0" step="0.01" placeholder="Price" required>
<button type="submit">Add Book</button>
</form>
<h2>Book Records</h2>
<table>
<tr><th>ID</th><th>Title</th><th>Author</th><th>Category</th>
<th>Quantity</th><th>Price</th><th>Actions</th></tr>
{% for b in books %}
<tr>
<td>{{b[0]}}</td><td>{{b[1]}}</td><td>{{b[2]}}</td>
<td>{{b[3]}}</td><td>{{b[4]}}</td><td>{{b[5]}}</td>
<td><a href="/edit/{{b[0]}}">Edit</a> |
<a href="/delete/{{b[0]}}" onclick="return confirm('Delete this book?')">Delete</a></td>
</tr>
{% endfor %}
</table>
</body></html>
"""

@app.route("/")
def home():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM books ORDER BY book_id DESC")
    books = cur.fetchall()
    cur.close()
    con.close()
    return render_template_string(HTML, books=books)

@app.route("/add", methods=["POST"])
def add():
    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO books (title, author, category, quantity, price) "
        "VALUES (%s,%s,%s,%s,%s)",
        (request.form["title"], request.form["author"],
         request.form["category"], int(request.form["quantity"]),
         float(request.form["price"]))
    )
    con.commit()
    cur.close()
    con.close()
    return redirect("/")

@app.route("/delete/<int:book_id>")
def delete(book_id):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
    con.commit()
    cur.close()
    con.close()
    return redirect("/")

@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    con = get_db()
    cur = con.cursor()
    if request.method == "POST":
        cur.execute(
            "UPDATE books SET title=%s, author=%s, category=%s, "
            "quantity=%s, price=%s WHERE book_id=%s",
            (request.form["title"], request.form["author"],
             request.form["category"], int(request.form["quantity"]),
             float(request.form["price"]), book_id)
        )
        con.commit()
        cur.close()
        con.close()
        return redirect("/")
    cur.execute("SELECT * FROM books WHERE book_id=%s", (book_id,))
    book = cur.fetchone()
    cur.close()
    con.close()
    if book is None:
        return "Book not found", 404
    form = """
    <h2>Edit Book</h2><form method="post">
    <input name="title" value="{{b[1]}}" required>
    <input name="author" value="{{b[2]}}" required>
    <input name="category" value="{{b[3] or ''}}">
    <input name="quantity" type="number" min="0" value="{{b[4]}}" required>
    <input name="price" type="number" min="0" step="0.01"
    value="{{b[5]}}" required>
    <button>Save Changes</button></form>
    """
    return render_template_string(form, b=book)

if __name__ == "__main__":
    app.run(debug=True)
