from DrissionPage import ChromiumPage, ChromiumOptions
import time
import os

def crawl_toutiao_article(url):
    """
    爬取今日头条文章内容
    :param url: 文章URL
    :return: 文章标题、内容和图片URL列表
    """
    # 创建配置对象
    options = ChromiumOptions()
    options.set_argument('--headless')  # 使用命令行参数设置无头模式
    
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
        
        
        
        result = {
            "标题": title,
            "内容": content,
        }
        
        return result
    
    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
        return None
    finally:
        # 关闭浏览器
        page.quit()
        print("已关闭浏览器")


def save_to_file(article_data, filename=None):
    """
    将文章内容保存到文件
    :param article_data: 文章数据字典
    :param filename: 文件名，默认使用文章标题
    :return: 保存的文件夹路径
    """
    if not article_data:
        return False
    
    if not filename:
        filename = article_data["标题"]
    
    # 替换文件名中的非法字符
    for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
        filename = filename.replace(char, '_')
    
    # 创建文件夹保存文章和图片
    folder_path = filename
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # 保存文章内容
    with open(os.path.join(folder_path, f"{filename}.txt"), "w", encoding="utf-8") as f:
        for key, value in article_data.items():
            if key == "内容":
                f.write(f"\n{'-'*50}\n{key}:\n{'-'*50}\n{value}\n")
            elif key == "图片URL":
                f.write(f"\n{'-'*50}\n图片数量: {len(value)}\n")
                for i, url in enumerate(value):
                    f.write(f"图片{i+1}: {url}\n")
            else:
                f.write(f"{key}: {value}\n")
    
    # 下载图片
    if article_data.get("图片URL"):
        print(f"\n开始下载图片...")
        img_count = download_images(article_data["图片URL"], folder_path)
        print(f"成功下载 {img_count}/{len(article_data['图片URL'])} 张图片")
    
    return folder_path

def main():
    print("=" * 50)
    print("今日头条文章爬取工具")
    print("=" * 50)
    
    while True:
        url = input("\n请输入今日头条文章URL (输入'q'退出): ")
        
        if url.lower() == 'q':
            print("程序已退出")
            break
        
        if not url.startswith("http"):
            print("请输入有效的URL地址")
            continue
        
        print("\n开始爬取文章...")
        article_data = crawl_toutiao_article(url)
        
        if article_data:
            print("\n爬取成功!")
            print(f"标题: {article_data['标题']}")
            print(f"作者: {article_data['作者']}")
            print(f"发布时间: {article_data['发布时间']}")
            print(f"内容长度: {len(article_data['内容'])}字符")
            print(f"图片数量: {len(article_data['图片URL'])}")
            
            save_option = input("\n是否保存文章和图片? (y/n): ")
            if save_option.lower() == 'y':
                filename = input("请输入保存文件夹名称(直接回车使用文章标题): ")
                if not filename:
                    filename = None
                
                folder_path = save_to_file(article_data, filename)
                if folder_path:
                    print(f"文章和图片已保存到文件夹: {folder_path}")
                else:
                    print("保存失败")
        else:
            print("文章爬取失败")

if __name__ == "__main__":
    main()
