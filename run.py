import threading
import os
import asyncio

from base import app

if __name__ == "__main__":
    print("Flask server starting ...")
    app.run(host = "0.0.0.0", debug = True, use_reloader = True)
    
