import requests
import json
import os
from datetime import datetime, timedelta
import time

def get_bing_image():
    try:
        # 获取 Bing 图片数据
        url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
        response = requests.get(url, timeout=30)
        data = response.json()
        
        image_data = data['images'][0]
        img_url_suffix = image_data['url']
        img_date = image_data['startdate']
        full_img_url = f"https://www.bing.com{img_url_suffix}"
        
        print(f"Image URL: {full_img_url}")
        print(f"Image Date: {img_date}")
        
        # 下载图片
        img_response = requests.get(full_img_url, timeout=60)
        pic_filename = f"pic/{img_date}.jpg"
        with open(pic_filename, "wb") as f:
            f.write(img_response.content)
        print(f"Downloaded image to {pic_filename}")
        
        # 保存 JSON 数据
        json_filename = f"json/{img_date}.json"
        with open(json_filename, "w") as f:
            json.dump(image_data, f, indent=2)
        
        return img_date, True
    except Exception as e:
        print(f"Error getting Bing image: {e}")
        return None, False

def copy_todays_wallpaper():
    try:
        # 复制当天图片为固定名称
        today = datetime.now().strftime('%Y%m%d')
        source_file = f"pic/{today}.jpg"
        target_file = "api/today/1920x1080.jpg"
        
        if os.path.exists(source_file):
            # 复制文件
            with open(source_file, 'rb') as src, open(target_file, 'wb') as dst:
                dst.write(src.read())
            print(f"Successfully copied {source_file} to {target_file}")
            return True
        else:
            print(f"Today's image {source_file} not found")
            return False
    except Exception as e:
        print(f"Error copying wallpaper: {e}")
        return False

def should_copy_wallpaper():
    # 判断是否应该复制壁纸（每2小时一次）
    try:
        if os.path.exists("api/today/1920x1080.jpg"):
            file_time = os.path.getmtime("api/today/1920x1080.jpg")
            current_time = time.time()
            # 如果文件修改时间在2小时内，不复制
            if current_time - file_time < 2 * 60 * 60:  # 2小时
                print("Wallpaper was updated within last 2 hours, skipping copy")
                return False
        return True
    except:
        return True

# 主执行逻辑
current_date, success = get_bing_image()

if success:
    # 更新日期索引
    dates = set()
    if os.path.exists('dates.txt'):
        with open('dates.txt', 'r') as f:
            dates = set(line.strip() for line in f if line.strip())
    
    if current_date:
        dates.add(current_date)
    
    with open('dates.txt', 'w') as f:
        for date in sorted(dates):
            f.write(f"{date}\n")
    
    print(f"Available dates: {len(dates)}")
    
    # 检查是否需要复制当天壁纸
    today = datetime.now().strftime('%Y%m%d')
    if current_date == today and should_copy_wallpaper():
        copy_todays_wallpaper()
    elif current_date != today:
        print(f"Current image date {current_date} is not today {today}, skipping copy")
else:
    print("Failed to get Bing image, will try again later")

