#墨菲斯托(Mephisto)地理引擎

v0.0.1

墨菲斯托引擎提供大量地理事件的计算支持，运行于python3平台。

##参考内容

###类功能

墨菲斯托引擎提供一个日期类Date和一个时间类Time。
地理坐标方面提供一个经度类Longitude和一个纬度类Latitude以及一个地点类Location。
天体方面提供一个地球类Earth

####源文件

`mephisto.logic` 地理实体属性依赖关系及规约方法的描述文件。

`mephisto_logic.boson` mephisto.logic语法描述BNF，用于用于语法分析器生成器[boson](https://github.com/ictxiangxin/boson)的输入。

`mp_aster.py` 天体类，包含地球（Earth）。

`mp_configure.py` 配置文件。

`mp_date_time.py` 日期时间类，包含日期（Date）和时间（Time）。

`mp_location.py` 地点类，包含地点（Location）、经度（longitude）、维度（Latitude）。

`mp_logic.py` 地理实体依赖逻辑处理部件，以mephisto.logic为输入文件。

`mp_logic_function.py` 地理实体依赖规约方法实现，实现mephisto.logic文件中指明的方法。

`mp_phenomenon.py` 地理现象的语义实现。