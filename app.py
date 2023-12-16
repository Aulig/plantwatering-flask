import json
import time

from flask import Flask, render_template, request, abort
from flask_apscheduler import APScheduler

from toolbox.utils import tail

app = Flask(__name__)

app.config["LOG_FILENAME"] = "activity.log"
app.config["GPIO_PIN"] = 8

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Setup the logger
from logger_setup import logger



def enable_pump(milliseconds):
    logger.info(f"Pumping for {milliseconds} milliseconds")

    try:
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(app.config["GPIO_PIN"], GPIO.OUT)

        GPIO.output(app.config["GPIO_PIN"], True)

        time.sleep(milliseconds / 1000)

        GPIO.output(app.config["GPIO_PIN"], False)

        GPIO.cleanup()
    except ModuleNotFoundError:
        logger.exception("No GPIO available")

    logger.info("Pumping finished")


@scheduler.task("interval", hours=1)
def regular_watering():
    logger.info("Watering through scheduler")
    enable_pump(5000)


@app.route("/")
def index():
    return render_template("index.html", log_lines=tail(app.config["LOG_FILENAME"], lines=100))


@app.route("/water", methods=["POST"])
def water():
    try:
        data = json.loads(request.data)
        milliseconds = int(data["milliseconds"])
    except:
        return abort(400, description="Invalid JSON body")

    logger.info("Watering through HTTP request")
    enable_pump(milliseconds)

    return "", 204


if __name__ == "__main__":
    app.run()
