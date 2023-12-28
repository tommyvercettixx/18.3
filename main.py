from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATA_FILE = 'data.json'


def load_posts():
  try:
    with open(DATA_FILE, 'r') as file:
      return json.load(file)
  except (FileNotFoundError, json.decoder.JSONDecodeError):
    return []


def save_posts(posts):
  with open(DATA_FILE, 'w') as file:
    json.dump(posts, file)


posts = load_posts()


def save_photo(photo):
  if photo:
    filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    photo.save(filename)
    return filename
  return None


@app.route('/')
def index():
  return render_template('index.html', posts=posts)


@app.route('/create_post', methods=['POST'])
def create_post():
  try:
    title = request.form.get('title')
    photo = request.files.get('photo')
    text = request.form.get('text')

    post = {'title': title, 'text': text, 'photo': save_photo(photo)}
    posts.append(post)
    save_posts(posts)

    return jsonify({'success': True})
  except Exception as e:
    print('Ошибка:', str(e))
    return jsonify({'success': False})


@app.route('/serve_photo/<filename>')
def serve_photo(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
