@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
    except Exception as e:
        return "Invalid name", 400
    else:
        if name == '':
            return "Invalid name", 400
    
    try:
        email = request.form['email']
    except Exception as e:
        return "Invalid email", 400
    else:
        if email == '':
            return "Invalid email", 400

    try:
        content = request.form['content']
    except Exception as e:
        return "Invalid content", 400
    else:
        if content == '':
            return "Invalid content", 400

    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return "Invalid email", 400
    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)
