from aider.file_content import file_content_with_master
from tree_hugger.core import PythonParser

code = file_content_with_master('7193',
                                'eureka-core/src/main/java/com/patsnap/eureka/manager/data/converter/translate/TransCommonConverter.java')

pp = PythonParser()
pp.parse_code_as_string(code)
print(pp.get_all_class_names())
