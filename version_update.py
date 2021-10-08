a_file = open("credits.txt", "r")

list_of_lines = a_file.readlines()

version = list_of_lines[1].strip('\n').split('.')
separator = '.'
version[2] = (int(version[2]) + 1)
for count, item in enumerate(version):
    version[count] = str(item)
update = (separator.join(version))

list_of_lines[1] = f"{update}\n"
print(update)



a_file = open("credits.txt", "w")

a_file.writelines(list_of_lines)

a_file.close()