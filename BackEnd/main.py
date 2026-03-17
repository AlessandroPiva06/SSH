import tornado.ioloop
import tornado.web
import mysql.connector


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("LogIn.html")

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        # Logica di autenticazione da implementare
        self.write(f"Login ricevuto per: {username}")


class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Register.html")

    def post(self):
        username = self.get_argument("username", "")
        email    = self.get_argument("email", "")
        password = self.get_argument("password", "")
        # Logica di registrazione da implementare
        self.write(f"Registrazione ricevuta per: {username} ({email})")


def make_app():
    return tornado.web.Application(
        [
            (r"/",          LoginHandler),
            (r"/login",     LoginHandler),
            (r"/register",  RegisterHandler),
        ],
        template_path=BASE_DIR,
        static_path=BASE_DIR,
        debug=True,
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server avviato su http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
