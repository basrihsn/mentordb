from flask import Flask, render_template, redirect, request, url_for
from flask_login import login_manager
from werkzeug.security import check_password_hash, generate_password_hash