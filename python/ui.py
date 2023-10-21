import threading, flask, requests, flask_cors, json, os, sys, webview, webbrowser, tkinter, time
from tkinter import Tk, ttk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class LoadingScreen(Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        window_height = 500
        window_width = 340
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        #self.geometry(f"340x500+340+500")
        self.configure(background='black')
        self.title("Revolution App Loading Engine")
        self.eval('tk::PlaceWindow . center')

        frame = tkinter.Frame(self)
        frame.grid()
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", troughcolor='#444', background='white')
        self.a = ttk.Progressbar(frame, style="red.Horizontal.TProgressbar", orient="horizontal",
                        length=340, mode="indeterminate", maximum=100, value=0)
        self.a.grid(row=1, column=1)
        frame.pack()

        def set_progress():
            for i in range(0, 100, 1):
                self.a.configure(value=i)
                time.sleep(0.1)
            for i in range(100, 0, -1):
                self.a.configure(value=i)
                time.sleep(0.1)

        #self.after(1000, set_progress)

    def start(self):
        self.mainloop()

fl = flask.Flask('app')
w = os.path.exists(resource_path('authorization/token'))

class App(flask.Flask):
    def __init__(self):
        super().__init__('app', template_folder=resource_path("ui/"))
        @self.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

        @self.route('/')
        def g():
            if w:
                print("Logging in with token: "+open('authorization/token','r').readline().split(' ')[0])
                return flask.render_template('i.html', token=open('authorization/token','r').readline().split(' ')[0])
            else: 
                webbrowser.open('https://revolution-web.repl.co/app/login/authorize-with-app', 2)
                return flask.render_template('login.html')
        
        @self.route('/auththw')
        def a():
            token = flask.request.args.get('token')
            with open(resource_path('authorization/token'), 'w') as f:
                f.write(token)
            print("Authorization successful")
            return """
You have successfully authorized. Please close this window and click the button saying "I have logged in" on the desktop app.
"""

        @self.route('/authorization/token')
        def gettokenauth():
            return open('authorization/token','r').readline().split(' ')[0]

        @self.route('/script.js')
        def script():
            return flask.send_file(resource_path('ui/script.js'))
        
        @self.route('/dms-new.js')
        def script2():
            return flask.send_file(resource_path('ui/dms-new.js'))
        
        @self.route('/server-beta.js')
        def script3():
            return flask.send_file(resource_path('ui/server-beta.js'))

    def start(self):
        threading.Thread(target=self.run, args=('0.0.0.0', 9273), daemon=True).start()
        uid = 'master' if len(webview.windows) == 0 else 'child_' + webview.uuid4().hex[:8]
        self.window = webview.Window(uid, 'Revolution Desktop', 'http://localhost:9273', zoomable=True, text_select=True, width=Tk().winfo_screenwidth(), height=Tk().winfo_screenheight())
        webview.windows.append(self.window)
        #webview.create_window('Revolution Desktop', 'http://localhost:9273', zoomable=False, frameless=True)
        webview.start()


@fl.route('/request')
@flask_cors.cross_origin()
def a_():
    #flask.request.headers.add("Access-Control-Allow-Origin", "*")
    r = flask.request.headers.get('to')
    t = flask.request.headers.get('type')
    h = flask.request.headers.get('rHeaders')
    d = flask.request.headers.get('rData')
    j = flask.request.headers.get('rJSON')
    if t.lower() == 'get':
        try:
            l = json.loads(h)
        except: l = None
        resp = requests.get(r, headers=l, data=d)
        try:
            json2 = resp.json()
        except: json2 = None
        return flask.jsonify({
            "status": resp.status_code,
            "text": resp.text,
            "json": (json2 or None),
            "url": resp.url,
            #"cookies": resp.cookies,
            #"headers": resp.headers,
            "body": resp.content.decode(),
            #"encoding": resp.encoding
        }), resp.status_code
    if t.lower() == 'post':
        try:
            l = json.loads(h)
        except: l = None
        resp = requests.post(r, headers=l, data=d, json=j)
        try:
            json2 = resp.json()
        except: json2 = None
        return flask.jsonify({
            "status": resp.status_code,
            "text": resp.text,
            "json": (json2 or None),
            "url": resp.url,
            #"cookies": resp.cookies,
            #"headers": resp.headers,
            "body": resp.content.decode(),
            #"encoding": resp.encoding
        }), resp.status_code
    return "401",401


threading.Thread(target=fl.run, args=('0.0.0.0', 9274), daemon=True).start()

#def updateUI():
    #resource_path()

def run():
    s = App()
    s.start()