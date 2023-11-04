from flask import Flask, request
from duckduckgo_search import DDGS
from itertools import islice
from flask_cors import CORS

app = Flask(__name__)
CORS(app,  origins=["http://127.0.0.1:5500", "https://tangible-super-manchego.glitch.me"])

@app.route('/analyze', methods=['OPTIONS'])
def analyze_options():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST"
    }



@app.after_request
def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  response.headers.add('Access-Control-Allow-Origin', 'https://tangible-super-manchego.glitch.me')

  return response
@app.route('/search')
def search():
    # 从请求参数中获取关键词
    keywords = request.args.get('q')
    # 从请求参数中获取最大结果数，如果未指定，则默认为10
    max_results = int(request.args.get('max_results', 10))
    results = []

    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.text(keywords, safesearch='Off', timelimit='y', backend="lite")
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'results': results}

if __name__ == '__main__':
    app.run(host='0.0.0.0')

