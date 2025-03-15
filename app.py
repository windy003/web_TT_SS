from DrissionPage import ChromiumPage, ChromiumOptions
import time
import os
from flask import Flask, request, render_template
import re
import html
import time
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'url' in request.form:
            url = request.form['url']
            return load_from_url(url)
    
    return render_template('index.html')



def load_from_url(url):
    """
    爬取今日头条文章内容
    :param url: 文章URL
    :return: 文章标题、内容和图片URL列表
    """
    # 创建配置对象
    options = ChromiumOptions()
    options.set_argument('--headless=new')  # 使用新的无头模式
    options.set_argument('--no-sandbox')    # 在Linux系统中添加此参数
    options.set_argument('--disable-dev-shm-usage')  # 避免内存不足问题
    
    # 使用配置创建页面对象
    page = ChromiumPage(options)
    print("已启动无头浏览器...")
    
    try:
        # 访问文章页面
        page.get(url)
        print("正在加载页面...")
        time.sleep(2)  # 等待页面加载
        
        # 获取文章标题
        title = page.ele('xpath://h1').text
        print(f"文章标题: {title}")
        
        # 获取文章内容
        content_elements = page.eles('xpath://article//p')
        content = '\n'.join([ele.text for ele in content_elements if ele.text])
        
        
        
        
        return render_template('index.html', title=title, content=content)
    
    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
        return None
    finally:
        # 关闭浏览器
        page.quit()
        print("已关闭浏览器")


# 定义一个专门的清理函数
def clean_text(text):
    if not text:
        return ""
    
    # 只替换特殊空白字符，保留HTML标签
    text = text.replace('\xa0', ' ')
    
    # 去除首尾空白
    text = text.strip()
    
    # 移除所有下划线，但保留下划线上的字符
    text = text.replace('_', '')
    
    return text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True) 