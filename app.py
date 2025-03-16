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
            url = url.split(' ',1)[0]
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
    options.set_argument('--headless=new')
    options.set_argument('--no-sandbox')
    options.set_argument('--disable-dev-shm-usage')
    options.set_browser_path('/usr/bin/google-chrome-stable')
    
    page = None
    try:
        page = ChromiumPage(options)
        print("已启动无头浏览器...")
        
        # 访问文章页面
        page.get(url)
        print("正在加载页面...")
        time.sleep(5)  # 等待页面加载
        
        # 获取页面标题
        title = page.title
        print(f"页面标题: {title}")
        
        # 尝试获取文章标题 - 今日头条特定结构
        try:
            # 尝试获取文章标题元素
            title_element = page.ele('xpath://h1[@class="article-title"]', timeout=2)
            if title_element and title_element.text.strip():
                title = title_element.text.strip()
        except:
            # 如果找不到特定标题元素，使用页面标题
            pass
        
        print(f"文章标题: {title}")
        
        
        # 获取文章内容 - 今日头条特定结构
        content = ""
        try:
            # 获取所有section元素，这些元素包含文章段落
            section_elements = page.eles('xpath://section[@style="line-height: 2em;"]')
            
            paragraphs = []
            for section in section_elements:
                # 获取section中的span元素，这些元素包含文本
                span_elements = section.eles('xpath:.//span')
                for span in span_elements:
                    if span.text and span.text.strip():
                        paragraphs.append(span.text.strip())
            
            if paragraphs:
                content = '\n\n'.join(paragraphs)
            
            # 如果上面的方法没有获取到内容，尝试直接获取div_tag中的内容
            if not content:
                content_div = page.ele('xpath://div[@id="js_content"]', timeout=2)
                if content_div:
                    content = content_div.text.strip()
        except Exception as e:
            print(f"提取内容时出错: {e}")
        
        # 如果仍然没有内容，尝试获取所有可见文本
        if not content:
            try:
                # 获取所有可见的段落文本
                p_elements = page.eles('xpath://p[string-length(text()) > 10]')
                paragraphs = [p.text.strip() for p in p_elements if p.text and p.text.strip()]
                if paragraphs:
                    content = '\n\n'.join(paragraphs)
            except:
                pass
        
        # 格式化内容，将换行符转换为HTML换行
        formatted_content = content.replace('\n', '<br>')
        
        return render_template('index.html', 
                              title=title, 
                              author=author, 
                              publish_time=publish_time, 
                              content=formatted_content,
                              url=url)
    
    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
        return render_template('index.html', error_message=f"爬取失败: {str(e)}")
    finally:
        if page:
            page.quit()
            print("已关闭浏览器")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True) 