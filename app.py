from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)