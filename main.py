import os, re
import pathlib
import shutil

paths = [  # 这些目录里只有*.jam文件
	r"E:\alter_translation\translate\HT僔僫儕僆\僔僫儕僆杮懱\杮曇",  # 本篇
	r"E:\alter_translation\translate\HT僔僫儕僆\僔僫儕僆杮懱\摯寠"  # 洞穴
]
output_path = r"E:\alter_translation\script_output"  # 输出位置
output_sub_paths = []
os.chdir(output_path)

files = []  # 文件列表
for p in paths:
	l = os.listdir(p)
	l.sort()
	for fname in l:
		files.append(p + "\\" + fname)
	
	dirname = p.split("\\")[-1]
	if pathlib.Path(dirname).exists():  # 删除以前输出的文件
		# os.rmdir(dirname)
		shutil.rmtree(dirname)
	os.mkdir(dirname)
	output_sub_paths.append(output_path + "\\" + dirname)

sentences = {}
count = 1
for f in files:
	print("Converting files...(" + str(count) + "/" + str(len(files)) + ")", end="\r")
	count += 1
	
	file = open(f, "r", encoding="UTF-8")
	lines = file.readlines()
	file.close()
	
	new_file_lines = []  # 用来writelines写入新文件中，预备一个list
	for line in lines:
		
		if bool(re.search(r"' [AR]\n", line)):  # 如果这一行是对话文本
			dialogue_text = re.findall(r"'(.+)' [AR]", line)[0]  # 文本内容，提取单引号里面的内容
			if dialogue_text not in sentences.keys():  # 统计这一句话一摸一样的重复出现了多少次（只出现一次记为0，出现两次即“重复出现了一次”记为1）
				sentences[dialogue_text] = 0
			else:
				sentences[dialogue_text] += 1
			
			line_to_write_without_number = r"'" + dialogue_text + "' " + line[-2] + "\n"
			line_to_write = "\t" + str(sentences[dialogue_text]) + " " + line_to_write_without_number
			if sentences[dialogue_text] == 0:
				line_to_write = "\t" + line_to_write_without_number
			new_file_lines.append(line_to_write)  # 对话文本行，重新编号后
		else:
			new_file_lines.append(line)  # 非对话文本行
	
	new_file_path = f.split("\\")[-2] + "\\" + f.split("\\")[-1]
	new_file = open(new_file_path, "w", encoding="UTF-8")  # 创建一个新的文件
	new_file.writelines(new_file_lines)
	new_file.close()

print("\nConverting complete")
