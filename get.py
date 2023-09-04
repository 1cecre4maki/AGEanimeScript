import requests
import win32api

from bs4 import BeautifulSoup
from selenium import webdriver


def getlink():
    browser_width = 1920  # 设置浏览器窗口的宽度
    browser_height = 1080  # 设置浏览器窗口的高度

    search = input('请输入搜索的番名：(input "q" to Quit other to Continue)')
    if search == 'q' or search == 'Q':
        print('期待下次使用！')
        return 1, 0, 0

    else:
        url = 'https://www.agemys.org/search?query={}'.format(search)
        # 发起 GET 请求
        print('请求中...请稍候...')
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

                status = soup.find('span', class_='video_play_status')
                status_text = status.get_text(strip=True) if status else "Element not found"
                print('更新状态：', status_text)

                num = input('请输入观看的集数：(input "q" to Quit other to Continue)')
                episode_num = '第{}集'.format(num)

                if num == 'q' or num == 'Q':
                    print('期待下次使用！')
                    return 1, 0, 0
                else:
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
                                print('加载网页中，请稍候...')
                                driver.get(url)

                                # 设置网页标题
                                driver.execute_script(f"document.title = '{video_title} {episode_num}'")

                                return code, driver, num

                        else:
                            print('视频信息提取失败，请确认有第{}集后重试！'.format(num))
                            return 0, 0, 0

                    else:
                        print('视频信息请求失败，请检查网络状态，状态码：', response.status_code)
                        return 0, 0, 0

            else:
                print('未搜索到结果，请确认番名后重试！')
                return 0, 0, 0

        else:
            print('请求错误，请检查网络后重试！')
            return 0, 0, 0


def get_next_link(code, num, driver):
    confirm = input('是否观看下一集：(input "y" to Conf other to Research)')
    if confirm == 'y' or confirm == 'Y':
        num = int(num) + 1
        episode_num = '第{}集'.format(num)

        v_url = 'https://www.agemys.org/play/{}/1/{}'.format(code, num)
        print('请求中...请稍候...')
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

                    # 在当前浏览器窗口中执行 JavaScript 来打开一个新标签页
                    driver.execute_script("window.open('', '_blank');")

                    # 获取所有窗口的句柄
                    all_windows = driver.window_handles

                    # 计算标签页的数量
                    num_tabs = len(all_windows)

                    # 切换到新标签页
                    driver.switch_to.window(driver.window_handles[num_tabs - 1])

                    # 打开新标签页中的网页
                    url = video_src
                    print('加载网页中，请稍候...')
                    driver.get(url)

                    # 设置网页标题
                    driver.execute_script(f"document.title = '{video_title} {episode_num}'")

                    return num, 0

            else:
                print('视频信息提取失败，请确认番剧更新进度，状态码：', response.status_code)
                num -= 1
                return num, 0

        else:
            print('视频信息请求失败，请确认网络状态，状态码：', response.status_code)
            num -= 1
            return num, 0

    else:
        return num, 1
