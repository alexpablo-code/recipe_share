from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route("/recipes")
def all_recipes():
    if "user_id" not in session:
        return redirect("/")

    user = User.select_by_id(session["user_id"])
    
    all_recipes = Recipe.all_recipes_with_creator()

    return render_template("all_recipes.html", user=user, all_recipes=all_recipes )

@app.route("/recipes/new")
def new_recipe():
    if "user_id" not in session:
        return redirect("/")

    return render_template("new_recipe.html")

@app.route("/add-recipe", methods=['POST'])
def add_recipe():
    if "user_id" not in session:
        return redirect("/")

    elif not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")

    Recipe.create_recipe(request.form)

    return redirect("/recipes")

@app.route("/recipes/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/")

    recipe = Recipe.select_by_id(recipe_id)

    return render_template("edit_recipe.html", recipe=recipe)

@app.route("/update-recipe", methods=['POST'])
def update_recipe():
    if "user_id" not in session:
        return redirect("/")

    elif not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")

    Recipe.update_recipe(request.form)

    return redirect("/recipes")

@app.route("/recipes/<int:recipe_id>")
def view_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/")

    recipe = Recipe.one_recipe_with_creator(recipe_id)

    return render_template("recipe_details.html", recipe=recipe)


@app.route("/delete-recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/")
    Recipe.delete(recipe_id)

    return redirect("/recipes")

    

