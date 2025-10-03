import requests
import os
from datetime import datetime

def main():
    # 获取 Bing 图片数据
    api_url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        image_data = data['images'][0]
        
        img_url_suffix = image_data['url']
        img_date = image_data['startdate']
        full_img_url = f"https://www.bing.com{img_url_suffix}"
        
        print(f"Image Date: {img_date}")
        print(f"Full Image URL: {full_img_url}")
        
        # 下载图片
        img_response = requests.get(full_img_url, timeout=30)
        img_response.raise_for_status()
        
        # 保存原始图片
        with open(f"pic/{img_date}.jpg", "wb") as f:
            f.write(img_response.content)
        print(f"✅ Original image saved: pic/{img_date}.jpg")
        
        # 保存 JSON 信息
        import json
        with open(f"json/{img_date}.json", "w") as f:
            json.dump(image_data, f, indent=2)
        print(f"✅ JSON info saved: json/{img_date}.json")
        
        # 如果是今天的图片，则复制为固定文件名
        today = datetime.utcnow().strftime('%Y%m%d')
        if img_date == today:
            with open("api/today/1920x1080.jpg", "wb") as f:
                f.write(img_response.content)
            print("✅ Today's wallpaper set: api/today/1920x1080.jpg")
            
            # 更新日期索引
            update_dates_index(img_date)
        else:
            print(f"ℹ️ Image date {img_date} is not today {today}, skipping fixed filename copy.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

def update_dates_index(current_date):
    """更新日期索引文件"""
    dates = set()
    
    # 读取现有日期
    if os.path.exists('dates.txt'):
        with open('dates.txt', 'r') as f:
            dates = set(line.strip() for line in f if line.strip())
    
    # 添加新日期
    dates.add(current_date)
    
    # 写回文件
    with open('dates.txt', 'w') as f:
        for date in sorted(dates):
            f.write(f"{date}\n")
    
    print(f"✅ Dates index updated. Total {len(dates)} dates.")

if __name__ == "__main__":
    main()
