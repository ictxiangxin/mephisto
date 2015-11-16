#墨菲斯托(Mephisto)地理引擎

v0.1.0

墨菲斯托引擎提供大量地理事件的计算支持，运行于python3平台。

##参考内容

####源文件列表

`mephisto.logic` 地理实体属性依赖关系及规约方法的描述文件。

`mephisto_language.boson` Mephisto中间语言的语法Boson Script。

`mephisto_language.lexical` Mephisto中间语言的词法Boson Script。

`mephisto_logic.boson` mephisto.logic文件语法的Boson Script，用于语法分析器生成器[boson](https://github.com/ictxiangxin/boson)的输入。

`mp_aster.py` 天体类，包含地球（Earth）实体。

`mp_configure.py` 配置文件。

`mp_data.py` Mephisto内置知识库。

`mp_date_time.py` 日期时间类，包含日期（Date）和时间（Time）。

`mp_engine.py` Mephisto推理引擎，负责执行原子语义动作和管理实体空间。

`mp_handle.py` Mephisto原子语义动作内置函数。

`mp_helper.py` 数据标准化辅助工具。

`mp_location.py` 地点类，包含地点（Location）、经度（longitude）、维度（Latitude）。

`mp_log.py` Mephisto内置日志分析系统。

`mp_logic.py` 地理实体依赖逻辑处理部件，以mephisto.logic为输入文件。

`mp_logic_function.py` 地理实体依赖规约方法实现，实现mephisto.logic文件中指明的方法。

`mp_mephisto_language.py` 原子语义动作分析器。

`mp_question_parser.py` 问句语法分析器，产生问句语义。

`mp_solver.py` 问句解题器，将问句语义翻译成原子语义动作序列并调用推理引擎进行推理。

`mp_tokenize.py` 问句关键词提取及词法标记。

`question.py` 问句语法分析器的Boson Script源码。