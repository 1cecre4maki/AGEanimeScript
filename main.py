from get import getlink, get_next_link


def main():
    while True:
        # 输入搜索参数
        search = input('请输入搜索的番名：(input "q" to Quit other to Continue)')
        if search == 'q' or search == 'Q':
            print('期待下次使用！')
            break
        else:
            num = input('请输入观看的集数：(input "q" to Quit other to Continue)')
            if num == 'q' or num == 'Q':
                print('期待下次使用！')
                break
            else:
                flg = getlink(search, num)
                if flg == 0:
                    continue
                else:
                    while True:
                        confirm = input('是否观看下一集：(input "y" to Conf other to Research)')
                        if confirm == 'y' or confirm == 'Y':
                            num = int(num) + 1
                            flg = get_next_link(flg, num)

                            if flg == 0:
                                print('请确认是否有第{}集。'.format(num))
                                num -= 1

                            else:
                                continue

                        else:
                            break


if __name__ == '__main__':
    main()
