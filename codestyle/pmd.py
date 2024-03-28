import subprocess


result = subprocess.run(['pmd', '-dir', 'D:\project\local-langchain\codestyle\ChatCopilotWebSocketHandler.java', '-rulesets', 'rulesets/java/quickstart.xml,category/java/codestyle.xml', '-encoding', ' UTF-8'], shell=True,stdout=subprocess.PIPE,text=True)
output = result.stdout
print(output)

complexity_info = {"class_complexity": 0, "methods_complexity": {}}

for line in output.split("\n"):
    if "Cyclomatic Complexity" in line:
        parts = line.split()
        method_name = parts[3].strip("'")
        complexity = int(parts[9])
        complexity_info["methods_complexity"][method_name] = complexity

# 假设类的复杂度是所有方法复杂度的总和
complexity_info["class_complexity"] = sum(complexity_info["methods_complexity"].values())

print(complexity_info)

