import requests
import win32api

from bs4 import BeautifulSoup
from selenium import webdriver


def getlink(search, num):
    browser_width = 1920  # 设置浏览器窗口的宽度
    browser_height = 1080  # 设置浏览器窗口的高度
    url = 'https://www.agemys.org/search?query={}'.format(search)
    episode_num = '第{}集'.format(num)
    # 发起 GET 请求
    response = requests.get(url, proxies={'http': 'http://localhost:7890',
                                          'https': 'http://localhost:7890'
                                          })
    print('网页请求完毕！')
    # time.sleep(1)

    # 检查响应状态码
    if response.status_code == 200:
        print('获取链接中，请稍候...')
        # 获取 HTML 内容
        html = response.text
        # 打印或处理 HTML 内容
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find('div', class_='video_cover_wrapper'):
            tag = soup.find('div', class_='video_cover_wrapper').find('a')
            href = tag['href']
            code = href.split('/')[-1]
            print('番剧代码：', code)

            v_url = 'https://www.agemys.org/play/{}/1/{}'.format(code, num)
            response = requests.get(v_url, proxies={'http': 'http://localhost:7890',
                                                    'https': 'http://localhost:7890'
                                                    })
            # time.sleep(1)

            # 检查响应状态码
            if response.status_code == 200:
                # 获取 HTML 内容
                v_html = response.text
                # 打印或处理 HTML 内容
                # print(html)
                # 创建一个 BeautifulSoup 对象
                soup = BeautifulSoup(v_html, 'html.parser')

                # 提取特定元素，例如提取标签的文本内容
                # 提取视频链接
                video_tag = soup.find('iframe', {'id': 'iframeForVideo'})

                if video_tag:
                    print('获取链接成功，准备打开Chrome！')
                    video_src = video_tag['src']
                    # print('视频链接:', video_src)

                    # 提取视频标题
                    title_tag = soup.find('h5', {'class': 'card-title'})
                    if title_tag:
                        video_title = title_tag.text.strip()
                        # print('视频标题:', video_title)

                        # 获取显示器的宽度和高度
                        screen_width = win32api.GetSystemMetrics(0)
                        screen_height = win32api.GetSystemMetrics(1)

                        # 计算浏览器窗口的位置，使其居中
                        browser_x = (screen_width - browser_width) // 2
                        browser_y = (screen_height - browser_height) // 2

                        # 创建一个 WebDriver 实例，例如 Chrome
                        driver = webdriver.Chrome()

                        # 设置窗口大小和位置
                        driver.set_window_size(browser_width, browser_height)
                        driver.set_window_position(browser_x, browser_y)

                        # 打开网页
                        url = video_src  # 替换为要访问的网页链接
                        driver.get(url)

                        # 设置网页标题
                        driver.execute_script(f"document.title = '{video_title} {episode_num}'")

                        return code
                else:
                    print('视频信息提取失败，请确认有第{}集后重试！'.format(num))
                    flg = 0
                    return flg

            else:
                print('视频信息请求失败，请检查网络状态，状态码：', response.status_code)
                flg = 0
                return flg

        else:
            print('未搜索到结果，请确认番名后重试！')
            flg = 0
            return flg

    else:
        print('视频搜索请求失败，请检查网络状态，状态码：', response.status_code)
        flg = 0
        return flg


def get_next_link(code, num):
    browser_width = 1920  # 设置浏览器窗口的宽度
    browser_height = 1080  # 设置浏览器窗口的高度

    episode_num = '第{}集'.format(num)

    v_url = 'https://www.agemys.org/play/{}/1/{}'.format(code, num)
    response = requests.get(v_url, proxies={'http': 'http://localhost:7890',
                                            'https': 'http://localhost:7890'
                                            })
    # time.sleep(1)

    # 检查响应状态码
    if response.status_code == 200:
        print('获取链接中，请稍候...')
        # 获取 HTML 内容
        v_html = response.text
        # 打印或处理 HTML 内容
        # print(html)
        # 创建一个 BeautifulSoup 对象
        soup = BeautifulSoup(v_html, 'html.parser')

        # 提取特定元素，例如提取标签的文本内容
        # 提取视频链接
        video_tag = soup.find('iframe', {'id': 'iframeForVideo'})

        if video_tag:
            video_src = video_tag['src']
            # print('视频链接:', video_src)

            # 提取视频标题
            title_tag = soup.find('h5', {'class': 'card-title'})
            if title_tag:
                print('获取链接成功，准备打开Chrome！')
                video_title = title_tag.text.strip()
                # print('视频标题:', video_title)

                # 获取显示器的宽度和高度
                screen_width = win32api.GetSystemMetrics(0)
                screen_height = win32api.GetSystemMetrics(1)

                # 计算浏览器窗口的位置，使其居中
                browser_x = (screen_width - browser_width) // 2
                browser_y = (screen_height - browser_height) // 2

                # 创建一个 WebDriver 实例，例如 Chrome
                driver = webdriver.Chrome()

                # 设置窗口大小和位置
                driver.set_window_size(browser_width, browser_height)
                driver.set_window_position(browser_x, browser_y)

                # 打开网页
                url = video_src
                driver.get(url)

                # 设置网页标题
                driver.execute_script(f"document.title = '{video_title} {episode_num}'")

                return code

        else:
            print('视频信息提取失败，状态码：', response.status_code)
            flg = 0
            return flg

    else:
        print('视频信息请求失败，状态码：', response.status_code)
        flg = 0
        return flg
