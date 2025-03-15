from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import ast
import math
import sympy as sp
import re
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Define allowed mathematical functions
allowed_functions = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'log': math.log, 'log10': math.log10, 'sqrt': math.sqrt,
    'exp': math.exp, 'pi': math.pi, 'e': math.e
}

@app.route('/')
def home():
    return "AOMC Backend is running!"

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get('expression')

    try:
        # ✅ Validate and safely evaluate the expression
        node = ast.parse(expression, mode='eval')
        allowed_nodes = {ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant, ast.Call, ast.Load, ast.Name}

        if not all(isinstance(n, tuple(allowed_nodes)) for n in ast.walk(node)):
            raise ValueError("Invalid expression!")

        result = eval(expression, {"__builtins__": None}, allowed_functions)

        # Extra validation for invalid math results
        if isinstance(result, complex) or math.isnan(result) or math.isinf(result):
            raise ValueError("Invalid mathematical result!")

        return jsonify({'result': result})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except ZeroDivisionError:
        return jsonify({'error': "Division by zero is not allowed!"}), 400
    except Exception:
        return jsonify({'error': "Invalid input!"}), 400

@app.route('/solve', methods=['POST'])
def solve_equation():
    data = request.json
    equation = data.get('equation')

    try:
        x = sp.Symbol('x')
        solved = sp.solve(equation, x)
        return jsonify({'solution': [str(sol) for sol in solved]})

    except Exception:
        return jsonify({'error': "Invalid equation!"}), 400

# ✅ Graph Plotting API
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLOT_PATH = os.path.join(BASE_DIR, "plot.png")

@app.route('/plot', methods=['POST'])
def plot_function():
    data = request.json
    function_str = data.get('function')

    try:
        x = sp.Symbol('x')
        function = sp.sympify(function_str, locals={"sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt})

        # ✅ Generate X and Y values
        x_vals = np.linspace(-10, 10, 400)
        y_vals = [float(function.subs(x, val)) if function.subs(x, val).is_real else np.nan for val in x_vals]

        # ✅ Create the graph
        plt.figure(figsize=(6, 4))
        plt.plot(x_vals, y_vals, label=function_str, color='blue')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.legend()

        # ✅ Save the graph
        plt.savefig(PLOT_PATH)
        plt.close()

        return jsonify({'message': "Graph created successfully"})

    except Exception as e:
        return jsonify({'error': f"Invalid function: {str(e)}"}), 400

# ✅ New GET route to fetch the graph image
@app.route('/get_plot', methods=['GET'])
def get_plot():
    return send_file(PLOT_PATH, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
