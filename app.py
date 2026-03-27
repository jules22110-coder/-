from flask import Flask, request, jsonify
import sympy as sp

app = Flask(__name__)

@app.route('/math', methods=['POST'])
def math():
    # 获取请求里的JSON数据
    data = request.get_json()
    expr_str = data.get('expr', '')      # 表达式，如 "x**2"
    operation = data.get('op', 'integrate')  # 操作：integrate, diff, solve
    var = data.get('var', 'x')           # 变量，默认x

    if not expr_str:
        return jsonify({'result': '请提供表达式', 'error': True})

    try:
        # 定义变量
        x = sp.Symbol(var)
        expr = sp.sympify(expr_str)

        if operation == 'integrate':
            result = sp.integrate(expr, x)
        elif operation == 'diff':
            result = sp.diff(expr, x)
        elif operation == 'solve':
            result = sp.solve(expr, x)
        else:
            result = '不支持的操作，请用 integrate/diff/solve'

        return jsonify({'result': str(result), 'error': False})
    except Exception as e:
        return jsonify({'result': f'计算错误: {str(e)}', 'error': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)