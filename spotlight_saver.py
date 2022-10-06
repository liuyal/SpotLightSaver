import os
import sys
import time
import cv2
import shutil
import datetime


def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp) and ".png" in fp:
                total_size += os.path.getsize(fp)
    return total_size


def update_readme(image_count, size):
    line0 = "# SpotLight_Saver\n"
    line1 = "\nImage Count: " + image_count + "\n"
    line2 = "\nSize: " + size + "\n"
    line3 = "\n" + r"[Script Link](https://github.com/liuyal/Archive/blob/master/Python/Utilities/Miscellaneous/spotlight_saver.py)"
    text = [line0 + line1 + line2 + line3]
    file = open(dst + os.sep + "README.md", "w+")
    file.truncate(0)
    file.write("".join(text))
    file.flush()
    file.close()


if __name__ == "__main__":

    src = r"C:\Users\USER\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
    src = src.replace("USER", os.getlogin())
    dst = r"C:\Users\Jerry\OneDrive\Pictures\SpotLightSaver"

    # Make new folder for new day
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d")
    time_stamp_year = time_stamp.split('-')[0]
    time_stamp_month = time_stamp.split('-')[1]
    time_stamp_day = time_stamp.split('-')[2]
    dst_folder = dst + os.sep + time_stamp_year + os.sep + time_stamp_month + os.sep + time_stamp_day

    if not os.path.exists(dst + os.sep + time_stamp_year):
        os.makedirs(dst + os.sep + time_stamp_year)
    if not os.path.exists(dst + os.sep + time_stamp_year + os.sep + time_stamp_month):
        os.makedirs(dst + os.sep + time_stamp_year + os.sep + time_stamp_month)
    if not os.path.exists(dst + os.sep + time_stamp_year + os.sep + time_stamp_month + os.sep + time_stamp_day):
        os.makedirs(dst + os.sep + time_stamp_year + os.sep + time_stamp_month + os.sep + time_stamp_day)

    # Copy src image to dst & rename portrait images
    for image in os.listdir(src):
        shutil.copy(src + os.sep + image, dst_folder + os.sep + image + ".png")
        if os.path.exists(dst_folder + os.sep + image + "_p.png"):
            os.remove(dst_folder + os.sep + image + "_p.png")
        im = cv2.imread(dst_folder + os.sep + image + ".png")
        if im.shape[0] > im.shape[1]:
            shutil.copy(dst_folder + os.sep + image + ".png", dst_folder + os.sep + image + "_p.png")
            os.remove(dst_folder + os.sep + image + ".png")

    # Check for duplicate images in different date folders
    images = []
    remove_list = {}
    for year_folder in os.listdir(dst):
        if os.path.isdir(dst + os.sep + year_folder) and '.' not in year_folder:
            for month_folder in os.listdir(dst + os.sep + year_folder):
                for day_folder in os.listdir(dst + os.sep + year_folder + os.sep + month_folder):
                    for file in os.listdir(dst + os.sep + year_folder + os.sep + month_folder + os.sep + day_folder):
                        try:
                            remove_list[file]
                        except:
                            remove_list[file] = []
                        remove_list[file].append(dst + os.sep + year_folder + os.sep + month_folder + os.sep + day_folder + os.sep + file)
                        images.append(dst + os.sep + year_folder + os.sep + month_folder + os.sep + day_folder + os.sep + file)
                        print(dst + os.sep + year_folder + os.sep + month_folder + os.sep + day_folder + os.sep + file)


    # Remove non duplicate images from list
    for key in list(remove_list):
        if len(remove_list[key]) == 1:
            del remove_list[key]

    # Remove 1 count of each duplicate image
    for key in list(remove_list):
        for i in range(0, len(remove_list[key]) - 1):
            remove_list[key].pop(i)

    # Remove Duplicate images from most recent date
    for key in list(remove_list):
        os.remove(remove_list[key][0])

    # Remove non spotlight images
    if os.path.exists(dst_folder):
        for image in os.listdir(dst_folder):
            if ".png" in image:
                im = cv2.imread(dst_folder + os.sep + image)
                if im.shape[0] < 900:
                    os.remove(dst_folder + os.sep + image)

    # Clean up empty folders
    for year_folder in os.listdir(dst):
        if os.path.isdir(dst + os.sep + year_folder) and '.' not in year_folder:
            for month_folder in os.listdir(dst + os.sep + year_folder):
                for day_folder in os.listdir(dst + os.sep + year_folder + os.sep + month_folder):
                    if len(os.listdir(dst + os.sep + year_folder + os.sep + month_folder + os.sep + day_folder)) < 1:
                        shutil.rmtree(dst + os.sep + year_folder + os.sep + month_folder + os.sep + day_folder)

    # Read count and size of images and write to readme
    size_gb = str(round(get_size(start_path=dst) / 1000 / 1000 / 1000, 3)) + " GB"
    print("\nImage Count: " + str(len(images)))
    print("Size: " + str(size_gb) + "\n")
    update_readme(str(len(images)), size_gb)

    # Commit images to github
    os.system(r"cd " + dst + " && python " + dst + r"\git_commit.py")
    time.sleep(5)
