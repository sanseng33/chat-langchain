from aider.file_content import file_content_with_master
import os

os.environ['TS_LIB_PATH']="D://project//local-langchain//tree_sitter//tslibs//py_php_js_cpp_java_windows_32.dll"

code = file_content_with_master('7193',
                                'eureka-core/src/main/java/com/patsnap/eureka/manager/data/converter/translate/TransCommonConverter.java')

from tree_hugger.core import JavaParser
jp = JavaParser()
jp.parse_code_as_string(code)

print(jp.get_all_class_names())
