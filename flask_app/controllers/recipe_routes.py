from flask import Flask, render_template, redirect, request, session
from flask_app.models import recipe_model, user_model
from flask_app import app

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    id={
        "id": session['user_id']
    }
    logged_user = user_model.User.get_one_user(id)
    return render_template('dashboard.html', all_recipes=recipe_model.Recipe.get_all_recipes_creator(), current_user=logged_user)

@app.route('/create/recipes')
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create.html')

@app.route('/process/recipe', methods=['POST'])
def process_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not recipe_model.Recipe.validate_recipe(request.form):
        return redirect('/create/recipes')
    recipe_data={
        "user_id": session['user_id'], #since we don't have user_id hidden input in our form we can put user_id here safetly
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_30": request.form['under_30']
    }
    recipe_model.Recipe.save_recipe(recipe_data)
    return redirect('/dashboard')

@app.route('/user/account')
def users_recipe():
    if 'user_id' not in session:
        return redirect('/')
    id={
        "id":session['user_id']
    }
    user= user_model.User.get_one_user_w_recipes(id)
    return render_template("dashboard.html", current_user=user)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    recipe_id={
        "id":id
    }
    one_recipe= recipe_model.Recipe.get_one_recipe_w_user(recipe_id)
    return render_template('edit.html', one_recipe= one_recipe)
   

@app.route('/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not recipe_model.Recipe.validate_recipe(request.form):
        return redirect('/create/recipes')
    reciepe_data={
        "id": id,
        "user_id": session['user_id'], #since we don't have user_id hidden input in our form we can put user_id here safetly
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_30": request.form['under_30']
    }
    recipe_model.Recipe.update_recipe(reciepe_data)
    return redirect(f"/show/{id}")

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    recipe_id={
        "id":id
    }
    recipe_model.Recipe.delete_recipe(recipe_id)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_recipe(id):
    recipe_id={
        "id":id
    }
    one_recipe= recipe_model.Recipe.get_one_recipe_w_user(recipe_id)
    return render_template('view.html', one_recipe= one_recipe)