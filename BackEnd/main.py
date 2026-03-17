import bcrypt
import tornado.ioloop
import tornado.web
import mysql.connector


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("LogIn.html")

    def post(self):
        body = tornado.escape.json_decode(self.request.body)
        email = self.get_argument("email", "")
        password = body.get("password", "")
        # Logica di autenticazione da implementare



class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Register.html")


    async def post(self):
        body = tornado.escape.json_decode(self.request.body)
        email = body.get("email", "").strip()
        password = body.get("password", "")
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.write(f"Registrazione ricevuta per: {email} ({hashed})")
        #return self.write_json({"message": "Registrazione completata"}, 201)


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
