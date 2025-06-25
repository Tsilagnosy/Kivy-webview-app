from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

if platform == "android":
    from jnius import autoclass, cast
    from android import activity
    from android_webview import WebView
    from android.permissions import request_permissions, Permission, check_permission
    from time import sleep
    import sys

    # 🔐 Active le blocage de captures d'écran
    Window = autoclass('org.kivy.android.PythonActivity').mActivity.getWindow()
    Window.addFlags(0x80000)  # FLAG_SECURE

    # 📋 Liste des autorisations nécessaires
    REQUIRED_PERMISSIONS = [
        Permission.CAMERA,
        Permission.RECORD_AUDIO,
        Permission.ACCESS_FINE_LOCATION,
        Permission.READ_SMS
    ]

    # ⛔️ Ferme l’application proprement
    def exit_app():
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        activity.finishAndRemoveTask()
        # Sécurité supplémentaire au cas où
        sys.exit()

    # 🔄 Demande les autorisations et vérifie le résultat
    def ask_critical_permissions():
        def callback(permissions, grants):
            for i in range(len(grants)):
                if not grants[i]:
                    print(f"Permission refusée : {permissions[i]}")
                    exit_app()
            print("✅ Toutes les autorisations ont été accordées")
        request_permissions(REQUIRED_PERMISSIONS, callback)

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        if platform == "android":
            ask_critical_permissions()  # 🔐 Déclenchée dès le lancement
            web = WebView(url="https://flask-app.onrender.com")  # 🔗 Remplace par ton vrai lien
            self.add_widget(web)

class WebViewApp(App):
    def build(self):
        return Root()

if __name__ == "__main__":
    WebViewApp().run()
