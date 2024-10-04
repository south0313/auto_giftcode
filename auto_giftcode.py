import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import giftcode_config

# ギフトコードを入力
gift_code = input("ギフトコードを入力してください:\n")

# フルスクリーンoption
options = webdriver.ChromeOptions()
options.add_argument("--start-fullscreen")

# Chrome起動、指定したURLに移動
driver = webdriver.Chrome(options=options)
driver.get(giftcode_config.URL)

# ギフトコードを入力
gift_code_target = driver.find_element(By.CSS_SELECTOR, 'div.code_con .input_wrap input')
gift_code_target.send_keys(gift_code)

starttime = time.time()

# ユーザーIDを入力
for item in giftcode_config.MEMBER_ID:
    # ユーザーIDを入力
    user_id_target = driver.find_element(By.CSS_SELECTOR, 'div.roleId_con .input_wrap input')
    user_id_target.clear()

    print(f"user_id: {item}に配布")
    user_id_target.send_keys(item)

    time.sleep(3)

    # ログインボタンを押下
    driver.find_element(By.CSS_SELECTOR, 'div.roleId_con .login_btn span').click()

    # モーダルウィンドウが表示されるのを待つ
    time.sleep(4)

    try:
        # 入力したログインIDが無効な場合処理を終了
        # モーダルの確認ボタンを押下して閉じる
        driver.find_element(By.CSS_SELECTOR, '.confirm_btn').click()        
        print("不正なIDです")
        continue

    except NoSuchElementException:
        # 交換確認ボタンを押下
        driver.find_element(By.CSS_SELECTOR, '.exchange_btn').click()
        time.sleep(3)
     
        # 入力したギフトコードが無効な場合処理を終了
        modal_message = driver.find_element(By.CSS_SELECTOR, '.modal_content .msg').text
        if modal_message == '交換コードがありません':
            print('入力したギフトコードは無効です。処理を終了します。')
            driver.close()
            break
        
        # モーダルの確認ボタンを押下
        driver.find_element(By.CSS_SELECTOR, '.modal_content .confirm_btn').click()

        # ユーザーをログアウトする
        driver.find_element(By.CSS_SELECTOR, '.exit_con').click()
   
if driver.service.process:
    driver.close()

print(f'処理が終わりました. {time.time() - starttime} 秒')
