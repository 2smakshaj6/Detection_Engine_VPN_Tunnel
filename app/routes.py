from flask import Blueprint, render_template, request, redirect, url_for, flash
from detection_engine import detect_ip
from app.utils import get_client_ip
import requests
import os

main = Blueprint('main', __name__)

def get_public_ip():
    try:
        return requests.get('https://api64.ipify.org?format=json').json()['ip']
    except:
        return None

@main.route('/', methods=['GET', 'POST'])
def index():
    ip = ''
    result = None
    if request.method == 'POST':
        ip = request.form.get('ip')
        if ip:
            return redirect(url_for('main.show_result', ip=ip))
    return render_template('index.html', ip=ip, result=result, my_ip=get_public_ip())

@main.route('/result/<ip>')
def show_result(ip):
    try:
        result = detect_ip(ip)
        return render_template(
            'result.html',
            ip=ip,
            result=result,
            my_ip=get_client_ip(request),
            google_maps_key=os.getenv("GOOGLE_MAPS_API_KEY")
        )
    except Exception as e:
        # This logs the actual error
        import logging
        logging.error(f"Error detecting IP {ip}: {e}", exc_info=True)
        flash("Something went wrong while analyzing the IP.", "danger")
        return redirect(url_for('main.index'))

@main.route('/my-ip')
def check_my_ip():
    user_ip = get_client_ip()
    if user_ip:
        return redirect(url_for('main.show_result', ip=user_ip))
    flash("Could not retrieve your IP address.")
    return redirect(url_for('main.index'))

@main.route('/flag-ip', methods=['POST'])
def flag_ip():
    flagged_ip = request.form.get('flagged_ip')
    if flagged_ip:
        try:
            with open('flagged_ips.txt', 'a') as f:
                f.write(f"{flagged_ip}\n")
            flash(f"IP {flagged_ip} has been flagged for review.", 'success')
        except Exception as e:
            flash(f"Error flagging IP: {e}", 'danger')
    return redirect(url_for('main.show_result', ip=flagged_ip))

