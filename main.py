# 将 md 文件中引用的图片移动到 md 文件所在文件夹下的 [.文件名] 的文件夹下，并修改 md 文件中的图片引用为相对路径
import os
import re
import shutil


def findAllFile(top_dir, tem):
    for root, dirs, files in os.walk(top_dir):
        for f in files:
            if f.endswith(tem):
                fullname = os.path.join(root, f)
                yield fullname


# TODO 图片名不能有重复的
def pre_main(img_type):
    # 先查找所有md文档里的图片文件名，然后在所有文件中查找该文件
    # 找到后移动到md文档所在的文件夹下的 [.文件名] 的文件夹里，并修改md文档中的图片引用为相对路径
    # 找不到图片，打印文件名和图片名
    project_dir = "C:/Users/xxx/Desktop/Notes"
    all_img_path = []

    # 查找图片，并将所有路径放在一个列表中
    for file_path in findAllFile(project_dir, img_type):
        all_img_path.append(file_path)

    for md_file_path in findAllFile(project_dir, ".md"):  # 查找所有md文档
        md_name = os.path.basename(md_file_path).split(".")[0]  # md_name = "xxx"
        f1 = open(md_file_path, "r", encoding="utf8")
        lines = f1.readlines()
        f1.close()

        f2 = open(md_file_path, "w", encoding="utf8")

        for s in lines:
            try:
                # 先查找md文档里的是否存在引用图片
                if img_type == ".png":
                    # 匹配引用图片语句，包括前面的中括号和感叹号
                    patt = r"(\!\[+?\]\(.+?\.png)"  # 匹配示例 ![xxx](xxx.png
                elif img_type == ".jpg":
                    patt = r"(\!\[+?\]\(.+?\.jpg)"  # 匹配示例 ![xxx](xxx.jpg
                else:
                    raise Exception("图片类型错误")

                s_new = s  # 如果文件中没有引用图片，那么保持文件原内容不变
                pattern = re.compile(patt)
                result = pattern.search(s)
                if result is not None:
                    # ========================修改图片引用为相对路径
                    result = result.group()[1:]
                    file_name_with_suffix = result.split("/")[-1]  # file_name_with_suffix = "xxx.png"
                    # 替换引用字符串
                    s_new = re.sub(pattern, "![](." + md_name + "/" + file_name_with_suffix, s)

                    # ========================移动图片到相对路径
                    # 查找图片位置，并移动到md文档所在的文件夹下的 [.文件名] 的文件夹里
                    # 如果找不到，打印文件名和图片名
                    finded = False
                    for png_path in all_img_path:
                        if finded:
                            break

                        if file_name_with_suffix in png_path:
                            finded = True

                            dest_dir = os.path.dirname(md_file_path) + "/." + md_name
                            if not os.path.exists(dest_dir):
                                os.mkdir(dest_dir)

                            # 移动图片到新文件夹
                            dest_filename = os.path.join(dest_dir, file_name_with_suffix)
                            if png_path != dest_filename:
                                shutil.move(png_path, dest_filename)
                                print(md_file_path)
                                print(png_path, "---->", dest_filename)

                    if not finded:
                        print(md_file_path)
                        print(s + "---->图片未找到")
                    elif s_new != s:
                        # 判断文件是否被修改过
                        print(md_file_path)
                        print(s + "---->" + s_new)
                    else:
                        pass

                f2.write(s_new)

            except Exception as e:
                # 防止发生错误导致文件内容丢失
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", e)
                print(md_file_path)
                f2.write(s)

        f2.close()  # 关闭文件


if __name__ == "__main__":
    ATTACH_IMG_TYPE = [".png", ".jpg"]
    for img_type in ATTACH_IMG_TYPE:
        pre_main(img_type)
