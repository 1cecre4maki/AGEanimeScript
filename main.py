from get import getlink, get_next_link


def main():
    while True:
        code, driver, num = getlink()
        if code == 0:
            continue

        elif code == 1:
            break

        else:
            while True:
                num, flg = get_next_link(code, num, driver)

                if flg == 0:
                    continue

                else:
                    print('关闭Chrome中，请稍候...')
                    driver.quit()
                    break


if __name__ == '__main__':
    main()
