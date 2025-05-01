from flask import Blueprint, render_template, redirect, url_for, re

site_bp = Blueprint('site', __name__)

@site_bp.route('/')
def index():
    return render_template('index.html')